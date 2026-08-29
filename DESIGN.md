# Combocizes — Design Summary

Design spec for a Python program that builds full-body workout class scripts (combinations of dumbbell, bodyweight, and resistance band exercises) from a structured exercise dictionary.

## 1. Exercise Schema

Each exercise is a single record — not duplicated per equipment variant.

### Classification fields
- `name`
- `movement_pattern` — push / pull / hinge / squat / lunge / core / plyo
- `body_region` — upper / lower / core / full (coarse; drives warmup/cooldown/full-body filtering)
- `muscle_group` — biceps, triceps, shoulders, chest, back, quads, hamstrings, glutes, abs, etc. (fine-grained; drives the arms/legs/abs focus songs)
- `body_position` — standing_narrow / standing_wide / seated / supine / prone / kneeling / plank
- `unilateral` — bool
- `impact` — high / low

### Equipment handling (single entry, override-merged)

Rather than one entry per equipment variant (risk of drift), each exercise carries:

- `equipment_options`: list of valid equipment *combos* for this exercise, each a dict of independent per-category flags — `heavy_dumbbells`, `light_dumbbells`, `heavy_band`, `light_band`, `block` — rather than one flat string enum, e.g. `{"heavy_dumbbells": True}`, `{"heavy_dumbbells": True, "single": True}`, `{"light_band": True}`. Dumbbells and bands are split by weight/resistance tier because a student typically has **both** a heavy and a light set on hand at once (two physical sets, not a dial to turn), so availability is naturally two independent yes/no's rather than one choice between them.
- `single` is **not** a sixth equipment category — it's a modifier on whichever dumbbell tier is chosen (one dumbbell from the pair, held with both hands, goblet-style), not a separate item a student owns.
- `overrides`: dict keyed by the equipment combo, containing **only** the fields that differ for that variant (`equipment_position`, `direction`, extra refinement cues, etc.). Dicts aren't hashable, so combo keys are normalized to a sorted tuple of `(flag, value)` pairs, e.g. `(("heavy_dumbbells", True),)` or `(("heavy_dumbbells", True), ("single", True))`.

`equipment_position` is a **controlled vocabulary, namespaced per equipment type** — not free text — so the transition-cost model can compare positions by exact match:

```python
DUMBBELL_POSITIONS = ["racked", "hanging_front", "hanging_side", "overhead", "extended"]
BAND_POSITIONS = ["around_thighs", "around_ankles", "anchored_underfoot", "anchored_overhead", "in_hands"]
```

`block` has no analogous position vocabulary — it's a fixed surface a hand or foot is elevated on, not something the body holds in variable positions.

It's a **single value**, not a start/end pair — it describes where the equipment is held for the exercise, which is often static even when the exercise itself involves a lot of movement (dumbbells stay `racked` through an entire reverse lunge, since it's the leg that's doing the work, not the arms). The travel that happens *during* a rep is tracked separately by the mover fields below, not by equipment position.

If descriptive detail is needed for cue text later, add it as a separate `equipment_position_note` (free text, never used programmatically) rather than loosening the enum — don't add this field preemptively.

### Mover fields (what's actually moving)

Distinct from equipment position: the body part doing the work often isn't the one holding the equipment, and it's usually the thing that travels during the rep.

- `mover` — the body part executing the movement (e.g. `"leg"`, `"arm"`, `"torso"`, `"hip"`), independent of which equipment is selected
- `mover_position_start` / `mover_position_end` — that body part's position at the start and end of the rep (e.g. a reverse lunge: `mover: "leg"`, start `"standing"`, end `"lunge_back"`)

Example — reverse lunge with dumbbells: `equipment_position: "racked"` (unchanged throughout) alongside `mover: "leg"`, `mover_position_start: "standing"`, `mover_position_end: "lunge_back"`. The equipment doesn't travel; the leg does.

**Open question:** `mover_position` vocabulary isn't defined yet (unlike equipment positions, body-part travel states are less standardized) — deferred, see section 6.

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
  - `moved_object` (equipment-resolved noun, keyed by the same combo shape as `overrides`, e.g. `{"heavy_dumbbells": "your dumbbells", "light_dumbbells": "your dumbbells", "heavy_band": "the band", "light_band": "the band"}`, with `single` combos overriding to the singular "your dumbbell")
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
| Full-body combos | remainder (~19-24 min typical) | fills gaps | flexible | main use of movement-pattern variety logic; no transition cost applied within a song, see section 4 |
| Cooldown | ~5 min | 1 | fixed last | last 90 sec = savasana |

**Ordering rule:** don't cluster plyo bursts or focus-songs back to back — intersperse with full-body combo stretches to manage the intensity curve.

**Transition cost applies only at song/segment boundaries, not between moves within a song.** Moves inside a song/combo are assumed to flow seamlessly — the instructor's own sequencing (movement-pattern variety, natural exercise chaining) handles internal flow, not a cost function. The only place the generator scores a transition is the handoff between one segment's last exercise and the next segment's first exercise. See section 4 for what that comparison uses.

Worked time budget (60 min class, midpoint durations): warmup 6 + plyo 12 + arms 4 + legs 5 + abs 4 + cooldown 5 = 36 min fixed/ranged → **~24 min left for full-body combos**. At 50 min (low end of each range): 31 min fixed → **~19 min for full-body combos**.

## 4. Generator Architecture

- **One parameterized combo-selection function** — "select N exercises from a filtered pool, respecting movement-pattern variety, fit to a time budget" — reused for plyo bursts, focus songs, and full-body combos, just configured differently per `ClassTemplate` segment (pool filter, exercise count, timing scheme). No transition-cost weighting inside this selection — moves within a segment are assumed to flow seamlessly (see section 3).
- **Transition-cost model, applied only at segment boundaries**: compares the **last exercise of segment N** to the **first exercise of segment N+1** on two fields — `body_position` (same → free, different → cost, since e.g. standing→supine means getting down on the floor) and equipment identity (same equipment → free, different equipment → cost, since it means physically swapping gear). `equipment_position` is *not* part of this comparison — it's static per exercise and gets re-established fresh at the start of any new song regardless of what the previous song ended in.
- Resolution order per exercise instance: choose equipment → resolve position/cue overrides → place in sequence.

**Follow-on idea (not built for v1):** the segment-boundary model guarantees no full reset (no equipment swap, no floor/standing switch) but doesn't guarantee ergonomically elegant chaining *within* a song. That finer quality — e.g. hammer curl ending near the shoulders flowing straight into an overhead press starting racked — comes from `mover_position_end` of one exercise matching `mover_position_start` of the next, not from anything on the equipment side. If combo quality ever needs to be scored/optimized rather than left to curation, `mover_position` matching between consecutive exercises is the mechanism to add — deferred until `mover_position` vocabulary itself is settled (section 6).

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
- `mover_position_start`/`mover_position_end` vocabulary (which values are valid, and whether it's one shared enum or per-`mover` like equipment positions are per-equipment)
- Exact transition-cost weights/numbers
- Equipment-availability-per-day, impact ceiling, difficulty level, and repeat-avoidance-across-classes were proposed as wizard questions but not selected for v1 — worth revisiting later if needed
