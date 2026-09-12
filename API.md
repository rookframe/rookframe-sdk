# Edition 2027 — initial authoring interface

Preload `res://rookframe/packages/<id>/sdk/package_sdk_facade.gd`; instantiate it
normally. The generated Implementation demonstrates native `_ready` setup:
Rookframe attaches the Package-scoped adapter as `rookframe_sdk` metadata before
adding the Node to its World subtree. In the editor that metadata is absent.
A Presentation instead receives the same scoped adapter as the argument of
`compose_presentation(host: Object) -> Control`. The generated Presentation binds
it automatically. These objects die with the World or local Presentation.

| Facade method | Contract |
| --- | --- |
| `bind(host: Object)` | Receives the host-supplied scoped adapter during setup. |
| `package_id() -> String` | Stable Package UUID, independent of builds. |
| `package_root() -> String` | Stable author root in the editor; immutable selected profile root in a World. |
| `presentation_experience() -> String` | `desktop`, `tablet` or `phone`; editor defaults to desktop. |
| `mount_rail(rail: String, content: Control) -> bool` | Mount an unparented authored entry in the left or right Rail's Package slot. System entries precede optional Packages. Host owns slot layout and cleanup. |
| `open_extension_surface(content: Control) -> bool` | Open authored content in the host-managed window. Reusing the same content retains its Node instance across close/reopen, dock/float and minimize/restore. Host owns chrome, focus and responsive placement. |

These methods require revision 1. The author kit checks declared minimum revision
against actual reviewed SDK operations; settings require revision 2 and trusted
service operations require revision 3. This initial public facade covers the
RFG-225 author-to-World path; broader Content, UI and domain API authoring grows
in the following Project 02 slices. Direct Godot APIs and public UI Kit resources
remain separate contracts and receive normal production admission checks.

Use ordinary `preload`, path-attached scripts, scenes and resources within your
Package. There are no Package autoloads or process-global class registrations.
Use the public component root's exported properties and methods, not its internal
child structure. The initial Rail scene connects `pressed` to a Presentation
method, which instantiates the window scene and calls `open_extension_surface`.
