"""Example script. Run with: just run run_example

Scripts are thin — they load inputs, call into `combocizes`, and write outputs.
Keep reusable logic in `src/combocizes/`, not here.
"""

import polars as pl

from combocizes.core import summarize
from combocizes.utils import OUTPUT_DIR, ensure_dir, get_logger

log = get_logger(__name__)


def main() -> None:
    frame = pl.DataFrame(
        {
            "group": ["a", "a", "b", "b", "c"],
            "value": [1.0, 3.0, 10.0, 12.0, 7.0],
        }
    )

    result = summarize(frame, group_by="group", value="value")
    log.info("summarized %d rows into %d groups", frame.height, result.height)
    print(result)

    out = ensure_dir(OUTPUT_DIR) / "example_summary.csv"
    result.write_csv(out)
    log.info("wrote %s", out)


if __name__ == "__main__":
    main()
