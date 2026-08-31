"""Squat jump — MoveBank: 7) Plyo / Jump jump squat."""

from combocizes.constants import HEAVY_BAND, LIGHT_BAND, LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="squat_jumps",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    # Dynamic, not held: the rep explodes from a squat up toward standing
    # at the jump's peak before landing back in the squat.
    body_positions=[BodyPosition("squat", "standing_narrow")],
    unilateral=False,
    impact="high",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(LIGHT_DUMBBELLS),
        dict(HEAVY_BAND),
        dict(LIGHT_BAND),
    ],
    # mover is "legs" (plural, bilateral) -- both legs drive the jump
    # together. With dumbbells, held at the chest through the jump; with a
    # band anchored underfoot, the band's own resistance is felt through
    # the same leg drive, not a separate arm action.
    mover="legs",
    location_start="squat",
    direction_start=None,
    location_end="jump",
    direction_end=None,
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="explode",
        action_pool_key="explode_up",
        direction="up",
    ),
)
