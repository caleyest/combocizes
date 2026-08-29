"""Core logic.

Placeholder module — replace `summarize` with the project's real entry points.
It exists so the package imports, the test suite runs, and CI is green from
the first commit.
"""

import polars as pl


def summarize(frame: pl.DataFrame, group_by: str, value: str) -> pl.DataFrame:
    """Aggregate `value` by `group_by`, returning count, mean, and sum.

    Args:
        frame: Input data.
        group_by: Column to group on.
        value: Numeric column to aggregate.

    Returns:
        One row per distinct `group_by` value, sorted by that column.

    Raises:
        KeyError: If either column is missing from `frame`.
    """
    missing = [c for c in (group_by, value) if c not in frame.columns]
    if missing:
        raise KeyError(f"column(s) not found in frame: {missing}")

    return (
        frame.group_by(group_by)
        .agg(
            pl.len().alias("n"),
            pl.col(value).mean().alias("mean"),
            pl.col(value).sum().alias("total"),
        )
        .sort(group_by)
    )
