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
    # mover_position "lunge_lateral" is new — added to constants.py alongside
    # this file, since no existing leg position covered a sideways step.
    mover="leg",
    mover_position_start="standing",
    mover_position_end="lunge_lateral",
    primary_cue=PrimaryCue(
        breath="Inhale",
        action="step",
        action_pool_key="step_side",
        direction="out to the side",
    ),
)
