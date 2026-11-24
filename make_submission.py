#!/usr/bin/env python3
"""
Create (optionally) and package a team module for Momotor submission.

Why this script exists
----------------------
Zipping a folder with macOS Finder ("Compress") or via editor tooling such as
VS Code tends to add files that do not belong in a submission:

  * __MACOSX/ and ._*   - resource-fork metadata added by Finder's Compress
  * .DS_Store           - Finder folder-view settings
  * __pycache__/, *.pyc - compiled bytecode created whenever Python runs your code
  * .vscode/, .idea/    - editor settings
  * *.pkl               - save/load state files from test games

Momotor expects the zip to contain exactly one top-level folder (e.g.
'team07_A1') with your Python module inside it. This script builds the zip
from scratch, including only the files that belong to the module.

Usage (run from the folder containing simulate_game.py, with the env active)
-------------------------------------------------------------------------------
  python make_submission.py team07_A0 --create   # copy naive_player -> team07_A0
  python make_submission.py team07_A0            # test it, then build team07_A0.zip
  python make_submission.py team07_A1 --no-test  # build the zip without a test game
"""

import argparse
import fnmatch
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

# The directory that contains this script, simulate_game.py and the player modules.
ROOT = Path(__file__).resolve().parent

# File and folder name patterns that must never end up in a submission.
JUNK_PATTERNS = [
    "__pycache__", "*.pyc", "*.pyo",           # Python bytecode
    ".DS_Store", "._*", "__MACOSX",             # macOS Finder metadata
    ".vscode", ".idea", ".ipynb_checkpoints",   # editor / notebook folders
    "*.pkl",                                    # save/load files from test games
    "*.zip", "*.log", "Thumbs.db", "desktop.ini",
]

# Expected folder name, e.g. team07_A0, team07_A1, team07_A2.
NAME_PATTERN = re.compile(r"^team\d+_A\d+$")


def is_junk(name: str) -> bool:
    """Return True if a file or folder name matches one of the junk patterns."""
    return any(fnmatch.fnmatch(name, pattern) for pattern in JUNK_PATTERNS)


def create_module(module_dir: Path) -> None:
    """Copy naive_player to a new team folder (step D of the A0 instructions)."""
    if module_dir.exists():
        sys.exit(f"'{module_dir.name}' already exists; not overwriting it.")
    shutil.copytree(ROOT / "naive_player", module_dir,
                    ignore=shutil.ignore_patterns(*JUNK_PATTERNS))
    print(f"Created {module_dir.name}/ as a copy of naive_player/.")


def run_test_game(module_name: str) -> None:
    """Play one game with the team module as first player (step E)."""
    print(f"Running: simulate_game.py --first={module_name} --quiet")
    result = subprocess.run(
        [sys.executable, "simulate_game.py", f"--first={module_name}", "--quiet"],
        cwd=ROOT, capture_output=True, text=True, timeout=600,
    )
    print(result.stdout.strip() or result.stderr.strip())
    if result.returncode != 0:
        sys.exit("The test game failed; fix the error above before submitting.")


def build_zip(module_dir: Path) -> Path:
    """Zip the module folder itself (not just its contents), skipping junk (step F)."""
    zip_path = ROOT / f"{module_dir.name}.zip"
    included = []
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(module_dir.rglob("*")):
            relative = path.relative_to(ROOT)
            # Skip the item if it, or any folder above it, is junk.
            if any(is_junk(part) for part in relative.parts):
                continue
            if path.is_file():
                arcname = relative.as_posix()  # forward slashes, top folder = module name
                zf.write(path, arcname)
                included.append(arcname)
    print(f"\nWrote {zip_path.name} containing:")
    for name in included:
        print(f"  {name}")
    return zip_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create and package a team module for submission.")
    parser.add_argument("module", help="team module folder name, e.g. team07_A0")
    parser.add_argument("--create", action="store_true", help="copy naive_player to this folder first")
    parser.add_argument("--no-test", action="store_true", help="skip the test game before zipping")
    args = parser.parse_args()

    if not NAME_PATTERN.match(args.module):
        sys.exit(f"'{args.module}' does not look like teamNN_AX (e.g. team07_A0).")

    module_dir = ROOT / args.module
    if args.create:
        create_module(module_dir)

    # Sanity checks: the folder must be an importable module with a sudokuai.py.
    for required in ("__init__.py", "sudokuai.py"):
        if not (module_dir / required).is_file():
            sys.exit(f"{args.module}/{required} is missing.")

    if not args.no_test:
        run_test_game(args.module)
    build_zip(module_dir)


if __name__ == "__main__":
    main()
