"""Read the shared UI Kit selection and construct its installation command."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
import re


DEPENDENCY_FILE = Path(__file__).with_name("ui-kit-dependency.json")


def ui_kit_dependency(path: Path = DEPENDENCY_FILE) -> dict[str, str]:
    dependency = json.loads(path.read_text(encoding="utf-8"))
    if set(dependency) != {"tag", "commit"} or not re.fullmatch(
        r"(?:[0-9a-f]{40}|v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?)",
        dependency["tag"],
    ) or not re.fullmatch(r"[0-9a-f]{40}", dependency["commit"]):
        raise ValueError("UI Kit dependency requires a release tag and its full commit.")
    version = os.environ.get("ROOKFRAME_UI_KIT_VERSION", "").strip()
    if not version:
        return dependency
    if re.fullmatch(r"[0-9a-f]{40}", version):
        return {"tag": version, "commit": version}
    if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", version):
        raise ValueError("ROOKFRAME_UI_KIT_VERSION must be a release tag or full commit.")
    ref = f"refs/tags/{version}"
    result = subprocess.run(
        ["git", "ls-remote", "--tags", "https://github.com/rookframe/rookframe-ui-kit.git",
         ref, ref + "^{}"], check=True, capture_output=True, text=True, timeout=30,
    )
    refs = {name: commit for commit, name in (line.split() for line in result.stdout.splitlines())}
    commit = refs.get(ref + "^{}", refs.get(ref, ""))
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError(f"UI Kit release tag not found: {version}")
    return {"tag": version, "commit": commit}


def materialize_published_ui_kit_command(
    godot: Path, project: Path
) -> list[str]:
    """Return the documented, non-interactive gd-plug install command."""
    return [
        str(godot),
        "--headless",
        "--path",
        str(project),
        "-s",
        "plug.gd",
        "install",
    ]
