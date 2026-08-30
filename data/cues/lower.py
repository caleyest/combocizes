"""Refinement cues for lower-body exercises."""

from combocizes.cues import RefinementCue

LOWER_CUES = [
    RefinementCue(
        text="Maybe your back knee taps the floor.",
        exercise_ids=["reverse_lunge"],
    ),
    RefinementCue(
        text="Fold forward over your legs at the top.",
        exercise_ids=["squat_to_fold"],
    ),
]
