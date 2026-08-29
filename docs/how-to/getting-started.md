# Getting started

Assumes you've finished [environment setup](environment-setup.md).

## The five commands you'll actually use

```powershell
just              # list every available recipe
just check        # lint + test — run before pushing
just run <name>   # execute scripts/<name>.py
just preview <n>  # live-preview quarto/<n>.qmd while editing
just docs-serve   # serve this docs site at localhost:8000
```

## A first pass through the repo

Run the example script:

```powershell
just run run_example
```

It builds a small frame, calls `combocizes.core.summarize`, prints the result,
and writes `output/example_summary.csv`.

Render the example report:

```powershell
just render-one report
```

That produces `quarto/report.html` — a self-contained file with the code, the
table, and the figure all regenerated from source.

## Adding your own work

The repo separates three concerns, and the split is worth keeping:

1. **Logic** goes in `src/combocizes/` — importable, tested, reusable.
2. **Execution** goes in `scripts/` — thin wrappers that load inputs, call into
   the package, and write outputs.
3. **Communication** goes in `quarto/` — reports that import from the package
   and present results.

A useful loop: write the function in `src/`, cover it in `tests/`, then call it
from a script or report. When a report starts accumulating logic, move that
logic into `src/` and import it back.

## Before you push

```powershell
just check
```

CI runs the same lint, format, and test steps on Python 3.12 and 3.13, so a
green `just check` locally means a green pipeline.
