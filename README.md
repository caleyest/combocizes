# combocizes

[![CI](https://github.com/caleyest/combocizes/actions/workflows/ci.yml/badge.svg)](https://github.com/caleyest/combocizes/actions/workflows/ci.yml)
[![Docs](https://github.com/caleyest/combocizes/actions/workflows/docs.yml/badge.svg)](https://caleyest.github.io/combocizes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Combocizes builds full-body workout class scripts — combinations of dumbbell,
bodyweight, and resistance band exercises — from a structured exercise
dictionary. It's for instructors and coaches who plan class sequences and want
generated, varied combos instead of writing them by hand.

📖 **[Documentation](https://caleyest.github.io/combocizes/)** · 📊 **[Reports](https://caleyest.github.io/combocizes/quarto/report.html)**

## Quick start

Install [Git](https://git-scm.com), [uv](https://docs.astral.sh/uv/),
[just](https://just.systems), and [Quarto](https://quarto.org) — on Windows:

```powershell
winget install Git.Git astral-sh.uv Casey.Just Posit.Quarto
```

Then clone and set up:

```powershell
git clone https://github.com/caleyest/combocizes.git
cd combocizes
uv sync
just install-hooks
```

Verify everything works:

```powershell
just check
```

## Usage

```powershell
just                    # list every recipe
just run run_example    # run scripts/run_example.py
just preview report     # live-preview quarto/report.qmd
just docs-serve         # serve the docs site at localhost:8000
just check              # lint + test, same as CI
```

```python
import polars as pl
from combocizes.core import summarize

frame = pl.DataFrame({"group": ["a", "a", "b"], "value": [1.0, 3.0, 10.0]})
summarize(frame, group_by="group", value="value")
```

## Layout

| Path              | Contains                                          |
| ----------------- | ------------------------------------------------- |
| `src/combocizes/` | The package — all reusable, tested logic           |
| `scripts/`        | Thin runnable entry points                         |
| `quarto/`         | `.qmd` reports (markdown + executable Python)      |
| `docs/`           | MkDocs prose documentation                         |
| `tests/`          | pytest suite, mirroring `src/`                     |
| `data/`           | Input data                                         |

Full description: [Project structure](https://caleyest.github.io/combocizes/reference/project-structure/).

## Publishing

Pushing to `main` renders every Quarto report and builds the docs site, then
deploys both to GitHub Pages:

- Docs — `https://caleyest.github.io/combocizes/`
- Reports — `https://caleyest.github.io/combocizes/quarto/<name>.html`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
