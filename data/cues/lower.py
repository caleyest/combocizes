"""Refinement cues for lower-body exercises."""

from combocizes.cues import RefinementCue

LOWER_CUES = {
    "back_knee_light_tap": RefinementCue(
        text="Maybe your back knee taps the floor.",
        tags={"movement_pattern": ["lunge"], "region": "lower"},
    ),
    "fold_forward_at_top": RefinementCue(
        text="Fold forward over your legs at the top.",
        tags={"movement_pattern": ["squat"], "region": "lower"},
    ),
}
