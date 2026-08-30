"""Reverse lunge — the worked example from DESIGN.md section 1."""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_DUMBBELLS, NO_EQUIPMENT
from combocizes.schema import Exercise, PrimaryCue

EXERCISE = Exercise(
    name="reverse_lunge",
    movement_pattern="lunge",
    body_region="lower",
    muscle_group="quads",
    body_position="standing_narrow",
    unilateral=True,
    impact="low",
    equipment_options=[
        dict(NO_EQUIPMENT),
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
    ],
    mover="leg",
    mover_position_start="standing",
    mover_position_end="lunge_back",
    # mover is "leg", not EQUIPMENT_MOVER: dumbbells stay racked and never
    # travel, so resolve_moved_object always resolves to "your leg" here,
    # regardless of the equipment combo chosen.
    primary_cue=PrimaryCue(
        breath="Inhale",
        action="step",
        action_pool_key="step_back",
        direction="back into a lunge",
    ),
    refinement_cue_ids=["back_knee_light_tap"],
)
