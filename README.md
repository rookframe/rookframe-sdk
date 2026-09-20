# Rookframe SDK Authoring Kit 0.15.0

Author ordinary Godot Packages for SDK Edition 2029 (revisions 1–7). The kit also authors 2027 revisions 1–7 and 2028 revisions 1–4;
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
    plug("rookframe/rookframe-sdk", {"tag": "v0.15.0", "include": ["addons/rookframe_sdk"]})
    plug("rookframe/rookframe-ui-kit", {"commit": "9de97beeede7f9d803e6ea0abef67730cdc84692", "include": ["rookframe/ui"]})
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
are documented in the [UI Kit](https://github.com/rookframe/rookframe-ui-kit/tree/9de97beeede7f9d803e6ea0abef67730cdc84692/docs).
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
Unsupported effects and incomplete analysis fail through the same GDShrapt-based
production verifier used by Rookframe; there is no author bypass.

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

SDK 0.15.0 includes the production admission rules for stock
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
