# Rookframe GDScript SDK

Install this repository with gd-plug. The files in `rookframe/sdk/` are ordinary,
typed GDScript source ready to use. Package authors do not generate or compile the SDK.
The SDK calls Rookframe's C# API; Rookframe owns its behavior and compatibility.

## Install

Use stock Godot .NET 4.7.2 with its documented prerequisites, an installed Rookframe
application, and Git. Package creation and export commands also use Python 3.10+.
Install [gd-plug](https://github.com/imjp94/gd-plug) in the author project, then add:

```gdscript
extends "res://addons/gd-plug/plug.gd"

func request_quit(exit_code := -1) -> bool:
    return super.request_quit(0 if exit_code == -1 else exit_code)

func _plugging() -> void:
    plug("rookframe/rookframe-sdk", {"tag": "v0.36.0-rc.1", "include": ["rookframe/sdk", "addons/rookframe_sdk"]})
    plug("rookframe/rookframe-development-plugin", {"tag": "v0.2.0-rc.1", "include": ["addons/rookframe_development"]})
```

Run `godot --headless --path . --script plug.gd install`. The SDK source is
ready to use. The Development Plugin provides the Package and Development World dock.

To create a separate new Package project from this downloaded tool:

```sh
python addons/rookframe_sdk/rookframe_authoring.py init --project ../my-package --name "My Package" --ui
python addons/rookframe_sdk/rookframe_authoring.py install-dependencies --project ../my-package
godot --headless --path ../my-package --script plug.gd install
```

Creation writes the new project's Manifest, source, export preset and complete
`plug.gd`, including its pinned public UI Kit. It preserves an existing `plug.gd`;
when adding Package structure to an existing project, merge its dependencies with
the complete examples in this repository before checking or exporting.

An Implementation starts with:

```gdscript
extends "res://rookframe/sdk/implementation.gd"

func start() -> void:
    var data: SDK.DataResult = sdk.world_data.read()
```

A Presentation extends `res://rookframe/sdk/presentation.gd` and overrides
`compose()`. Authored windows can extend `res://rookframe/sdk/window.gd`.
Use ordinary Godot scenes, Resources, signals and public UI Kit Controls.
See [API.md](API.md) for the domain operations and callbacks.

## Develop, check and export

Open the author project in stock Godot .NET. Enable **Rookframe Development**,
select the installed Rookframe application in the dock, and reuse one named
Development World. The plugin prepares Godot's library cache from that
application. Run the World, save supported script and scene edits, and reimport
assets in the same session. Use Godot's normal debugger and breakpoints.

The installed Rookframe application checks both source and exported Packages:

```sh
python addons/rookframe_sdk/rookframe_authoring.py check --project . --godot /path/to/godot --rookframe /path/to/Rookframe
python addons/rookframe_sdk/rookframe_authoring.py build --project . --godot /path/to/godot --rookframe /path/to/Rookframe
```

The application path can also come from the dock's saved configuration or
`ROOKFRAME_APP`. One Package archive contains the Package's own code and assets.
Rookframe supplies the shared SDK and UI Kit at runtime; neither is copied into
that archive. Commit Package source, Manifest, dependency lock, `plug.gd` and
export presets. Ignore downloaded dependencies, `.godot/`, local Development
World files and build output.

Publish only after checking and review. See [PUBLICATION.md](PUBLICATION.md).
Other Packages in a Development World must be published and acquired through
public HTTPS Manifest URLs.

## Maintain this SDK

Edit the GDScript files here directly. Keep C# API changes in `rookframe-godot`
and editor tools in `rookframe-development-plugin`. There is no SDK source
assembly step in the application repository.

Run `python -m unittest discover -s tests -v` for the Package tools. Verify SDK
changes with the matching application and the existing Development World before
publishing an immutable version. Release metadata records the exact source files;
it does not produce SDK code or a checker executable.
