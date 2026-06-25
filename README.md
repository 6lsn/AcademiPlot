# AcademiPlot

> **Publication-ready academic figures in one line.**
>
> 一行代码，论文图表直达 Nature 级。

[![PyPI version](https://img.shields.io/pypi/v/acadp.svg)](https://pypi.org/project/acadp/)
[![Python](https://img.shields.io/pypi/pyversions/acadp.svg)](https://pypi.org/project/acadp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Why AcademiPlot?

<table>
<tr>
<td align="center"><b>Before (matplotlib default)</b></td>
<td align="center"><b>After (AcademiPlot)</b></td>
</tr>
<tr>
<td><img src="gallery/before_after/before.png" width="400"></td>
<td><img src="gallery/before_after/after.png" width="400"></td>
</tr>
</table>

**What makes it different:**

- **Nature/Science-grade styles** — not just colors, complete academic figure standards
- **Smart suggest** — describe your goal, it picks the best chart type
- **Quality review** — 6-dimension scoring checks if your figure meets academic standards
- **14 chart types** — from line plots to Pareto frontiers

---

## Quick Start

```bash
pip install acadp
```

```python
import acadp
import numpy as np

# One-line chart
x = np.linspace(0, 10, 50)
ax = acadp.lineplot(x=x, y=np.sin(x), title="示例曲线", xlabel="X", ylabel="Y")

# Smart suggest — describe what you want to show
ax = acadp.suggest(df, task="展示各方案的成本对比")

# Full pipeline — suggest + render + quality review
result = acadp.auto_plot(df, task="展示成本分解与优化空间")
print(result.report.status)  # "pass"
```

---

## Gallery

| Line | Bar | Scatter |
|:---:|:---:|:---:|
| ![line](gallery/showcase/line.png) | ![bar](gallery/showcase/bar.png) | ![scatter](gallery/showcase/scatter.png) |

| Heatmap | Box Plot | Radar |
|:---:|:---:|:---:|
| ![heatmap](gallery/showcase/heatmap.png) | ![boxplot](gallery/showcase/boxplot.png) | ![radar](gallery/showcase/radar.png) |

| Histogram | Stacked Bar | Pareto |
|:---:|:---:|:---:|
| ![hist](gallery/showcase/histogram.png) | ![stacked](gallery/showcase/stacked_bar.png) | ![pareto](gallery/showcase/pareto.png) |

---

## API Reference

### Chart Functions

| Function | Description | Key Args |
|----------|-------------|----------|
| `lineplot()` | Line chart | `x, y, title, trend` |
| `barplot()` | Bar chart | `x, y, highlight="max"` |
| `scatter()` | Scatter plot | `x, y, trend=True` |
| `heatmap()` | Correlation heatmap | `data, labels, annot` |
| `boxplot()` | Box plot | `data, groupby` |
| `violinplot()` | Violin plot | `data, groupby` |
| `histogram()` | Histogram + KDE | `data, kde=True` |
| `radar()` | Radar/spider chart | `labels, values` |
| `area()` | Stacked area | `x, y_dict` |
| `stacked_bar()` | Stacked bar | `categories, series_dict` |
| `pareto()` | Pareto frontier | `x, y, frontier` |
| `contour()` | Contour plot | `X, Y, Z, optimum` |
| `waterfall()` | Waterfall chart | `categories, values` |
| `dumbbell()` | Before/after comparison | `before, after, labels` |

### Smart Functions

| Function | Description |
|----------|-------------|
| `suggest(data, task)` | Auto-select best chart from data + description |
| `auto_plot(data, task)` | Full pipeline: suggest, render, review, revise |
| `review(source)` | 6-dimension quality review |
| `set_style("nature")` | Switch theme (nature/science/ieee) |

---

## Why not just use seaborn/matplotlib?

| Feature | matplotlib | seaborn | **AcademiPlot** |
|---------|:---:|:---:|:---:|
| Academic styles | no | no | Nature/Science/IEEE |
| Smart chart selection | no | no | yes |
| Quality review | no | no | 6-dimension scoring |
| One-line API | no | yes | yes |
| Pareto/Contour/Waterfall | manual | no | yes |
| Chinese labels | manual | manual | built-in |

---

## License

MIT
