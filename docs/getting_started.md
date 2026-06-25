# Getting Started

## Installation

```bash
pip install acadp
```

## Your First Chart

```python
import acadp

ax = acadp.lineplot(x=[1, 2, 3, 4, 5], y=[2, 4, 1, 5, 3], title="My Data")
ax.figure.savefig("my_chart.png", dpi=150, bbox_inches="tight")
```

## Using DataFrames

```python
import pandas as pd

df = pd.read_csv("data.csv")
ax = acadp.barplot(df, x="category", y="value", highlight="max")
```

## Smart Suggest

Let AcademiPlot choose the best chart type for your data and task:

```python
ax = acadp.suggest(df, task="Show cost comparison across methods")
```

The `task` parameter describes what you want to communicate. AcademiPlot analyzes
the data structure and picks the most suitable chart automatically.

## Quality Review

Review a figure's metadata against publication standards:

```python
metadata = {
    "figure_name": "fig1",
    "plot_type": "bar",
    "problem_type": "Evaluation",
    "modeling_purpose": "Compare accuracy across methods",
    "variables": {"x": "method", "y": "accuracy"},
    "axis_labels": {"x": "Method", "y": "Accuracy"},
    "caption": "Comparison of accuracy across methods",
    "usage": "paper",
}
report = acadp.review(metadata)
print(report.status)          # pass / revise / manual_review / reject
print(report.to_markdown())   # detailed markdown report
```

## Auto-Plot Pipeline

The full pipeline: suggest -> render -> review -> revise -> re-review:

```python
result = acadp.auto_plot(df, task="Accuracy distribution across methods")
print(result.report.status)
print(result.changes)
result.chart.figure.savefig("auto_fig.png", dpi=300, bbox_inches="tight")
```

## Style Themes

```python
acadp.set_style("nature")    # Nature journal (default)
acadp.set_style("science")   # Science journal
acadp.set_style("ieee")      # IEEE conference
```

## Chart Types

All chart functions return a `matplotlib.axes.Axes` object:

```python
# Line chart
ax = acadp.lineplot(x, y, title="Trend")

# Bar chart with max/min highlight
ax = acadp.barplot(x=categories, y=values, highlight="max")

# Scatter with optional trend line
ax = acadp.scatter(x=x_vals, y=y_vals, trend=True)

# Heatmap (e.g. correlation matrix)
ax = acadp.heatmap(corr_matrix, labels=col_names)

# Box plot (grouped)
ax = acadp.boxplot(df, groupby="method", y="accuracy")

# Violin plot
ax = acadp.violinplot(df, groupby="method", y="accuracy")

# Histogram with optional KDE
ax = acadp.histogram(values, bins=30, kde=True)

# Radar / spider chart
ax = acadp.radar(labels, values, title="Profile")

# Stacked area chart
ax = acadp.area(x, y={"Series A": a, "Series B": b})

# Stacked bar chart
ax = acadp.stacked_bar(categories, {"Q1": q1, "Q2": q2})
```
