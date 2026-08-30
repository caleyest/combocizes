"""V/L raise — MoveBank: 1) Push / Lateral raise variation.

Decomposed from the base lateral raise per grip: palms facing in. Folds
MoveBank's separate "V" and "L" variations together (same grip, same
lateral-plane raise; V vs. L only differs by elbow bend, not modeled here).
"""

from combocizes.constants import LIGHT_DUMBBELLS
from combocizes.schema import Exercise, PrimaryCue, equipment_combo_key

_HEAVY_SINGLE = equipment_combo_key({"heavy_dumbbells": True, "single": True})
_LIGHT_SINGLE = equipment_combo_key({"light_dumbbells": True, "single": True})

EXERCISE = Exercise(
    name="v_l_raise",
    movement_pattern="push",
    body_region="upper",
    muscle_group="shoulders",
    body_positions=["seated", "kneeling", "standing_narrow", "standing_wide"],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(LIGHT_DUMBBELLS),
        {"heavy_dumbbells": True, "single": True},
        {"light_dumbbells": True, "single": True},
    ],
    mover="equipment",
    mover_position_start="hanging_palms_in",
    mover_position_end="extended",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="raise",
        action_pool_key="raise_out",
        direction="out to your sides",
    ),
    overrides={
        _LIGHT_SINGLE: {"unilateral": True},
    },
)
