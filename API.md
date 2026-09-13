# Typed Package authoring — SDK 0.8.0

Edition 2029 revision 1 includes the typed UI, World, settings and awaitable
integration APIs below. The earlier Edition/revision headings record when shared
facilities were introduced. Edition 2029 uses the typed `DeviceExperience` return
from `presentation_experience()`.

SDK 0.8 also authors earlier 2027 revisions 1–7 and 2028 revisions 1–4. For the
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
