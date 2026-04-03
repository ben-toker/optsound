# optsound — implementation plan

## goal

Get the core pipeline working end-to-end: audio files (or CSV) in, optimized playlist ordering out.

```
input → track.py → models.py → parse.py → solve.py → main.py → ordered playlist
```

---

## milestone 1: housekeeping

Quick fixes so the existing code is clean and importable.

- [ ] **requirements.txt** — add `cvxpy`, `numpy`; remove `requests`, `python-dotenv` if unused (#1)
- [ ] **solve.py line 145** — delete `solve('models/test.txt')` so it can be imported as a module (#2)
- [ ] **track.py** — add `to_dict()` method to `Track` class (#3)
  ```python
  def to_dict(self):
      return {"id": self.id, "tempo": self.tempo, "key": self.key,
              "mode": self.mode, "time_sig": self.time_sig,
              "loudness": self.loudness, "duration": self.duration}
  ```

**done when:** `from solve import solve` and `from track import Track` work without side effects, and `solve.solve('models/test.txt')` still returns the correct solution.

---

## milestone 2: model templates

Implement the preset objective functions in `models/models.py`. (#4)

Each function returns a spec dict — no formulation logic here, just declarations.

- [ ] `uniform_tempo(tracks)` → `{"problem_type": "min", "feature": "tempo", "objective_type": "uniform"}`
- [ ] `uniform_increasing_tempo(tracks)` → `{"problem_type": "min", "feature": "tempo", "objective_type": "increasing"}`
- [ ] `uniform_decreasing_tempo(tracks)` → `{"problem_type": "min", "feature": "tempo", "objective_type": "decreasing"}`
- [ ] add a `MODELS` dict mapping CLI names to functions:
  ```python
  MODELS = {
      "uniform_tempo": uniform_tempo,
      "increasing_tempo": uniform_increasing_tempo,
      "decreasing_tempo": uniform_decreasing_tempo,
  }
  ```

**done when:** `from models.models import MODELS; MODELS["uniform_tempo"]([])` returns the correct spec dict.

---

## milestone 3: parse.py — the core

This is the bulk of the work. `parse.py` translates tracks + a model spec into the text file format `solve.py` reads. (#5)

### function signature

```python
def parse(tracks, size, model_spec, output_file="models/custom.txt"):
```

- `tracks` — list of feature dicts (from `Track.to_dict()` or CSV)
- `size` — int, playlist length K
- `model_spec` — dict from models.py
- `output_file` — path to write

### what to implement, in order

1. **variable index**
   - [ ] generate variable names `x_i_j` for all track `i` in `[1..N]`, position `j` in `[1..K]`
   - [ ] build a lookup: `(i, j)` → flat index, and `(i, j)` → variable name string

2. **assignment constraints**
   - [ ] column constraints: `Σ_i x_ij = 1` for each position `j` (each slot filled by exactly one track)
   - [ ] row constraints: `Σ_j x_ij ≤ 1` for each track `i` (each track used at most once)
   - [ ] total constraint: `Σ_ij x_ij = K`
   - [ ] each constraint is a list of N×K integer coefficients + operator + RHS

3. **objective line with abs-value terms**
   - [ ] for `uniform` / `increasing` / `decreasing`: build abs-value segments for consecutive position pairs
   - [ ] each segment for pair `(j, j+1)`:
     ```
     var_names:  '', x_1_j, ..., x_N_j, x_1_(j+1), ..., x_N_(j+1), ''
     coeffs:     '|', t_1,  ...,  t_N,   -t_1,      ..., -t_N,       '|'
     ```
     where `t_i = round(tempo_i)`
   - [ ] prepend canonical variable list with zero coefficients (so solve.py's first-occurrence scan matches constraint order)

4. **monotonicity constraints** (increasing/decreasing only)
   - [ ] increasing: `Σ_i t_i · x_{i,j+1} − Σ_i t_i · x_{i,j} ≥ 0` for each consecutive pair
   - [ ] decreasing: flip to `≤ 0`

5. **file writer**
   - [ ] line 0: comma-joined variable names (canonical + abs-value padding)
   - [ ] line 1: problem type (`min` or `max`)
   - [ ] line 2: comma-joined objective coefficients
   - [ ] lines 3+: comma-joined constraint coefficients + operator + RHS

### coefficient scaling

solve.py parses `int()`, so:
- tempo → `round()`
- loudness → `round(val * 10)` (if used in future objectives)

**done when:** `parse(tracks, 3, spec)` writes a valid model file, and `solve.solve('models/custom.txt')` returns a feasible solution that respects all assignment constraints.

---

## milestone 4: main.py CLI

Wire everything together with a command-line interface. (#6)

### interface

```
python main.py --input <dir_or_csv> --size <int> --objective <name>
```

### what to implement

- [ ] **argparse setup** — `--input`/`-i`, `--size`/`-s`, `--objective`/`-o`
- [ ] **input detection** — if path is a directory, treat as audio files; if `.csv`, load as pre-computed features
- [ ] **audio file loader** — glob `*.mp3`, `*.wav`, `*.flac` → create `Track` objects → `extract_basic_features()` → `to_dict()`
- [ ] **CSV loader** — `csv.DictReader`, cast numeric fields, return list of feature dicts
- [ ] **validation** — `size ≤ len(tracks)`, required features present
- [ ] **pipeline call** — get model spec → `parse()` → `solve()` → collect results
- [ ] **result interpreter** — filter solution for `x_i_j == 1`, parse variable names to recover `(track, position)` pairs, sort by position
- [ ] **output** — print the ordered playlist with track names, positions, and key features (tempo at minimum)

**done when:** `python main.py -i test.csv -s 3 -o uniform_tempo` prints a correctly ordered playlist. `python main.py -i ./audio_folder/ -s 3 -o increasing_tempo` does the same from raw audio files.

---

## milestone 5: verification

- [ ] **regression** — `solve.solve('models/test.txt')` returns the same result as before
- [ ] **round-trip with known data** — create a 5-track CSV with tempos `[60, 90, 120, 150, 180]`, run `uniform_tempo` with size 3, verify the selected tracks have minimal tempo gaps
- [ ] **increasing tempo** — same CSV, verify output is in ascending tempo order
- [ ] **decreasing tempo** — verify descending
- [ ] **audio file path** — run against a folder with a few real audio files, verify no crashes and sensible output
