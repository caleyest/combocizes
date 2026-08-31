"""Touchdown squats — MoveBank: 7) Plyo / Touchdown squats."""

from combocizes.constants import HEAVY_BAND, LIGHT_BAND, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="touchdown_squats",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=[BodyPosition("squat", "standing_narrow")],
    unilateral=False,
    impact="high",
    equipment_options=[
        dict(NO_EQUIPMENT),
        # Single dumbbell, held goblet-style with both hands and touched to
        # the floor -- centered, not alternating sides, so the squat itself
        # stays bilateral regardless of dumbbell count.
        {"light_dumbbells": True, "single": True},
        {"heavy_dumbbells": True, "single": True},
        dict(HEAVY_BAND),
        dict(LIGHT_BAND),
    ],
    mover="legs",
    location_start="squat",
    direction_start=None,
    location_end="standing",
    direction_end=None,
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="drive",
        action_pool_key="drive_up",
        direction="up to standing",
    ),
)
