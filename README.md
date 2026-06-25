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

### Single Charts

| Line | Bar | Scatter |
|:---:|:---:|:---:|
| ![line](gallery/showcase/line.png) | ![bar](gallery/showcase/bar.png) | ![scatter](gallery/showcase/scatter.png) |

| Heatmap | Box Plot | Radar |
|:---:|:---:|:---:|
| ![heatmap](gallery/showcase/heatmap.png) | ![boxplot](gallery/showcase/boxplot.png) | ![radar](gallery/showcase/radar.png) |

| Histogram | Stacked Bar | Pareto |
|:---:|:---:|:---:|
| ![hist](gallery/showcase/histogram.png) | ![stacked](gallery/showcase/stacked_bar.png) | ![pareto](gallery/showcase/pareto.png) |

| Contour | Waterfall | Dumbbell |
|:---:|:---:|:---:|
| ![contour](gallery/showcase/contour.png) | ![waterfall](gallery/showcase/waterfall.png) | ![dumbbell](gallery/showcase/dumbbell.png) |

### Multi-panel Figures

| 4-panel (2x2) | 6-panel (2x3) |
|:---:|:---:|
| ![4panel](gallery/showcase/multipanel_4panel.png) | ![6panel](gallery/showcase/multipanel_6panel.png) |

---

## Usage Guide

### 1. Direct API — When You Know What You Want

```python
import acadp

# Line chart
ax = acadp.lineplot(x=[1,2,3,4,5], y=[2,4,1,5,3],
                     title="Growth Trend", xlabel="Year", ylabel="GDP")

# Bar chart with highlight
ax = acadp.barplot(["Method A", "Method B", "Method C"],
                    [85, 92, 78], highlight="max",
                    title="Performance Comparison")

# Scatter with trend line + R-squared
ax = acadp.scatter(x=var1, y=var2, trend=True,
                    title="Correlation Analysis")

# Correlation heatmap
ax = acadp.heatmap(corr_matrix, labels=["Var1","Var2","Var3"],
                    title="Correlation Matrix")

# Box plot with grouping
ax = acadp.boxplot(df, y="score", groupby="method")

# Histogram with KDE overlay
ax = acadp.histogram(values, kde=True, title="Error Distribution")

# Radar chart
ax = acadp.radar(["Speed","Accuracy","Memory","Cost"],
                  [0.85, 0.92, 0.7, 0.75], title="Multi-dimensional Evaluation")

# Stacked bar
ax = acadp.stacked_bar(["Q1","Q2","Q3","Q4"],
                        {"Materials": [30,35,28,32], "Labor": [20,22,18,25]},
                        title="Quarterly Cost Breakdown")

# Pareto frontier
ax = acadp.pareto(x=costs, y=quality, frontier=True,
                   title="Multi-objective Optimization")

# Contour with optimum
ax = acadp.contour(X, Y, Z, optimum=(5, 5), title="Parameter Optimization")

# Waterfall
ax = acadp.waterfall(["Base","Cost+","Revenue-","Final"],
                      [100, 20, -15, 105], title="Cost Decomposition")

# Dumbbell (before/after comparison)
ax = acadp.dumbbell([72, 65, 80], [88, 82, 85], ["A","B","C"],
                     title="Before vs After")
```

### 2. Smart Suggest — When You're Not Sure Which Chart

```python
import pandas as pd

df = pd.read_csv("data.csv")

# Just describe what you want to show
ax = acadp.suggest(df, task="展示各方案的成本对比")
# -> Automatically picks barplot, detects "cost" column, adds labels

ax = acadp.suggest(df, task="分析变量之间的相关性")
# -> Automatically picks heatmap, computes correlation matrix

ax = acadp.suggest(df, task="展示时间趋势变化")
# -> Automatically picks lineplot, uses time column as x-axis

ax = acadp.suggest(df, task="对比各方法的性能分布")
# -> Automatically picks boxplot with groupby
```

### 3. Full Pipeline — Suggest + Review + Auto-fix

```python
result = acadp.auto_plot(df, task="展示成本分解与优化空间")

# result.chart  — the generated matplotlib Axes
# result.report — ReviewResult with scores and status
# result.changes — list of auto-applied fixes

print(f"Status: {result.report.status}")    # "pass" / "revise" / "manual_review"
print(f"Score:  {result.report.scores}")    # 6-dimension scores
print(f"Changes: {result.changes}")         # what was auto-fixed
```

### 4. Quality Review

```python
# Review from metadata dict
metadata = {
    "figure_name": "fig1",
    "plot_type": "bar",
    "problem_type": "评价类",
    "modeling_purpose": "展示各方案成本对比",
    "variables": {"x": "Method", "y": "Cost"},
    "axis_labels": {"x": "Method", "y": "Cost ($)"},
    "caption": "Comparison of cost across methods",
    "usage": "paper",
}
report = acadp.review(metadata)
print(report.status)          # "pass"
print(report.to_markdown())   # formatted review report

# Review all figures in a directory
batch = acadp.review_dir("figures/")
batch.to_markdown("review_report.md")
```

### 5. Style Themes

```python
# Nature journal style (default)
acadp.set_style("nature")

# Science journal style (serif fonts)
acadp.set_style("science")

# IEEE conference style (compact, high DPI)
acadp.set_style("ieee")

# Customize
acadp.set_dpi(600)         # high-res output
acadp.set_font("SimHei")   # Chinese font
acadp.set_context("paper") # paper / presentation / poster
```

### 6. Data Input Formats

```python
# Direct arrays
ax = acadp.lineplot(x=[1,2,3], y=[4,5,6])

# Pandas DataFrame
import pandas as pd
df = pd.read_csv("data.csv")
ax = acadp.barplot(df, x="category", y="value")

# From Excel
df = pd.read_excel("results.xlsx")
ax = acadp.scatter(df, x="input", y="output", trend=True)

# Smart suggest accepts file paths directly
ax = acadp.suggest("data.csv", task="展示趋势变化")
ax = acadp.suggest("results.xlsx", task="对比各方案")
```

### 7. Multi-panel Figures (Advanced)

```python
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(10, 6))
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])
acadp.lineplot(x=x, y=y1, ax=ax1, title="A. Trend Analysis")

ax2 = fig.add_subplot(gs[0, 1])
acadp.barplot(categories, values, ax=ax2, title="B. Comparison")

ax3 = fig.add_subplot(gs[1, 0])
acadp.scatter(x=x, y=y, trend=True, ax=ax3, title="C. Correlation")

ax4 = fig.add_subplot(gs[1, 1])
acadp.boxplot(data, ax=ax4, title="D. Distribution")

fig.savefig("multi_panel.png", dpi=300, bbox_inches="tight")
```

### 8. Export for Papers

```python
# Standard export (300 DPI, tight bbox)
ax = acadp.lineplot(x, y, title="My Figure")
ax.figure.savefig("figure1.png", dpi=300, bbox_inches="tight")

# Using built-in helper
acadp.save_figure(ax.figure, "figure1.png", dpi=300)

# LaTeX-friendly vector format
ax.figure.savefig("figure1.pdf", bbox_inches="tight")
ax.figure.savefig("figure1.svg", bbox_inches="tight")
```

---

## API Reference

### Chart Functions

| Function | Description | Key Args |
|----------|-------------|----------|
| `lineplot()` | Line chart | `x, y, title, color, marker` |
| `barplot()` | Bar chart | `x, y, highlight="max", horizontal` |
| `scatter()` | Scatter plot | `x, y, trend=True, alpha` |
| `heatmap()` | Correlation heatmap | `data, labels, annot, cmap` |
| `boxplot()` | Box plot | `data, groupby` |
| `violinplot()` | Violin plot | `data, groupby` |
| `histogram()` | Histogram + KDE | `data, bins, kde=True` |
| `radar()` | Radar/spider chart | `labels, values, fill` |
| `area()` | Stacked area | `x, y_dict, labels` |
| `stacked_bar()` | Stacked bar | `categories, series_dict` |
| `pareto()` | Pareto frontier | `x, y, frontier=True` |
| `contour()` | Contour plot | `X, Y, Z, optimum, filled` |
| `waterfall()` | Waterfall chart | `categories, values` |
| `dumbbell()` | Before/after comparison | `before, after, labels` |

### Smart Functions

| Function | Description |
|----------|-------------|
| `suggest(data, task)` | Auto-select best chart from data + description |
| `auto_plot(data, task)` | Full pipeline: suggest, render, review, revise |
| `review(source)` | 6-dimension quality review |
| `review_dir(path)` | Batch review all figures in directory |
| `set_style("nature")` | Switch theme (nature / science / ieee) |
| `set_dpi(n)` | Set output DPI (default: 300) |
| `set_font(name)` | Override font family |
| `set_context(ctx)` | Set context (paper / presentation / poster) |

---

## Comparison

| Feature | matplotlib | seaborn | **AcademiPlot** |
|---------|:---:|:---:|:---:|
| Academic styles | no | no | Nature/Science/IEEE |
| Smart chart selection | no | no | yes |
| Quality review | no | no | 6-dimension scoring |
| One-line API | no | yes | yes |
| Pareto/Contour/Waterfall | manual | no | yes |
| Chinese labels | manual | manual | built-in |
| Multi-panel support | manual | no | yes |

---

## License

MIT
