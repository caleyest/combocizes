"""Run in place — MoveBank: 7) Plyo / Run in place."""

from combocizes.constants import HEAVY_BAND, LIGHT_BAND, LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="run_in_place",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    # Dynamic, not held: an alternating single-leg jog, even though both
    # ends share the "standing_narrow" label.
    body_positions=[BodyPosition("standing_narrow", "standing_narrow")],
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(LIGHT_DUMBBELLS),
        dict(HEAVY_BAND),
        dict(LIGHT_BAND),
    ],
    mover="legs",
    location_start="standing",
    direction_start="right",
    location_end="standing",
    direction_end="left",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="run",
        action_pool_key="run_in_place",
        direction="in place",
    ),
)
