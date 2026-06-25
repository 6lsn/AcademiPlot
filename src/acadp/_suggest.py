"""Smart chart suggestion — analyze data + task → pick best chart → render."""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from acadp._profiler import profile_data
from acadp._planner import choose_chart
from acadp._reviewer import review, ReviewResult
from acadp._reviser import revise_metadata
from acadp import charts


def _load_data(data):
    """Accept DataFrame / CSV path / Excel path, return DataFrame."""
    if isinstance(data, pd.DataFrame):
        return data
    if isinstance(data, str):
        if data.endswith(".csv"):
            return pd.read_csv(data)
        if data.endswith((".xls", ".xlsx")):
            return pd.read_excel(data)
    raise ValueError(f"Unsupported data type: {type(data)}")


def suggest(data, task, **kwargs):
    """Smart chart selection: analyze data + task → pick best chart → render.

    Args:
        data: DataFrame, CSV path, or Excel path
        task: str describing what to show (e.g., "展示各方案的成本对比")
        **kwargs: passed to the chosen chart function

    Returns:
        matplotlib.axes.Axes
    """
    df = _load_data(data)
    profile = profile_data(df)
    chart_name = choose_chart(profile, task)
    chart_fn = getattr(charts, chart_name)

    cols = profile.get("columns", {})
    hints = profile.get("plotting_hints", {})
    col_names = list(cols.keys())

    # Auto-detect x/y from profile
    x_col, y_col = None, None
    for name, info in cols.items():
        stype = info.get("semantic_type", "")
        if stype == "category" and x_col is None:
            x_col = name
        if stype in ("numeric", "cost", "ratio", "objective") and y_col is None:
            y_col = name
    if x_col is None and len(col_names) >= 1:
        x_col = col_names[0]
    if y_col is None and len(col_names) >= 2:
        y_col = col_names[1]

    # Call chart function with appropriate args
    if chart_name == "heatmap":
        numeric_df = df.select_dtypes(include=[np.number])
        return chart_fn(
            numeric_df.corr(), labels=list(numeric_df.columns), title=task, **kwargs
        )
    elif chart_name == "radar":
        labels = df[x_col].tolist() if x_col else col_names
        values = df[y_col].tolist() if y_col else [0] * len(labels)
        return chart_fn(labels, values, title=task, **kwargs)
    elif chart_name == "histogram":
        return chart_fn(df[y_col].values, title=task, **kwargs)
    elif chart_name == "stacked_bar":
        if x_col and y_col:
            return chart_fn(
                df[x_col].tolist(), {y_col: df[y_col].tolist()}, title=task, **kwargs
            )
        return chart_fn(
            df.iloc[:, 0].tolist(),
            {df.columns[1]: df.iloc[:, 1].tolist()},
            title=task,
            **kwargs,
        )
    elif chart_name == "area":
        x_vals = df[x_col].tolist() if x_col else list(range(len(df)))
        y_dict = {}
        for name, info in cols.items():
            if info.get("semantic_type") in ("numeric", "cost", "ratio", "objective"):
                y_dict[name] = df[name].tolist()
        if not y_dict and y_col:
            y_dict = {y_col: df[y_col].tolist()}
        return chart_fn(x_vals, y_dict, title=task, **kwargs)
    else:
        # lineplot, barplot, scatter, boxplot, violinplot — all accept (data, x, y, title)
        return chart_fn(df, x=x_col, y=y_col, title=task, **kwargs)


# ============================================================
# Auto-plot pipeline
# ============================================================

@dataclass
class AutoPlotResult:
    chart: object  # matplotlib Axes
    report: ReviewResult = None
    recipe: str = ""
    changes: list = field(default_factory=list)


def auto_plot(data, task, max_rounds=2, **kwargs):
    """Full pipeline: suggest -> render -> review -> revise -> re-review.

    Args:
        data: DataFrame, CSV path, or Excel path
        task: str describing what to show
        max_rounds: max revision rounds (default 2)
        **kwargs: passed to chart function

    Returns:
        AutoPlotResult with .chart, .report, .recipe, .changes
    """
    ax = suggest(data, task, **kwargs)

    # Build metadata from the rendered chart
    from acadp._style import build_figure_metadata

    meta = build_figure_metadata(task, fig=ax.figure)

    all_changes = []
    for _ in range(max_rounds):
        r = review(meta)
        if r.status in ("pass", "manual_review"):
            break
        meta, changes = revise_metadata(meta, r)
        if not changes:
            break
        all_changes.extend(changes)

    # Final review
    final_report = review(meta)

    return AutoPlotResult(
        chart=ax,
        report=final_report,
        recipe=task,
        changes=all_changes,
    )
