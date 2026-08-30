"""Hammer curl — demonstrates the `single` modifier and a real override."""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_BAND, LIGHT_DUMBBELLS
from combocizes.schema import BodyPosition, Exercise, PrimaryCue, equipment_combo_key

_HEAVY_SINGLE = equipment_combo_key({"heavy_dumbbells": True, "single": True})
_LIGHT_SINGLE = equipment_combo_key({"light_dumbbells": True, "single": True})

EXERCISE = Exercise(
    name="hammer_curl",
    movement_pattern="pull",
    body_region="upper",
    muscle_group="biceps",
    body_positions=[
        BodyPosition.held("standing_narrow"),
        BodyPosition.held("standing_wide"),
        BodyPosition.held("kneeling"),
        BodyPosition.held("lunge"),
    ],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
        dict(LIGHT_BAND),
        {"heavy_dumbbells": True, "single": True},
        {"light_dumbbells": True, "single": True},
    ],
    # mover is "equipment": the dumbbells are what travel and what the cue
    # should name ("curl your dumbbells up"), not a body part. Neutral grip
    # (palms facing in) throughout is what makes this a "hammer" curl.
    mover="equipment",
    location_start="extended",
    direction_start="palms_in",
    location_end="shoulder",
    direction_end="palms_in",
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
)
