# Edition 2027 — typed Package authoring

Extend the generated Package-local Presentation base. It supplies a typed `sdk`
before calling `compose()`. A window-opening entry is an authored resource:

```gdscript
extends "res://rookframe/packages/<id>/sdk/presentation.gd"

const CALENDAR_WINDOW_BUTTON: SDK.WindowButton = preload("res://rookframe/packages/<id>/ui/window_button.tres")

func compose() -> void:
    var rail: SDK.Rail = sdk.rails.left
    rail.push(CALENDAR_WINDOW_BUTTON)
```

The Publisher chooses the Rail and the entry. Rookframe owns native scene
instantiation, opening signals, mounting, ordering across Packages, responsive
geometry, registration lifetime, failure reporting and managed-window mechanics.
No Publisher-side binding, string-based mount, boolean cleanup branch or native
signal connection is required for this standard action.

## Types available in Godot

| Type / member | Contract |
| --- | --- |
| `SDK.Rail` | Package-scoped access to one Rail's Package contribution slot. It is not the private host Node. |
| `sdk.rails.left`, `sdk.rails.right` | Read-only typed Rail handles. |
| `Rail.push(entry: SDK.WindowButton) -> void` | Register an authored window-opening entry. Multiple entries retain insertion order within the Package; System precedes optional Packages in stable Package-ID order. The same button-scene/window-scene pair is idempotent within one Rail and Presentation. |
| `SDK.WindowButton` | Authored Resource with `button_scene: PackedScene` and `window: SDK.ExtensionSurface`. The button scene must have a native Button root. |
| `SDK.ExtensionSurface` | Authored Resource with `scene: PackedScene`. The scene must have a Control root; its internal UI belongs to the Package. |
| `sdk.package_id() -> String` | Stable Package UUID, independent of builds and installations. |
| `sdk.package_root() -> String` | Current admitted resource root for this Package. |
| `sdk.presentation_experience() -> String` | Current `desktop`, `tablet` or `phone` experience. |

Open `ui/window_button.tres` in the Inspector to choose the button scene and its
typed window target. Edit those scenes with the ordinary Godot scene editor and
public UI Kit. Type hints use path-preloaded scripts, following
[Godot's custom type support](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html#custom-variable-types).
They do not require global `class_name` registrations or Package autoloads.

## Ownership and errors

A window is instantiated lazily on its first activation. Reopening, docking,
floating, minimizing and restoring preserve its live content. Different entries
targeting the same scene share that window. Presentation replacement updates the
Rail entries while retaining window content and its draft state until World
teardown. A different target scene has separate content. Closing a managed
window hides it; World teardown frees the content and all registrations.

Registration validates the authored scenes through the Package-bound checked
resource loader. Invalid setup fails the existing Package startup or staged
Presentation replacement operation, with a diagnostic. A failure while opening
a window is attributed to that Package and scene and ends the affected World
Application through its existing return-to-Manager cleanup. Publishers do not
own disposal of rejected registration controls.

## Implementation setup

Extend `sdk/implementation.gd` and override `start() -> void` when Implementation
setup is needed. The SDK binds before `start()` in an installed World. The
surrounding Node lifecycle remains native Godot. The generated base owns the
metadata binding; Publisher code receives the typed facade directly.

All files in the generated `sdk/` directory ship with the Package. They are
checked against the exact authoring kit and receive the same production source
and resource verification as other Package code. No generated file is exempt
from admission. These facilities require Edition 2027 revision 1; broader
Content and domain APIs continue in later Project 02 work.

Direct Godot behavior within authored Package UI and the independently versioned
UI Kit remain their existing contracts. Use public component properties and
signals for Package-internal behavior, without depending on private child paths.

## Migrating the initial 0.1.x example

Update the exact SDK pin and authoring lock together. Replace the generated
`sdk/` directory with the current `facade` command, extend its Presentation base,
and move the button/window references into a `WindowButton` resource. Replace
manual binding, button instantiation, opening signal wiring and `mount_rail`
with `Rail.push`. Keep the authored button and window scenes. Initialization
does not overwrite a Publisher's existing source to perform this migration.
