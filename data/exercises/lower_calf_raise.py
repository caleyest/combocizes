"""Calf raise — MoveBank: 1) Push / Calf raise."""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_BAND, LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="calf_raise",
    movement_pattern="push",
    body_region="lower",
    muscle_group="lower",
    body_positions=[BodyPosition.held("standing_narrow"), BodyPosition.held("standing_wide")],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
        dict(LIGHT_BAND),
    ],
    # mover is "legs" (plural, bilateral heel rise) — a heel rise isn't a
    # stance-width change like jumping_jacks' "feet", so it's namespaced
    # under "legs" instead, with "up"/"down" as its direction axis.
    mover="legs",
    location_start="standing",
    direction_start="down",
    location_end="calf_raise",
    direction_end="up",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="rise",
        action_pool_key="rise_up",
        direction="up onto your toes",
    ),
)
