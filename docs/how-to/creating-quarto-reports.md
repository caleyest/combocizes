# Creating Quarto reports

A `.qmd` file is markdown with executable Python chunks. Rendering runs the code
and embeds its output, so a report can never drift from the code that produced
it. Start by copying [`quarto/report.qmd`](https://github.com/caleyest/combocizes/blob/main/quarto/report.qmd).

## Write

Every report opens with a YAML header:

````markdown
---
title: "My Analysis"
author: "caleyest"
date: today
format:
  html:
    toc: true
    code-fold: true
---
````

Then alternate prose and chunks:

````markdown
## Results

```{python}
from combocizes.core import summarize
result = summarize(frame, group_by="group", value="value")
result
```
````

The last expression in a chunk is displayed, notebook-style.

## Chunk options

Options go at the top of a chunk behind `#|`:

```python
#| label: fig-totals
#| fig-cap: "Total value by group."
#| echo: true
```

| Option    | Effect                                              |
| --------- | --------------------------------------------------- |
| `echo`    | Show the source code                                 |
| `eval`    | Execute the chunk                                    |
| `output`  | Show the result                                      |
| `warning` | Show warnings                                        |
| `label`   | Name the chunk so it can be cross-referenced         |

`quarto/_quarto.yaml` sets `echo: false` and `warning: false` for every report;
a chunk-level option overrides it.

## Cross-references

Label a chunk `fig-*` or `tbl-*` and reference it inline with `@`:

````markdown
```{python}
#| label: fig-totals
#| fig-cap: "Total value by group."
```

@fig-totals shows the distribution.
````

Quarto numbers them and links them automatically.

## Render

```powershell
just preview report          # live reload while editing — the usual loop
just render-one report       # one report to HTML
just render-one-pdf report   # one report to PDF (needs TinyTeX)
just render                  # everything in quarto/ to HTML
```

Output lands beside the source as `quarto/report.html`. Because
`embed-resources: true` is set, that single file carries its own CSS, JS, and
images — you can email it and it works offline.

## Import from the package

`uv sync` installs `combocizes` in editable mode, so reports import it directly:

```python
from combocizes.core import summarize
```

Prefer this over pasting logic into a chunk. Anything worth reusing belongs in
`src/combocizes/`, where it can be tested; the report should read as a
narrative, not an implementation.

## Publish

Pushing to `main` triggers `.github/workflows/docs.yml`, which renders every
report and deploys it alongside these docs:

```
https://caleyest.github.io/combocizes/quarto/<name>.html
```

Add new reports to the `nav:` block in `mkdocs.yml` so they're linked from the
site.

## Slides

Swap the format to get a reveal.js deck from the same content:

```yaml
format:
  revealjs:
    theme: simple
    slide-number: true
```

Each `##` heading becomes a slide.
