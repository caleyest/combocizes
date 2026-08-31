"""High knees — MoveBank: 7) Plyo / High knees."""

from combocizes.constants import LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="high_knees",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=[BodyPosition("standing_narrow", "standing_narrow")],
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(LIGHT_DUMBBELLS),
    ],
    # mover is "leg" (singular) -- reuses the existing standing/raised_bent
    # vocabulary directly, unlike its "legs" (plural) siblings in this
    # batch. No direction stated: "leg"'s vocabulary has no left/right
    # axis (only forward/back/lateral/kickstand), unlike "legs"/"arm".
    mover="leg",
    location_start="standing",
    direction_start=None,
    location_end="raised_bent",
    direction_end=None,
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="drive",
        action_pool_key="drive_knee_up",
        direction="up",
    ),
)
