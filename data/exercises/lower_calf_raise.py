"""Calf raise — MoveBank: 1) Push / Calf raise."""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_BAND, LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import Exercise, PrimaryCue

EXERCISE = Exercise(
    name="calf_raise",
    movement_pattern="push",
    body_region="lower",
    muscle_group="lower",
    body_positions=["standing_narrow", "standing_wide"],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
        dict(LIGHT_BAND),
    ],
    # mover is "feet" (plural, bilateral heel rise), reusing the same key
    # as jumping_jacks but a different axis (heel height, not stance
    # width) — "heels_down"/"heels_up" added to its vocabulary for this.
    mover="feet",
    mover_position_start="heels_down",
    mover_position_end="heels_up",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="rise",
        action_pool_key="rise_up",
        direction="up onto your toes",
    ),
)
