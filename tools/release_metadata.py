"""Record SDK source hashes without generating code or installing helper libraries."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "addons/rookframe_sdk/release.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", help="SDK release version; defaults to the current metadata version")
    args = parser.parse_args()
    previous = json.loads(METADATA.read_text(encoding="utf-8"))
    hashes = {}
    for path in sorted((ROOT / "rookframe/sdk").rglob("*")):
        if path.is_file():
            data = path.read_bytes().replace(b"\r\n", b"\n")
            path.write_bytes(data)
            hashes[path.relative_to(ROOT / "rookframe/sdk").as_posix()] = hashlib.sha256(data).hexdigest()
    metadata = {"version": args.version or previous["version"], "files": {}, "sdkFiles": hashes}
    METADATA.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
