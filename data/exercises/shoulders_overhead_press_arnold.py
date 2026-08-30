"""Arnold press — MoveBank: 1) Push / Overhead press variation.

Decomposed from the base overhead press per grip: palms facing back.
The classic Arnold press rotates the grip through the press (palms back
at the bottom, front at the top) — now modeled directly via
direction_start/direction_end.

No band option: the rotating grip doesn't work with a band's fixed
handle, so this drops light_band from the base press's equipment set.
"""

from combocizes.constants import HEAVY_DUMBBELLS, LIGHT_DUMBBELLS
from combocizes.schema import BodyPosition, Exercise, PrimaryCue, equipment_combo_key

_HEAVY_SINGLE = equipment_combo_key({"heavy_dumbbells": True, "single": True})
_LIGHT_SINGLE = equipment_combo_key({"light_dumbbells": True, "single": True})

EXERCISE = Exercise(
    name="overhead_press_arnold",
    movement_pattern="push",
    body_region="upper",
    muscle_group="shoulders",
    body_positions=[
        BodyPosition.held("seated"),
        BodyPosition.held("kneeling"),
        BodyPosition.held("standing_narrow"),
        BodyPosition.held("standing_wide"),
    ],
    unilateral=False,
    impact="low",
    equipment_options=[
        dict(HEAVY_DUMBBELLS),
        dict(LIGHT_DUMBBELLS),
        {"heavy_dumbbells": True, "single": True},
        {"light_dumbbells": True, "single": True},
    ],
    mover="equipment",
    location_start="shoulder",
    direction_start="palms_back",
    location_end="overhead",
    direction_end="palms_front",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="press",
        action_pool_key="press_overhead",
        direction="overhead",
    ),
    overrides={
        _HEAVY_SINGLE: {"unilateral": True},
        _LIGHT_SINGLE: {"unilateral": True},
    },
)
