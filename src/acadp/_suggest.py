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


def _detect_xy(profile):
    """Auto-detect x/y columns from data profile."""
    cols = profile.get("columns", {})
    col_names = list(cols.keys())
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
    return x_col, y_col


def _render_generic(df, profile, chart_name, task, **kwargs):
    """Render lineplot, barplot, scatter, boxplot, violinplot."""
    x_col, y_col = _detect_xy(profile)
    chart_fn = getattr(charts, chart_name)
    return chart_fn(df, x=x_col, y=y_col, title=task, **kwargs)


def _render_heatmap(df, profile, chart_name, task, **kwargs):
    numeric_df = df.select_dtypes(include=[np.number])
    return charts.heatmap(numeric_df.corr(), labels=list(numeric_df.columns), title=task, **kwargs)


def _render_radar(df, profile, chart_name, task, **kwargs):
    x_col, y_col = _detect_xy(profile)
    labels = df[x_col].tolist() if x_col else list(profile.get("columns", {}).keys())
    values = df[y_col].tolist() if y_col else [0] * len(labels)
    return charts.radar(labels, values, title=task, **kwargs)


def _render_histogram(df, profile, chart_name, task, **kwargs):
    cols = profile.get("columns", {})
    y_col = None
    for name, info in cols.items():
        if info.get("semantic_type") in ("numeric", "cost", "ratio", "objective"):
            y_col = name
            break
    if y_col is None:
        y_col = list(cols.keys())[-1] if cols else df.columns[0]
    return charts.histogram(df[y_col].values, title=task, **kwargs)


def _render_stacked_bar(df, profile, chart_name, task, **kwargs):
    x_col, y_col = _detect_xy(profile)
    if x_col and y_col:
        return charts.stacked_bar(df[x_col].tolist(), {y_col: df[y_col].tolist()}, title=task, **kwargs)
    return charts.stacked_bar(
        df.iloc[:, 0].tolist(),
        {df.columns[1]: df.iloc[:, 1].tolist()},
        title=task, **kwargs,
    )


def _render_area(df, profile, chart_name, task, **kwargs):
    cols = profile.get("columns", {})
    x_col = None
    for name, info in cols.items():
        if info.get("semantic_type") == "category" and x_col is None:
            x_col = name
    x_vals = df[x_col].tolist() if x_col else list(range(len(df)))
    y_dict = {}
    for name, info in cols.items():
        if info.get("semantic_type") in ("numeric", "cost", "ratio", "objective"):
            y_dict[name] = df[name].tolist()
    if not y_dict:
        col_names = list(cols.keys())
        y_col = col_names[1] if len(col_names) >= 2 else col_names[0]
        y_dict = {y_col: df[y_col].tolist()}
    return charts.area(x_vals, y_dict, title=task, **kwargs)


def _render_pareto(df, profile, chart_name, task, **kwargs):
    cols = profile.get("columns", {})
    col_names = list(cols.keys())
    x_col, y_col = None, None
    for name, info in cols.items():
        if info.get("semantic_type") in ("numeric", "cost", "ratio", "objective"):
            if x_col is None:
                x_col = name
            elif y_col is None:
                y_col = name
    if x_col is None:
        x_col = col_names[0]
    if y_col is None:
        y_col = col_names[1] if len(col_names) >= 2 else col_names[0]
    return charts.pareto(df, x=x_col, y=y_col, title=task, **kwargs)


def _render_contour(df, profile, chart_name, task, **kwargs):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) >= 3:
        x_vals = df[numeric_cols[0]].values
        y_vals = df[numeric_cols[1]].values
        z_vals = df[numeric_cols[2]].values
        xi = np.linspace(x_vals.min(), x_vals.max(), 30)
        yi = np.linspace(y_vals.min(), y_vals.max(), 30)
        Xi, Yi = np.meshgrid(xi, yi)
        try:
            from scipy.interpolate import griddata
            Zi = griddata((x_vals, y_vals), z_vals, (Xi, Yi), method="linear")
            return charts.contour(Xi, Yi, Zi, title=task, **kwargs)
        except ImportError:
            pass
    return _render_generic(df, profile, "lineplot", task, **kwargs)


def _render_waterfall(df, profile, chart_name, task, **kwargs):
    categories = df.iloc[:, 0].tolist()
    values = df.iloc[:, 1].tolist()
    return charts.waterfall(categories, values, title=task, **kwargs)


def _render_dumbbell(df, profile, chart_name, task, **kwargs):
    cols = list(df.columns)
    if len(cols) >= 3:
        labels = df.iloc[:, 0].tolist()
        before = df.iloc[:, 1].values
        after = df.iloc[:, 2].values
        return charts.dumbbell(before, after, labels, title=task, **kwargs)
    return _render_generic(df, profile, "barplot", task, **kwargs)


_CHART_RENDERERS = {
    "heatmap": _render_heatmap,
    "radar": _render_radar,
    "histogram": _render_histogram,
    "stacked_bar": _render_stacked_bar,
    "area": _render_area,
    "pareto": _render_pareto,
    "contour": _render_contour,
    "waterfall": _render_waterfall,
    "dumbbell": _render_dumbbell,
}

_DEFAULT_RENDERER = _render_generic


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
    renderer = _CHART_RENDERERS.get(chart_name, _DEFAULT_RENDERER)
    return renderer(df, profile, chart_name, task, **kwargs)


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

    from acadp._style import build_figure_metadata
    meta = build_figure_metadata(task, fig=ax.figure)

    all_changes = []
    for _ in range(max_rounds):
        r = review(meta)
        if r.status in ("pass", "manual_review"):
            break
        meta, changes, blocked = revise_metadata(meta, r)
        if not changes:
            break
        all_changes.extend(changes)

    final_report = review(meta)
    return AutoPlotResult(
        chart=ax,
        report=final_report,
        recipe=task,
        changes=all_changes,
    )
