"""Row, wide grip — MoveBank: 2) Pull / Row variation.

Decomposed from the base row per grip: palms facing back (overhand/
pronated grip).
"""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_DUMBBELLS
from combocizes.schema import Exercise, PrimaryCue, equipment_combo_key

_HEAVY_SINGLE = equipment_combo_key({"heavy_dumbbells": True, "single": True})
_LIGHT_SINGLE = equipment_combo_key({"light_dumbbells": True, "single": True})

EXERCISE = Exercise(
    name="row_wide",
    movement_pattern="pull",
    body_region="upper",
    muscle_group="back",
    body_positions=["hinge"],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
        {"heavy_dumbbells": True, "single": True},
        {"light_dumbbells": True, "single": True},
    ],
    mover="equipment",
    mover_position_start="extended",
    mover_position_end="hanging_palms_back",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="row",
        action_pool_key="row_back",
        direction="back to your ribs",
    ),
    overrides={
        _HEAVY_SINGLE: {"unilateral": True},
        _LIGHT_SINGLE: {"unilateral": True},
    },
)
