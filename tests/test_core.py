import polars as pl
import pytest

from combocizes.core import summarize


@pytest.fixture
def frame() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "group": ["a", "a", "b"],
            "value": [1.0, 3.0, 10.0],
        }
    )


def test_summarize_aggregates_per_group(frame: pl.DataFrame) -> None:
    result = summarize(frame, group_by="group", value="value").to_dicts()

    assert result == [
        {"group": "a", "n": 2, "mean": 2.0, "total": 4.0},
        {"group": "b", "n": 1, "mean": 10.0, "total": 10.0},
    ]


def test_summarize_raises_on_missing_column(frame: pl.DataFrame) -> None:
    with pytest.raises(KeyError, match="nope"):
        summarize(frame, group_by="group", value="nope")
