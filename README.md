<img width="1480" height="499" alt="optsound" src="https://github.com/user-attachments/assets/a4c68f26-2329-46d9-9a3e-1699e92a6212" />

Playlist optimizer that uses mathematical optimization to find the best track ordering. Given a set of audio tracks and an objective (e.g. smooth tempo flow), optsound extracts audio features, formulates an integer assignment problem, and solves it with cvxpy.

# Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# How it works

## Pipeline

1. **Extract features** — librosa analyzes each audio file for tempo, key, mode, time signature, loudness, and duration (`track.py`)
2. **Build model** — track features + user objective are translated into a text-based optimization model (`parse.py` → `models/custom.txt`)
3. **Solve** — the model file is parsed into a cvxpy integer program and solved (`solve.py`)
4. **Output** — the optimal track ordering is returned (`main.py`)

## Formulation

The core formulation is an **assignment problem**:

- **Variables:** `x_ij = 1` if track `i` is placed in position `j`, else `0`
- **Constraints:** each position filled by exactly one track, each track used at most once
- **Objective:** depends on the chosen model (e.g. minimize absolute tempo differences between consecutive positions)

## Files

| File | Role |
|------|------|
| `track.py` | Audio feature extraction via librosa |
| `parse.py` | Generates the optimization model file from tracks + objective |
| `solve.py` | Reads model file, builds and solves the cvxpy problem |
| `models/models.py` | Preset objective templates (uniform tempo, increasing, decreasing) |
| `main.py` | CLI entrypoint — wires the pipeline together |

## Model file format

The text files in `models/` describe optimization problems that `solve.py` reads:

- **Line 0:** decision variable names, comma-separated (empty strings align with `|` delimiters in the objective)
- **Line 1:** `max` or `min`
- **Line 2:** objective coefficients, comma-separated (`|` marks absolute value groups)
- **Lines 3+:** constraint coefficients, operator, RHS — all comma-separated

# Current status

Core pipeline under active development. See [plan.md](plan.md) for implementation milestones and [open issues](https://github.com/ben-toker/optsound/issues) for specific tasks.
