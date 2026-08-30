# Combocizes — Design Summary

Design spec for a Python program that builds full-body workout class scripts (combinations of dumbbell, bodyweight, and resistance band exercises) from a structured exercise dictionary.

## 1. Exercise Schema

Each exercise is a single record — not duplicated per equipment variant.

### Classification fields
- `name`
- `movement_pattern` — push / pull / hinge / squat / lunge / core / plyo
- `body_region` — upper / lower / core / full (coarse; drives warmup/cooldown/full-body filtering)
- `muscle_group` — biceps, triceps, shoulders, chest, back, quads, hamstrings, glutes, abs, etc. (fine-grained; drives the arms/legs/abs focus songs)
- `body_positions` — a list of `BodyPosition(start, end)` pairs, each drawn from: standing_narrow / standing_wide / seated / supine / prone / kneeling / plank / hinge / lunge / squat. A list, not a single pair, since some exercises validly work from several alternative stances (e.g. a hammer curl done standing_narrow, standing_wide, kneeling, or from a lunge) — purely additive, unlike equipment, since cue text doesn't change based on stance. Each pair itself captures whether the whole-body stance changes over the course of the rep, the same start/end shape as the mover fields below but at the whole-body level instead of the moving limb's: most exercises hold one stance throughout (`BodyPosition.held(position)` is shorthand for `start == end`), but a handful genuinely transition — a reverse lunge is `BodyPosition("standing_narrow", "lunge")`, a good morning is `BodyPosition("standing_narrow", "hinge")`. `combocizes.constants.BODY_POSITION_TIERS` groups the vocabulary by transition cost from standing, and `select_combo`'s chaining and guardrails (section 5) key off both the pair's exact values and its tier.
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
        "lunge_lateral",
        "squat_bottom",
        "kneeling",
        "raised_bent",
        "raised_straight",
        "straddle",
    ],
    "legs": ["standing", "squat_bottom", "kneeling"],
    "arm": ["at_sides", "extended", "raised", "overhead", "bent"],
    "torso": ["upright", "rotated_left", "rotated_right", "flexed_forward", "extended_back"],
    "hip": ["neutral", "hinged", "extended", "raised"],
    "back": ["neutral", "arched"],
    "feet": ["together", "apart"],
}
```

`"arm"`/`"hip"` aren't used by any exercise yet — starter placeholders, adjust the first time a real exercise needs a value not listed.

`"back"`, `"legs"`, and `"feet"` exist alongside `"leg"`/`"arm"`/`"torso"`/`"hip"` for a specific reason: `mover` is read straight into the cue as `"your {mover}"`, so it has to be a noun that's correct in that singular-possessive form. That's fine for a genuinely unilateral movement (`"leg"` in a reverse lunge — one leg moves), but wrong for a movement where both sides of a paired limb act together — `"lift your arm off the mat"` when both arms lift reads as one arm. `"back"` and `"torso"` sidestep this because they're unpaired; `"legs"` and `"feet"` sidestep it because they're already plural (`"legs"` for a bend/descend, like a squat; `"feet"` for a stance-width change, like a jumping jack). Prefer one of those (extending `MOVER_POSITIONS` with a new key if none fits) over forcing a paired-limb term to cover a bilateral movement.

**When more than one mover is physically plausible, break the tie with `movement_pattern`, not by which reads most distinctively.** A squat (`movement_pattern: "squat"`) should use a leg-family mover even though "the fold" is what makes `squat_to_fold` distinct from a plain squat — the fold becomes a refinement cue, the squat descent stays the primary cue. A `"core"` exercise like `bird_dog` has no limb of its own in `movement_pattern` terms; its job is torso stability, not a limb reach, and picking arm-vs-leg as the mover would be an arbitrary tie-break between two limbs that move simultaneously and symmetrically — so `mover="torso"` (held, `mover_position_start == mover_position_end`) with both limbs named in a refinement cue instead.

Example — reverse lunge with dumbbells: `mover: "leg"`, `mover_position_start: "standing"`, `mover_position_end: "lunge_back"`. The dumbbells stay racked and never travel; the leg does — so nothing about the equipment is tracked here at all for this exercise.

- `mat_orientation_start` / `mat_orientation_end` — which way the student faces on the mat (`"front"` / `"left"` / `"right"` / `"back"`) at the start and end of the rep. Distinct from `mover_position` and `body_positions`: neither can express a turn (a fast-feet drill pivoting to face right isn't a stance-width change or a limb-travel state, it's a change of facing direction). Both default to `"front"`, so only exercises that actually turn — mostly plyo — ever need to set them; the plyo-burst selector chains on them the same way `select_combo` chains on `mover_position`.

**Next step, not built yet:** for an exercise where equipment is held but isn't the mover (like the reverse lunge above), what to do with it — "keep your dumbbells racked at your sides" — is a candidate for a common, shared refinement cue (authored once in the cue bank, pointed at the relevant exercises via the cue's own `exercise_ids`) rather than a structured schema field.

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
  - `action_pool_key` (points into a shared synonym pool for randomized verb variety, e.g. `curl_up: ["drive", "curl", "pull", "draw"]`) — authored on every exercise already, but inert until the pool itself exists; see section 7. Until then, rendering just prints `action` literally.
  - `direction` (fixed, exercise-specific free text — usually doesn't vary by equipment)

  The equipment-resolved object noun (`moved_object`) isn't authored as a
  field — it's derived from `mover` and the chosen equipment (see the Mover
  fields section above): `"your dumbbells"` (or `"your dumbbell"` for the
  single-dumbbell combo) when `mover` is `"equipment"`, otherwise `"your
  {mover}"`.

  Assembled at render time into: `"{breath}, {exercise_name}, {action} {moved_object} {direction}."`
  Said once, on first appearance of the exercise in the class.

  **Keep `direction` to one minimal "where," not a second clause.** E.g.
  `direction="forward"`, not `direction="back into a squat, then fold
  forward at your hips"`. A second phase, a coordination note ("reach your
  opposite arm forward"), or a setup detail ("rotate your elbows out
  first") belongs in a refinement cue instead — it rotates across repeat
  appearances there, where it would just repeat verbatim stuck in the
  primary cue.

- `own_refinement_cues`: exercise-specific cues too particular to generalize into the shared bank. Shared cues aren't referenced from the exercise side at all — see below.

## 2. Refinement Cue Bank (shared, flat list)

A separate list, not embedded per-exercise:

```python
CUE_BANK = [
  RefinementCue(
      text="Keep your elbows pinned to your ribs.",
      exercise_ids=["hammer_curl"],
  ),
  ...
]
```

- Cues declare which exercises they apply to explicitly, via `exercise_ids` — no cue ID, no tags, no auto-matching by category at runtime, to avoid a cue silently surfacing in a contextually wrong spot. This is the only place the exercise/cue relationship is authored; `Exercise` carries no reference back to the cue bank, so there's a single copy of the link instead of two that could drift apart.
- The cue bank isn't a module-level constant: `combocizes.cues.build_cue_bank()` is called from `combocizes.loader.load_exercises`, once the exercise pool exists, since a cue's `exercise_ids` can't be checked against real exercise names any earlier.
- Editing bank text once propagates everywhere it's referenced — solves the same duplication/drift problem the equipment-override pattern solves.
- Refinement cues rotate across repeat appearances of an exercise within a class, so the script doesn't repeat verbatim.

**Open question:** plyo/continuous-tempo exercises may need a different cue shape than breath-per-rep (setup cue + safety/landing cue + pacing cue, no per-rep breath). Not yet resolved.

## 3. Data Layout

### Format: Python, not YAML/JSON

Each exercise and cue is authored directly as a Python object (dataclass instance), not YAML/JSON. Since equipment combos are per-category boolean flags, a Python data file can reference the same constants used elsewhere — `MOVER_POSITIONS`, the `movement_pattern` enum — instead of duplicating them as bare strings that can silently drift out of sync with the enum. A `@dataclass` with `__post_init__` validation (asserting equipment flags are drawn from the known set, `movement_pattern` is a valid value, etc.) catches authoring typos at import time rather than only when the generator runs, without needing a separate schema-validation library (pydantic/jsonschema) for something the project already has enum/constant machinery for; a cue's `exercise_ids` is the one thing that can't be validated this way, since it's checked against the exercise pool in `load_exercises` instead (see section 2). Trade-off: less safe to hand-edit blind than YAML, since loading a file executes code — acceptable here since this is a single-maintainer Python project, not a format meant for non-programmers to edit.

### Exercises: one file per exercise

`exercises/` is a flat directory, one file per exercise, named `{muscle_group}_{name}.py` (e.g. `biceps_hammer_curl.py`, `lower_reverse_lunge.py`). The filename prefix gives fast visual grouping by muscle group in any directory listing/sort, without creating a folder hierarchy that has to be physically reorganized if an exercise is ever reclassified — renaming a file is a one-line diff, moving it between nested folders isn't. A loader function globs the directory, imports each file's exercise object, and combines them into the pool the generator selects from; this parsing step is cheap and runs once at startup, not per-generation.

Nested folders by `movement_pattern` were considered (only 7 stable values, less prone to reclassification than `muscle_group`) but rejected in favor of the filename convention, since `muscle_group` is the axis actually used for browsing/editing exercises, not `movement_pattern`.

### Cues: category files, not one-per-cue

Refinement cues stay grouped, not split one-per-file — each cue is only 2-3 lines, so hundreds of near-empty files would be harder to browse than the single large list this split is meant to avoid. Instead, the cue bank is split across a handful of category files (`cues/upper.py`, `cues/lower.py`, `cues/core.py`, `cues/plyo.py`), each exposing a local `list[RefinementCue]`; `build_cue_bank` merges them into one flat list when called — the same "split for readability, combine cheaply at load" pattern as exercises, just at a coarser grain.

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

**Ordering rules:** no two plyo bursts ever adjacent, and the segment immediately before cooldown is never a plyo burst — both to manage the intensity curve. Everything else (focus songs, full-body-combo stretches, and plyo next to any of those) may appear in any order, including back to back — e.g. two full-body-combo songs in a row is deliberately fine, since it lets a unilateral move hit right side in one and left side in the next.

**Equipment rules:**
- Warmup and cooldown always use **no equipment** (bodyweight only).
- Every other segment (plyo, arms, legs, abs, full-body combos) is equipment-eligible. Across the whole class, heavy dumbbells, light dumbbells, and band (either weight — it's one identity for this rule) must each be used by **at least one** segment, guaranteed by construction when equipment is assigned, not checked-and-retried afterward.

Segment-to-segment transitions (equipment swaps, floor/standing changes) are an expected, known part of moving between songs — not something the generator scores or optimizes against.

Worked time budget (60 min class, midpoint durations): warmup 6 + plyo 12 + arms 4 + legs 5 + abs 4 + cooldown 5 = 36 min fixed/ranged → **~24 min left for full-body combos**. At 50 min (low end of each range): 31 min fixed → **~19 min for full-body combos**. Generalizing to any class length: each fixed-ish segment keeps its own midpoint duration regardless of total length, and full-body-combo time is always whatever's left over — split into stretches sized like a typical focus song (~4 min each) rather than one single block, so there's something to intersperse plyo bursts between.

## 5. Generator Architecture

- **One parameterized combo-selection function** (`select_combo`) — "select N exercises from a filtered pool, chained by mover position and varied by movement pattern, fit to a time budget" — reused for focus songs and full-body combos, configured differently per segment (pool filter, exercise count, equipment).
- **Stance-transition guardrail**, applied before the preference ordering below: `body_positions` values are grouped into three tiers by transition cost from standing — 1) upright (`standing_narrow`, `standing_wide`, `hinge`, `lunge`, `squat`), 2) bridge (`kneeling`, `seated`), 3) floor (`plank`, `supine`, `prone`). A pick's assumed stance may not transition directly between tier 1 and tier 3 — going straight from upright to the floor skips the low-cost stepping-stone the bridge tier provides. Tier 1 ↔ tier 2 and tier 2 ↔ tier 3 are both unrestricted — once already grounded (or already at the bridge), moving further is a low-cost shift by comparison. The restriction is symmetric (applies whichever direction the transition runs) and scoped to one song (intra-`select_combo` picks only), consistent with the rule below that segment-to-segment transitions aren't optimized against. `plank`/`supine`/`prone` sharing tier 3 doesn't mean they're free to swap between — no separate mechanism for that, since the exact-match preference below already deprioritizes any stance change, tier-crossing or not. Enforcement today: a hard filter within each pick's candidate set, but with no fallback if it empties that set — the pick falls through to the full remaining pool and the guardrail is silently violated for that one pick, same as the exact-match preference's own fallback below. Revisit if that's too permissive: either force a bridge-stance pick into the sequence when needed, or backtrack and reselect earlier picks so a valid combo is found instead of ever accepting a banned jump (real work, not yet designed).
- **Same-tier preference**, a second guardrail-adjacent step, applied after the hard filter above and before the preference ordering below: crossing into (or out of) the bridge tier is *legal* per the guardrail, but it isn't free, so a candidate that can stay in the previous pick's own tier is preferred over one that can only continue via a different (still-legal) tier. This is coarser than the exact-match preference below — it only checks tier, not the specific stance value — so it narrows the candidate set a step before exact match gets a turn.
- **Plane-transition guardrail**, a third axis alongside the tier guardrails above: `standing_narrow` and `standing_wide` are not interchangeable by default, even though both sit in tier 1 — a stance-width change is its own real cost, separate from height. There's no hand-picked exception list for this; the rule is structural, since chaining matches on the specific `body_positions` pair's `.start`/`.end` value (see section 1's `BodyPosition` field) rather than a coarser tier or a single unordered `body_positions` list — any exercise whose own declared pair already spans narrow and wide absorbs the plane change as part of its normal chaining, the same way a tier-spanning exercise would. Example: a reverse lunge (`BodyPosition("standing_narrow", "lunge")`) chains directly into a sumo-squat variant whose own pair starts `"lunge"` and ends `"standing_wide"` — the plane change happens inside that second exercise's own rep, not as an illegal jump between two static-stance picks. A plain sumo squat (`BodyPosition.held("standing_wide")`, no transition) can't take that same role. Symmetric, same scope as the tier guardrails (intra-song only).
- Each pick after the first is narrowed by the guardrails above, then by preference, in order. First, a candidate with a `body_positions` pair whose `.start` exactly matches the previous pick's recorded `.end` — same specific stance, no transition needed — since a stance change (e.g. standing to supine) costs real time and disrupts flow more than a mover-position mismatch does. Among those (or whatever the guardrail/tier steps left if none match exactly), a candidate whose `mover_position_start` matches the previous pick's `mover_position_end` — in-song chaining (e.g. a curl ending near the shoulders flowing straight into an overhead press starting racked). Among whichever candidates that leaves, the exercise whose `movement_pattern` has been used least so far in the selection is preferred; further ties break randomly. Since an exercise can list more than one valid `BodyPosition` pair, the specific one actually assumed for each pick — mirroring the same guardrail/same-tier/exact-match ordering, applied to the winning candidate's own pairs — is recorded on the result (`ComboSelection.body_positions`), rather than left for callers to re-derive.
- **Plyo bursts get their own selection function** (`select_plyo_burst`), not `select_combo` — every plyo-pool candidate already shares `movement_pattern: "plyo"`, so movement-pattern variety wouldn't discriminate among them, and impact needs a repeating pattern rather than free variety. It follows a **2:1 or 3:1 high:low impact pattern** (e.g. high, high, low, high, high, low, ...; ratio chosen per burst), and within whichever impact a slot needs, prefers a candidate whose `mat_orientation_start` matches the previous pick's `mat_orientation_end` — the same end-matches-next-start mechanism as `mover_position` chaining, but for which way the student faces on the mat (see `mat_orientation_start`/`mat_orientation_end` in section 1's mover fields — a fast-feet drill turning to face right is the case this exists for).
- Resolution order per exercise instance: choose equipment → resolve position/cue overrides → place in sequence.
- **Class assembly** (`build_class`) sits above both selection functions: it decides segment count/duration (section 4's formula), picks a plyo-burst count (3 or 4), orders the middle segments (plyo bursts inserted into random non-adjacent, non-final gaps among the shuffled focus-song/full-body-combo segments — satisfying both ordering rules in section 4 by construction), and assigns each segment's equipment (guaranteeing the coverage rule in section 4, also by construction, before randomizing the rest). Every non-plyo segment's own selection is computed before final ordering is decided (segments don't chain into each other, so this is safe) — this is what lets the segment immediately before cooldown be chosen, when the pool allows it, from among the non-plyo segments whose selection actually ends in a `LOW_BODY_POSITIONS` stance (section 1), rather than picked blind.

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
- Exact verb synonym-pool vocabulary — the pool `action_pool_key` (section 1) is meant to index into; no such pool, and no code that reads the key, exists yet
- Full `muscle_group` taxonomy list
- Equipment-availability-per-day, impact ceiling, difficulty level, and repeat-avoidance-across-classes were proposed as wizard questions but not selected for v1 — worth revisiting later if needed
- A common/shared refinement cue for equipment that's held but not the mover (e.g. "keep your dumbbells racked at your sides") — see section 1
- Author dedicated warmup and cooldown movements. Both segments currently
  draw from the same `body_region == "full"` pool as full-body combos;
  warmup wants gentler ramp-up moves and cooldown wants static
  stretches/holds, which the general full-body pool isn't guaranteed to
  contain.
- Consider whether refinement cues can be generalized beyond per-exercise
  `exercise_ids` — e.g. cues keyed by a shared trait (a `body_positions`
  value, a `movement_pattern`, "equipment held but not the mover") that
  would apply across many exercises at once, instead of every cue having
  to list out each exercise it applies to individually.
- ~~Body-position-transition model~~ — done: `body_positions` is now a list
  of `BodyPosition(start, end)` pairs (section 1), and `select_combo`
  chaining prefers an exact stance-end == stance-start match the same way
  it already prefers `mover_position_end == mover_position_start`, with the
  tier/plane guardrails (section 5) governing what happens when that match
  fails. Also resolved the pre-cooldown-segment ordering item this
  unblocked: `build_class` now places, when the pool allows it, a
  low-ending segment (`LOW_BODY_POSITIONS`, section 1) immediately before
  cooldown (section 5).
- **Bidirectional stance-transition pairs, and a distinct "fold" position**
  — open question surfaced while migrating `squat_to_fold` to the new
  start/end pair model above: should a rep-cycling exercise (one that
  returns to its starting stance every rep, e.g. `squat_to_fold`,
  `reverse_lunge`, `lateral_lunge`, `good_morning`) list *both* directions
  as separate valid pairs (`standing_narrow -> squat` and `squat ->
  standing_narrow`), so chaining can key off whichever end fits the
  surrounding picks — or does that double-count and just needs the one
  canonical direction? Also worth reconsidering whether `squat_to_fold`'s
  end state should be its own dedicated body position (a "fold," distinct
  from a plain `squat` bottom) rather than reusing `"squat"`, given the
  exercise is explicitly about the forward fold and not just the descent.
  Not resolved yet — revisit before leaning on either shape.
