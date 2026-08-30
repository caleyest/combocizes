"""Row, narrow grip — MoveBank: 2) Pull / Row variation.

Decomposed from the base row per grip: palms facing in (neutral/hammer
grip). Renegade row (still deferred) is typically done with this same
neutral grip, in a plank position.
"""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_BAND, LIGHT_DUMBBELLS
from combocizes.schema import Exercise, PrimaryCue, equipment_combo_key

_HEAVY_SINGLE = equipment_combo_key({"heavy_dumbbells": True, "single": True})
_LIGHT_SINGLE = equipment_combo_key({"light_dumbbells": True, "single": True})

EXERCISE = Exercise(
    name="row_narrow",
    movement_pattern="pull",
    body_region="upper",
    muscle_group="back",
    body_positions=["plank", "hinge"],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
        dict(LIGHT_BAND),
        {"heavy_dumbbells": True, "single": True},
        {"light_dumbbells": True, "single": True},
    ],
    mover="equipment",
    mover_position_start="extended",
    mover_position_end="hanging_palms_in",
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
