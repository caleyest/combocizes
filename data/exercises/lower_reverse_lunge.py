"""Reverse lunge — the worked example from DESIGN.md section 1."""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="reverse_lunge",
    movement_pattern="lunge",
    body_region="lower",
    muscle_group="lower",
    body_positions=[BodyPosition("standing_narrow", "lunge")],
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
    ],
    mover="leg",
    location_start="standing",
    direction_start="forward",
    location_end="lunge",
    direction_end="back",
    # mover is "leg", not "equipment": dumbbells stay racked and never
    # travel, so resolve_moved_object always resolves to "your leg" here,
    # regardless of the equipment combo chosen.
    primary_cue=PrimaryCue(
        breath="Inhale",
        action="step",
        action_pool_key="step_back",
        direction="back",
    ),
)
