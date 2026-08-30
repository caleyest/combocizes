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
    "quads",
    "hamstrings",
    "glutes",
    "abs",
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
        "squat_bottom",
        "kneeling",
        "raised_bent",
        "raised_straight",
    ],
    "arm": ["at_sides", "extended", "raised", "overhead", "bent"],
    "torso": ["upright", "rotated_left", "rotated_right", "flexed_forward", "extended_back"],
    "hip": ["neutral", "hinged", "extended", "raised"],
}

# Provisional: DESIGN.md doesn't specify a real per-exercise duration, so a
# fixed convention stands in for now (DESIGN.md section 7).
SECONDS_PER_EXERCISE = 30
