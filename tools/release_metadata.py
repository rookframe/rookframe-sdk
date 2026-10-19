"""Record release source hashes; never generates SDK code or compiles a checker."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ADDON = ROOT / "addons/rookframe_sdk"
sys.path.insert(0, str(ADDON))
from rookframe_authoring import SDK_VERSION, UI_VERSION, UI_COMMIT
from rookframe_authoring_checks import committed_ui_files


def source_hashes(root):
    result = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == "release.json" or "__pycache__" in path.parts:
            continue
        data = path.read_bytes().replace(b"\r\n", b"\n")
        path.write_bytes(data)
        result[path.relative_to(root).as_posix()] = hashlib.sha256(data).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ui-kit", type=Path, required=True, help="Git checkout containing the pinned UI Kit commit")
    args = parser.parse_args()
    metadata = {"version": SDK_VERSION, "uiKit": {"version": UI_VERSION, "commit": UI_COMMIT},
                "files": source_hashes(ADDON), "sdkFiles": source_hashes(ROOT / "rookframe/sdk"),
                "uiFiles": committed_ui_files(args.ui_kit, UI_COMMIT)}
    (ADDON / "release.json").write_bytes((json.dumps(metadata, indent=2) + "\n").encode())


if __name__ == "__main__":
    main()
