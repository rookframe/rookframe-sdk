# Rookframe SDK Authoring Kit 0.32.42

This version binds the public Silkbound Ledger theme, fonts, textures and
collection component. Package-owned Controls can apply admitted font/style
resources and change reviewed presentation properties on stock `duplicate()`
copies. Shared resources stay read-only. Public composition slots keep their
owning component's provenance; stock OptionButton item icons are type checked.
SDK Editions and gameplay APIs remain unchanged.

This release adds Package creation, scene registration and the **Development World** editor dock. Run the compiled
Rookframe development runtime from the Package's own Godot project, then save
scripts and reimport models without restarting the World. Unpublished Packages
need no published baseline. See [development setup](#run-a-development-world-without-rookframe-source).

The SDK also admits script-free, Package-owned `FontVariation` resources based
on the original public `assets/fonts/Inter-VariableFont_opsz,wght.ttf`. Authored
`variation_opentype` accepts a finite `wght` coordinate; `opentype_features`
accepts `tnum: 1` for tabular figures. Stock integer tags and the reviewed string
names are supported, with ambiguous duplicate aliases refused. The original
font and its source/imported dependency bytes remain bound to checked loading.
It also admits the stock serialized StyleBoxFlat shadow properties:
`shadow_color` (Color), `shadow_offset` (Vector2), and `shadow_size` (integer).
These exact Resource rules add no constructors or GDScript native operations.
SDK Editions, APIs, parser and public UI Kit/font bytes are unchanged.

The kit records the stock TextEdit-to-Control inheritance used by the
unchanged public TextArea. Inspected Package scenes and their reviewed public
UI children retain owned provenance for existing Control presentation methods.
TextEdit construction and editor-specific operations remain unadmitted. The
existing basic native property contract is unchanged; theme/focus and Resource
operations retain their specific ownership, type and dependency checks.
SDK Editions, APIs, parser and public UI Kit bytes are unchanged.

The kit also admits the stock serialized `StyleBoxFlat.draw_center` Boolean and
four numeric `expand_margin_*` render properties on inspected Package-owned
native Resources. They can draw focus borders outside the Control rectangle
without expanding its clickable area. Exact Resource type, Script effects,
ownership and dependency checks remain required; no GDScript operation is added.

The kit binds the existing public `theme/task_action.tres` FontVariation
(Inter 700) for authored font overrides on Package-owned native Controls,
including attached or inherited scripts. The public display font remains
supported. Resource closure, hashes, type and ownership checks still apply.
SDK Edition 2029 remains at revision 29, with unchanged APIs, parser and public
UI Kit bytes.

The kit replaces inline Actor portraits with retained World filepaths and
adds authority-side conversion of saved image bytes. Regenerate portrait callers
and save only the returned filepath through ordinary Actor/World operations.

The kit also admits authored stock `AtlasTexture` resources that frame already
admitted Package textures. Serialized atlas properties remain type checked;
scripts, unrelated resources and native API escalation remain rejected. Loaded
and authored atlas values use the existing `Texture2D` capability.

This kit admits the stock `LineEdit.text_changed` signal on Package-owned
authored or constructed controls, carrying the native String callback value.

Edition 2029 revision 28 adds `sdk.windows.open_actor_task(surface, actor, task)`
and `Window.opened_task(actor, task)`. An authored task receives copied Package
context and remains bound to its initiating Actor through selection changes.
Ordinary Actor inspection and its private draft behavior remain unchanged.

Edition 2029 revision 27 adds the selected System Extension’s Character HUD
contribution, owned selection/fallback context and native Dice Tray entry point.
It uses authored Godot Controls above floating windows and below docks and
Full-viewport Surfaces, without exposing host Nodes.

Edition 2029 revision 26 adds `sdk.dice.roll_requested(request_id, source)`.
An authored full-viewport surface can present its Participant's pending requested
Throw as Window Dice using the accepted immutable plan. Closing that surface
preserves its dice; the explicit request identity prevents unrelated requests
from attaching to retained surfaces.

Edition 2029 revision 29 adds authority-side retention for saved inline portrait
conversion. Shared portraits now use World-relative filepaths; regenerate the
facade and replace saved byte values through synchronous System saved-data
migration callbacks before Authority startup. Dedicated Authority uses the same
conversion without requiring a local Participant.

Edition 2029 revision 25 introduced host-owned Actor portrait selection and decoding.
The result contains a local texture and a retained World-relative filepath for
ordinary Actor or World data. Original image bytes, format and dimensions remain
unchanged. Multiple Actors may share a file. Selection cancellation leaves
existing Actor data unchanged.

This kit also admits stock read-only key callbacks and exposes collection focus
return through the public UI Kit. Native input construction remains prohibited.

Revision 24 adds fixed `full-viewport` task placement and cancellation
of abandoned immediate physical Rolls by their caller-owned request identity.
Full-viewport tasks retain underlying windows, host authored child tasks, and
render their dice locally while accepted results remain shared. See [API.md](API.md).

Author ordinary Godot Packages for SDK Edition 2029 (revisions 1–29). The kit also authors 2027 revisions 1–7 and 2028 revisions 1–4;
2027:8 / 2028:5 authors retain SDK 0.7.0. Unchanged generated capabilities keep
their existing contracts. Earlier inline-byte portrait callers must regenerate
and adopt the filepath API; the old portrait gameplay API is replaced. The kit supplies a
Package-local facade, an optional editor plugin, and `init`, `facade`, `check`,
`build`, `publish-github` and `catalogue` commands. It is an authoring dependency; only the generated facade
ships in a Package. The UI Kit is a separate source dependency.

Express game logic through Rookframe domain capabilities: Actors, Rooks, Scenes,
Worlds, access, and targeting. The SDK handles authority, persistence and engine
integration behind those contracts. Use ordinary GDScript calculations, Resources,
Godot controls and signals, and public UI Kit components for their native roles.
The SDK does not introduce a replacement UI or signal framework.

SDK 0.32.36 binds the approved Silkbound Ledger Theme, font resources and
Miniature list/preview browser from the public UI Kit. The approved linen uses
a lossless runtime tile so native SVG import does not alter its fine weave.
Stock FontFile resources retain the original EB Garamond data and native shaping
with prerendered glyph coverage for the approved reference appearance. Existing surfaces opt in
by assigning that Theme; SDK Edition operations and revisions are unchanged.

## Install the two dependencies

Use Godot **4.7.2**, Python **3.10+**, Git and the **.NET 10 runtime** on PATH.
Install Godot's matching export templates for the local authoring host. The exporter produces a shared PCK, not an OS application.
The tools accept an explicit Godot executable on every host. Development mode
requires a matching stock Godot .NET editor and compiled runtime bundle for the
local OS and CPU architecture.

Start with a normal `project.godot`. Install gd-plug's bootstrap at
`addons/gd-plug/plug.gd` using its [upstream instructions](https://github.com/imjp94/gd-plug).
The [Calendar example](https://github.com/rookframe/rookframe-calendar) includes
that bootstrap and its license, so cloning the example needs no bootstrap step.
Use this `plug.gd`:

```gdscript
extends "res://addons/gd-plug/plug.gd"

func request_quit(exit_code := -1) -> bool:
    return super.request_quit(0 if exit_code == -1 else exit_code)

func _plugging() -> void:
    plug("rookframe/rookframe-sdk", {"tag": "v0.32.42", "include": ["addons/rookframe_sdk"]})
    plug("rookframe/rookframe-ui-kit", {"commit": "9a124f5b5ebcf03a064b314771a303f3ca11d83f", "include": ["rookframe/ui"]})
```

The SDK tag is an exact immutable authoring version. The separately recorded
UI version is `v1.0.0-rc.1`; its full commit is authoritative because the initial
candidate label may move. This does not publish stable UI Kit 1.0.0.
Run from the author project, replacing `godot` with your executable:

```sh
godot --headless --path . --script plug.gd install
python3 addons/rookframe_sdk/rookframe_authoring.py init --project . --name "My Package" --ui
python3 addons/rookframe_sdk/rookframe_authoring.py check --project . --godot /path/to/godot
python3 addons/rookframe_sdk/rookframe_authoring.py build --project . --godot /path/to/godot
```

`init` also works in an empty directory when invoked from an installed kit.
Install the resulting `plug.gd` dependencies before opening Godot. `--ui` adds
an authored scene, a Rail entry and its Presentation for a new Package. Without
it the initial Package has an Implementation only. Packages have no OS dependency
or target: one `package` export produces the same code and resources for iOS,
Android, Linux, macOS and Windows. There is no OS target command-line option.
The export automatically includes the required Godot texture format alternatives.
Phone/tablet/desktop variation belongs to Presentations: phone → tablet → desktop,
tablet → desktop → phone, and desktop → tablet → phone. Fallback is visible and
non-blocking; no Presentations means the Package runs without Package UI.
Existing published archives remain usable without rebuilding; legacy member
labels do not declare OS support.
A build requires no account, GitHub publication or Catalogue entry.

Commit the Manifest, Package source/scenes, generated facade, `.rookframe/authoring.lock.json`,
`plug.gd`, project settings and export presets. Ignore `.godot/`, `.plugged/`,
`addons/rookframe_sdk/`, `rookframe/ui/`, `build/` and Python caches.
The SDK lock records its exact version; the UI lock records its independent
SemVer and full commit. Explicit UI upgrades also update the gd-plug commit.
Checks compare installed bytes to the selected release; alternate UI releases
use the local gd-plug Git object store, with no network fetch or execution.

## Author in Godot

Enable **Rookframe SDK** in Project Settings → Plugins for an existing project.
A newly initialized project enables it automatically. On editor entry the
plugin generates a missing facade or diagnoses a stale one. Project → Tools
provides **Rookframe: Check Package** and **Rookframe: Build Package**. These
commands report in Output and may take a moment while Godot prepares copies.
Set `ROOKFRAME_PYTHON` if Python is not on the editor's PATH.

The dock's **Package** tab works in a blank Godot project with the SDK add-on
installed. Enter a name, choose **Extension with UI**, **Content pack** or
**System Extension**, and choose **Create Package**. Then choose **Install
authoring dependencies** to install the locked UI Kit and gd-plug bootstrap.
This preserves existing files and refuses conflicting dependency bytes.

Save your scenes, scripts and imported models below the Package directory shown
in the dock: `res://rookframe/packages/<package-id>/`. Other subdirectories are
your choice. Select a saved scene with **Use open scene** or **Browse**, give it
a stable ID and choose **Register scene**:

- For UI, choose a left/right Rail window, Package UI root, selected-Rook slot,
  or (for Systems) Actor Creation. Attach ordinary Godot scripts to the scene's
  Controls. Registration creates typed SDK descriptors and a generated
  Presentation wrapper which also calls your existing `compose()`.
- For models, choose Prop, Wall Style, Surface Finish or Miniature. **Prepare
  model scene** creates an editable wrapper that retains the imported model
  instance. Props receive a starting box collider; inspect it before registering.
  Walls and finishes need a single-surface mesh named `Surface`, with UVs and a
  native 3D material. Walls run along +X with +Y up; finishes lie in XZ.
  Preparation adds scale and sample-span metadata. One Godot unit is one World unit.

Registration updates the Manifest. Content appears in the corresponding tools
of the running Development World after import. Adding a file alone does not
register Content or place an instance in the World. Registering an additional
UI entry also updates the running Presentation. Commit `.rookframe/ui-entries.json`
with the generated descriptors and wrapper; customize your original Presentation
and scenes. If you edit the generated wrapper directly, registration refuses to
overwrite it.

## Run a Development World without Rookframe source

Install the compiled development support supplied with Rookframe and open this
project in its matching **Godot .NET** editor. Open **Project → Tools → Rookframe:
Development World**. In the dock, choose the runtime's
`rookframe-development-runtime.json`, a local World name, and any published
Package Manifest URLs you want to use. An optional Package also needs a published
System Manifest URL; an editable System supplies the System itself. The editable
Package does not need a published release.

Choose **Save and prepare**. First setup offers a one-time **Save and reopen
editor** action so Godot can apply its native launch/Game-tab settings. Then
**Run development World** or normal Play opens Rookframe inside Godot. Save
scripts and scenes, or reimport models, to update the running World. Repeated
Run clicks in the dock keep the current session. Errors appear in Godot's
Debugger and Output; fix and save to retry.

The World, Actors, links and piece positions survive supported hot reloads.
Reimported model hierarchy replaces the affected model nodes, including nested
scenes; their transient node fields initialize again. Godot applies ordinary
live script and scene edits, including retained script members. Reload does not
rerun `_ready()`/`start()` on retained Implementation instances. Content and
Presentation declarations update live; saving Presentation code recomposes its
authored UI with fresh transient Control state. A failed replacement keeps the previous usable UI. SDK Edition,
Implementation entry point, Package identity/version and the session's Package
selection are chosen before Play. Godot's restrictions on changing a
script's native base class still apply.

Rookframe blocks network hosting and joining for the entire development process.
Only the selected source Package bypasses publication and code/hash admission;
every other Package uses normal public HTTPS acquisition and local verification.
This mode runs your trusted author code; it is not an installed-Package sandbox.

The dock works in this project directly. Its local settings and data are
`.rookframe/development.json`, `.rookframe/development-runtime.json`,
`.rookframe-development/`, `.rookframe-development.pck`, `rookframe/development/`, `.godot/` and the staged
native libraries in `addons/webrtc_native/lib/`. Ignore them
in source control. Reopening the same World name keeps its data; another name
creates a separate World. Clearing `.godot/` is recoverable by preparing again.
The matching runtime bundle contains the application PCK and compiled libraries,
not Rookframe C# source or a project to build. Keep the complete bundle together.

## Authored scenes and UI

Open `rookframe/packages/<package-id>/ui/window.tscn` to edit and run the initial
scene using Godot's ordinary scene editor. The public Theme is
`res://rookframe/ui/theme/rookframe_theme.tres`; reusable scenes and their API
are documented in the [UI Kit](https://github.com/rookframe/rookframe-ui-kit/tree/9a124f5b5ebcf03a064b314771a303f3ca11d83f/docs).
Use its semantic Theme variations and public component properties. Internal
component child paths are not a stable API. Package resources and private
libraries belong below the Package's own UUID namespace.

The generated SDK provides concrete `Rail`, `WindowButton`, and
`ExtensionSurface` types, with documented members visible through Godot completion.
Extend its Presentation base and register an authored entry with
`sdk.rails.left.push(calendar_window_button)`. The SDK owns binding, opening,
mounting and cleanup. Read [API.md](API.md) for the complete initial interface. Calendar includes authoritative date and note actions and dedicated settings for classic or custom calendar rules.

## Checks, collisions and builds

`init` preserves existing Manifest/source/settings and appends only missing
compatible presets. All discovered collisions fail before scaffolding writes.
It does not migrate an existing Manifest or replace Publisher choices. For a
revision change, edit the Manifest and lock deliberately, remove only the
previous generated `sdk/` directory, then run `facade`. Commit the complete
generated directory. The command preflights all generated files before filling
missing ones; changed files are diagnosed without overwrites. When upgrading
from 0.1.x, also migrate the Presentation to the typed API shown in [API.md](API.md).

`check` is read-only for Publisher inputs. Manifest semantics, namespace,
dependency pins, facade, SDK minimum revision and shared resource export are checked first.
Godot import, binary normalization and Publisher tool scripts execute only in
disposable copies of the trusted author project. This is not a sandbox for
untrusted projects. Source results explicitly do not constitute runtime admission.
Unsupported effects and incomplete analysis fail through the same bounded
production operation verifier used by Rookframe; there is no author bypass.

`build` creates one fresh UUID and one shared resource root. It preserves the exact
Manifest, native relative references and importer parameters while preparing
static references, UIDs, imports and remaps. It verifies all prepared artifact
members and the shared textual script set through the production checker.
Output includes Package content/private libraries/facade and excludes the SDK,
UI Kit, kit imports and author project registries. Only a complete checked archive
is atomically published. Existing output paths are never replaced; a failed
export or final check leaves no successful-looking partial archive.

Use Manager's existing file import, select Calendar with exactly one System
Extension, and open the World. The full selection must pass production admission
before any Package executes. Reinstalling an archive retains its build identity;
rebuilding the same version deliberately creates another identity.

## Distribution

`release.json` records the exact SDK source revision, shipped file hashes, SDK
Edition/revision metadata, and the recommended independent UI release's hashes.
The standalone `Rookframe.PackageCheck.dll` is a framework-dependent author tool
compiled from the production verifier sources, not a Rookframe application or
private host assembly dependency. .NET is required by author checking/build and
the compiled development runtime; published Package code remains GDScript.
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for dependency notices.

## Imported architectural materials

SDK 0.22.5 includes the production admission rules for stock
`BaseMaterial3D.cull_mode` and `normal_scale`. These preserve the original
double-sided faces and normal-map strength of imported Builder assets. The
complete resource closure and all other setter rules are still checked.

## Content and Package forms

Miniatures may use native `Node3D` scenes with `ArrayMesh` geometry and
`StandardMaterial3D` textures. Save imported static models as Godot text scenes
before including them in the Package namespace. Both text formats 3 and 4 are
inspected, including format 4's base64 mesh buffers; normal dependency and size
checks still apply. The Tabletop Pieces example includes the Bevy Amber Warden
and Goblin Raider in this form.

Physical mesh Miniatures and Props must cast native dynamic shadows and receive
Scene lighting and shadows, including default Content. Use per-pixel
`StandardMaterial3D` shading, shadow receiving enabled and native mesh shadow
casting. Opaque materials are the usual choice; use supported alpha cutout modes
where needed. Reserve unshaded/emissive, shadowless materials for effects such
as flames and indicators. The host preserves physical shadows during camera
cutaways, suppresses deliberately hidden Rooks locally, and keeps new placement
ghosts shadowless. See [physical mesh lighting](../docs/implementation/physical-mesh-lighting.md)
for the complete presentation contract and shipped-asset audit.

The bounded [conformance projects](examples/package-conformance/README.md) cover
a 2029 System, 2027 data-only Content and 2029 Presentation-only UI. Install them
with the separate Calendar example to exercise the mixed-Edition World.
Data-only Packages receive no executable facade; Presentation-only Packages
receive no Implementation base. Neither form can register Package Settings.
Choose `--edition 2028` when initializing a new 2028 project. Existing manifests
and locks must be changed deliberately; an unsupported Edition/revision fails
before any Package executes. Both Editions share the independently pinned UI Kit.

## World data and game logic

Edition 2027 revision 5 and Edition 2028 revision 2 add focused, typed capabilities:
`world_data`, `actors`, `system_records`, `rooks`, `scenes`, `content`, and `windows`.
Use concrete SDK IDs, ContentReference, entity snapshots and operation results.
Only a Package's payload remains `Variant`; GDScript has no Package-defined generic return types.
See [API.md](API.md) for the authorization, persistence and Resource contracts.

## Package Settings

Edition 2027 revision 6 / 2028 revision 3 adds typed descriptors, snapshots,
validation, migration and custom-view drafts. Rookframe owns the separate User
and World transactions, ordinary controls, authority checks and deliberate
restart actions. See [the Settings API](API.md#package-settings--edition-2027-revision-6--2028-revision-3).
Calendar is the ordinary public example; Workshop supplies a bounded custom
form with restart-local and restart-world fields.

Edition 2027 revision 7 / 2028 revision 4 adds typed text and integer lists and
a dedicated Package Settings journey with complex Calendar configuration.

## Immediate named dice

Edition 2029 revision 6 lets the selected System Extension request an immediate
physical Roll with ordered, uniquely named terms through `await sdk.dice.roll(request)`.
Rookframe returns the raw faces and results after the shipped dice settle and
automatically appends the raw Roll to the shared Action Log. The System Extension owns all
game meaning and deliberately publishes its separate interpreted report through
`sdk.action_log.publish`. See [the complete contract and example](API.md#immediate-named-dice-2029-revision-6).

## Requested human Throws

Edition 2029 revision 7 lets the selected System Extension ask a specific
Participant to complete an immutable physical Throw through the native Dice Tray.
`sdk.dice.new_request_id()` allocates the stable identity so the Extension can
persist why the action is waiting before `sdk.dice.request_throw(request)` submits
it. The request call returns the current durable snapshot immediately; it never
keeps an await suspended while a human acts. Retry after `sdk.world_changed` or a
fresh binding. A terminal Roll already has Rookframe's raw Action Log entry; the
Extension explicitly publishes its rolled or cancelled game interpretation.
See [the complete contract and recovery example](API.md#requested-human-throws-2029-revision-7).

## Initial managed-window presentation

Edition 2029 revision 8 lets a Publisher declare a managed window's first-open
placement, optional dock width, and optional floating rectangle on its ordinary
`ExtensionSurface` Resource. Rookframe still owns responsive geometry, retained
window state, redocking, and every later Participant layout choice. Older facade
revisions retain their existing responsive default. See
[the complete contract](API.md#initial-managed-window-presentation-2029-revision-8).


## Checked integrations and protected authentication

Edition 2029 revision 1 exposes typed `files`, `clipboard`,
`network`, `secrets`, `authentication` and `browser` capabilities. The
[Integration example](examples/integrations/README.md) is a separate ordinary
optional Package; Calendar uses only clipboard copying and remains offline.
See [the integration API](API.md#checked-integrations--edition-2029-revision-1).

## Publish and list a release

Publication is a separate, deliberate author action. It never runs as part of
`build` and is not required for local import or direct public Manifest links.
See [PUBLICATION.md](PUBLICATION.md) for registration, GitHub hosting, metadata
review, submission readback, and retries. Authoring credentials stay in the
Publisher environment and are never supplied to Manager acquisition.

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

Participants submit `sdk.system_actions.submit(name, data)`. The selected System
Implementation overrides `handle_system_intent(context, name, data)` and executes
synchronously on World Authority, including a dedicated authority with no local GM.
The context authenticates the requester and provides authoritative Actor reads, committed
Rook positions, Scene distance, session-bound Throws and atomic Actor consequences.
All Participants receive the complete World data. Actor privacy is implemented only
by local UI display; the callback reply supplies the action outcome, not a data
confidentiality boundary. The System validates source access, target types, counts
and its own rules before committing.
See [API.md](API.md#authority-side-system-intents-2029-revision-12).


## Testing extensions

Use GdUnit4 for GDScript domain and UI component tests. Rookframe's supported
baseline is official GdUnit4 6.2.1 (commit
`08ffc7c65b61b1b2edd545616061a99973c13ce1`) on stock Godot 4.7.2 Mono.
Add it as a development dependency in `plug.gd`:

```gdscript
plug("godot-gdunit-labs/gdUnit4", {
    "commit": "08ffc7c65b61b1b2edd545616061a99973c13ce1",
    "include": ["addons/gdUnit4"],
})
```

Put suites extending `GdUnitTestSuite` under `tests/`, with named `test_*`
methods, native assertions, `auto_free` fixture cleanup and signals/await for
async completion. Exercise Actors, World Data, access and targeting through the
public SDK; substitute only the external host boundary for fast domain tests.
MÖRK BORG and Calendar contain complete examples and runners that require a
fresh, nonempty passing JUnit report. Real host integration belongs in
rookframe-godot. Enable GdUnit's Godot error reporting and disable flaky retries.

Exclude `addons/gdUnit4/**,tests/**,reports/**` from every Package export preset,
and ignore the installed addon and generated reports. Do not ship a test
framework in a published Package. Headless tests cover rules and explicitly
injected Viewport events; use a graphical run for OS input and screenshots.
See [GdUnit4 documentation](https://godot-gdunit-labs.github.io/gdUnit4/latest/).

Authored decision dialogs may use stock Window transparency and an owned
CanvasLayer/ColorRect backdrop. Viewport, CanvasLayer and ColorRect property access remains
limited to Package-owned nodes; host traversal does not grant ownership.

SDK 0.22.5 also admits authored stock Godot `CheckBox` controls and inherited
Button operations. Package-owned focus is supported; host-node casts do not
acquire focus operations.

SDK 0.22.5 pins the UI Kit checkbox theme correction: canonical 22px indicators
use the existing aqua and ink tokens, including disabled variants.

Edition 2029 revision 15 adds atomic Actor materialization from a live System
action with ordinary creator Owner grants. See [the API](API.md#actor-creation-from-system-actions-2029-revision-15).

Edition 2029 revision 16 adds Package World data reads and validated replacements
inside System actions, including dedicated authority and remote GM callers.

SDK 0.24.1 admits authored native `OptionButton` controls, item selection signals,
local button state, visibility, focus and scrolling. It also supports ordinary
local Array edits and primitive calculations over persisted World values. These
operations retain Package ownership and conservative value origins during admission.

SDK 0.25.0 / Edition 2029 revision 17 adds `rooks.preview` for showing an
existing Rook Miniature inside authored UI through the shared Content renderer.

SDK 0.25.1 admits the existing public ActionBar and TaskState components, the
chevron icon, and bounded `load()` of already admitted Package resources. It
also reports the required revision for window closure.

SDK 0.25.2 models stock Rect2 geometry, owned Control bounds/focus queries,
and ordinary GUI input and rectangle-change signals for responsive Package UI.

SDK 0.25.3 runs Package file analysis on bounded concurrent workers while
preserving ordered SDK bindings, diagnostics, source closure and per-file limits.
It uses the same pinned parser as runtime admission.

SDK 0.25.4 verifies stock runtime casts to checked Package GDScript types,
including possible derived implementations, for communication between authored
Package controls. Native casts and annotations do not grant host authority.

SDK 0.26.0 / Edition 2029 revision 18 adds `rooks.set_hidden` and `Rook.hidden`.
The GM controls durable Rook visibility through the SDK or the contextual rook
button. Hidden Rooks stay fully shared, render striped for the GM, and clear
all targeting. See [Rook hiding](API.md#rook-hiding-edition-2029-revision-18).

SDK 0.27.2 / Edition 2029 revision 19 adds the reusable UI Kit Miniature browser,
previews for unplaced Miniatures, source-Package localized Content names and
checked dynamic data keys for persisted Package dictionaries.

SDK 0.29.1 / Edition 2029 revision 21 adds System-owned Actor Definition categories, individual definition sheets, and Library Create/drop callbacks. See [the Library contract](API.md#actor-definitions-in-library-edition-2029-revision-21).

SDK 0.29.2 admits Godot TabContainer for Package-owned sheets, including localized tab titles.

SDK 0.30.0 / Edition 2029 revision 22 adds explicit child windows. `windows.push`
retains the parent draft while a picker runs; `windows.pop`, Escape and Close
return to it. See [child windows](API.md#child-windows-edition-2029-revision-22).

## Actor previews and placement (2029 revision 23)

`ActorSummary` accepts a Miniature ContentReference alongside the optional portrait.
Rookframe uses it for the Actor list preview, falling back to the built-in default
Miniature when no portrait or available Miniature was supplied. Set the summary’s
`can_place` flag to enable dragging, and override
`place_actor(actor, scene, position)` to create and link a Rook through SDK operations.
The host dispatches an existing Actor drop only with current Owner access; placement
must re-read access and report any failure through SDK feedback.

SDK 0.31.0 also admits stock Button text clipping for compact native tab layouts.

SDK 0.31.1 preserves canonical LF script bytes during Package preparation on
Windows, so relocated generated facades pass the same exact admission checks.

The shared UI Kit also provides `paginated_text_area` for fixed-page Silkbound
writing. Its complete-text `value` and `value_changed` contract retains drafts
across page turns; `get_pager()` composes its native pager into a fixed footer.
Reading surfaces can retain their one-page pager with
`paginated_content.always_show_pager`.
