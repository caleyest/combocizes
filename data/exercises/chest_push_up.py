"""Push-up — MoveBank: 1) Push / Push-up.

Variations text ("wide, tricep, diamond, hand release, knees") deferred —
not yet decomposed into separate files/overrides.
"""

from combocizes.constants import LIGHT_BAND, NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="push_up",
    movement_pattern="push",
    body_region="upper",
    muscle_group="chest",
    body_positions=[BodyPosition.held("plank")],
    unilateral=False,
    impact="low",
    equipment_options=[dict(NO_EQUIPMENT), dict(LIGHT_BAND)],
    # mover is "arms" (plural, bodyweight bilateral press) — both arms
    # press together, so singular "arm" would wrongly imply one side.
    mover="arms",
    mover_position_start="bent",
    mover_position_end="extended",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="press",
        action_pool_key="press_up",
        direction="up",
    ),
)
