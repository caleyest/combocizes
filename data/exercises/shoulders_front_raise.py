"""Front raise — MoveBank: 1) Push / Lateral raise variation.

Decomposed from the base lateral raise per grip: palms facing back. Unlike
the V/L raise, a front raise lifts in front of the body rather than out to
the side, so direction is set to match the actual plane of motion rather
than reusing the lateral raise's cue text.
"""

from combocizes.constants import LIGHT_BAND, LIGHT_DUMBBELLS
from combocizes.schema import Exercise, PrimaryCue, equipment_combo_key

_HEAVY_SINGLE = equipment_combo_key({"heavy_dumbbells": True, "single": True})
_LIGHT_SINGLE = equipment_combo_key({"light_dumbbells": True, "single": True})

EXERCISE = Exercise(
    name="front_raise",
    movement_pattern="push",
    body_region="upper",
    muscle_group="shoulders",
    body_positions=["seated", "kneeling", "standing_narrow", "standing_wide"],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(LIGHT_DUMBBELLS),
        dict(LIGHT_BAND),
        {"heavy_dumbbells": True, "single": True},
        {"light_dumbbells": True, "single": True},
    ],
    mover="equipment",
    mover_position_start="hanging_palms_back",
    mover_position_end="extended",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="raise",
        action_pool_key="raise_forward",
        direction="in front of you",
    ),
    overrides={
        _LIGHT_SINGLE: {"unilateral": True},
    },
)
