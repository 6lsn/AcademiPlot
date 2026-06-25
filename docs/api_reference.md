# API Reference

## Chart Functions

All chart functions return `matplotlib.axes.Axes`.

### `lineplot(data=None, x=None, y=None, title=None, xlabel=None, ylabel=None, color=None, linewidth=1.8, marker=None, label=None, ax=None, **kwargs)`

Line chart. Pass `data` as a DataFrame with `x`/`y` as column names, or pass `x`/`y` as arrays directly.

### `barplot(data=None, x=None, y=None, highlight=None, title=None, xlabel=None, ylabel=None, horizontal=False, ax=None, **kwargs)`

Bar chart. `highlight` can be `"max"` or `"min"` to annotate the highest/lowest bar.

### `scatter(data=None, x=None, y=None, trend=False, title=None, xlabel=None, ylabel=None, color=None, alpha=0.7, ax=None, **kwargs)`

Scatter plot. Set `trend=True` to add a linear regression line with R-squared annotation.

### `heatmap(data, annot=True, cmap="diverging", title=None, labels=None, ax=None, **kwargs)`

Heatmap for correlation matrices or 2D data. `labels` sets axis tick labels.

### `boxplot(data=None, x=None, y=None, groupby=None, title=None, xlabel=None, ylabel=None, ax=None, **kwargs)`

Box plot. Use `groupby` with a DataFrame to create grouped box plots.

### `violinplot(data=None, x=None, y=None, groupby=None, title=None, xlabel=None, ylabel=None, showmedians=True, ax=None, **kwargs)`

Violin plot. Similar interface to `boxplot`.

### `histogram(data, bins=30, kde=False, title=None, xlabel=None, ylabel=None, color=None, ax=None, **kwargs)`

Histogram. Set `kde=True` to overlay a kernel density estimate.

### `radar(labels, values, title=None, fill=True, color=None, ax=None, **kwargs)`

Radar / spider chart. `labels` is a list of axis names, `values` is a list of corresponding values.

### `area(x, y=None, title=None, xlabel=None, ylabel=None, labels=None, ax=None, **kwargs)`

Stacked area chart. `y` can be a dict of `{label: values}` or a 2D array.

### `stacked_bar(categories, series_dict, title=None, xlabel=None, ylabel=None, ax=None, **kwargs)`

Stacked bar chart. `series_dict` maps series labels to value lists.

---

## Smart Suggest

### `suggest(data, task, **kwargs)`

Analyze data and task description, then automatically pick and render the best chart.

- `data`: DataFrame, CSV path, or Excel path
- `task`: str describing what to show (e.g., "Show cost comparison")
- Returns: `matplotlib.axes.Axes`

### `auto_plot(data, task, max_rounds=2, **kwargs)`

Full pipeline: suggest -> render -> review -> revise -> re-review.

- Returns: `AutoPlotResult` with attributes:
  - `.chart` -- matplotlib Axes
  - `.report` -- `ReviewResult`
  - `.recipe` -- task string
  - `.changes` -- list of revision changes applied

---

## Quality Review

### `review(source)`

Review a figure against publication standards.

- `source`: a metadata `dict`, or a `.json` file path
- Returns: `ReviewResult` with attributes:
  - `.status` -- one of `"pass"`, `"revise"`, `"manual_review"`, `"reject"`
  - `.score` -- overall score (0-100)
  - `.scores` -- dict of 6 dimension scores
  - `.major_issues` -- list of major issues
  - `.minor_issues` -- list of minor issues
  - `.suggested_caption` -- suggested figure caption
  - `.suggested_plot_type` -- recommended plot type (if current one is unsuitable)
  - `.to_markdown()` -- render full report as markdown

### `review_dir(directory)`

Review all `.metadata.json` files in a directory.

- Returns: `BatchReport` with attributes:
  - `.total`, `.pass_count`, `.revise_count`, `.manual_count`, `.reject_count`
  - `.results` -- list of `ReviewResult`
  - `.to_markdown()` -- render full batch report as markdown

---

## Style Configuration

### `set_style(name)`

Switch theme. Valid names: `"nature"` (default), `"science"`, `"ieee"`.

### `get_style()`

Return current configuration dict with keys: `style`, `dpi`, `font`, `context`.

### `set_dpi(dpi)`

Set the default save DPI.

### `set_font(font)`

Override the primary font family (e.g., `"serif"`, `"sans-serif"`).

### `set_context(ctx)`

Set rendering context (e.g., `"paper"`, `"presentation"`).
