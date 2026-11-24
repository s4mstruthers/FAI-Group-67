#!/bin/zsh
# ---------------------------------------------------------------------------
# FAINT competitive sudoku – one-click environment setup for macOS.
#
# Double-click this file in Finder (or run it in Terminal). It will:
#   1. find your conda installation,
#   2. create (or update) the conda environment 'faint' with Python 3.10.9,
#   3. run the A0 smoke tests: simulate_game.py --help / --check / a default game,
#   4. point VS Code at the new environment for this folder.
# Everything printed is also saved to setup_env.log next to this file.
# ---------------------------------------------------------------------------
set -u
cd "${0:A:h}" || exit 1            # work in the folder that contains this script
exec > >(tee setup_env.log) 2>&1   # show output and save it to a log file

ENV_NAME="faint"

# --- 1. Locate conda --------------------------------------------------------
CONDA=""
for candidate in \
    "$(command -v conda 2>/dev/null)" \
    "$HOME/anaconda3/bin/conda" "$HOME/miniconda3/bin/conda" "$HOME/miniforge3/bin/conda" \
    "$HOME/opt/anaconda3/bin/conda" "$HOME/opt/miniconda3/bin/conda" \
    /opt/anaconda3/bin/conda /opt/miniconda3/bin/conda /opt/miniforge3/bin/conda \
    /opt/homebrew/anaconda3/bin/conda /opt/homebrew/Caskroom/miniforge/base/bin/conda \
    /opt/homebrew/Caskroom/miniconda/base/bin/conda /usr/local/anaconda3/bin/conda; do
  if [[ -n "$candidate" && -x "$candidate" ]]; then CONDA="$candidate"; break; fi
done
if [[ -z "$CONDA" ]]; then
  echo "ERROR: could not find conda. Install Miniforge or Anaconda first."; exit 1
fi
echo "Using conda at: $CONDA"
eval "$("$CONDA" shell.zsh hook)"   # makes 'conda activate' work in this script

# --- 2. Create or update the environment -----------------------------------
if conda env list | grep -qE "^${ENV_NAME}[[:space:]]"; then
  echo "\n== Updating existing environment '$ENV_NAME' =="
  conda env update -n "$ENV_NAME" -f environment.yml --prune || exit 1
else
  echo "\n== Creating environment '$ENV_NAME' =="
  conda env create -f environment.yml || exit 1
fi
conda activate "$ENV_NAME" || exit 1
echo "Python in use: $(command -v python) ($(python --version))"

# --- 3. Smoke tests from Assignment 0, step C -------------------------------
chmod +x bin/solve_sudoku   # zip extraction can drop the executable bit
if xattr -p com.apple.quarantine bin/solve_sudoku >/dev/null 2>&1; then
  echo "\nNOTE: macOS has quarantined bin/solve_sudoku (it came from a download)."
  echo "If --check fails below, see the instructions Claude gave you."
fi
echo "\n== simulate_game.py --help ==";  python simulate_game.py --help
echo "\n== simulate_game.py --check =="; python simulate_game.py --check
echo "\n== simulate_game.py (default game) =="; python simulate_game.py

# --- 4. Tell VS Code to use this environment for this folder ---------------
mkdir -p .vscode
if [[ ! -f .vscode/settings.json ]]; then
  cat > .vscode/settings.json <<EOF
{
  "python.defaultInterpreterPath": "$(command -v python)",
  "python.terminal.activateEnvironment": true
}
EOF
  echo "\nWrote .vscode/settings.json (VS Code will use the '$ENV_NAME' interpreter here)."
fi

echo "\n== Setup finished. Log saved to setup_env.log =="
