import pytest

from combocizes.schema import Exercise, PrimaryCue


@pytest.fixture
def make_exercise():
    """Factory fixture for a minimal, valid `Exercise`, one field at a time.

    Usage: `make_exercise(name="a", muscle_group="triceps")` — any field not
    passed falls back to a sensible default (a generic upper-body dumbbell
    curl), so each test only spells out the fields it actually cares about.
    """

    def _make_exercise(**overrides) -> Exercise:
        fields = {
            "name": "test_exercise",
            "movement_pattern": "pull",
            "body_region": "upper",
            "muscle_group": "biceps",
            "body_positions": ["standing_narrow"],
            "unilateral": False,
            "impact": "low",
            "equipment_options": [{}, {"heavy_dumbbells": True}],
            "mover": "arm",
            "mover_position_start": "at_sides",
            "mover_position_end": "bent",
            "primary_cue": PrimaryCue(
                breath="Exhale", action="curl", action_pool_key="curl_up", direction="up"
            ),
        }
        fields.update(overrides)
        return Exercise(**fields)

    return _make_exercise
