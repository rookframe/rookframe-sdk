# Rookframe SDK Authoring Kit 0.8.0

Author ordinary Godot Packages for SDK Edition 2029 (revision 1). The kit also authors 2027 revisions 1–7 and 2028 revisions 1–4;
2027:8 / 2028:5 authors retain SDK 0.7.0. Existing emitted facades remain supported
by the host. The kit supplies a
Package-local facade, an optional editor plugin, and `init`, `facade`, `check`
and `build` commands. It is an authoring dependency; only the generated facade
ships in a Package. The UI Kit is a separate source dependency.

## Install the two dependencies

Use Godot **4.7.2**, Python **3.10+**, Git and the **.NET 8 runtime** on PATH.
Godot's matching export templates must be installed for your configured profiles.
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
    plug("rookframe/rookframe-sdk", {"tag": "v0.8.0", "include": ["addons/rookframe_sdk"]})
    plug("rookframe/rookframe-ui-kit", {"commit": "238339d390ec01873585c002917c164948a0578d", "include": ["rookframe/ui"]})
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
it the initial Package has an Implementation only. `--profile` can be repeated
for `desktop`, `android`, `ios` or `dedicated-headless`; desktop is the default.
Only configured Rookframe profiles are required, and every one must succeed.
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
are documented in the [UI Kit](https://github.com/rookframe/rookframe-ui-kit/tree/238339d390ec01873585c002917c164948a0578d/docs).
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
dependency pins, facade, SDK minimum revision and profiles are checked first.
Godot import, binary normalization and Publisher tool scripts execute only in
disposable copies of the trusted author project. This is not a sandbox for
untrusted projects. Source results explicitly do not constitute runtime admission.
Unsupported effects and incomplete analysis fail through the same GDShrapt-based
production verifier used by Rookframe; there is no author bypass.

`build` creates one fresh UUID and distinct profile roots. It preserves the exact
Manifest, native relative references and importer parameters while preparing
static references, UIDs, imports and remaps. It verifies actual prepared profile
members and one common textual script set through the production checker.
Output includes Package content/private libraries/facade and excludes the SDK,
UI Kit, kit imports and author project registries. Only a complete checked archive
is atomically published. Existing output paths are never replaced; a failed
profile or final check leaves no successful-looking partial archive.

Use Manager's existing file import, select Calendar with exactly one System
Extension, and open the World. The full selection must pass production admission
before any Package executes. Reinstalling an archive retains its build identity;
rebuilding the same version deliberately creates another identity.

See [Package lifecycle and typed authorship](docs/manager-lifecycle.md) for update,
repair, disable and deletion consequences.

## Distribution

`release.json` records the exact SDK source revision, shipped file hashes, SDK
Edition/revision metadata, and the recommended independent UI release's hashes.
The standalone `Rookframe.PackageCheck.dll` is a framework-dependent author tool
compiled from the production verifier sources, not a Rookframe application or
private host assembly dependency. .NET is required only by author checking/build.
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for dependency notices.

## Content and Package forms

The bounded [conformance projects](examples/package-conformance/README.md) cover
a 2028 System, 2027 data-only Content and 2027 Presentation-only UI. Install them
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


## Checked integrations and protected authentication

Edition 2029 revision 1 exposes typed `files`, `clipboard`,
`network`, `secrets`, `authentication` and `browser` capabilities. The
[Integration example](examples/integrations/README.md) is a separate ordinary
optional Package; Calendar uses only clipboard copying and remains offline.
See [the integration API](API.md#checked-integrations--edition-2029-revision-1).
