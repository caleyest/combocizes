"""Refinement cues for upper-body exercises."""

from combocizes.cues import RefinementCue

UPPER_CUES = {
    "elbows_pinned_ribs": RefinementCue(
        text="Keep your elbows pinned to your ribs.",
        tags={"movement_pattern": ["pull"], "region": "upper"},
    ),
    "elbows_rotate_out": RefinementCue(
        text="Rotate your elbows out before you press.",
        tags={"movement_pattern": ["push"], "region": "upper"},
    ),
}
