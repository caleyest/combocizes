# Exercise data model

The exercise schema, refinement-cue bank, and their loaders — see
[DESIGN.md](https://github.com/caleyest/combocizes/blob/main/DESIGN.md)
sections 1–3 for the full design rationale. These three modules exist to
load `data/exercises/` and `data/cues/` into validated, in-memory pools once
at startup; they don't select or sequence exercises into a class (that's the
not-yet-built generator).

## Modules

| Module        | Responsibility                                                    |
| ------------- | ------------------------------------------------------------------ |
| `constants.py` | Controlled vocabularies (movement pattern, body region, muscle group, body position, impact, equipment flags) and derived shared constants. |
| `schema.py`    | The `Exercise` and `PrimaryCue` dataclasses, equipment-combo resolution, and moved-object derivation. |
| `cues.py`      | The `RefinementCue` dataclass and the merged `CUE_BANK`. |
| `loader.py`    | Globs and loads `data/exercises/*.py` into one pool. |

## Authoring an exercise

Each file in `data/exercises/` exposes one module-level `EXERCISE: Exercise`
instance, named `{muscle_group}_{name}.py` (e.g. `quads_reverse_lunge.py`).
Constructing that instance runs `Exercise.__post_init__` immediately, which
validates every classification field, equipment flag, override key, and
referenced cue ID — so a typo fails at import time with a traceback pointing
at the offending file, not silently later. See
`data/exercises/quads_reverse_lunge.py` and
`data/exercises/biceps_hammer_curl.py` in the repo for worked examples.

### Equipment: one record, resolved by merge

An exercise lists every equipment combo it supports in `equipment_options`
(a combo is a dict of flags, e.g. `{"heavy_dumbbells": True}`; the empty
dict `{}` means bodyweight), and puts only the fields that differ per combo
in `overrides`, keyed by `equipment_combo_key(combo)` — a sorted, hashable
tuple. `resolve_exercise(exercise, equipment)` shallow-merges the matching
override on top of the base fields. `constants.py` exposes the common
single-flag keys (`HEAVY_DUMBBELLS`, `LIGHT_DUMBBELLS`, `HEAVY_BAND`,
`LIGHT_BAND`, `NO_EQUIPMENT`) so exercise files don't each recompute them;
compound combos (e.g. adding the `single` modifier) are built inline with
`equipment_combo_key`.

### The moved-object noun is derived, not authored

The primary cue's object noun (e.g. "your dumbbells", "your leg") comes from
`resolve_moved_object`, not from data an author writes per exercise. It
looks at `Exercise.mover`:

- If `mover` is the `EQUIPMENT_MOVER` sentinel (`"equipment"`), the equipment
  itself is what's moving (e.g. a curl), so the noun is looked up in
  `EQUIPMENT_PHRASES` for whichever flag is set, singularized if `single` is
  also set (`"your dumbbells"` → `"your dumbbell"`).
- Otherwise, the noun is `"your {mover}"` — the equipment stays put (e.g.
  dumbbells racked through a lunge) and the body part named by `mover` is
  what's actually moving.

### Refinement cues

`CUE_BANK` is built once, at import time of `combocizes.cues`, by merging
every category file under `data/cues/` (e.g. `data/cues/upper.py` exposing a
local `UPPER_CUES` dict). It must exist before any `Exercise` is
constructed, since cue-ID validation checks against it — which is why
`cues.py` builds `CUE_BANK` as module-level code rather than behind a
function an exercise-loading step would need to call first. Cue tags
(`{"region": "upper"}`) are restricted to `combocizes`'s own vocabularies
(`movement_pattern`, `region`, `muscle_group`) rather than free text, since
there's no interactive shortlist to pick them from — but they're purely
advisory, never auto-injected into a class.

## Loading the pool

```python
from combocizes.loader import load_exercises

exercises = load_exercises()  # dict[str, Exercise], keyed by name
```

`load_exercises` globs `data/exercises/*.py`, dynamically imports each file,
and raises `ValueError` on a duplicate exercise name. It's meant to run once
at startup, not per-generation.
