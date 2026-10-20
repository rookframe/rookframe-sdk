"""Build a standalone optional SDK library ZIP; no authoring tools or UI Kit."""
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build(output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for source in sorted((ROOT / "rookframe/sdk").rglob("*")):
            if source.is_file():
                archive.write(source, source.relative_to(ROOT).as_posix())
        archive.write(ROOT / "addons/rookframe_sdk/release.json", ".rookframe/libraries/sdk/release.json")
        archive.write(ROOT / "THIRD_PARTY_NOTICES.md", ".rookframe/libraries/sdk/THIRD_PARTY_NOTICES.md")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    build(parser.parse_args().output)
