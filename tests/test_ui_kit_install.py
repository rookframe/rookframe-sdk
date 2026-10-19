"""Offline tests of UI Kit file ownership and revision changes."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1] / "addons/rookframe_sdk"
sys.path.insert(0, str(TOOLS))
from rookframe_ui_kit_install import install_runtime, write_provenance, committed_runtime, INVENTORY
from rookframe_authoring_checks import committed_ui_files


class UiKitInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "source"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Local fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        # Match the real UI Kit's byte-stable text checkout on every Git host.
        self.put(".gitattributes", b"* text=auto eol=lf\n")
        self.resource = b'[gd_resource type="Resource" format=3 uid="uid://bfixture"]\n[resource]\n'
        self.put("rookframe/ui/core.tres", self.resource)
        self.put("rookframe/ui/core.gd.uid", b"uid://bfixture\n")
        self.put("rookframe/ui/theme/legacy.tres", b"legacy bundled theme")
        self.current = self.commit()
        shutil.rmtree(self.repo / "rookframe")
        self.put("ui-kit/rookframe/ui/core.tres", self.resource)
        self.put("ui-kit/rookframe/ui/core.gd.uid", b"uid://bfixture\n")
        self.put("ui-kit/rookframe/ui/new.tres", b"new core")
        self.put("themes/fantasy/rookframe/ui/optional.tres", b"excluded")
        self.put("showcase/rookframe/ui/showcase.tres", b"excluded")
        self.next = self.commit()
        self.project = self.root / "project"
        cache = self.project / ".plugged/rookframe-ui-kit"
        cache.parent.mkdir(parents=True)
        subprocess.run(["git", "clone", "--quiet", str(self.repo), str(cache)], check=True)

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], stderr=subprocess.PIPE).decode().strip()

    def put(self, name, data):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "layout fixture")
        return self.git("rev-parse", "HEAD")

    def install(self, commit):
        selected = {"tag": commit, "commit": commit}
        result = install_runtime(self.project, selected)
        write_provenance(self.project, selected)
        return result

    def test_fresh_layouts_switch_repeat_and_exclusions(self):
        for commit in (self.next, self.current, self.next, self.current, self.current):
            result = self.install(commit)
            self.assertEqual((self.project / "rookframe/ui/core.tres").read_bytes(), self.resource)
            self.assertEqual((self.project / "rookframe/ui/core.gd.uid").read_bytes(), b"uid://bfixture\n")
            self.assertEqual((self.project / "rookframe/ui/theme/legacy.tres").exists(), commit == self.current)
            self.assertEqual((self.project / "rookframe/ui/new.tres").exists(), commit == self.next)
            self.assertFalse((self.project / "ui-kit").exists())
            self.assertFalse((self.project / "themes").exists())
            self.assertFalse((self.project / "showcase").exists())
            self.assertEqual(set(committed_ui_files(self.project / ".plugged/rookframe-ui-kit", commit)), set(result["files"]))
            self.assertEqual(json.loads((self.project / "rookframe_ui_kit_provenance.json").read_text())["sourceRoot"], result["sourceRoot"])
        unrelated = self.project / "rookframe/ui/author.txt"
        unrelated.write_text("keep me")
        self.install(self.next)
        self.assertEqual(unrelated.read_text(), "keep me")

    def test_modifications_and_unowned_collisions_fail_without_mutation(self):
        self.install(self.current)
        before = (self.project / "rookframe_ui_kit_provenance.json").read_bytes()
        stale = self.project / "rookframe/ui/theme/legacy.tres"
        stale.write_text("local edit")
        with self.assertRaisesRegex(ValueError, "Locally modified"):
            self.install(self.next)
        self.assertEqual(stale.read_text(), "local edit")
        self.assertEqual((self.project / "rookframe_ui_kit_provenance.json").read_bytes(), before)
        stale.write_bytes(b"legacy bundled theme")
        collision = self.project / "rookframe/ui/new.tres"
        collision.write_bytes(b"new core")
        with self.assertRaisesRegex(ValueError, "unrelated"):
            self.install(self.next)
        self.assertEqual(stale.read_bytes(), b"legacy bundled theme")
        self.assertEqual(collision.read_bytes(), b"new core")

    def test_core_submodules_are_rejected(self):
        self.git("update-index", "--add", "--cacheinfo", "160000," + self.current + ",ui-kit/rookframe/ui/nested")
        self.git("commit", "-qm", "unsupported submodule")
        revision = self.git("rev-parse", "HEAD")
        with self.assertRaisesRegex(ValueError, "must not contain Git submodules"):
            committed_runtime(self.repo, revision)

    def test_legacy_gdplug_ownership_migration(self):
        _, files = committed_runtime(self.repo, self.current)
        for name, data in files.items():
            dest = self.project / "rookframe/ui" / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        install_runtime(self.project, {"tag": self.next, "commit": self.next}, previous_commit=self.current,
                        legacy_files=["res://rookframe/ui/" + name for name in files])
        self.assertFalse((self.project / "rookframe/ui/theme/legacy.tres").exists())
        self.assertTrue((self.project / INVENTORY).exists())

    def test_failed_write_rolls_back_files_inventory_and_provenance(self):
        self.install(self.current)
        before = {p.relative_to(self.project): p.read_bytes() for p in self.project.rglob("*") if p.is_file() and ".git" not in p.parts}
        from rookframe_ui_kit_install import atomic_write
        failed = False
        def fail_once(path, contents):
            nonlocal failed
            if path.name == "new.tres" and not failed:
                failed = True
                raise OSError("fixture write failure")
            atomic_write(path, contents)
        with patch("rookframe_ui_kit_install.atomic_write", side_effect=fail_once):
            with self.assertRaisesRegex(OSError, "fixture write failure"):
                self.install(self.next)
        after = {p.relative_to(self.project): p.read_bytes() for p in self.project.rglob("*") if p.is_file() and ".git" not in p.parts}
        self.assertEqual(before, after)

    def test_sdk_dependency_installer_uses_locked_layout(self):
        from rookframe_authoring_entries import install_dependencies
        bootstrap = self.root / "bootstrap"
        bootstrap.mkdir()
        subprocess.run(["git", "init", "-q", str(bootstrap)], check=True)
        script = bootstrap / "addons/gd-plug/plug.gd"
        script.parent.mkdir(parents=True)
        script.write_text("extends SceneTree\n")
        (bootstrap / "LICENSE").write_text("fixture license")
        subprocess.run(["git", "-C", str(bootstrap), "add", "."], check=True)
        subprocess.run(["git", "-C", str(bootstrap), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "bootstrap"], check=True)
        revision = subprocess.check_output(["git", "-C", str(bootstrap), "rev-parse", "HEAD"], text=True).strip()
        original_run = subprocess.run
        def local_run(args, **kwargs):
            args = [str(arg) for arg in args]
            args = [str(bootstrap) if arg == "https://github.com/imjp94/gd-plug.git" else revision if arg == "209276d1f00d14b49b74403d9839f29598e9a8eb" else arg for arg in args]
            self.assertFalse(any("https://" in arg for arg in args), args)
            return original_run(args, **kwargs)
        (self.project / ".rookframe").mkdir()
        for commit in (self.current, self.next, self.current):
            (self.project / ".rookframe/authoring.lock.json").write_text(json.dumps({"uiKit": {"version": commit, "commit": commit}}))
            with patch("subprocess.run", side_effect=local_run):
                install_dependencies(self.project)
            self.assertEqual(json.loads((self.project / "rookframe_ui_kit_provenance.json").read_text())["commit"], commit)
            self.assertEqual((self.project / "rookframe/ui/theme/legacy.tres").exists(), commit == self.current)

if __name__ == "__main__":
    unittest.main()
