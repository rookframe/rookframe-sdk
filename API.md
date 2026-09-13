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
from admission. These UI facilities require Edition 2027 revision 1.
The typed World and Content scopes below require revision 5 (Edition 2028 revision 2).

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

## SDK 0.3.0: Edition 2027 revision 4 and Edition 2028 revision 1

Both Editions retain the typed Rails, WindowButton and ExtensionSurface API.
Edition 2028 has its own native adapter and returns `SDK.DeviceExperience` from
`presentation_experience()`, with read-only `is_desktop`, `is_tablet`, `is_phone`
properties. Edition 2027 retains its String return. No UI Kit API is folded into
the SDK Edition.

A `SDK.Contribution` Resource holds an authored Control `scene`. Register it with
`sdk.ui_root.push(entry)`, `sdk.slots.selected_rook.push(entry)` or
`sdk.slots.actor_creation.push(entry)` (System only). Each slot retains Package
order and Package-local insertion order; repeating a scene is idempotent.
The host loads and mounts it, observes setup errors and removes it on shutdown.
Package controls do not own the workspace or surface chrome.

Authored window/contribution roots can extend generated `sdk/window.gd`. The host
binds its concrete `sdk` before native readiness; override `ready()` to initialize
children. `sdk` remains null when running the scene alone in the editor.

`SDK.FeedbackMessage` is a Resource with `title`, `message` and
`Array[SDK.FeedbackAction]` (`id`, `title`). Use `sdk.feedback.notice(message)`,
`.warning(message)`, `.error(message)` or `.confirm(message)`. Host-owned notices
render wrapping copy and named actions. `sdk.feedback.action_selected(action)`
emits only for that facade's current request. Dismissal requires no action and
never implies confirmation; keep destructive work behind explicit named actions.

Declare translations in `rookframe.json` as
`"translations": [{"locale":"de", "domain":"default", "path":"i18n/de.tres"}]`.
Each resource is a normal Godot Translation with the matching locale, inside
the Package namespace. Use `sdk.translations.text("Calendar")` or pass the
declared domain as the second argument. Domains are private to each Package,
registered before Implementation setup and disposed at shutdown. Missing keys
retain their source text. The active application locale selects the translation.

Override `cleanup(completed: SDK.Cleanup)` on an Implementation or Presentation;
call `completed.complete()` when finished, immediately or after asynchronous
work. All callbacks share one second, including partial startup. Service
admission is closed first; SDK/loading/UI authority is revoked after that window.
Timeout warnings name the Package and possible retained work; they do not claim
blocked-thread preemption or universal job cleanup.

Content is declared semantically in the Manifest, rather than pushed from an
Implementation. The host projects Library metadata before readiness and resolves
payloads/previews through checked loading on demand. A Content Reference uses
Package UUID/local ID, independently of a build UUID. A data-only Package has no
Implementation, Presentation, Settings or generated executable SDK.

Presentation settings show declared choices. Preparation checks replacement
Control setup before retiring the live contribution set. Successful changes
preserve the Implementation and World Session. A window with the same declared
scene retains its native Control instance, text draft, selection and scroll state;
closing/reopening also retains it until World shutdown. Failed preparation leaves
the live view and settings intact and displays a diagnostic.


## World game data — Edition 2027 revision 5 / 2028 revision 2

`SDK` exposes concrete `ActorId`, `SystemRecordId`, `RookId`, `SceneId`,
`ContentReference`, snapshot and result classes. No caller supplies a Participant,
peer identity, authority flag, World path or another Package's data-slot identity.
`SDK.context()` returns an `SDK.WorldContext` containing the host-bound Participant
and current authority/GM status. IDs identify records; they never grant access.
Current foreground admission is the existing local GM session. Remote Participant
admission and managed connectivity remain owned by their later project.

All mutation results extend `SDK.OperationResult` (`ok`, `code`, `message`).
An accepted result means the whole World save completed. Payload interpretation
errors return `invalid_data`; unavailable authority and insufficient access return
explicit failures. A durable publication failure returns no success and terminates
the affected World Application. Reopening uses the last coherent save.

### One Package World data value

```gdscript
var read: SDK.DataResult = sdk.world_data.read()
if not read.ok:
    return
# A short-lived Package helper interprets read.value and calculates a new value.
var calculated: Variant = calculate(read.value)
var saved: SDK.OperationResult = sdk.world_data.replace(calculated)
if saved.ok:
    refresh_from(sdk.world_data.read().value)
```

The handle is automatically scoped to this Package and World. It exposes the
one live authority-owned Variant; only the admitted GM may read or commit this
additional World data in the current foreground session. `null` means never
committed and cannot be committed as a root. `replace(value)` commits implicitly;
mutating a live Dictionary, Array or Resource requires `commit()` explicitly.
An unrelated domain save preserves the last explicitly committed representation.
Submissions are sequential; nested operations are rejected. Do not mirror Actors,
Rooks or System Records in this slot or retain a second synchronized entity tree.

The codec supports ordinary scalar/math values, strings, packed arrays, Arrays,
Dictionaries and plain or Package-scripted `Resource` data. It preserves shared
container/Resource identities and typed container contracts. Native asset Resources
such as textures and meshes use stable Content References instead. Nodes, arbitrary
non-Resource Objects, Callables, Signals and RIDs reject. Bounds are 8 MiB encoded,
4096 graph objects and 64 levels while encoding. Container types cannot embed
runtime-only handles. Typed helpers may validate/calculate on temporary values.

Custom Resources use storage properties and their Package-relative script path.
The entire current Package selection is admitted before execution; every saved
script and typed-container dependency must resolve in that admission before any
Resource is reconstructed. No retained build path is loaded as a fallback. Authors
own the compatibility of their Resource scripts, constructors and stored properties
across releases. Prefer pure values for release-independent schemas, as Calendar does.
Failed interpretation preserves the opaque bytes and cannot silently replace them.

New releases, disabled/unavailable/uninstalled code, unrelated saves, host Copy
and recovery export/import preserve opaque data without executing its scripts.
Explicit Package Deletion removes only that Package's slot and settings. Protected
secrets are excluded from the portable World; supplementary checked files remain
separate from its coherent data value.

### Actors and System Records

The selected System Extension owns these operations and payload meaning.
`actors.list()` returns `ActorListResult.items`; `read(id)`, `create(definition,
choices)` and `update(id, data)` return `ActorResult.actor`. An `Actor` has a typed
`id` and generic `data`. `delete(id)` returns `OperationResult`. The host filters
Actor discovery/read by Actor Access and requires Owner access (or GM authority)
for mutation. Creating from a declared, available `actor_definition` invokes its
`create_data(choices)` method, assigns a fresh Actor identity, and grants the
bound confirming human creator Owner access. It never creates a Rook.

Author definitions by extending `SDK.ActorDefinition` through its generated script
path and declaring the Resource in a System Content group. Use an Actor Creation
contribution to open an `SDK.ExtensionSurface` with `sdk.windows.open(surface)`;
the final authored confirmation button calls `sdk.actors.create(...)`.
Repeated definition execution produces independent Actors.

`system_records.list(type_name)` optionally filters the Package-defined type;
`read(id)`, `create(type_name, data)`, `update(id, data)` and `delete(id)` use typed
`SystemRecordId` and results. `SystemRecord` contains `id`, `type_name`, and generic
`data`. The host owns identity, World membership and persistence; the System owns
its schema. Mutation currently requires the admitted GM. Reads require the selected
System and an admitted Participant. Actor/Record reads are supplied values for
calculation; submit changes explicitly through their owners.

### Tabletop and integration boundaries

- `content.list(SDK.ContentKind.Value.MINIATURE)` / `read(ContentReference)` return typed
  metadata with stable Package/local references. Resource/build paths stay private.
- `scenes.current()` returns a typed Scene. `scenes.distance(from, to)` uses committed
  Rook centers in the same current Scene's logical coordinates; it does not predict
  collision, physical movement or a Roll result.
- `rooks.list/read/create/move/link/unlink/delete` use typed IDs and `Vector2` poses.
  Current Scene and available Miniature requirements, placement bounds and holder
  rules remain enforced by the established Rooks/Rook owners. Creation requires GM
  authority; control uses Actor ownership or GM authority. Multiple Rooks may link
  to one Actor. Deleting an Actor removes its links/access but preserves Rooks;
  deleting a Rook preserves the Actor. No combined Actor-plus-Rook operation is added.
- `builder.status()`, `targeting.status()` and `dice.status()` explicitly return
  unavailable. Managed connectivity/Targeting and physical Throws/Rolls retain
  their existing project boundaries; this SDK adds no transport or replication model.

The Workshop System example demonstrates authored Actor creation, a typed Resource
HP calculation/update, and journal System Records. The separate optional Calendar
uses only its scoped World value for Gregorian dates and dated notes.

Content entries expose `kind: SDK.ContentKind.Value`, matching `SDK.ContentKind.Value` query constants. Dictionary keys may contain acyclic container graphs; cyclic key dependencies reject before publication or Resource construction.
