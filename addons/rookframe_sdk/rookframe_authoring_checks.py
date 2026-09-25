"""Read-only Publisher input checks and the shared production verifier process."""

from __future__ import annotations

import configparser
import hashlib
import io
import tarfile
import json
from pathlib import Path
import re
import subprocess

# The Godot exporter runs on the authoring host. This is not a Package OS target.
RESOURCE_EXPORT = "package"
EXPORT_PLATFORMS = {"macOS", "Windows Desktop", "Linux"}


def configured_profiles(project: Path) -> list[str]:
    config = configparser.ConfigParser(interpolation=None, strict=True)
    config.read(project / "export_presets.cfg")
    profiles = []
    for section in config.sections():
        if not re.fullmatch(r"preset\.\d+", section):
            continue
        values = config[section]
        name = values.get("name", "").strip('"')
        if name != RESOURCE_EXPORT:
            continue
        if name in profiles:
            raise RuntimeError(f"EXPORT.DUPLICATE: {name} is configured more than once.")
        if values.get("platform", "").strip('"') not in EXPORT_PLATFORMS:
            raise RuntimeError(f"EXPORT.PLATFORM: {name} must use the local Godot desktop exporter for the shared PCK, not an app export.")
        if values.get("script_export_mode") != "0":
            raise RuntimeError(f"EXPORT.SCRIPT: {name} must export textual GDScript (script_export_mode=0).")
        if values.get("dedicated_server", "false") != "false":
            raise RuntimeError("EXPORT.CONTENTS: The shared Package export must retain graphical resources (dedicated_server=false).")
        features = set(values.get("custom_features", "").strip('"').split(","))
        if not {"s3tc", "bptc", "etc2", "astc"}.issubset(features):
            raise RuntimeError("EXPORT.TEXTURES: The shared Package export must include s3tc,bptc,etc2,astc texture formats.")
        if values.get("encrypt_pck", "false") != "false" or values.get("encrypt_directory", "false") != "false":
            raise RuntimeError(f"EXPORT.ENCRYPTION: {name} must remain inspectable.")
        profiles.append(name)
    if not profiles:
        raise RuntimeError("EXPORT.MISSING: Run init to add the single package resource export preset; Packages have no OS targets.")
    return profiles


def verifier_path() -> Path:
    here = Path(__file__).resolve().parent
    shipped = here / "checker/Rookframe.PackageCheck.dll"
    if shipped.exists():
        return shipped
    development = here / "Rookframe.PackageCheck/bin/Debug/net8.0/Rookframe.PackageCheck.dll"
    if development.exists():
        return development
    raise RuntimeError("CHECK.TOOL: Install the exact SDK Authoring Kit (or build Rookframe.PackageCheck when developing the SDK).")


def verify(*arguments: str) -> dict:
    result = subprocess.run(["dotnet", str(verifier_path()), *map(str, arguments)],
                            capture_output=True, text=True, timeout=300)
    if result.returncode:
        raise RuntimeError("CHECK.PRODUCTION: " + result.stdout + result.stderr)
    return json.loads(result.stdout)


def check_dependencies(project: Path, sdk_version: str, ui_version: str, ui_commit: str) -> None:
    lock = json.loads((project / ".rookframe/authoring.lock.json").read_text())
    if lock.get("sdkAuthoringKitVersion") != sdk_version:
        raise RuntimeError("SDK.LOCK: Select the SDK's exact released version explicitly.")
    ui_pin = lock.get("uiKit", {})
    if not re.fullmatch(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", ui_pin.get("version", "")) or not re.fullmatch(r"[0-9a-f]{40}", ui_pin.get("commit", "")):
        raise RuntimeError("UI.LOCK: Record the UI Kit SemVer and full release commit.")
    sdk = project / "addons/rookframe_sdk"
    metadata = json.loads((sdk / "release.json").read_text())
    if metadata.get("version") != sdk_version:
        raise RuntimeError("SDK.VERSION: Installed SDK does not match the authoring lock.")
    for relative, expected in metadata["files"].items():
        if hashlib.sha256((sdk / relative).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"SDK.CONTENTS: Restore the exact SDK; {relative} was changed.")
    ui = project / "rookframe/ui"
    ui_files = metadata["uiFiles"]
    if ui_pin != {"version": ui_version, "commit": ui_commit}:
        # Other independently selected UI releases do not require an SDK release.
        # Compare the gd-plug checkout's committed tree without executing it.
        checkout = project / ".plugged/rookframe-ui-kit"
        archived = subprocess.check_output(["git", "-C", str(checkout), "archive", ui_pin["commit"], "rookframe/ui"], timeout=30)
        with tarfile.open(fileobj=io.BytesIO(archived)) as tree:
            ui_files = {member.name[len("rookframe/ui/"):]: hashlib.sha256(tree.extractfile(member).read()).hexdigest()
                        for member in tree.getmembers() if member.isfile() and not member.name.endswith(".import")}
        if not ui_files:
            raise RuntimeError("UI.CONTENTS: The selected UI release has no public resources.")
    for relative, expected in ui_files.items():
        if hashlib.sha256((ui / relative).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"UI.CONTENTS: Restore UI Kit {ui_pin['commit']}; {relative} was changed.")
    # Installed byte identities are authoritative; ordinary acquisition must
    # also retain the exact dependency selections recorded by initialization.
    plug = (project / "plug.gd").read_text()
    for repository, pin in (("rookframe-sdk", {"tag": f"v{sdk_version}"}),
                            ("rookframe-ui-kit", {"commit": ui_pin["commit"]})):
        # This is acquisition metadata, not Package source analysis. Require the
        # documented literal gd-plug declaration so ordinary install cannot float.
        declarations = re.findall(r'plug\(\s*"rookframe/' + repository + r'"\s*,\s*(\{[^}]*\})\s*\)', plug)
        if len(declarations) != 1:
            raise RuntimeError(f"DEPENDENCY.PIN: Use one literal gd-plug declaration for {repository}.")
        options = json.loads(declarations[0])
        selections = {key: options[key] for key in ("tag", "commit", "branch") if key in options}
        if selections != pin:
            raise RuntimeError(f"DEPENDENCY.PIN: {repository} must select {pin} exactly.")
