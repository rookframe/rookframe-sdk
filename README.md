# Rookframe GDScript SDK

An optional typed GDScript helper library in `rookframe/sdk/`. Rookframe owns
runtime behavior and API compatibility. No Package kind requires this library
or the UI Kit. Packages can use ordinary Godot nodes and the host domain API.

## Install when wanted

Install the standalone [Development Plugin ZIP](https://github.com/rookframe/rookframe-development-plugin/releases/download/v0.3.1-rc.1/rookframe-development-0.3.1-rc.1.zip) in Godot and enable **Rookframe Development**. Choose **Project > Tools >
Rookframe: Install latest SDK** to download the helper library automatically.
**Install latest UI Kit** is a separate, optional action. Neither requires
manual gd-plug setup. Existing dependency managers may still install just
`rookframe/sdk/` from an exact SDK release.

## Use the typed helpers

An Implementation choosing the SDK can extend `res://rookframe/sdk/implementation.gd`:

```gdscript
extends "res://rookframe/sdk/implementation.gd"

func start() -> void:
    var data: SDK.DataResult = sdk.world_data.read()
```

A Presentation choosing the SDK can extend `res://rookframe/sdk/presentation.gd`
and override `compose()`. Authored windows may extend the SDK's `window.gd`.
Use ordinary Godot Controls, signals and Resources; UI Kit components are optional.
See [API.md](API.md) for operations and callbacks.

## Author, develop and publish Packages

All authoring tools live exclusively in the Development Plugin: creation,
registration, model preparation, media, checks, builds and publication commands.
Use its Package tab and Project > Tools menu. Its commands live under
`addons/rookframe_development/`; there are no Package authoring commands in this SDK.
The installed application performs source and archive admission checks.
See the plugin's [README](https://github.com/rookframe/rookframe-development-plugin#author-packages)
and [publication instructions](https://github.com/rookframe/rookframe-development-plugin/blob/main/PUBLICATION.md).

## Maintain this SDK

Edit GDScript here directly. Keep runtime behavior in `rookframe-godot` and all
Package authoring tools in `rookframe-development-plugin`. The SDK never requires
a UI Kit checkout. `python tools/release_metadata.py --version VERSION` records
SDK source hashes only. Verify changed helper calls against the matching
application before publishing an immutable release.
