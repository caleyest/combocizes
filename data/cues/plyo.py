"""Refinement cues for plyo exercises."""

from combocizes.cues import RefinementCue

PLYO_CUES = {
    "arms_reach_overhead": RefinementCue(
        text="Reach your arms overhead.",
        tags={"movement_pattern": ["plyo"], "region": "full"},
    ),
}
