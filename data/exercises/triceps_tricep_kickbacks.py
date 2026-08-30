"""Tricep kickbacks — MoveBank: 1) Push / Tricep kickbacks."""

from combocizes.constants import LIGHT_BAND, LIGHT_DUMBBELLS
from combocizes.schema import BodyPosition, Exercise, PrimaryCue, equipment_combo_key

_HEAVY_SINGLE = equipment_combo_key({"heavy_dumbbells": True, "single": True})
_LIGHT_SINGLE = equipment_combo_key({"light_dumbbells": True, "single": True})

EXERCISE = Exercise(
    name="tricep_kickbacks",
    movement_pattern="push",
    body_region="upper",
    muscle_group="triceps",
    body_positions=[BodyPosition.held("kneeling"), BodyPosition.held("hinge")],
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
        action="extend",
        action_pool_key="extend_back",
        direction="back",
    ),
    overrides={
        _LIGHT_SINGLE: {"unilateral": True},
    },
)
