"""Refinement cues for upper-body exercises."""

from combocizes.cues import RefinementCue

UPPER_CUES = [
    RefinementCue(
        text="Keep your elbows pinned to your ribs.",
        exercise_ids=["hammer_curl"],
    ),
    RefinementCue(
        text="Rotate your elbows out before you press.",
        exercise_ids=["cuban_press"],
    ),
]
