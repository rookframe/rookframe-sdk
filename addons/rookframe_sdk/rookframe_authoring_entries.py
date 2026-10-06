"""Register authored scenes without replacing Publisher-owned code or files."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import os

from rookframe_sdk_facade import facade_sources

CONTENT_TYPES = ("miniature", "prop", "wall_style", "surface_finish")
UI_SLOTS = ("left", "right", "ui_root", "actor_creation", "selected_rook")


def install_dependencies(project: Path) -> dict:
    lock = json.loads((project / ".rookframe/authoring.lock.json").read_text(encoding="utf-8"))
    commit = lock["uiKit"]["commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("The UI Kit lock must contain a full commit.")
    # The editor installs exactly the author's UI lock and a pinned MIT bootstrap.
    # It never replaces the installed SDK or updates the lock implicitly.
    bootstrap = "209276d1f00d14b49b74403d9839f29598e9a8eb"
    with tempfile.TemporaryDirectory(prefix="rookframe-dependencies-") as directory:
        work = Path(directory)
        def git(*arguments):
            result = subprocess.run(["git", "-c", "credential.helper=", *arguments],
                                    env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
                                    capture_output=True, text=True, timeout=120)
            if result.returncode:
                raise ValueError("Dependency download failed: " + result.stderr.strip())
        def checkout(repository: str, revision: str, target: Path):
            git("clone", "--quiet", "--no-checkout", "--filter=blob:none",
                "https://github.com/" + repository + ".git", str(target))
            git("-C", str(target), "fetch", "--quiet", "--depth=1", "origin", revision)
            git("-C", str(target), "checkout", "--quiet", "--detach", revision)
        checkout("rookframe/rookframe-ui-kit", commit, work / "ui")
        checkout("imjp94/gd-plug", bootstrap, work / "plug")
        files = {project / "rookframe/ui" / path.relative_to(work / "ui/rookframe/ui"): path.read_bytes()
                 for path in (work / "ui/rookframe/ui").rglob("*") if path.is_file()}
        if not files:
            raise ValueError("The pinned UI Kit has no public UI files.")
        files[project / "addons/gd-plug/plug.gd"] = (work / "plug/addons/gd-plug/plug.gd").read_bytes()
        files[project / "addons/gd-plug/LICENSE"] = (work / "plug/LICENSE").read_bytes()
        for path, contents in files.items():
            if not path.resolve().is_relative_to(project.resolve()):
                raise ValueError("Dependency files must stay inside the author project.")
            if path.exists() and path.read_bytes() != contents:
                raise ValueError(f"Dependency installation would replace {path.relative_to(project)}. Preserve or reconcile that file first.")
        cache = project / ".plugged/rookframe-ui-kit"
        if not cache.resolve().is_relative_to(project.resolve()) or cache.is_symlink() or cache.parent.is_symlink():
            raise ValueError("The dependency cache must be a real directory inside the author project.")
        if not cache.exists():
            cache.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(work / "ui", cache)
        else:
            git("-C", str(cache), "fetch", "--quiet", "--depth=1",
                "https://github.com/rookframe/rookframe-ui-kit.git", commit)
        for path, contents in files.items():
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(contents)
    return {"status": "dependencies_installed", "uiCommit": commit}


def encoded(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def register(project: Path, scene: str, entry_id: str, name: str, kind: str,
             presentation_id: str | None = None) -> dict:
    from rookframe_authoring import SDK_VERSION, check_edition
    if not re.fullmatch(r"[a-z][a-z0-9_-]*", entry_id) or not name.strip():
        raise ValueError("Choose a name and a stable ID using lowercase letters, numbers, '-' or '_'.")
    if kind not in CONTENT_TYPES + UI_SLOTS:
        raise ValueError("Choose a supported Content type or UI contribution slot.")
    manifest_path = project / "rookframe.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if kind == "actor_creation" and manifest["kind"] != "system-extension":
        raise ValueError("Only a System Extension can register Actor Creation UI.")
    if (kind in UI_SLOTS[2:] and manifest["sdk"]["edition"] == "2027"
            and manifest["sdk"]["minimumRevision"] < 4):
        raise ValueError("This UI slot requires SDK Edition 2027 revision 4 or a later Edition.")
    package_id = manifest["id"]
    root = project / "rookframe/packages" / package_id
    resource = (project / scene.removeprefix("res://")).resolve()
    if not resource.is_relative_to(root.resolve()) or not resource.is_file():
        raise ValueError("Choose a saved scene inside this Package's UUID directory.")
    if resource.suffix not in (".tscn", ".glb", ".gltf"):
        raise ValueError("Choose a Godot scene or imported glTF model.")
    relative = resource.relative_to(root.resolve()).as_posix()
    changes: dict[Path, str] = {}
    if kind in CONTENT_TYPES:
        groups = manifest.setdefault("content", [])
        if any(entry["id"] == entry_id for group in groups for entry in group.get("entries", [])):
            raise ValueError("That Content ID already exists. Edit its scene or choose another ID.")
        group = next((item for item in groups if item.get("kind") == "visual"), None)
        if group is None:
            group = {"kind": "visual", "entries": []}
            groups.append(group)
        group["entries"].append({"id": entry_id, "displayName": name.strip(),
                                "type": kind, "payload": relative})
    else:
        presentations = manifest.setdefault("presentations", [])
        if not presentations:
            presentations.append({"id": "default", "experiences": ["desktop", "tablet", "phone"],
                                  "entryPoint": "sdk/presentation.gd"})
        selected = next((p for p in presentations if presentation_id is None or p["id"] == presentation_id), None)
        if selected is None:
            raise ValueError("The selected Presentation no longer exists.")
        state_path = project / ".rookframe/ui-entries.json"
        state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"presentations": {}}
        key = selected["id"]
        suffix = hashlib.sha256(key.encode()).hexdigest()[:12]
        wrapper = f"ui/editor_{suffix}.gd"
        owned = state["presentations"].get(key)
        if owned is None:
            if (root / wrapper).exists():
                raise ValueError("The generated Presentation path is already occupied.")
            owned = {"base": selected["entryPoint"], "entries": [], "sha256": None}
        else:
            current = root / wrapper
            if (selected["entryPoint"] != wrapper or not current.is_file()
                    or hashlib.sha256(current.read_bytes()).hexdigest() != owned["sha256"]):
                raise ValueError("The generated Presentation was edited. Reconcile it before adding another editor entry.")
        if any(item["id"] == entry_id for item in owned["entries"]):
            raise ValueError("That UI entry ID already exists.")
        owned["entries"].append({"id": entry_id, "slot": kind})
        state["presentations"][key] = owned
        base = f"res://rookframe/packages/{package_id}"
        descriptor = f"ui/entries/{entry_id}.tres"
        quote = lambda value: json.dumps(value, ensure_ascii=False)
        if kind in ("left", "right"):
            from rookframe_authoring_scenes import rail_scene
            changes[root / f"ui/entries/{entry_id}.tscn"] = rail_scene(name.strip())
            body = f'''[gd_resource type="Resource" load_steps=6 format=3]
[ext_resource type="Script" path={quote(base + '/sdk/window_button.gd')} id="entry"]
[ext_resource type="Script" path={quote(base + '/sdk/extension_surface.gd')} id="surface"]
[ext_resource type="PackedScene" path={quote(base + '/ui/entries/' + entry_id + '.tscn')} id="button"]
[ext_resource type="PackedScene" path={quote(base + '/' + relative)} id="scene"]
[sub_resource type="Resource" id="window"]
script = ExtResource("surface")
scene = ExtResource("scene")
[resource]
script = ExtResource("entry")
button_scene = ExtResource("button")
window = SubResource("window")
'''
        else:
            body = f'''[gd_resource type="Resource" load_steps=3 format=3]
[ext_resource type="Script" path={quote(base + '/sdk/contribution.gd')} id="entry"]
[ext_resource type="PackedScene" path={quote(base + '/' + relative)} id="scene"]
[resource]
script = ExtResource("entry")
scene = ExtResource("scene")
'''
        changes[root / descriptor] = body
        for path in changes:
            if path.exists():
                raise ValueError(f"An author file already occupies {path.relative_to(project)}.")
        lines = ["# Generated by Rookframe editor authoring; customize the source scenes or base Presentation.",
                 f"extends {quote(base + '/' + owned['base'])}", ""]
        for index, item in enumerate(owned["entries"]):
            type_name = "WindowButton" if item["slot"] in ("left", "right") else "Contribution"
            lines.append(f"const ENTRY_{index}: SDK.{type_name} = preload({quote(base + '/ui/entries/' + item['id'] + '.tres')})")
        lines.extend(["", "func compose() -> void:", "\tsuper.compose()"])
        for index, item in enumerate(owned["entries"]):
            target = "rails." + item["slot"] if item["slot"] in ("left", "right") else (
                "ui_root" if item["slot"] == "ui_root" else "slots." + item["slot"])
            lines.append(f"\tsdk.{target}.push(ENTRY_{index})")
        wrapper_text = "\n".join(lines) + "\n"
        changes[root / wrapper] = wrapper_text
        owned["sha256"] = hashlib.sha256(wrapper_text.encode()).hexdigest()
        selected["entryPoint"] = wrapper
        changes[state_path] = encoded(state)
        edition = manifest["sdk"]["edition"]
        revision = manifest["sdk"]["minimumRevision"]
        check_edition(edition, revision)
        for filename, source in facade_sources(package_id, revision, SDK_VERSION, edition,
                implementation="implementation" in manifest, presentations=True).items():
            target = root / "sdk" / filename
            if target.exists() and target.read_text(encoding="utf-8") != source:
                raise ValueError("The generated SDK differs from this kit. Resolve the SDK version before registering UI.")
            if not target.exists():
                changes[target] = source
    # All semantic and collision checks precede writes. Restore previous bytes on
    # an I/O failure, including the Manifest and editor ownership record.
    changes[manifest_path] = encoded(manifest)
    for path in changes:
        if not path.resolve().is_relative_to(project.resolve()) or path.is_symlink() or any(
                parent.is_symlink() for parent in path.parents if parent != project and project in parent.parents):
            raise ValueError("Authoring output must remain inside real directories in this project.")
    backup = {path: path.read_bytes() if path.exists() else None for path in changes}
    try:
        for path, text in changes.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.encode())
    except OSError:
        for path, previous in backup.items():
            if previous is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(previous)
        raise
    return {"status": "registered", "id": entry_id, "kind": kind, "scene": relative,
            "changedPaths": ["res://" + path.relative_to(project).as_posix()
                             for path in changes if path.is_relative_to(root)]}
