"""Mountain climber (fast) — MoveBank: 7) Plyo / Mountain climber (fast)."""

from combocizes.constants import NO_EQUIPMENT
from combocizes.schema import BodyPosition, Exercise, PrimaryCue

EXERCISE = Exercise(
    name="mountain_climbers",
    movement_pattern="plyo",
    body_region="full",
    muscle_group="plyo",
    body_positions=[BodyPosition.held("plank")],
    unilateral=True,
    impact="high",
    equipment_options=[
        dict(NO_EQUIPMENT),
    ],
    # mover is "knee", not "leg" or "legs": the driving knee travels toward
    # the opposite elbow while the torso holds a plank -- neither the
    # standing-based "leg" vocabulary nor a torso-stability framing (cf.
    # bird_dog) fits a rep whose whole point is the knee's own travel.
    mover="knee",
    location_start="plank",
    direction_start="right",
    location_end="toward_elbow",
    direction_end="left",
    primary_cue=PrimaryCue(
        breath="Exhale",
        action="drive",
        action_pool_key="drive_knee_in",
        direction="toward your elbow",
    ),
)
