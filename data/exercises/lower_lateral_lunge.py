"""Lateral lunge — MoveBank: 4) Lunge / Lateral Lunge."""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_BAND, LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="lateral_lunge",
    movement_pattern="lunge",
    body_region="lower",
    muscle_group="lower",
    # Starts from a normal narrow stance and steps out sideways into the
    # lunge -- the old single-value body_positions ("standing_wide") named
    # the exercise's wide *character*, not its actual starting stance.
    body_positions=[BodyPosition("standing_narrow", "lunge")],
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
        dict(LIGHT_BAND),
    ],
    # direction "lateral" is new — added to constants.py alongside this
    # file, since no existing leg direction covered a sideways step.
    mover="leg",
    location_start="standing",
    direction_start="forward",
    location_end="lunge",
    direction_end="lateral",
    primary_cue=PrimaryCue(
        breath="Inhale",
        action="step",
        action_pool_key="step_side",
        direction="out to the side",
    ),
)
