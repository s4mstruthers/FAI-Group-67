# FAI Group 67 – Competitive Sudoku

Team 67's code for the Foundations of AI (TU/e) competitive sudoku assignments.
The course framework is included unchanged; our code lives in the `team67_*` folders.

## Layout

| Path | What it is |
|---|---|
| `team67_A1/` | **Our A1 player.** `sudokuai.py` (search), `moves.py` (move generation), `evaluation.py` (scoring) |
| `team67_A0/` | Trial submission (copy of `naive_player`), already handed in |
| `competitive_sudoku/`, `*_player/`, `simulate_game.py`, `play_match.py`, `boards/` | Course framework – **do not edit** (the grader runs our module against the original) |
| `environment.yml` | Conda environment `faint` (Python 3.10.9, same as the grading server) |
| `make_submission.py` | Tests a team folder and builds a clean submission zip |
| `setup_env.command` | One-click environment setup for macOS |

## First-time setup

1. Clone this repo.
2. Copy the `bin/` folder from **your own OS's** course bundle into the repo root
   (it is git-ignored because the solver differs per OS).
3. Create the environment:
   - macOS: run `zsh setup_env.command`
   - Windows / Linux: `conda env create -f environment.yml`, then `conda activate faint`
4. Check it works: `python simulate_game.py --check` should print *The sudoku_solve program works.*
5. In VS Code, open this folder and select the `faint` interpreter
   (Cmd/Ctrl+Shift+P → *Python: Select Interpreter*).

macOS only: if `--check` fails, macOS has quarantined the solver; run
`xattr -d com.apple.quarantine bin/solve_sudoku`.

## Working together

- **Pull before you start:** `git pull`
- **Work on a branch:** `git switch -c your-name/what-you-are-doing`
- **Stick to your file** where possible (moves / evaluation / search) to avoid merge conflicts.
- **Import within the team folder relatively:** `from .evaluation import evaluate`, not
  `from team67_A1.evaluation import ...` – so the folder can become `team67_A2` unchanged.
- **Before merging, test:**
  ```
  python simulate_game.py --first=team67_A1 --second=greedy_player --board=boards/empty-3x3.txt
  python play_match.py --first=team67_A1 --second=greedy_player --board=boards/empty-3x3.txt --count=5
  ```
- Open a pull request on GitHub and let someone else glance at it before merging into `main`.

Rules from the course README worth remembering: Python only, single-threaded, all code and data
files inside the team folder, and state between moves only via the provided `save`/`load`.

## Submitting

Never zip by hand (Finder/VS Code add `.DS_Store`, `__MACOSX`, `__pycache__`, `.vscode`). Use:

```
python make_submission.py team67_A1
```

This plays a test game and writes `team67_A1.zip` containing only the module files.
One person uploads it to Canvas.
