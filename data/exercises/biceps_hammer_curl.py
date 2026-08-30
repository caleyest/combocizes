"""Hammer curl — demonstrates the `single` modifier and a real override."""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_DUMBBELLS
from combocizes.schema import Exercise, PrimaryCue, equipment_combo_key

_HEAVY_SINGLE = equipment_combo_key({"heavy_dumbbells": True, "single": True})
_LIGHT_SINGLE = equipment_combo_key({"light_dumbbells": True, "single": True})

EXERCISE = Exercise(
    name="hammer_curl",
    movement_pattern="pull",
    body_region="upper",
    muscle_group="biceps",
    body_positions=["standing_narrow", "standing_wide", "kneeling", "lunge"],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
        {"heavy_dumbbells": True, "single": True},
        {"light_dumbbells": True, "single": True},
    ],
    # mover is "equipment": the dumbbells are what travel and what the cue
    # should name ("curl your dumbbells up"), not a body part. Neutral grip
    # (palms facing in) throughout is what makes this a "hammer" curl.
    mover="equipment",
    mover_position_start="hanging_palms_in",
    mover_position_end="shoulder",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="curl",
        action_pool_key="curl_up",
        direction="up toward your shoulders",
    ),
    # Holding a single dumbbell turns this into a one-arm-at-a-time exercise.
    overrides={
        _HEAVY_SINGLE: {"unilateral": True},
        _LIGHT_SINGLE: {"unilateral": True},
    },
    refinement_cue_ids=["elbows_pinned_ribs"],
)
