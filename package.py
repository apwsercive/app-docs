"""Package only the portable documentation source for browser uploads."""
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
SOURCES = ("README.md", "DEPLOYMENT.md", "THIRD_PARTY.md", ".gitignore", "site.json",
           "build.py", "check.py", "markdown_content.py", "package.py", "content", "assets", "vendor")


def package(output):
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in SOURCES:
            source = ROOT / name
            for path in sorted(source.rglob("*")) if source.is_dir() else [source]:
                if not path.is_file() or path.is_symlink() or path == output:
                    continue
                relative = path.relative_to(ROOT)
                if "__pycache__" in relative.parts or path.suffix == ".pyc":
                    continue
                archive.write(path, relative.as_posix())
        print(f"Packaged {len(archive.namelist())} source files into {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(ROOT / "source.zip"))
    package(parser.parse_args().output)
