"""Read-only Publisher input checks and the shared production verifier process."""

from __future__ import annotations

import configparser
import hashlib
import json
import os
import shutil
import sys
import tempfile
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


_application: Path | None = None


def configure_application(project: Path, explicit: Path | None = None) -> None:
    global _application
    config_path = project / ".rookframe/development.json"
    config = json.loads(config_path.read_text()) if config_path.is_file() else {}
    selected = explicit or os.environ.get("ROOKFRAME_APP") or config.get("rookframe")
    if selected:
        application = Path(selected).expanduser().resolve()
        if application.suffix.lower() == ".app":
            application /= "Contents/MacOS/Rookframe"
        if not application.is_file():
            raise RuntimeError(f"CHECK.ROOKFRAME: Selected Rookframe application does not exist: {application}")
        _application = application
        return
    candidates = []
    if sys.platform == "win32":
        candidates.extend(Path(os.environ.get(key, "")) / "Rookframe/Rookframe.exe"
                          for key in ("ProgramFiles", "LOCALAPPDATA"))
    elif sys.platform == "darwin":
        candidates.extend([Path("/Applications/Rookframe.app/Contents/MacOS/Rookframe"),
                           Path.home() / "Applications/Rookframe.app/Contents/MacOS/Rookframe"])
    found = shutil.which("rookframe")
    if found:
        candidates.append(Path(found))
    _application = next((p.resolve() for p in candidates if p.is_file()), None)
    if _application is None:
        raise RuntimeError("CHECK.ROOKFRAME: Select your installed Rookframe with --rookframe or in the Development World dock.")


def verify(*arguments: str) -> dict:
    if _application is None:
        raise RuntimeError("CHECK.ROOKFRAME: Select your installed Rookframe before checking a Package.")
    mode, path, *rest = map(str, arguments)
    with tempfile.TemporaryDirectory(prefix="rookframe-check-") as directory:
        report = Path(directory) / "report.json"
        command = [str(_application), "--headless", "--",
                   "--package-check=" + mode, "--input=" + str(Path(path).resolve()),
                   "--report=" + str(report)]
        if rest:
            command.append("--profile=" + rest[0])
        process = subprocess.run(command, capture_output=True, text=True, timeout=300)
        if not report.is_file():
            raise RuntimeError("CHECK.ROOKFRAME: Rookframe did not return a Package check report. Update the installed application. "
                               + process.stdout + process.stderr)
        result = json.loads(report.read_text(encoding="utf-8"))
        if process.returncode or result.get("status") == "rejected":
            raise RuntimeError("CHECK.PRODUCTION: " + json.dumps(result))
        return result


def committed_ui_files(checkout: Path, revision: str) -> dict[str, str]:
    """Hash the public release tree, independently of checkout line endings."""
    from rookframe_ui_kit_install import committed_runtime, hashes
    _, files = committed_runtime(checkout, revision)
    return hashes({name: data for name, data in files.items() if not name.endswith(".import")})



def check_dependencies(project: Path, sdk_version: str, ui_version: str, ui_commit: str) -> None:
    lock = json.loads((project / ".rookframe/authoring.lock.json").read_text())
    if lock.get("sdkAuthoringKitVersion") != sdk_version:
        raise RuntimeError("SDK.LOCK: Select the SDK's exact released version explicitly.")
    ui_pin = lock.get("uiKit", {})
    if not re.fullmatch(r"(?:[0-9a-f]{40}|v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)", ui_pin.get("version", "")) or not re.fullmatch(r"[0-9a-f]{40}", ui_pin.get("commit", "")):
        raise RuntimeError("UI.LOCK: Record the UI Kit version (release tag or full commit) and full commit.")
    sdk = project / "addons/rookframe_sdk"
    metadata = json.loads((sdk / "release.json").read_text())
    if metadata.get("version") != sdk_version:
        raise RuntimeError("SDK.VERSION: Installed SDK does not match the authoring lock.")
    for relative, expected in metadata["files"].items():
        if hashlib.sha256((sdk / relative).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"SDK.CONTENTS: Restore the exact SDK; {relative} was changed.")
    for relative, expected in metadata["sdkFiles"].items():
        if hashlib.sha256((project / "rookframe/sdk" / relative).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"SDK.CONTENTS: Restore the installed SDK source; {relative} was changed.")
    ui = project / "rookframe/ui"
    ui_files = metadata["uiFiles"]
    if ui_pin != metadata["uiKit"]:
        # Other independently selected UI releases do not require an SDK release.
        # Compare the gd-plug checkout's committed tree without executing it.
        checkout = project / ".plugged/rookframe-ui-kit"
        ui_files = committed_ui_files(checkout, ui_pin["commit"])
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
