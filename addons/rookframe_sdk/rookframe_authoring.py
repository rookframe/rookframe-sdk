#!/usr/bin/env python3
"""Rookframe SDK authoring commands. Publisher inputs remain Publisher-owned."""

from __future__ import annotations

import argparse
import configparser
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid

from rookframe_sdk_facade import facade_sources
from rookframe_authoring_checks import check_dependencies, configured_profiles, verify
from rookframe_package_build import (BUILD_SCHEMA,
    deterministic_archive, export_prepared_profile, new_build_id, normalize_binary_resources,
    prepare_profile, run_godot, shared_profile_sources, source_identity)

SDK_VERSION = "0.3.0"
SDK_EDITION = "2027"
SDK_EDITIONS = {"2027": 4, "2028": 1}
UI_VERSION = "v1.0.0-rc.1"
UI_COMMIT = "238339d390ec01873585c002917c164948a0578d"
PROFILES = ("desktop", "android", "ios", "dedicated-headless")


class AuthoringError(RuntimeError):
    pass


def json_text(value: object) -> str:
    return json.dumps(value, indent=2) + "\n"


def preset(index: int, profile: str, package_id: str) -> str:
    desktop_platform = {"darwin": "macOS", "win32": "Windows Desktop"}.get(sys.platform, "Linux")
    platform = {"android": "Android", "ios": "iOS"}.get(profile, desktop_platform)
    return f'''[preset.{index}]
name="{profile}"
platform="{platform}"
runnable=false
dedicated_server={str(profile == "dedicated-headless").lower()}
export_filter="selected_resources"
include_filter="rookframe/packages/{package_id}/**"
exclude_filter="rookframe.json,rookframe/ui/**,addons/**,.rookframe/**,.plugged/**,plug.gd,README.md,presentation/**"
export_path="build/{profile}.pck"
script_export_mode=0
encrypt_pck=false
encrypt_directory=false

[preset.{index}.options]
texture_format/s3tc_bptc=true
texture_format/etc2_astc=true
codesign/codesign=0
application/bundle_identifier="org.rookframe.package"
'''


def read_presets(project: Path) -> configparser.ConfigParser:
    config = configparser.ConfigParser(interpolation=None, strict=True)
    config.read(project / "export_presets.cfg")
    return config


def initialize(project: Path, name: str, kind: str, profiles: list[str], ui: bool = False, edition: str = SDK_EDITION) -> None:
    presets_path = project / "export_presets.cfg"
    if presets_path.exists() and not presets_path.is_file():
        raise AuthoringError("INIT.CONFLICT: export_presets.cfg must be a regular file.")
    manifest_path = project / "rookframe.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        package_id = manifest["id"]
        if manifest.get("kind") != kind or manifest.get("sdk", {}).get("edition") != edition:
            raise AuthoringError("INIT.CONFLICT: Existing Manifest has a different Kind or SDK Edition.")
    else:
        package_id = str(uuid.uuid4())
        manifest = {"manifestVersion": 1, "id": package_id, "kind": kind,
                    "name": name, "version": "0.1.0", "summary": name,
                    "sdk": {"edition": edition, "minimumRevision": 1},
                    "rookframeCompatibility": {"minimum": "0.1.0", "verified": "0.1.0"},
                    "implementation": {"entryPoint": "logic/implementation.gd"}}
    identity = uuid.UUID(package_id)
    if identity.version != 4 or str(identity) != package_id:
        raise AuthoringError("INIT.CONFLICT: Package ID must be a canonical UUIDv4.")
    revision = manifest["sdk"]["minimumRevision"]
    package_root = f"rookframe/packages/{package_id}"
    lock = {"sdkEdition": edition, "sdkAuthoringKitVersion": SDK_VERSION,
            "minimumRevision": revision,
            "uiKit": {"version": UI_VERSION, "commit": UI_COMMIT}}
    proposed = {
        "rookframe.json": json_text(manifest),
        ".rookframe/authoring.lock.json": json_text(lock),
    }
    proposed.update({f"{package_root}/sdk/{name}": source
                     for name, source in facade_sources(package_id, revision, SDK_VERSION, edition, implementation="implementation" in manifest, presentations=bool(manifest.get("presentations")) or (ui and not manifest_path.exists())).items()})
    if ui and not manifest_path.exists():
        from rookframe_authoring_scenes import presentation, window_scene, rail_scene, window_button
        manifest["presentations"] = [{"id": "default", "experiences": ["desktop", "tablet", "phone"],
                                      "entryPoint": "ui/presentation.gd"}]
        proposed["rookframe.json"] = json_text(manifest)
        proposed[f"{package_root}/ui/presentation.gd"] = presentation(package_id)
        proposed[f"{package_root}/ui/window.tscn"] = window_scene(name)
        proposed[f"{package_root}/ui/window_button.tscn"] = rail_scene(name)
        proposed[f"{package_root}/ui/window_button.tres"] = window_button(package_id)
    if not (project / "plug.gd").exists():
        proposed["plug.gd"] = f'''extends "res://addons/gd-plug/plug.gd"


func request_quit(exit_code := -1) -> bool:
\treturn super.request_quit(0 if exit_code == -1 else exit_code)


func _plugging() -> void:
\tplug("rookframe/rookframe-sdk", {{"tag": "v{SDK_VERSION}", "include": ["addons/rookframe_sdk"]}})
\tplug("rookframe/rookframe-ui-kit", {{"commit": "{UI_COMMIT}", "include": ["rookframe/ui"]}})
'''
    implementation = manifest.get("implementation")
    if implementation and not manifest_path.exists():
        proposed[f"{package_root}/logic/implementation.gd"] = f'extends "res://{package_root}/sdk/implementation.gd"\n'
    if not (project / "project.godot").exists():
        proposed["project.godot"] = 'config_version=5\n[application]\nconfig/name=' + json.dumps(name) + '\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n'
        if ui:
            proposed["project.godot"] = proposed["project.godot"].replace('[rendering]',
                f'run/main_scene="res://{package_root}/ui/window.tscn"\n[editor_plugins]\nenabled=PackedStringArray("res://addons/rookframe_sdk/plugin.cfg")\n[rendering]')
    config = read_presets(project)
    existing_names = {config.get(s, "name", fallback="").strip('"'): s
                      for s in config.sections() if not s.endswith(".options")}
    additions = []
    indices = [int(s.split(".")[1]) for s in config.sections() if s.startswith("preset.") and not s.endswith(".options")]
    index = max(indices, default=-1) + 1
    for profile in dict.fromkeys(profiles):
        if profile in existing_names:
            section = config[existing_names[profile]]
            if section.get("script_export_mode") != "0" or package_root not in section.get("include_filter", ""):
                raise AuthoringError(f"INIT.CONFLICT: Export preset {profile} is incompatible; configure textual Package exports explicitly.")
        else:
            additions.append(preset(index, profile, package_id))
            index += 1
    # Preflight every owned/generated collision before adding any scaffolding.
    for relative in (*proposed, "export_presets.cfg"):
        path = project / relative
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != project and project in parent.parents):
            raise AuthoringError(f"INIT.CONFLICT: {relative} traverses a symbolic link.")
    for relative, content in proposed.items():
        path = project / relative
        if path.exists() and relative != "rookframe.json" and path.read_text() != content:
            raise AuthoringError(f"INIT.CONFLICT: {relative} differs; reconcile it explicitly. No files were overwritten.")
        if any(parent.exists() and not parent.is_dir() for parent in path.parents):
            raise AuthoringError(f"INIT.CONFLICT: Parent of {relative} is not a directory.")
    for relative, content in proposed.items():
        path = project / relative
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    if additions:
        with (project / "export_presets.cfg").open("a") as output:
            output.write("\n" + "\n".join(additions))


def check_facade(project: Path, *, generate_missing: bool = False) -> dict:
    manifest = json.loads((project / "rookframe.json").read_text())
    identity = uuid.UUID(manifest["id"])
    revision = manifest["sdk"]["minimumRevision"]
    if str(identity) != manifest["id"] or identity.version != 4:
        raise AuthoringError("MANIFEST.ID: Use a canonical UUIDv4 Package identity.")
    edition = manifest["sdk"]["edition"]
    if type(revision) is not int or not 1 <= revision <= SDK_EDITIONS.get(edition, 0):
        raise AuthoringError("SDK.REVISION: Supported Editions are 2027 revisions 1–4 and 2028 revision 1.")
    lock = json.loads((project / ".rookframe/authoring.lock.json").read_text())
    if (lock.get("sdkEdition") != edition or lock.get("minimumRevision") != revision
            or lock.get("sdkAuthoringKitVersion") != SDK_VERSION):
        raise AuthoringError("SDK.REVISION: Manifest and exact authoring lock disagree.")
    generated = {project / f"rookframe/packages/{identity}/sdk/{name}": source
                 for name, source in facade_sources(str(identity), revision, SDK_VERSION, edition, implementation="implementation" in manifest, presentations=bool(manifest.get("presentations"))).items()}
    # Preflight the complete generated surface before adding any missing file.
    for path, expected in generated.items():
        if any(parent.exists() and not parent.is_dir() for parent in path.parents):
            raise AuthoringError(f"SDK.FACADE: Parent of {path.name} must be a directory.")
        if path.exists() and (not path.is_file() or path.read_text() != expected):
            raise AuthoringError(f"SDK.FACADE: {path.name} differs. Reconcile the lock, then regenerate the SDK directory explicitly.")
        if not path.exists() and not generate_missing:
            raise AuthoringError(f"SDK.FACADE: {path.name} is absent. Run `facade` to generate the typed SDK.")
    for path, expected in generated.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected)
    return manifest


def check_project(project: Path, godot: Path, work: Path) -> tuple[dict, list[str], dict]:
    # All discovery and independent input checks happen without opening Godot.
    errors = []
    manifest = None
    profiles = []
    manifest_check = {}
    for operation in (
        lambda: check_facade(project),
        lambda: check_dependencies(project, SDK_VERSION, UI_VERSION, UI_COMMIT),
        lambda: configured_profiles(project),
        lambda: verify("manifest", project / "rookframe.json"),
    ):
        try:
            value = operation()
            if isinstance(value, dict) and "id" in value:
                manifest = value
            elif isinstance(value, list):
                profiles = value
            elif isinstance(value, dict):
                manifest_check = value
        except (RuntimeError, OSError, ValueError, KeyError, configparser.Error) as error:
            errors.append(str(error))
    if manifest:
        prefix = f"res://rookframe/packages/{manifest['id']}/"
        for path in manifest_check.get("paths", []):
            if not path.startswith(prefix) or not (project / path[6:]).is_file():
                errors.append(f"MANIFEST.RESOURCE: {path} must exist within the owning Package namespace.")
    if errors:
        raise AuthoringError("\n".join(errors))
    for path in project.rglob("*"):
        if path.is_symlink():
            raise AuthoringError(f"SOURCE.SYMLINK: Materialize {path} before author checking.")
    snapshot = work / "check"
    shutil.copytree(project, snapshot, ignore=shutil.ignore_patterns(
        ".godot", ".git", "build", "bin", "obj", "__pycache__"))
    root = snapshot / f"rookframe/packages/{manifest['id']}"
    normalize_binary_resources(godot, snapshot, root)
    run_godot(godot, snapshot, "--editor", "--import")
    # No PCK/export is produced by check. Source diagnostics cannot serve as a
    # runtime receipt; finished profile contents pass inspection again at build.
    source_checks = {profile: verify("source", snapshot, profile) for profile in profiles}
    for checked in source_checks.values():
        check_revision(manifest, checked)
    return manifest, profiles, {"status": "source_checked",
        "scope": "Source only; prepared exports and runtime admission are still required.",
        "profiles": source_checks}


def check_revision(manifest: dict, checked: dict) -> None:
    required = 1 if manifest["sdk"]["edition"] == "2028" else checked.get("minimumSdkRevision", 1)
    if manifest["sdk"]["minimumRevision"] < required:
        raise AuthoringError(f"SDK.MINIMUM: These operations require additive revision {required}; update the Manifest, lock and generated facade explicitly.")


def build_project(project: Path, godot: Path, work: Path, manifest: dict,
                  profiles: list[str], output: Path, *, headless: bool) -> dict:
    if output.exists():
        raise AuthoringError(f"BUILD.OUTPUT_EXISTS: Choose a new output path; {output} already contains an earlier build.")
    package_id = manifest["id"]
    build_id = new_build_id()
    metadata = {"schema": BUILD_SCHEMA, "packageId": package_id, "buildId": build_id,
                "sourceSha256": source_identity(project),
                "engine": subprocess.check_output([str(godot), "--version"], text=True).strip(), "profiles": {}}
    pcks = {}
    for profile in profiles:
        profile_work = work / profile
        prepared, runtime_root = prepare_profile(godot, project, profile_work, package_id, build_id, profile)
        pcks[profile], metadata["profiles"][profile] = export_prepared_profile(
            godot, prepared, profile_work, profile, runtime_root, headless=headless)
    staged = work / "candidate.rookpackage"
    staged.write_bytes(deterministic_archive(
        (project / "rookframe.json").read_bytes(), pcks,
        shared_profile_sources(pcks, metadata), metadata))
    checked = verify("artifact", staged, project / "rookframe/ui")
    check_revision(manifest, checked)
    output.parent.mkdir(parents=True, exist_ok=True)
    # Publish only the fully checked set, atomically even across filesystems.
    with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".rookframe-", delete=False) as stream:
        pending = Path(stream.name)
        try:
            stream.write(staged.read_bytes())
            stream.flush()
            os.fsync(stream.fileno())
            stream.close()
            os.link(pending, output)  # Atomic publication; never replace an existing build.
        finally:
            pending.unlink(missing_ok=True)
    return {"status": "built", "archive": str(output), "buildId": build_id,
            "profiles": profiles, "verification": checked}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("init", "facade", "check", "build"))
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--name", default="My Package")
    parser.add_argument("--kind", choices=("optional", "system-extension"), default="optional")
    parser.add_argument("--profile", choices=PROFILES, action="append", default=[])
    parser.add_argument("--edition", choices=tuple(SDK_EDITIONS), default=SDK_EDITION)
    parser.add_argument("--ui", action="store_true", help="Scaffold an authored scene and a Rail-to-window Presentation for a new Package.")
    parser.add_argument("--godot", type=Path, default=Path(os.environ.get("ROOKFRAME_GODOT", "/Applications/Godot_mono.app/Contents/MacOS/Godot")))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--graphical", action="store_true", help="Use the graphical export renderer when required by the host.")
    args = parser.parse_args()
    try:
        project = args.project.resolve()
        if args.command == "init":
            initialize(project, args.name, args.kind, args.profile or ["desktop"], args.ui, args.edition)
            result = {"status": "initialized", "project": str(project)}
        elif args.command == "facade":
            check_facade(project, generate_missing=True)
            result = {"status": "facade_checked"}
        else:
            with tempfile.TemporaryDirectory(prefix="rookframe-author-") as directory:
                work = Path(directory)
                manifest, profiles, result = check_project(project, args.godot, work)
                if args.command == "build":
                    output = args.output or project / f"build/{manifest['id']}-{manifest['version']}-{uuid.uuid4()}.rookpackage"
                    result = build_project(project, args.godot, work, manifest, profiles,
                                           output.resolve(), headless=not args.graphical)
        print(json_text(result), end="")
        return 0
    except (RuntimeError, OSError, ValueError, KeyError, configparser.Error, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
