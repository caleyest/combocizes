# Generator

The in-song exercise selector — see
[DESIGN.md](https://github.com/caleyest/combocizes/blob/main/DESIGN.md)
section 5. This is the piece that turns a loaded exercise pool (see
[Exercise data model](exercise-data.md)) into one song's worth of ordered
exercises. It doesn't yet build a full class — no `ClassTemplate`, no
segment ordering, no rendered script. That's a later milestone.

## `select_combo`

```python
from combocizes.combo_selector import select_combo
from combocizes.loader import load_exercises

pool = load_exercises()
selection = select_combo(pool, equipment={"heavy_dumbbells": True}, count=5)
# selection.exercises: list[Exercise], selection.equipment: the combo used
```

One equipment combo per call — every exercise in a `ComboSelection` shares
the same equipment, since a song doesn't ask a student to switch gear
mid-song. `select_combo` filters `pool` down to exercises that support the
given combo (and, optionally, an extra `pool_filter` — e.g. restricting to
a muscle group for a focus song), then picks `count` of them one at a time:

1. **Chaining (primary preference).** After the first pick, prefer a
   candidate whose `mover_position_start` matches the previous pick's
   `mover_position_end` — DESIGN.md's own example is a curl ending near the
   shoulders flowing straight into an overhead press that starts racked.
   If nothing chains, this step falls back to the full remaining pool
   rather than failing — chaining is a preference, not a requirement.
2. **Movement-pattern variety (secondary).** Among whichever candidates
   step 1 left, prefer whichever `movement_pattern` has been used least so
   far in this selection.
3. **Random tie-break.** Anything still tied is broken randomly (pass
   `rng=random.Random(seed)` for reproducible selections, e.g. in tests).

Both the chaining state and the pattern-usage counts are scoped to one
`select_combo` call — they reset for the next song, not carried across a
whole class.

`mover_position_start`/`mover_position_end` are free-text right now
(DESIGN.md section 7 still hasn't settled a shared vocabulary), so chaining
is exact-string-match — two exercises describing the same physical
position with different words simply won't chain. Worth keeping consistent
across `data/exercises/*.py` files as more get authored.

## Timing

```python
from combocizes.combo_selector import exercise_count_for_duration

exercise_count_for_duration(3.5)  # -> exercises that fit a 3.5-minute segment
```

There's no per-exercise duration field on `Exercise` — DESIGN.md doesn't
specify one. `exercise_count_for_duration` instead converts a segment's
minute budget into a count using a single fixed convention,
`constants.SECONDS_PER_EXERCISE` (currently 30s), floored to at least 1.
