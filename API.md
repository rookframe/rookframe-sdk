# Typed Package authoring — SDK 0.17.1

Edition 2029 revision 9 includes the typed UI, World, settings, physical-Throw,
and initial managed-window presentation
integration APIs below. The earlier Edition/revision headings record when shared
facilities were introduced. Edition 2029 uses the typed `DeviceExperience` return
from `presentation_experience()`.

SDK 0.17.1 also authors 2027 revisions 1–7 and 2028 revisions 1–4. For the
operation-based integration API in 2027:8 / 2028:5, retain immutable SDK 0.7.0.
Already generated Packages using those Editions remain supported by the host.

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
| `sdk.presentation_experience() -> DeviceExperience` | Current experience via `is_desktop`, `is_tablet`, `is_phone` (Edition 2027 returns a String). |

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

## Atomic Actor creation — 2029 revision 9

`await sdk.actors.create_atomic(definition, choices, child_requests)` creates
one primary Actor and up to 31 additional Actors in one durable save. Each child
request contains `package_id`, `local_id`, and `choices` for an available Actor
Definition. Validation or publication failure creates none of the Actors. Every
created Actor grants Owner to the creator; the GM retains inherent Owner access.
The result contains the primary Actor. Close or discard drafts before submitting;
final confirmation submits the durable operation and is not an undoable draft.

## Initial managed-window presentation — 2029 revision 8

The Publisher may configure these ordinary exported fields on an
`SDK.ExtensionSurface` Resource:

- `initial_placement`: `"left"`, `"right"`, or `"floating"`; the default is
  `"right"`.
- `initial_dock_width`: an optional logical-pixel width. Zero asks Rookframe for
  its responsive default.
- `initial_floating_rect`: an optional `Rect2`. An empty rectangle asks
  Rookframe for its responsive default.

The generated `Rail.push`, `sdk.windows.open`, and `sdk.windows.open_actor`
operations submit that portable first-open presentation to Rookframe. It is an
initial author preference, not World state: the Participant may move or redock
the retained window, and Rookframe owns safe-area clamping and responsive
fallbacks. Facades generated for earlier revisions call their original host
operations and expose no initial-presentation fields.

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
registered before Implementation setup and disposed at shutdown. The saved
Rookframe language selects the translation. Unsupported locales and
missing messages fall back to the Package's default language, then source text.
Set `"defaultLocale": "de"` alongside `translations` for a German default; every
domain must contain that explicitly declared default. Omitting `defaultLocale`
preserves English source text as the default without requiring an English
resource. Hardcoded Package text remains supported and is not translated by the
host catalog. See [Application and Package language](https://github.com/rookframe/rookframe-godot/blob/main/docs/implementation/internationalization.md).

Override `cleanup(completed: SDK.Cleanup)` on an Implementation or Presentation;
call `completed.complete()` when finished, immediately or after asynchronous
work. All callbacks share one second, including partial startup. Service
admission is closed first; SDK/loading/UI authority is revoked after that window.
Timeout warnings name the Package and possible retained work; they do not claim
blocked-thread preemption or universal job cleanup.

After connection loss the application offers explicit Reconnect/Leave and revokes
the ended Session's commands, services and callbacks. Reconnect authenticates a
new Session and loads current shared state before making the workspace interactive.
Package instances and adapters are fresh; never retain an adapter or retry an old
command. The selected Presentation experience is kept when the exact requirements
still match. Changed requirements return through stopped Manager preparation.

An Implementation, Presentation, or currently open SDK Window may opt in to
private draft preservation with ordinary GDScript callbacks:

```gdscript
func capture_reconnect_state() -> Dictionary:
    return {"name": actor_name.value}

func restore_reconnect_state(state: Dictionary) -> void:
    var saved_name: String = state.get("name", "")
    actor_name.value = saved_name
```

Both callbacks are required. Return only local form values: null, booleans,
numbers, strings, arrays, and dictionaries with string keys. Each root is bounded
to 64 KiB, 4096 values and 32 nesting levels; unsupported state is discarded with
a diagnostic. Nodes, Resources, capabilities, Callables, pending operation IDs,
gesture state and queued commands are not private drafts. Capture runs after
Session revocation. Restore runs on the fresh instance after normal setup and
current-state bootstrap, with shared operations disabled during the callback.
It must only populate local UI, never submit or schedule actions. The user acts
again in the new Session; query current Actor Access and values when they do.
An Actor window is reopened only if it remains readable. Leaving or application
termination discards these in-memory drafts. This does not promise static/cache
reset or preemption of arbitrary Package code.

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
The host binds the active Package, authenticated Participant and current Session.
`context().session_id` identifies that Session; an old facade never inherits a new
Session. Read-only context fields and supplied IDs convey no additional authority.

All mutation results extend `SDK.OperationResult` (`ok`, `code`, `message`).
For durable World mutations, an accepted result means the whole World save completed. Action Log reports instead acknowledge authority acceptance and broadcast without saving the World. Payload interpretation
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
committed Variant to every admitted Participant through the same complete shared
World state. `read()` works on each Participant; only the World Authority GM may
commit this additional World data. UI display rules determine which details are
shown. World secret settings are local credentials, separate from gameplay data. `null` means never
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
`id`, generic `data`, and current `access_level` (`Viewer` or `Owner`). `delete(id)` returns `OperationResult`. Actor discovery/read is an access-aware local presentation query over the complete
shared World state, never an Authority-side replication filter. Every Participant
receives all Actor data, grants and Actor–Rook links. Mutation requires Owner access
(or GM authority). Creating from a declared, available `actor_definition` invokes its
`create_data(choices)` method, assigns a fresh Actor identity, and grants the
bound confirming human creator Owner access. It never creates a Rook.

Author definitions by extending `SDK.ActorDefinition` through its generated script
path and declaring the Resource in a System Content group. Use an Actor Creation
contribution to open an `SDK.ExtensionSurface` with `sdk.windows.open(surface)`;
the final authored confirmation button calls `sdk.actors.create(...)`.
Repeated definition execution produces independent Actors. Await all Actor and
System Record mutations, including creation and deletion. Success follows the
single durable publication and arrival of coherent authorized state. Queries stay
synchronous. Disable repeated submission while awaiting and display refusals
without changing the displayed accepted data. Package calculations remain shared
textual GDScript; Rookframe interprets no game rules.

In Edition 2029 revision 2, `actors.access(id) -> ActorAccessListResult` lets the
GM list Player entries (`participant_id`, `display_name`, `access_level`).
`await actors.set_access(id, participant_id, level) -> OperationResult` accepts
`None`, `Viewer`, or `Owner`. The Participant argument identifies the grant's
subject; the caller always comes from the authenticated Session. GMs have
inherent Owner access. Viewer permits reading; Owner permits Actor changes and
control of every linked Rook. Unlinked Rooks require GM control.

Connect `sdk.world_changed` and re-query current data to refresh a Package
surface. When `read(id)` returns `access_denied`, discard the displayed Actor and
close its actions. Revocation retains the Actor, its Rooks and accepted data.
A completion re-checks current access so it cannot reopen a revoked Actor.

Edition 2029 revision 3 adds explicit Actor inspection:

- `sdk.rooks.selected() -> SDK.RookId` returns this Participant's local Selection,
  or null. Read the Rook through `sdk.rooks.read(id)` to resolve its current Actor
  link. Selection conveys no Actor Access.
- `sdk.windows.open_actor(surface, actor_id) -> SDK.OperationResult` checks current
  access and opens an Actor-specific Extension Surface. Its SDK Window receives
  `opened(actor: SDK.ActorId)` on every explicit opening. The extension queries
  that Actor and renders the returned data using normal Godot UI and signals.
- An Actor sheet keeps the requested identity. Switching Actors calls
  `open_actor` again; Actor browsing and creation use separate ordinary windows.
  Opening another Actor replaces the previous instance of that sheet. Closing
  an Actor sheet releases it, and reopening queries fresh data. Docking, resizing,
  minimizing and restoring preserve the live sheet. Generic `windows.open`
  retains its existing window-state contract.
- Rookframe closes and releases inaccessible Actor sheets after current World
  state changes, including hidden sheets, without removing Actors or Rooks.
  Extension code continues to re-query on `sdk.world_changed` for Viewer/Owner
  changes and accepted data updates; the SDK does not render game data.

```gdscript
func opened(actor: SDK.ActorId) -> void:
    actor_id = actor
    refresh()

func refresh() -> void:
    var result: SDK.ActorResult = sdk.actors.read(actor_id)
    if result.ok:
        var hero: HeroData = result.actor.data
        name_label.text = hero.display_name
```

Edition 2029 revision 4 connects the native Actors list to the selected System's
active Presentation. Override these ordinary callbacks:

```gdscript
func describe_actor(actor: SDK.Actor) -> SDK.ActorSummary:
    var hero: HeroData = actor.data
    return SDK.ActorSummary.new(hero.display_name)

func inspect_actor(actor: SDK.ActorId) -> void:
    sdk.windows.open_actor(SHEET, actor)
```

`ActorSummary` contains `display_name` and an optional `Texture2D` portrait.
Rookframe reads only currently accessible Actors through the bound SDK, calls
`describe_actor`, and sorts the native list by name then Actor ID. Missing
portraits use the neutral UI Kit icon. The projection is local presentation,
not an extra durable Actor schema. Names refresh after accepted World changes
and Presentation replacement. Row activation rechecks access before delivering
`inspect_actor`; the sheet still queries current data in `Window.opened`.
Only the selected System's active Presentation provides these callbacks.
Actor creation stays a Package-authored action in `sdk.slots.actor_creation`;
it opens a creation form rather than another Actor browser.

Current caller context also supplies `display_name`; Actor Access entries supply
`is_connected` for identity/status presentation. These are domain values, not
native Participant Nodes.

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
  Await mutations: `var result = await sdk.rooks.move(id, position)` (also
  `create`, `link`, `unlink`, and `delete`). Local and remote calls return the same
  final result contract; success follows durable Authority publication and coherent
  local state. Remote completion uses a stock Godot signal. Reads remain synchronous.
- `builder.status()` explicitly returns unavailable. Through Edition 2029
  revision 5, `dice.status()` also returns unavailable; revision 6 replaces it
  with the narrow immediate named-roll capability documented below. Physical
  Throws/Rolls retain their Rookframe-owned boundary. Earlier facade revisions retain
  `targeting.status()` as unavailable.

### Shared Targeting — Edition 2029 revision 2

On desktop, point at a Rook and press **T**. **Shift+T** adds another target;
pressing **T** over an existing target removes it. **T** over empty tabletop clears
the set. On phone/tablet, the contextual crosshair toggles one Rook while retaining
other targets. The rail crosshair enters targeting mode: tap Rooks to add/remove,
drag to pan, Done to retain the set, or Clear to empty it. Selection and hover stay
local. Any current-Scene Rook may be targeted, including
an unlinked Rook; Targeting grants no Actor Access and applies no game rule.

`await sdk.targeting.snapshot() -> TargetSnapshotResult` returns the current
Session's accepted set after earlier targeting commands on the same reliable
channel. `.snapshot` contains `participant_id`, `session_id`, `display_name`,
`scene: SceneId`, `revision`, and `rooks: Array[RookId]` (unique, sorted, at most 64).
Snapshot failure is explicit; never calculate against a predicted target set.
`sdk.targeting.changed(snapshot: TargetSnapshot)` reports complete accepted sets
for visible Sessions, including an empty set when a Session departs. Use
`context().session_id` to distinguish your own set. Observe future changes from
the signal and query your snapshot when opening a surface or starting an action.
The host owns the target picker and named Presence Cursors. Packages observe
Targeting; they do not send cursor positions or acquire native multiplayer Nodes.
Targets and cursors disappear with their owning Session and never enter the save.

To adopt these additions, pin SDK `0.10.0`, declare Edition `2029` minimum revision
`2` in the Manifest and authoring lock, and regenerate the complete facade. Earlier
Editions retain their existing contract and reject these new operations. The
bounded Workshop uses the query → shared Hero calculation → awaited submission
path; it also demonstrates Viewer presentation and GM access changes.

The Workshop System example demonstrates authored Actor creation, a typed Resource
HP calculation/update, and journal System Records. The separate optional Calendar
uses only its scoped World value for Gregorian dates and dated notes.

Content entries expose `kind: SDK.ContentKind.Value`, matching `SDK.ContentKind.Value` query constants. Dictionary keys may contain acyclic container graphs; cyclic key dependencies reject before publication or Resource construction.

## Package Settings — Edition 2027 revision 6 / 2028 revision 3

An executable Enabled Package describes its fixed settings from its typed
Implementation. Rookframe supplies the namespace, including on headless roles.
Author individual descriptors as ordinary `.tres` Resources and assemble the
registration with typed GDScript:

```gdscript
const DATE_FORMAT: SDK.TextSetting = preload("res://rookframe/packages/<id>/logic/date_format.tres")
const TITLE: SDK.TextSetting = preload("res://rookframe/packages/<id>/logic/title.tres")

func describe_settings() -> SDK.SettingsRegistration:
    var registration := SDK.SettingsRegistration.new()
    registration.user = [DATE_FORMAT]
    registration.world = [TITLE]
    return registration

func validate_settings(candidate: SDK.SettingsCandidate) -> SDK.SettingsValidation:
    if candidate.scope == SDK.SettingsScope.Kind.WORLD and candidate.text(TITLE).strip_edges().is_empty():
        return SDK.SettingsValidation.new("Enter a title with visible text.")
    return SDK.SettingsValidation.new()
```

`TextSetting`, `ToggleSetting`, `IntegerSetting`, `NumberSetting`, `ObjectSetting`
and `ArraySetting` share a local `key`, `title`, `description` and typed
`Setting.Application`. Text supports choices and length bounds; numbers support
bounds. Objects contain typed properties; arrays contain an item descriptor.
Application policy belongs to the containing top-level setting; nested descriptors
must leave `application` at `LIVE`, or registration rejects.
The ordinary transaction contains every non-secret field, including nested
fields. It rejects missing, unknown, duplicate or invalid fields atomically.
`SecretSetting` declares a protected destination without a default or ordinary
value. Protected authentication and secret editing use the checked-service
contract, independently of this form.

`sdk.settings.user` and `.world` return `SettingsValues` snapshots. Read with
`text(descriptor)`, `toggle`, `integer`, `number`, `object` or `array`. Copies do
not carry registration Resources or service handles; mutating a local copy does
not change the accepted values. `sdk.settings.changed(scope)` signals only the
owning Package after acceptance; read a fresh snapshot to update behavior.
`read_other(package_id, scope)` permits a non-secret snapshot of another Enabled
Package. It grants no write, registration or subscription authority.

User settings belong to the installation and exact Package version. World
settings belong to the World and exact version; saving requires the real current
World Authority GM. Each scope has its own draft, validation, reset and Save.
Validators run on a detached fresh Implementation with only the portable
candidate; they have no bound SDK or live Implementation fields. Keep validators
pure: admission rejects Resource/Node/container writes, host operations and
signal effects throughout validation helpers, accessors and evaluator construction.
Local variables and typed RefCounted calculation/result fields are allowed.
Rejection displays its message on the containing form and leaves committed
values unchanged. Package management remains unavailable during a running World.

`Setting.Application.LIVE` updates behavior immediately. User descriptors may
choose `RESTART_LOCAL`; World descriptors may choose `RESTART_WORLD`. The first
Save explains the restart. A deliberate second action saves and recreates the
World activation/session within the same application. Editing the candidate
requires a new warning before any restart can be accepted.

A Presentation may assign an authored `SettingsViewDefinition` to its inherited
`settings_view`. Its scene extends the generated `sdk/settings_view.gd` path.
Override `edit()` to populate controls from the typed `draft` and `scope`.
Control callbacks use `draft.set_text(descriptor, value)` and the other typed
setters. Rookframe owns the containing form and complete Save; the custom view
must not persist changes itself. Different Presentations may choose different
forms for the same registered settings. Headless activation constructs no form.

Override `migrate_settings(migration: SDK.SettingsMigration) -> SDK.SettingsValues`
for a new exact version. The migration carries `scope`, `source_version`,
`target_version` and typed draft setters. The default returns the prior values;
target defaults fill newly added fields and obsolete fields are dropped before
validation. An existing target copy is reused. A newly validated copy publishes
atomically during guarded startup and survives a later unrelated startup failure.
Migration failure publishes nothing for that scope. Returning to a release
reuses its prior target; opaque World Data compatibility remains the Package's
separate responsibility.

Disable retains both copies. Exact-version uninstall removes that version's
User settings and retains World settings. Explicit Package Deletion removes
World settings/data and retains User settings. The existing protected-store
lifetime hooks apply; ordinary descriptor-copy serialization excludes secrets.

### Typed lists and dedicated Package Settings pages (0.6.0)

Edition 2027 revision 7 / Edition 2028 revision 4 add `TextListSetting` and
`IntegerListSetting`. Both declare bounded defaults and minimum/maximum item
counts; text lists also bound each name's length, integer lists each number's
range. Register them alongside scalar settings in `SettingsRegistration`.

`SettingsValues.text_list(descriptor)` returns a detached `TextList`;
`integer_list(descriptor)` returns an `IntegerList`. Their `size()`, `is_empty()`,
and `at(index)` methods are typed. Build a new list with `TextList.new()` or
`IntegerList.new()` and typed `append(value)`, then stage it with
`SettingsDraft.set_text_list` or `set_integer_list`. Reading or building a list
does not publish settings. Validation reads the candidate through the same types.

The host opens a package browser, then a dedicated page for the selected Package.
World Settings, My Settings, and Presentation have separate sections. A custom
`SettingsView` can use authored sections, conditional fields, and dynamic repeated
rows for complex configuration; Calendar 0.6.0 demonstrates month and weekday
editors. The host retains complete drafts while browsing between Packages and
owns scope Save/Reset, validation, authorization, restart confirmation, and
publication. Default object/list editors also use structured controls, not JSON.
## Checked integrations — Edition 2029 revision 1

This Edition replaces SDK 0.7 operation objects and polling with completed values.
To migrate, set the Manifest and authoring lock to Edition `2029`, minimum revision
`1`, pin SDK `0.8.0`, and regenerate the entire `sdk/` directory. Replace operation
creation/polling with `await`, bind an `Account` from the `SecretSetting` once, and
pass it to `network.service`. Device experience is typed as in Edition 2028.

The concrete SDK capabilities are `files`, `clipboard`, `network`, `secrets`,
`authentication` and `browser`. Asynchronous methods return their completed typed
result through ordinary GDScript `await`. Package scenes do not retain operation
IDs, poll in `_process`, or coordinate completion flags. `IntegrationResult`
subtypes expose `ok`, `code`, `message` and `retry_after`; they never represent pending work.

Rookframe owns main-thread completion delivery. Immediate failures return the same
typed result. A pending operation resumes its caller once while its SDK is active.
Stopping disposes the native completion signals without resuming suspended Package
code, and cancels ordinary transport. New work on a stopped scope is refused.
A launched browser flow may still finish its protected write independently, as
specified below. Window close normally hides the live scene; World teardown ends it.

### Files, selection, portraits and clipboard

```gdscript
var file: SDK.ScopedFile = sdk.files.user.file("notes/session.txt")
var saved: SDK.IntegrationResult = file.write_text("Reached the gate.")
var read: SDK.TextResult = file.read_text()
var remembered: SDK.InternalFileReference = file.to_reference()
var reopened: SDK.ScopedFile = sdk.files.open(remembered)
var selection: SDK.FileSelectionResult = await sdk.files.user.select_file()
var copy: SDK.IntegrationResult = sdk.clipboard.write_text(read.text)
```

`files.package`, `.user` and `.world` are `FileArea` values. `file(relative_name)`
and `folder(relative_name)` produce scoped values, never absolute OS paths.
Package content is immutable; World writes require the existing authority.
User files belong to this Package on this installation. Every operation checks
the live caller, area, traversal, links and approved backing before access.
Manager data, other Worlds, recovery and protected secrets remain outside these areas.

| Typed value | Operations |
| --- | --- |
| `ScopedFile` | `read_text() -> TextResult`, `read_bytes() -> BytesResult`, `write_text(String)`, `write_bytes(PackedByteArray)`, `read_portrait() -> PortraitResult`, `to_reference()` |
| `ScopedFolder` | `file(relative_name) -> ScopedFile`, `to_reference() -> InternalFolderReference` |
| `FileArea` | `await select_file() -> FileSelectionResult`, `await select_folder() -> FolderSelectionResult` |
| `Clipboard` | `read_text() -> TextResult`, `write_text(String) -> IntegrationResult` |

`FileArea.select_file()` and `select_folder()` open host-owned selection within
the requested area. They remain distinct choices. Remember an internal reference
to reopen an already authorized internal file without prompting again. References
contain only `FileLocation.Area` and a relative `name`; store those fields in your
Package data or an authored Resource and reopen with the current SDK's `files.open`
or `open_folder`. They confer no new access. A retained old `ScopedFile` keeps its
old lifetime and cannot be rebound to a later World.

`BytesResult.data` is `PackedByteArray`; `TextResult.text` is `String`.
`read_portrait()` decodes PNG/JPEG/WebP through the host into a fitted 512 × 512
`Texture2D`, exposed as `PortraitResult.texture`. Encoded input is limited to
8 MiB; arbitrary scene/Resource files are never evaluated as images. Decoding
retains the existing native decoder's memory limits. Clipboard text is limited
to 1 MiB of UTF-8. Check outcomes such as `display_unavailable`,
`clipboard_unavailable`, `clipboard_denied`, `portrait_invalid` and `portrait_limit`.
An OS that silently supplies an empty clipboard cannot always distinguish denial
from genuinely empty text. A GM cannot grant another device permission.

### Named network operations

Create an authored `ServiceDefinition` Resource with `name` matching a declaration
in the Package's `services.json`, then use `sdk.network.service(definition)`.

```gdscript
var headers: SDK.RequestHeaders = SDK.RequestHeaders.new()
headers.accept = "application/json"
var response: SDK.ResponseResult = await sdk.network.service(API).request(
    "identity", SDK.HttpMethod.Value.GET, "", headers)
if response.ok:
    status.text = "HTTP %d" % response.status
```

`request(path, method = GET, body = "", headers = null)` returns typed status,
text and bytes. Transport success is separate from HTTP success; inspect `status`.
`HttpMethod.Value` includes GET, POST, PUT, PATCH, DELETE, HEAD and OPTIONS;
the declaration still restricts allowed methods. `RequestHeaders` allows only
authorization, accept, content_type, if_match, if_none_match and api_key.

`await open_stream(path) -> StreamResult` supplies `.stream: ScopedStream`.
Use `await stream.read(maximum_bytes = 65536) -> BytesResult` and `stream.close()`;
an empty successful chunk is end-of-stream. `await download(path, target: ScopedFile)`
returns `IntegrationResult` after publishing the internal file. `await upload(path,
source: ScopedFile, method = POST)` returns `ResponseResult`. Streams and transfers
retain their declaration permissions and bounds. A bound account supplies their
authorization too; request-specific custom headers remain on `request()`.
Cross-SDK file/account values are refused with `scope_mismatch`.

```gdscript
var opened: SDK.StreamResult = await service.open_stream("messages")
if opened.ok:
    var chunk: SDK.BytesResult = await opened.stream.read(1024)
    opened.stream.close()
    if chunk.ok:
        status.text = "Read %d bytes" % chunk.data.size()
```

Declarations do not authorize private network access. The application-owned
destination checks, DNS/private-address checks, redirect rules, byte limits and
per-Package/destination traffic and concurrency budgets apply to every adapter
and survive World switches. Trusted companion pairing comes only from explicit
host configuration with its actual address and certificate fingerprint. A port
number or Package declaration is insufficient. Stopping/revoking cancels ordinary
requests, streams and transfers; Package code is never called after stop.

### Protected settings and provider authentication

Register top-level `SecretSetting` descriptors in User or World settings as usual.
The host renders password input plus immediate save/clear actions separately from
ordinary drafts. Secret values never appear in settings snapshots, migration,
replication, World copies, exports or backups. World controls require the current
GM World Authority. User secrets are exact Package/version on this installation;
World secrets are exact Package/version at the original World Address. Dedicated
authorities have no installation-user scope. Protected keys are at most 64
characters and cannot be nested or request an ordinary settings restart.

Set a descriptor's optional `authentication: AuthenticationProviderDefinition`
to expose host-owned Sign in, Refresh and Clear actions instead of manual input.
The provider Resource's `name` must match admitted `authentication.json`.
Neither Resource contains a confidential client credential.

```gdscript
var account: SDK.Account = sdk.authentication.account(ACCOUNT)
var service: SDK.NamedService = sdk.network.service(API, account)

# A deliberate sign-in action:
var signed_in: SDK.IntegrationResult = await account.sign_in()
if signed_in.ok:
    var response: SDK.ResponseResult = await service.request("identity")
    if response.ok:
        status.text = "HTTP %d" % response.status
```

`authentication.account(setting, area = SDK.SettingsScope.Kind.USER)` binds the
setting's configured provider and protected key once. Use `WORLD` for a GM World
account. The handle never rebinds to another SDK or World. `account.status()`
returns `AccountStatus`: check `ok`, then `state` (`SIGNED_OUT`, `SIGNED_IN` or
`EXPIRED`). Errors use `UNAVAILABLE` and a sanitized `code`/`message`.

`network.service(definition, account = null)` binds authentication for requests,
streams, downloads and uploads. It reads current credentials for each operation,
validates their provider, and applies Authorization without exposing tokens to
the ordinary workflow. Caller-supplied Authorization conflicts are refused.

`account.refresh_policy` is typed `Account.RefreshPolicy`. `WHEN_EXPIRED` (default)
refreshes expired credentials before sending. `EXPLICIT` returns `refresh_required`
instead; the Package can call `await account.refresh()`. Missing credentials return
`sign_in_required`. A refresh already in progress may return `refresh_busy` under
the existing protected rotation lease. HTTP responses are never automatically
replayed, including 401 and non-idempotent requests, and a request never opens a
browser. The Package owns decisions about the provider's HTTP response and account
meaning. `account.clear()` revokes the stored credential.

`SecretArea.entry(name)` accesses a named protected entry without a settings
descriptor; `.setting(descriptor)` uses its key. `SecretEntry.read()` returns
`SecretResult` with `found` and raw `text`; `write(String)` and `clear()` return
`IntegrationResult`. `read_tokens()` returns `ProviderTokenResult` with `found`
and typed `ProviderTokens`: access_token, token_type, refresh_token, scope,
has_expiry and expires_at (Unix seconds). Missing credentials are a successful
`found = false`; malformed token material yields sanitized `secret_format`.
`account.read_tokens()` supplies the same typed raw credentials with an additional
provider identity check when an advanced integration needs them.
Only the owning Package receives these raw credentials for its checked API use.
Keep them out of ordinary data and diagnostics. Rookframe does not define provider
membership, entitlements or store acquisition credentials.

`await account.sign_in()` returns a completed `IntegrationResult`. Rookframe
confirms the original Package/version, provider origin and destination before
opening the browser. Cancel/World exit before confirmation opens nothing.
Replacement/revocation while confirmation is open invalidates its captured
destination generation. Headless launches return `browser_unavailable`.

After launch, the application owns the native return, state/issuer validation,
PKCE proof, checked exchange and conditional protected write. It may finish after
World exit without retaining Package code, invoking a stopped callback or changing
the destination to a newly opened World. Uninstall/deletion/revocation/intervening
secret edits invalidate stale completion. Callback URLs contain a one-use code,
state and issuer, never provider tokens. Flows expire after ten minutes and do not
survive application termination.

`await account.refresh() -> IntegrationResult` refreshes using the same
protected exchange, rotation lease, provider identity and conditional write.
`await sdk.browser.open(https_url) -> IntegrationResult` confirms a deliberate web
link without creating credentials. Public native clients must support the native
redirect, PKCE and issuer contract. With `publisher-transfer`, the Publisher's
backend owns confidential exchange and refresh; its client secret never ships in
a Package. New compatible provider declarations need no per-provider app build.
The shipped example uses placeholder providers. Controlled evidence is not live
provider certification; deployment still requires the provider's registration.

## Shared Action Log (2029 revision 5)

Deliberately publish a completed outcome through `sdk.action_log.publish` from
an Implementation or Presentation. Both System Extensions and enabled optional
Packages use the same capability. Await its `SDK.ActionLogResult`: `ok` means the
World Authority accepted, saved locally and broadcast the entry; `sequence` is its authoritative
order. Success does not guarantee every Participant received or saved it.
Attribution is supplied by Rookframe from the authenticated Participant and bound
Package. Publishing does not roll dice or infer outcomes from other SDK calls.
Rookframe automatically adds only completed raw Rolls. Builder operations,
object manipulation, targeting, and every other app action remain silent unless
an Extension deliberately publishes a message through this capability.

```gdscript
var message := SDK.ActionLogMessage.new("Watch begins")
message.text = [SDK.ActionLogText.new("The northern gate", "strong"),
    SDK.ActionLogText.new(" falls silent.")]
message.dice = [SDK.ActionLogDie.new(20, 17)]
message.result = "READY"
message.tone = "success"
var outcome: SDK.ActionLogResult = await sdk.action_log.publish(message)
if not outcome.ok:
    show_failure(outcome.message)
```

The title accepts 1–72 printable characters. Text contains at most eight runs
and 512 characters in total, using `normal`, `strong`, or `emphasis`; newlines
are allowed in runs. Dice preserve caller order, up to sixteen raw faces with
2–1000 sides and values within those sides. `result` allows 32 printable
characters; `tone` is `info`, `success`, `attention`, or `roll`. Markup is literal
text. Links, buttons, callbacks and embedded UI are not message fields.

Each Participant locally retains the latest twenty received entries, newest at the bottom.
The host viewer shows four by default and expands into a scrollable retained
window. Reading state is local to each Participant. Evicted entries have no
archive. Each application saves its received window locally and restores it when
reconnecting or reopening that World. It does not recover missed entries from peers;
histories may differ between Participants. Reports are sent one at a time by
reliable Godot RPC. Local log storage is separate from the World document.
World revision and durable entity validity do not depend on log history.
Malformed messages, unavailable sessions and disabled Packages are refused;
local save failures are reported. Do not retry an
uncertain publication automatically: an intentional second call is a new entry.

## Immediate named dice (2029 revision 6)

The selected System Extension may request a physical Roll with ordered, named
terms. Rookframe uses the same native dice bodies, collision, settling,
Participant identity, World Authority, replication, and Action Log path as the
human Dice Tray. The originating graphical Participant runs the natural physics;
when the World Authority is remote or dedicated, it validates and commits
the reported upward faces. There is no predicted result, success calculation,
modifier, or separate Package network path.

```gdscript
var request := SDK.DiceRequest.new([
    SDK.DiceTerm.new("attack", 20),
    SDK.DiceTerm.new("damage", 6, 2)
])
var rolled: SDK.DiceRollResult = await sdk.dice.roll(request)
if not rolled.ok:
    show_failure(rolled.message)
    return

var report := SDK.ActionLogMessage.new("Blade strikes")
report.text = [SDK.ActionLogText.new(
    "The attack connects; damage is resolved by the Extension.")]
for term in rolled.terms:
    for value in term.results:
        report.dice.append(SDK.ActionLogDie.new(term.faces, value))
report.result = "HIT"
report.tone = "success"
var published: SDK.ActionLogResult = await sdk.action_log.publish(report)
```

`SDK.DiceTerm` contains `name: String`, `faces: int`, and `count: int`.
Names are trimmed, printable, unique within the request, and at most 64
characters. `faces` accepts the shipped d4, d6, d8, d10, d12, or d20; `count`
is positive; the complete request contains at most sixteen dice.
`SDK.DiceRequest.terms` preserves caller order.

Successful `SDK.DiceRollResult` values contain `terms:
Array[SDK.DiceTermResult]` in the same order. Each result exposes the unchanged
`name`, `faces`, and ordered `results: Array[int]`. `sequence` identifies
Rookframe's built-in raw Roll entry, which is already committed to the shared
Action Log before the await completes. The System Extension decides attack,
defence, damage, armor, tables, and every other game meaning. It must explicitly
publish a separate message when that interpretation belongs in the Action Log;
the dice capability never opens a dialog or invents a game outcome.

Immediate dice are unavailable to optional Packages, an unselected System
Extension, a headless caller without a graphical tabletop, a World that is not
ready, and an ended or revoked World Session. A pending await is World Session-bound:
teardown discards its completion, and it cannot attach to a later World Session or
another World. Invalid requests create no Throw or Action Log entry.

## Requested human Throws (2029 revision 7)

The selected System Extension can request an immutable physical Throw from one
World Participant. The request is durable World state; the dice bodies and their
motion are ordinary transient Godot nodes. A disconnect removes old motion while
the same pending request remains available to the target's fresh Session.

```gdscript
var request_id: String = sdk.dice.new_request_id()
var waiting := await sdk.system_records.create("requested-throw-action", {
    "request_id": request_id,
    "participant_id": target_participant_id,
    "reason": "Waiting for the target Participant's attack Throw."
})
if not waiting.ok:
    show_failure(waiting.message)
    return

var planned := SDK.HumanThrowRequest.new(request_id, target_participant_id, [
    SDK.DiceTerm.new("attack", 20),
    SDK.DiceTerm.new("damage", 6, 2)
])
var current: SDK.HumanThrowResult = await sdk.dice.request_throw(planned)
if not current.ok:
    show_failure(current.message)
    await sdk.system_records.delete(waiting.system_record.id)
    return
```

`new_request_id()` allocates the UUID before the Extension records why its action
is waiting, so a fresh binding can safely submit or recover the exact same request.
An empty `request_id` also asks Rookframe to assign a UUID on first acceptance,
but that form is intended for callers that do not need to persist work first.
Every retry must use the accepted identity, the same target, and the same ordered
terms. Reusing an identity with a different target or plan is a `request_conflict`.
A successful snapshot has `status` `pending`, `rolled`, or `cancelled`, plus
`request_id`, `participant_id`, the immutable `plan`, terminal `terms`, and the
raw Roll `sequence` (zero until rolled).

This operation does not wait for the human. Listen for `sdk.world_changed`, or
reconcile after Package activation/reconnect, and call it again:

```gdscript
var retry := SDK.HumanThrowRequest.new(saved_request_id, saved_participant_id,
    saved_terms)
var current: SDK.HumanThrowResult = await sdk.dice.request_throw(retry)
if current.ok and current.status == "rolled":
    var report := SDK.ActionLogMessage.new("Attack resolved")
    report.text = [SDK.ActionLogText.new(
        "The Extension interpreted the completed human Throw.")]
    report.result = "HIT"
    report.tone = "success"
    await sdk.action_log.publish(report)
    await sdk.system_records.delete(waiting.id)
elif current.ok and current.status == "cancelled":
    var report := SDK.ActionLogMessage.new("Attack cancelled")
    report.text = [SDK.ActionLogText.new("The requested human Throw was cancelled.")]
    report.result = "CANCELLED"
    report.tone = "attention"
    var published := await sdk.action_log.publish(report)
    if published.ok:
        await sdk.system_records.delete(waiting.id)
```

The target sees the existing native Dice Tray with the requested pool prefilled
and editing locked. Dragging and releasing uses the normal physical dice path.
Back, closing the tray, right-click, or releasing outside the tabletop is an
explicit cancellation and creates no Roll report; transient interruption is not
cancellation. Rookframe appends the raw Roll once, independently of the retained
latest-twenty Action Log window. The Extension owns all meaning and publishes any
separate resolution explicitly. Optional Packages and non-selected Systems cannot
request Throws.

### Rook appearance (Edition 2029 revision 10)

`await sdk.rooks.set_miniature(rook_id, content_reference)` returns a `RookResult`.
It replaces only that controlled Rook's Miniature using available enabled World
Content. The Rook identity, Actor link, Scene and pose remain unchanged. World
Authority checks ordinary Rook control and refuses changes while held; success
follows durable publication and uses the existing Rook replication. Actor default
appearance remains System-owned Actor data and is used when placing future Rooks.

## Session-bound requested Throws (2029 revision 11)

Use `sdk.dice.request_session_throw(request)` for a human Throw that must end
when either its requesting Participant or its target Participant connection ends.
Both must be connected at creation. The immutable plan includes the requester;
a cancelled request ID always returns cancelled, including after reconnect or
Authority restart. A lost required connection cancels pending requests even if
that Participant has another application connected. Generic `request_throw` keeps
its existing durable recovery behavior.

`sdk.dice.cancel_throw(request_id)` is available to the target Participant and,
for session-bound requests, their original requester. It never removes or changes
an already completed Roll. Packages must discard their own pending consequences
on interruption and must not restore an action from a completed request.

SDK `Window.closed` is an ordinary Godot signal emitted on explicit managed-window
closure, dock replacement, Actor replacement or loss of access. Temporary Dice
Tray hiding and minimization do not emit it. Connect the signal to the System's
action cancellation. The source sheet stays alive during a Throw and reappears
when the tray ends; reopening it earlier retains its participant-adjusted layout.
No workflow, undo, takeover or action recovery is provided.

## Authority-side System intents (2029 revision 12)

`await sdk.system_actions.submit(name: String, data: Variant) -> DataResult` sends
a bounded intent through Rookframe's existing reliable Godot RPC. It carries no
Participant/role assertions. The selected System Implementation overrides:

```gdscript
func handle_system_intent(context: SDK.SystemActionContext, name: String, data: Variant) -> Variant:
    # Validate the action, then deliberately return its public outcome.
    return {"state": "error", "message": "Unsupported action."}
```

The callback runs synchronously on peer-1 World Authority. It must not await or
retain the context; all its operations expire when the callback returns. It works
without a local Participant or fake GM on dedicated authority. Ordinary SDK CRUD
keeps its Participant access rules. Nested ordinary SDK operations are refused.
The callback's input and public return value are Package data; neither conveys
runtime authority. Every Participant already receives the complete shared World data.
Actor privacy is a UI display rule: use public labels and appropriate detail in
reports, and hide inaccessible sheets. This callback adds no confidentiality boundary.

The context provides:

- `caller() -> DataResult`: authenticated `participant_id`, `session_id`,
  `display_name`, `is_gm`, `is_authority` and current shared target Rook IDs in `targets`.
- `read_actor(ActorId) -> ActorResult`: authoritative snapshot of shared Actor data; its
  `access_level` is the requesting Participant's actual access, never a new grant.
- `read_rook(RookId) -> RookResult`: authoritative Actor link and committed position.
- `actor_access(ActorId) -> ActorAccessListResult`: Player grants and connection state.
- `distance(RookId, RookId) -> DistanceResult`: existing logical-center Scene
  distance. One tabletop unit equals one metre; multiply feet by 0.3048.
  Held previews do not move committed centers. This performs no line-of-sight test.
- `read_throw(id)`, `request_throw(HumanThrowRequest)`, `cancel_throw(id)`:
  session-bound requested Throws attributed to the authenticated requester.
- `commit(Array[ActorChange], ActionLogMessage = null) -> OperationResult`:
  validate every distinct Actor replacement and the public report before saving
  one coherent World change. Invalid batches apply nothing; failed saves end the
  World and are never acknowledged. It grants no Actor Access. Once accepted,
  report storage failures use the existing local Action Log retention/retry path.

The System owns rule checks, meaningful idempotency, its active action lifetime,
and every selected target's validation. The host supplies no generalized workflow,
resumption, undo, game rules or implied target permission. `ActorChange` takes an
Actor ID and its complete replacement data. At most 32 Actors can change together.

### Targeting handoff (2029 revision 13)

`targeting.choose() -> OperationResult` starts the existing tabletop target picker from the Package’s active managed window. Visible windows temporarily yield the tabletop; Done restores their placements and focuses the source window. Read `targeting.snapshot()` or subscribe to `targeting.changed` for the committed selection. This does not submit an action or change access.

### Live Participant sessions (2029 revision 14)

`context.participant_sessions() -> DataResult` returns all currently connected
Participant sessions as dictionaries containing `participant_id`, `session_id`
and `is_gm`. It uses the same callback-scoped authority as the other context
operations. A dedicated Authority contributes no invented Participant or GM.
Compare the exact session identities captured when an action begins before
accepting later decisions, including after all requested Throws have settled.
An absent or replaced session ends that action; reconnect does not resume it.
This query changes no grants and does not filter shared World gameplay data.

### Authored decision dialogs

SDK Authoring Kit 0.22.1 admits stock Godot `Window` scenes for compact authored
UI. Package-owned Windows can `popup_centered()`, `hide()`, receive
`close_requested`, and mark their own input handled. Authored Controls can
`grab_focus()`, and input callbacks can inspect `InputEvent.is_action_pressed()`.
Casts and annotations do not grant access to the host Window or Viewport.
The public UI Kit close icon and managed-surface frame are available for this
composition; existing design tokens and assets remain unchanged.

### Actor creation from System actions (2029 revision 15)

`context.create_actors(requests: Array, creator_participant: String,
report: ActionLogMessage = null) -> ActorListResult` materializes 1–32 individual
Actors from declared Actor Definitions. Each request contains `package_id`,
`local_id` and `choices`, matching the child requests for `actors.create_atomic`.
Every definition and the report are validated before one coherent World save.
Failure creates none; success returns the fresh Actors in request order and
publishes the supplied outcome through the existing Action Log retention path.

The connected creator receives ordinary Owner access to each Actor, with the
GM retaining inherent Owner access. Only a GM-initiated action can name another
connected Participant as creator. No Rooks or separate permission model are
created. The callback must validate the rule and its live action before calling;
its capability expires on return, and the System remains responsible for
idempotency and rejection of late results. All Actor data and grants continue
to be shared with every Participant.

### World data from System actions (2029 revision 16)

`context.read_world_data() -> DataResult` reads the complete selected System
Package's World data. `context.commit_world_data(value, report = null)` replaces
that value durably, then publishes the validated Action Log report after success.
A malformed report or failed save publishes no new outcome. Null means never
committed and is rejected as a replacement. The context expires on callback exit.
The System validates the authenticated caller and its domain rules. This works
for remote GM callers and dedicated authority without a local GM. Every
Participant receives complete World data; display privacy belongs to Presentation.
Use this callback boundary rather than nesting ordinary World data operations.

### Rook Miniature previews (2029 revision 17)

`rooks.preview(id: RookId, target: Control) -> OperationResult` displays the
Rook's current Miniature in a Package-authored UI placeholder. The host reuses
its existing Content preview renderer and owns resource resolution and the 3D
preview scene. The placeholder must be inside this Package's bound UI and have
an authored size. Its children are released with the placeholder. Calling again
reuses the preview; call after `world_changed` to reflect Miniature changes.
This operation changes no World data and returns no host node or image handle.
A missing Rook, unavailable Miniature or unrelated UI target returns a failure.

`rooks.selection_changed` announces Participant-local tabletop selection changes.
Read `rooks.selected()` when handling it. `windows.close(surface)` closes that
Package's retained surface through the ordinary host lifecycle, including its
`closed` signal. It preserves local placement and cannot close another Package's
surface. Closing an already closed surface succeeds without recreating it.

### Rook hiding (Edition 2029 revision 18)

`await sdk.rooks.set_hidden(rook_id, hidden)` returns a `RookResult` after the
visibility change is durable. This is a GM-only Rookframe capability available
to System Extensions and optional Packages. Read `result.rook.hidden`, or use
`rooks.read` / `rooks.list` to inspect the current flag.

A hidden Rook remains in the complete shared World state. Players do not render
or pick it; the GM sees diagonal shader stripes and retains selection and
control. Hiding removes that Rook from every Session's targets, and nobody can
target it while hidden. Showing it again does not restore discarded targets.

```gdscript
var result := await sdk.rooks.set_hidden(rook_id, true)
if not result.ok:
    push_warning(result.message)
```

### Miniature browser previews (Edition 2029 revision 19)

`content.preview_miniature(reference: ContentReference, target: Control)` returns
an OperationResult and renders an enabled Miniature into the Package's bound
authored UI. It reuses the host Content renderer, requires no existing Rook and
exposes no resource path. Unavailable/wrong-kind content clears stale previews.
`ContentEntry.package_title` supplies the source Package display name; identity
remains the complete ContentReference. The UI Kit Miniature browser can emit
preview requests directly to this capability. Selection never mutates World data.

`ContentEntry.localized_title` resolves the source Package’s default translation
domain in the current UI language, with that Package’s default-locale fallback.
`title` remains the original Manifest display name.

`content.list` and `content.read` also work synchronously inside a live System
intent callback. They read shared, declared Content metadata through that current
intent; they do not start a nested World operation or grant mutation authority.

## Rookframe standard Content (Edition 2029 revision 20)

Every World includes Rookframe's application-owned Content. Its stable source
identity is `fbf21a78-626e-4f35-b2ce-bd196083d9b7`, carried in the existing
ContentReference `package_id` field. It is not a Package to install or enable.
The application release supplies these resources; source title is Rookframe.
Use normal Content queries, previews and Rook operations, never resource paths.

Miniature local IDs: `default-miniature`, `knight`, `goblin-raider`, `goblin`,
`barbarian`, `bandit`. The default is a featureless dark-grey humanoid.
Wall Style IDs: `wood`, `ornate-stone-panel-wall`, `rough-stone-wall`,
`timber-plaster-wall`. Surface Finish IDs: `stone`, `dark-stone-tiles`,
`oak-planks`, usable for both Floor and Ceiling. Names are localized by Rookframe.

Systems may use the default implicitly when no Miniature preference is saved.
A missing explicit preference is not the same as no preference: keep it visible
as unavailable and let the user choose a replacement. Built-in Content is
shared with every Participant through the ordinary World Content library.
