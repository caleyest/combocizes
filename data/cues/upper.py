"""Refinement cues for upper-body exercises."""

from combocizes.cues import RefinementCue

UPPER_CUES = [
    RefinementCue(
        text="Keep your elbows pinned to your ribs.",
        exercise_ids=["hammer_curl", "bicep_curl"],
    ),
    RefinementCue(
        text="Rotate your elbows out before you press.",
        exercise_ids=["cuban_press"],
    ),
    RefinementCue(
        text="Option to drop to your knees.",
        exercise_ids=["push_up"],
    ),
    RefinementCue(
        text="Option to add an oblique crunch.",
        exercise_ids=["overhead_press_narrow", "overhead_press_wide", "overhead_press_arnold"],
    ),
]
