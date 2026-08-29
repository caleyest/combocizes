# Combocizes — Design Summary

Design spec for a Python program that builds full-body workout class scripts (combinations of dumbbell, bodyweight, and resistance band exercises) from a structured exercise dictionary.

## 1. Exercise Schema

Each exercise is a single record — not duplicated per equipment variant.

### Classification fields
- `name`
- `movement_pattern` — push / pull / hinge / squat / lunge / rotation / carry / curl / isolation
- `body_region` — upper / lower / core / full (coarse; drives warmup/cooldown/full-body filtering)
- `muscle_group` — biceps, triceps, shoulders, chest, back, quads, hamstrings, glutes, abs, etc. (fine-grained; drives the arms/legs/abs focus songs)
- `body_position` — standing / seated / supine / prone / kneeling / plank
- `unilateral` — bool
- `plyometric` — bool
- `impact` — high / low
- Timing fields: work/rest or rep scheme, `setup_seconds` (feeds transition cost)

### Equipment handling (single entry, override-merged)

Rather than one entry per equipment variant (risk of drift), each exercise carries:

- `equipment_options`: list of valid equipment (e.g. `["dumbbell", "band"]`)
- `overrides`: dict keyed by equipment, containing **only** the fields that differ for that variant (`equipment_position`, `direction`, extra refinement cues, etc.)

Resolution at build time: pick equipment first → shallow-merge `base + overrides[equipment]` → resolved variant.

```python
resolved = {**base, **overrides.get(chosen_equipment, {})}
```

Resolution order matters: **choose equipment → then resolve position/cues from it**, not the reverse.

### Cue fields

- `primary_cue`: decomposed into:
  - `breath` (e.g. "exhale")
  - `action` (verb, e.g. "drive")
  - `action_pool_key` (points into a shared synonym pool for randomized verb variety, e.g. `curl_up: ["drive", "curl", "pull", "draw"]`)
  - `moved_object` (equipment-resolved noun, e.g. `{dumbbell: "your dumbbells", band: "the band"}`)
  - `direction` (fixed, exercise-specific free text — usually doesn't vary by equipment)

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

## 3. Class Template (fixed format, drives generation)

| Segment | Duration | Count | Position | Notes |
|---|---|---|---|---|
| Warmup | 5-8 min | 1 | fixed first | full-body, low intensity |
| Plyo bursts | 10-15 min total | 3-4 bursts | spread through middle | **no rest** — active recovery via alternating high/low impact within each burst (hard sequencing rule); multiple exercises per burst; pulled from a dedicated plyo exercise bank |
| Arms-only song | 3-5 min | 1 | flexible, middle | filters on `muscle_group` |
| Legs-only song | 5 min | 1 | flexible, middle | filters on `muscle_group` |
| Abs-only song | 3-5 min | 1 | flexible, middle | filters on `muscle_group` |
| Full-body combos | remainder (~19-24 min typical) | fills gaps | flexible | main use of transition-cost + variety logic |
| Cooldown | ~5 min | 1 | fixed last | last 90 sec = savasana |

**Ordering rule:** don't cluster plyo bursts or focus-songs back to back — intersperse with full-body combo stretches to manage the intensity curve.

Worked time budget (60 min class, midpoint durations): warmup 6 + plyo 12 + arms 4 + legs 5 + abs 4 + cooldown 5 = 36 min fixed/ranged → **~24 min left for full-body combos**. At 50 min (low end of each range): 31 min fixed → **~19 min for full-body combos**.

## 4. Generator Architecture

- **One parameterized combo-selection function** — "select N exercises from a filtered pool, respecting movement-pattern variety and equipment-transition cost, fit to a time budget" — reused for plyo bursts, focus songs, and full-body combos, just configured differently per `ClassTemplate` segment (pool filter, exercise count, timing scheme).
- **Transition-cost model**: same `equipment_position` → free; same equipment, different position → cheap; different equipment entirely → expensive. Used to keep exercise ordering smooth within a segment.
- Resolution order per exercise instance: choose equipment → resolve position/cue overrides → place in sequence.

## 5. User Interface

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

## 6. Explicitly deferred / not yet decided

- Plyo cue shape (breath-per-rep vs. setup+safety+pacing)
- Exact verb synonym-pool vocabulary
- Full `muscle_group` taxonomy list
- Exact transition-cost weights/numbers
- Equipment-availability-per-day, impact ceiling, difficulty level, and repeat-avoidance-across-classes were proposed as wizard questions but not selected for v1 — worth revisiting later if needed
