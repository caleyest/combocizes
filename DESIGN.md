# Combocizes — Design Summary

Design spec for a Python program that builds full-body workout class scripts (combinations of dumbbell, bodyweight, and resistance band exercises) from a structured exercise dictionary.

## 1. Exercise Schema

Each exercise is a single record — not duplicated per equipment variant.

### Classification fields
- `name`
- `movement_pattern` — push / pull / hinge / squat / lunge / core / plyo
- `body_region` — upper / lower / core / full (coarse; drives warmup/cooldown/full-body filtering)
- `muscle_group` — biceps, triceps, shoulders, chest, back, quads, hamstrings, glutes, abs, etc. (fine-grained; drives the arms/legs/abs focus songs)
- `body_positions` — list of one or more of: standing_narrow / standing_wide / seated / supine / prone / kneeling / plank / hinge / lunge. A list, not a single value, since some exercises validly work from several stances (e.g. a hammer curl done standing_narrow, standing_wide, kneeling, or from a lunge) — purely additive, unlike equipment, since cue text doesn't change based on stance.
- `unilateral` — bool
- `impact` — high / low

### Equipment handling (single entry, override-merged)

Rather than one entry per equipment variant (risk of drift), each exercise carries:

- `equipment_options`: list of valid equipment *combos* for this exercise, each a dict of independent per-category flags — `heavy_dumbbells`, `light_dumbbells`, `heavy_band`, `light_band`, `block` — rather than one flat string enum, e.g. `{"heavy_dumbbells": True}`, `{"heavy_dumbbells": True, "single": True}`, `{"light_band": True}`. Dumbbells and bands are split by weight/resistance tier because a student typically has **both** a heavy and a light set on hand at once (two physical sets, not a dial to turn), so availability is naturally two independent yes/no's rather than one choice between them.
- `single` is **not** a sixth equipment category — it's a modifier on whichever dumbbell tier is chosen (one dumbbell from the pair, held with both hands, goblet-style), not a separate item a student owns.
- `overrides`: dict keyed by the equipment combo, containing **only** the fields that differ for that variant (`direction`, `unilateral`, extra refinement cues, etc.). Dicts aren't hashable, so combo keys are normalized to a sorted tuple of `(flag, value)` pairs, e.g. `(("heavy_dumbbells", True),)` or `(("heavy_dumbbells", True), ("single", True))`.

### Mover fields (what's actually moving)

There's no separate `equipment_position` field — an earlier design had one, but it was never implemented and would have needed nearly the same vocabulary as `mover_position` anyway. Instead, `mover`/`mover_position_start`/`mover_position_end` are the *only* fields for "where is the thing that's moving":

- `mover` — what's executing the movement: a body part (e.g. `"leg"`, `"arm"`, `"torso"`, `"hip"`), independent of which equipment is selected, or `"equipment"` when the equipment itself is what travels and what the cue should name (e.g. a curl). Controlled vocabulary — must be a key in `MOVER_POSITIONS` (below).
- `mover_position_start` / `mover_position_end` — that mover's position at the start and end of the rep (e.g. a reverse lunge: `mover: "leg"`, start `"standing"`, end `"lunge_back"`). Controlled vocabulary, namespaced **per mover** (a leg's travel states and the equipment's are unrelated), for the same reason as the other classification fields — authoring consistency and typo-catching:

```python
MOVER_POSITIONS = {
    "equipment": [
        "racked",
        "hanging_palms_in",
        "hanging_palms_front",
        "hanging_palms_back",
        "heart's center",
        "overhead",
        "extended",
        "shoulder",
        "around_thighs",
        "around_ankles",
        "anchored_underfoot",
        "around_wrists",
    ],
    "leg": [
        "standing",
        "lunge_back",
        "lunge_forward",
        "squat_bottom",
        "kneeling",
        "raised_bent",
        "raised_straight",
    ],
    "arm": ["at_sides", "extended", "raised", "overhead", "bent"],
    "torso": ["upright", "rotated_left", "rotated_right", "flexed_forward", "extended_back"],
    "hip": ["neutral", "hinged", "extended", "raised"],
}
```

`"arm"`/`"torso"`/`"hip"` aren't used by any exercise yet — starter placeholders, adjust the first time a real exercise needs a value not listed.

Example — reverse lunge with dumbbells: `mover: "leg"`, `mover_position_start: "standing"`, `mover_position_end: "lunge_back"`. The dumbbells stay racked and never travel; the leg does — so nothing about the equipment is tracked here at all for this exercise.

**Next step, not built yet:** for an exercise where equipment is held but isn't the mover (like the reverse lunge above), what to do with it — "keep your dumbbells racked at your sides" — is a candidate for a common, shared refinement cue (authored once in the cue bank, referenced via `refinement_cue_ids`) rather than a structured schema field.

Resolution at build time: pick equipment first → shallow-merge `base + overrides[combo_key]` → resolved variant.

```python
combo_key = tuple(sorted(chosen_equipment.items()))
resolved = {**base, **overrides.get(combo_key, {})}
```

Resolution order matters: **choose equipment → then resolve position/cues from it**, not the reverse.

### Cue fields

- `primary_cue`: decomposed into:
  - `breath` (e.g. "exhale")
  - `action` (verb, e.g. "drive")
  - `action_pool_key` (points into a shared synonym pool for randomized verb variety, e.g. `curl_up: ["drive", "curl", "pull", "draw"]`)
  - `direction` (fixed, exercise-specific free text — usually doesn't vary by equipment)

  The equipment-resolved object noun (`moved_object`) isn't authored as a
  field — it's derived from `mover` and the chosen equipment (see the Mover
  fields section above): `"your dumbbells"` (or `"your dumbbell"` for the
  single-dumbbell combo) when `mover` is `"equipment"`, otherwise `"your
  {mover}"`.

  Assembled at render time into: `"{breath}, {exercise_name}, {action} {moved_object} {direction}."`
  Said once, on first appearance of the exercise in the class.

- `refinement_cue_ids`: explicit references into the shared cue bank (see below)
- `own_refinement_cues`: exercise-specific cues too particular to generalize

## 2. Refinement Cue Bank (shared, global table)

A separate table, not embedded per-exercise:

```python
CUE_BANK = {
  "elbows_pinned_ribs": {
      "text": "Keep your elbows pinned to your ribs.",
      "tags": {"joint_focus": "elbow", "movement_pattern": ["curl"], "region": "upper"}
  },
  ...
}
```

- Exercises reference cues by ID explicitly — **not** auto-matched by tag at runtime, to avoid a cue silently surfacing in a contextually wrong spot.
- Tags are used only to **suggest** candidates during authoring (you pick from a shortlist), never to auto-inject at generation time.
- Editing bank text once propagates everywhere it's referenced — solves the same duplication/drift problem the equipment-override pattern solves.
- Refinement cues rotate across repeat appearances of an exercise within a class, so the script doesn't repeat verbatim.

**Open question:** plyo/continuous-tempo exercises may need a different cue shape than breath-per-rep (setup cue + safety/landing cue + pacing cue, no per-rep breath). Not yet resolved.

## 3. Data Layout

### Format: Python, not YAML/JSON

Each exercise and cue is authored directly as a Python object (dataclass instance), not YAML/JSON. Since equipment combos are per-category boolean flags and refinement cues are referenced by ID, a Python data file can reference the same constants used elsewhere — `DUMBBELL_POSITIONS`, `BAND_POSITIONS`, the `movement_pattern` enum, `CUE_BANK` IDs — instead of duplicating them as bare strings that can silently drift out of sync with the enum. A `@dataclass` with `__post_init__` validation (asserting equipment flags are drawn from the known set, `movement_pattern` is a valid value, referenced cue IDs exist, etc.) catches authoring typos at import time rather than only when the generator runs, without needing a separate schema-validation library (pydantic/jsonschema) for something the project already has enum/constant machinery for. Trade-off: less safe to hand-edit blind than YAML, since loading a file executes code — acceptable here since this is a single-maintainer Python project, not a format meant for non-programmers to edit.

### Exercises: one file per exercise

`exercises/` is a flat directory, one file per exercise, named `{muscle_group}_{name}.py` (e.g. `biceps_hammer_curl.py`, `quads_reverse_lunge.py`). The filename prefix gives fast visual grouping by muscle group in any directory listing/sort, without creating a folder hierarchy that has to be physically reorganized if an exercise is ever reclassified — renaming a file is a one-line diff, moving it between nested folders isn't. A loader function globs the directory, imports each file's exercise object, and combines them into the pool the generator selects from; this parsing step is cheap and runs once at startup, not per-generation.

Nested folders by `movement_pattern` were considered (only 7 stable values, less prone to reclassification than `muscle_group`) but rejected in favor of the filename convention, since `muscle_group` is the axis actually used for browsing/editing exercises, not `movement_pattern`.

### Cues: category files, not one-per-cue

Refinement cues stay grouped, not split one-per-file — each cue is only 3-4 lines, so hundreds of near-empty files would be harder to browse than the single large dict this split is meant to avoid. Instead, `CUE_BANK` is split across a handful of category files (`cues/upper.py`, `cues/lower.py`, `cues/core.py`, `cues/plyo.py`), each exposing a local dict; the same loader merges them into one `CUE_BANK` at import time — the same "split for readability, combine cheaply at load" pattern as exercises, just at a coarser grain.

## 4. Class Template (fixed format, drives generation)

| Segment | Duration | Count | Position | Notes |
|---|---|---|---|---|
| Warmup | 5-8 min | 1 | fixed first | full-body, low intensity |
| Plyo bursts | 10-15 min total | 3-4 bursts | spread through middle | **no rest** — active recovery via alternating high/low impact within each burst (hard sequencing rule); multiple exercises per burst; pulled from a dedicated plyo exercise bank |
| Arms-only song | 3-5 min | 1 | flexible, middle | filters on `muscle_group` |
| Legs-only song | 5 min | 1 | flexible, middle | filters on `muscle_group` |
| Abs-only song | 3-5 min | 1 | flexible, middle | filters on `muscle_group` |
| Full-body combos | remainder (~19-24 min typical) | fills gaps | flexible | main use of movement-pattern variety and mover-position chaining logic, see section 5 |
| Cooldown | ~5 min | 1 | fixed last | last 90 sec = savasana |

**Ordering rule:** don't cluster plyo bursts or focus-songs back to back — intersperse with full-body combo stretches to manage the intensity curve.

Segment-to-segment transitions (equipment swaps, floor/standing changes) are an expected, known part of moving between songs — not something the generator scores or optimizes against.

Worked time budget (60 min class, midpoint durations): warmup 6 + plyo 12 + arms 4 + legs 5 + abs 4 + cooldown 5 = 36 min fixed/ranged → **~24 min left for full-body combos**. At 50 min (low end of each range): 31 min fixed → **~19 min for full-body combos**.

## 5. Generator Architecture

- **One parameterized combo-selection function** — "select N exercises from a filtered pool, chained by mover position and varied by movement pattern, fit to a time budget" — reused for plyo bursts, focus songs, and full-body combos, configured differently per `ClassTemplate` segment (pool filter, exercise count, equipment).
- Each pick after the first prefers a candidate whose `mover_position_start` matches the previous pick's `mover_position_end` — in-song chaining (e.g. a curl ending near the shoulders flowing straight into an overhead press starting racked), the primary preference. Among whichever candidates that leaves (the chained ones, or the full remaining pool if none chain), the exercise whose `movement_pattern` has been used least so far in the selection is preferred; further ties break randomly.
- Resolution order per exercise instance: choose equipment → resolve position/cue overrides → place in sequence.

## 6. User Interface

### Upfront wizard questions (confirmed for v1)
1. Class length (50/60/custom)
2. Song durations, if fixed (exact lengths vs. pick within range)
3. Theme/emphasis for the day (optional bias, not a hard filter)
4. Must-include / must-exclude exercises

### Post-generation flow
- Generate a draft skeleton first (exercise names + timing only, no cues yet)
- Review loop: lock a segment / reroll a single segment / manually swap one exercise / regenerate all unlocked segments
- Only once the skeleton is finalized, expand into the full timestamped cue script

### Modality
CLI wizard to start (prompts → draft → lock/reroll loop → export finished script to text/markdown). YAML config file as a companion for saving reusable "class recipes." A GUI (e.g. Streamlit) is a possible v2, not needed for v1.

## 7. Explicitly deferred / not yet decided

- Plyo cue shape (breath-per-rep vs. setup+safety+pacing)
- Exact verb synonym-pool vocabulary
- Full `muscle_group` taxonomy list
- Equipment-availability-per-day, impact ceiling, difficulty level, and repeat-avoidance-across-classes were proposed as wizard questions but not selected for v1 — worth revisiting later if needed
- A common/shared refinement cue for equipment that's held but not the mover (e.g. "keep your dumbbells racked at your sides") — see section 1
