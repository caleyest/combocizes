# Running scripts

Scripts in `scripts/` are entry points for analyses you want to run repeatedly.

## Run one

```powershell
just run run_example
```

The recipe expands to `uv run python scripts/run_example.py`. `uv run` resolves
the environment first, so you never need to activate `.venv` by hand.

To pass arguments, call it directly:

```powershell
uv run python scripts/run_example.py --start 2020-01-01
```

## Writing a new script

Keep scripts thin. They orchestrate; they don't hold logic:

```python
"""What this script produces, and why."""

from combocizes.core import summarize
from combocizes.utils import OUTPUT_DIR, ensure_dir, get_logger

log = get_logger(__name__)


def main() -> None: ...


if __name__ == "__main__":
    main()
```

Conventions worth following:

- **`main()` plus the `__main__` guard.** Makes the script importable from a
  test or a notebook without executing it.
- **Log, don't `print`, for progress.** `get_logger` gives you timestamps and
  levels; reserve `print` for results a human is meant to read.
- **Resolve paths through `combocizes.utils`.** `PROJECT_ROOT`, `DATA_DIR`, and
  `OUTPUT_DIR` are absolute, so a script behaves the same regardless of the
  directory you invoke it from. Never hardcode a relative path.
- **Write outputs to `output/`.** It's gitignored — commit results only when you
  deliberately want them versioned.

## Command-line arguments

Use `argparse` from the standard library:

```python
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--start", required=True, help="ISO start date")
args = parser.parse_args()
```

## Secrets

Anything in `.env` is available via `python-dotenv`:

```python
import os

from dotenv import load_dotenv

load_dotenv()
api_key = os.environ["SOME_API_KEY"]
```

Document each new variable in `.env.example` — with an empty value — so others
know what to set.
