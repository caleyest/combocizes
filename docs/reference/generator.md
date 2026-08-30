# Generator

The exercise-selection and class-assembly layer — see
[DESIGN.md](https://github.com/caleyest/combocizes/blob/main/DESIGN.md)
sections 4–5. `select_combo`/`select_plyo_burst` (in `combo_selector.py`)
turn a loaded exercise pool (see [Exercise data model](exercise-data.md))
into one segment's worth of ordered exercises; `build_class`
(`class_template.py`) assembles a full sequence of segments — timing,
ordering, and equipment — on top of them. There's no CLI or rendered
script yet — that's a later milestone; `build_class` returns structured
data (a list of `ClassSegment`), not text.

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

`mover_position_start`/`mover_position_end` are validated against
`constants.MOVER_POSITIONS` (see [Exercise data model](exercise-data.md)),
but chaining itself is still exact-string-match on top of that — two
exercises describing the same physical position with different words from
that vocabulary simply won't chain. Worth keeping consistent across
`data/exercises/*.py` files as more get authored.

## `select_plyo_burst`

```python
from combocizes.combo_selector import select_plyo_burst

selection = select_plyo_burst(pool, equipment={}, count=8)
```

Plyo bursts get their own function rather than `select_combo`, because
their structuring rule is fundamentally different — every plyo-pool
candidate already shares `movement_pattern == "plyo"`, so movement-pattern
variety wouldn't discriminate between them, and impact needs a repeating
pattern, not free variety:

1. **Impact pattern (hard rule).** Follows a repeating **2:1 or 3:1
   high:low impact** pattern (the ratio is chosen per burst) — e.g. high,
   high, low, high, high, low, .... Raises `ValueError` if either impact
   level has no candidates at all (when `count > 1`).
2. **Mat-orientation chaining (secondary preference).** Within whichever
   impact a slot needs, prefers a candidate whose `mat_orientation_start`
   matches the previous pick's `mat_orientation_end` — a burst has no rest
   between exercises, so it shouldn't force an unplanned turn mid-burst.
   Falls back to the full same-impact bucket if nothing matches, same
   "preference, not requirement" pattern as `select_combo`'s chaining.
3. **Random tie-break**, same as `select_combo`.

`mat_orientation_start`/`mat_orientation_end` default to `"front"` on
every `Exercise` (see [Exercise data model](exercise-data.md)), so only
exercises that actually turn need to set them.

## `build_class`

```python
from combocizes.class_template import build_class

segments = build_class(pool, minutes=60)
# list[ClassSegment]: kind, selection (a ComboSelection), duration_minutes
```

Assembles a full class on top of the two selection functions above:

- **Timing**: each fixed-ish segment (warmup, plyo total, arms, legs, abs,
  cooldown) uses the midpoint of its DESIGN.md range regardless of total
  class length; whatever time is left goes to full-body-combo stretches,
  sized like a typical focus song (~4 min each) rather than one big block.
  Raises `ValueError` if `minutes` is too short to fit the fixed segments.
- **Ordering**: warmup first, cooldown last. In between, plyo bursts are
  inserted into random gaps among the shuffled focus-song/full-body-combo
  segments — a gap-insertion scheme that guarantees no two plyo bursts are
  ever adjacent and the segment right before cooldown is never plyo,
  without ever needing to check-and-retry. Everything else can appear in
  any order, including back to back.
- **Equipment**: warmup and cooldown always use no equipment. Every other
  segment is equipment-eligible; three of them are pre-assigned heavy
  dumbbells, light dumbbells, and band (either weight) respectively,
  guaranteeing that coverage rule by construction — the rest get a random
  combo (bodyweight included).

## Timing

```python
from combocizes.combo_selector import exercise_count_for_duration

exercise_count_for_duration(3.5)  # -> exercises that fit a 3.5-minute segment
```

There's no per-exercise duration field on `Exercise` — DESIGN.md doesn't
specify one. `exercise_count_for_duration` instead converts a segment's
minute budget into a count using a single fixed convention,
`constants.SECONDS_PER_EXERCISE` (currently 30s), floored to at least 1.
