"""Controlled vocabularies for exercise classification and equipment.

Plain string lists rather than `enum.Enum` — keeps validation as simple
membership checks in `combocizes.schema`.
"""

MOVEMENT_PATTERNS = ["push", "pull", "hinge", "squat", "lunge", "core", "plyo"]
BODY_REGIONS = ["upper", "lower", "core", "full"]

# Starter taxonomy — the exact values DESIGN.md names. Full list still open
# (DESIGN.md section 7); extend as new exercises need muscle groups not here.
MUSCLE_GROUPS = [
    "biceps",
    "triceps",
    "shoulders",
    "chest",
    "back",
    "lower",
    "posterior",
    "core",
    "plyo",
]

BODY_POSITIONS = [
    "standing_narrow",
    "standing_wide",
    "seated",
    "supine",
    "prone",
    "kneeling",
    "plank",
    "hinge",
    "lunge",
]
IMPACT_LEVELS = ["high", "low"]

# Equipment categories a student may have on hand. "single" is a separate
# modifier (one dumbbell held goblet-style), valid only alongside a dumbbell
# flag — not a sixth category here.
EQUIPMENT_FLAGS = ["heavy_dumbbells", "light_dumbbells", "heavy_band", "light_band", "block"]
DUMBBELL_FLAGS = ["heavy_dumbbells", "light_dumbbells"]
SINGLE_MODIFIER = "single"

# Single-flag combo keys — the same shape `combocizes.schema.equipment_combo_key`
# produces — shared so exercise files don't each recompute the same handful
# of keys. Compound combos (e.g. with the `single` modifier) are exercise-
# specific enough to build inline with `equipment_combo_key` instead.
NO_EQUIPMENT = ()
HEAVY_DUMBBELLS = (("heavy_dumbbells", True),)
LIGHT_DUMBBELLS = (("light_dumbbells", True),)
HEAVY_BAND = (("heavy_band", True),)
LIGHT_BAND = (("light_band", True),)

# The primary-cue "moved object" noun is derived, not authored: `mover` set
# to "equipment" means the equipment itself is what the cue should name
# (e.g. a curl: "curl your dumbbells up"); any other mover value (leg,
# torso, hip, ...) means the equipment stays put (e.g. dumbbells racked
# through a lunge) and the cue names that body part instead.
EQUIPMENT_PHRASES = {
    "heavy_dumbbells": "your dumbbells",
    "light_dumbbells": "your dumbbells",
    "heavy_band": "the band",
    "light_band": "the band",
}

# mover_position vocabulary (DESIGN.md section 7 — now settled). Keyed per
# mover, since different movers travel through entirely different physical
# states. "equipment" (the mover for exercises where the equipment itself
# travels, e.g. a curl) absorbs what used to be separate dumbbell/band
# position constants — there's no separate equipment_position field, so
# this is the only place "where's the equipment" is tracked. "arm"/"torso"/
# "hip" aren't exercised by any file yet — starter placeholders, adjust the
# first time a real exercise needs a value not listed here (same treatment
# as MUSCLE_GROUPS).
MOVER_POSITIONS = {
    "equipment": [
        "racked",
        "heart's center",
        "hanging_palms_in",
        "hanging_palms_front",
        "hanging_palms_back",
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
    # "legs" (plural) mirrors "leg" for bilateral leg movements (both bend
    # together, e.g. a squat) — same reasoning as "feet" vs. "leg" above.
    "legs": ["standing", "squat_bottom", "kneeling"],
    "arm": ["at_sides", "extended", "raised", "overhead", "bent"],
    "torso": ["upright", "rotated_left", "rotated_right", "flexed_forward", "extended_back"],
    "hip": ["neutral", "hinged", "extended", "raised"],
    "back": ["neutral", "arched"],
    # "feet" (plural noun, not "leg") is for movements where both legs act
    # together — "your feet" reads correctly as inherently plural, where
    # "your leg" would wrongly imply one side.
    "feet": ["together", "apart"],
}

# Provisional: DESIGN.md doesn't specify a real per-exercise duration, so a
# fixed convention stands in for now (DESIGN.md section 7).
SECONDS_PER_EXERCISE = 30

# Which way the student faces on the mat, distinct from body_positions
# (stance width/shape) -- a fast-feet drill turning to face right can't be
# expressed by body_positions alone. Exercise.mat_orientation_start/end
# both default to "front", so only exercises that actually turn (mostly
# plyo) ever need to mention this.
MAT_ORIENTATIONS = ["front", "left", "right", "back"]

# DESIGN.md section 4's segment-duration ranges, collapsed to their
# midpoints -- exactly its own "worked time budget" numbers -- so
# combocizes.class_template.build_class can generalize to any class
# length, not just the 50/60-minute cases DESIGN.md works through
# explicitly.
WARMUP_MINUTES = 6
PLYO_TOTAL_MINUTES = 12
ARMS_MINUTES = 4
LEGS_MINUTES = 5
ABS_MINUTES = 4
COOLDOWN_MINUTES = 5
FIXED_SEGMENT_MINUTES = (
    WARMUP_MINUTES
    + PLYO_TOTAL_MINUTES
    + ARMS_MINUTES
    + LEGS_MINUTES
    + ABS_MINUTES
    + COOLDOWN_MINUTES
)

# A full-body-combo stretch is sized like a typical focus song.
FULL_BODY_STRETCH_TARGET_MINUTES = 4

# DESIGN.md: "multiple exercises per burst" -- a floor above
# exercise_count_for_duration's generic "at least 1", since the burst's
# impact pattern needs at least 2 to mean anything.
MIN_PLYO_BURST_EXERCISES = 2

# muscle_group values driving each focus song (DESIGN.md: muscle_group is
# the "fine-grained" field that "drives the arms/legs/abs focus songs").
# Reflects the current MUSCLE_GROUPS taxonomy above -- update here if that
# taxonomy changes.
ARMS_MUSCLE_GROUPS = {"biceps", "triceps", "shoulders", "chest", "back"}
LEGS_MUSCLE_GROUPS = {"lower", "posterior"}
ABS_MUSCLE_GROUPS = {"core"}

# Every equipment identity a segment can be assigned, bodyweight included.
EQUIPMENT_CHOICES = [
    dict(NO_EQUIPMENT),
    dict(HEAVY_DUMBBELLS),
    dict(LIGHT_DUMBBELLS),
    dict(HEAVY_BAND),
    dict(LIGHT_BAND),
]
