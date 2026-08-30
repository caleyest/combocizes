"""Superman — MoveBank: 2) Pull / Superman."""

from combocizes.constants import LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import Exercise, PrimaryCue

EXERCISE = Exercise(
    name="superman",
    movement_pattern="pull",
    # body_region judgment call: erector-spinae/glute activation work reads
    # as core-adjacent for filtering purposes, despite muscle_group="back".
    body_region="core",
    muscle_group="back",
    body_positions=["plank"],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(LIGHT_DUMBBELLS),
    ],
    # mover is "back", not "arm" or "leg": both arms and both legs lift
    # together, and naming either one singular ("lift your arm") wrongly
    # implies one side. "back" isn't a paired body part, so the simplest
    # cue just names it directly.
    mover="back",
    mover_position_start="neutral",
    mover_position_end="arched",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="lift",
        action_pool_key="lift_up",
        direction="toward the sky",
    ),
)
