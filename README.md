# Rookframe SDK Authoring Kit 0.27.1

Author ordinary Godot Packages for SDK Edition 2029 (revisions 1–19). The kit also authors 2027 revisions 1–7 and 2028 revisions 1–4;
2027:8 / 2028:5 authors retain SDK 0.7.0. Existing emitted facades remain supported
by the host. The kit supplies a
Package-local facade, an optional editor plugin, and `init`, `facade`, `check`,
`build`, `publish-github` and `catalogue` commands. It is an authoring dependency; only the generated facade
ships in a Package. The UI Kit is a separate source dependency.

Express game logic through Rookframe domain capabilities: Actors, Rooks, Scenes,
Worlds, access, and targeting. The SDK handles authority, persistence and engine
integration behind those contracts. Use ordinary GDScript calculations, Resources,
Godot controls and signals, and public UI Kit components for their native roles.
The SDK does not introduce a replacement UI or signal framework.

## Install the two dependencies

Use Godot **4.7.2**, Python **3.10+**, Git and the **.NET 8 runtime** on PATH.
Install Godot's matching export templates for the local authoring host. The exporter produces a shared PCK, not an OS application.
Rookframe currently tests this authoring path on macOS with Godot Mono; the tools
accept an explicit Godot executable on every host.

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
    plug("rookframe/rookframe-sdk", {"tag": "v0.27.1", "include": ["addons/rookframe_sdk"]})
    plug("rookframe/rookframe-ui-kit", {"commit": "ad1a168e726640de8ca14687a72fc86aa06311bc", "include": ["rookframe/ui"]})
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
A newly initialized UI project enables it automatically. On editor entry the
plugin generates a missing facade or diagnoses a stale one. Project → Tools
provides **Rookframe: Check Package** and **Rookframe: Build Package**. These
commands report in Output and may take a moment while Godot prepares copies.
Set `ROOKFRAME_PYTHON` if Python is not on the editor's PATH.

Open `rookframe/packages/<package-id>/ui/window.tscn` to edit and run the initial
scene using Godot's ordinary scene editor. The public Theme is
`res://rookframe/ui/theme/rookframe_theme.tres`; reusable scenes and their API
are documented in the [UI Kit](https://github.com/rookframe/rookframe-ui-kit/tree/ad1a168e726640de8ca14687a72fc86aa06311bc/docs).
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
private host assembly dependency. .NET is required only by author checking/build.
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

SDK 0.27.1 verifies stock runtime casts to checked Package GDScript types,
including possible derived implementations, for communication between authored
Package controls. Native casts and annotations do not grant host authority.

SDK 0.27.1 / Edition 2029 revision 18 adds `rooks.set_hidden` and `Rook.hidden`.
The GM controls durable Rook visibility through the SDK or the contextual rook
button. Hidden Rooks stay fully shared, render striped for the GM, and clear
all targeting. See [Rook hiding](API.md#rook-hiding-edition-2029-revision-18).
