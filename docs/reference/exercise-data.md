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
| `constants.py` | Controlled vocabularies (movement pattern, body region, muscle group, body position, impact, equipment flags, mover positions) and derived shared constants. |
| `schema.py`    | The `Exercise` and `PrimaryCue` dataclasses, equipment-combo resolution, and moved-object derivation. |
| `cues.py`      | The `RefinementCue` dataclass and `build_cue_bank`, which merges the category files under `data/cues/`. |
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

### `mover` and `mover_position`: validated, per-mover vocabulary

`mover` names whatever the primary cue should treat as "the thing doing the
work": a body part (`"leg"`, `"arm"`, `"torso"`, `"hip"`) or `"equipment"`,
when the equipment itself is what travels and what the cue should name
(e.g. a curl). It must be a key in `constants.MOVER_POSITIONS`, and
`mover_position_start`/`mover_position_end` must each be one of that
mover's listed positions — different movers travel through entirely
different physical states, so the vocabulary is namespaced per mover rather
than shared. `"equipment"`'s list absorbs what an earlier design called
`equipment_position` (there's no separate field for that — see DESIGN.md
section 1).

### The moved-object noun is derived, not authored

The primary cue's object noun (e.g. "your dumbbells", "your leg") comes from
`resolve_moved_object`, not from data an author writes per exercise:

- If `mover` is `"equipment"`, the equipment itself is what's moving (e.g. a
  curl), so the noun is looked up in `EQUIPMENT_PHRASES` for whichever flag
  is set, singularized if `single` is also set (`"your dumbbells"` →
  `"your dumbbell"`).
- Otherwise, the noun is `"your {mover}"` — the equipment stays put (e.g.
  dumbbells racked through a lunge) and the body part named by `mover` is
  what's actually moving.

### Refinement cues

`build_cue_bank()` merges every category file under `data/cues/` (e.g.
`data/cues/upper.py` exposing a local `UPPER_CUES` list) into one flat
`list[RefinementCue]`. Each `RefinementCue` names the exercises it applies to
via its own `exercise_ids` — that's the only place the exercise/cue
relationship is authored; `Exercise` carries no reference back into the cue
bank.

The cue bank isn't built as a module-level constant in `combocizes.cues`: a
cue's `exercise_ids` can't be validated against real exercise names until the
exercise pool exists, so `build_cue_bank()` is called from `load_exercises`
instead, once that pool is assembled.

## Loading the pool

```python
from combocizes.loader import load_exercises

exercises = load_exercises()  # dict[str, Exercise], keyed by name
```

`load_exercises` globs `data/exercises/*.py`, dynamically imports each file,
raises `ValueError` on a duplicate exercise name, and cross-checks every
cue's `exercise_ids` against the resulting pool — raising `ValueError` if a
cue names an exercise that doesn't exist. It's meant to run once at startup,
not per-generation.
