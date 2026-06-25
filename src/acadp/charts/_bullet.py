"""Bullet chart — threshold compliance visualization."""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.ticker import PercentFormatter
from acadp._style import COLORS, _ensure_style, finalize_plot, set_chart_title


def _pass_check(actual, threshold, direction):
    direction = str(direction).strip()
    if direction.startswith("<"):
        return actual <= threshold
    if direction.startswith(">"):
        return actual >= threshold
    return abs(actual - threshold) <= 1e-9


def _format_number(value, as_percent=False):
    if as_percent:
        return f"{value * 100:.1f}%"
    return f"{value:.1f}"


def bullet(categories, actual, threshold, directions=None, unit="",
           title=None, xlabel=None, ylabel=None, ax=None, **kwargs):
    """Bullet chart showing threshold compliance status.

    Args:
        categories: list of category labels
        actual: array of actual values
        threshold: array of threshold values
        directions: list of direction strings (e.g., [">=", ">="])
        unit: "ratio"/"percent"/"%" for percentage formatting
        title: chart title
        ax: existing Axes or None

    Returns:
        matplotlib.axes.Axes
    """
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8.2, 4.9))

    categories = [str(c) for c in categories]
    actual = np.asarray(actual, dtype=float)
    threshold = np.asarray(threshold, dtype=float)
    if directions is None:
        directions = [">="] * len(categories)
    y = np.arange(len(categories))

    as_percent = unit.lower() in {"ratio", "percent", "%"} or unit == ""
    if as_percent and max(np.nanmax(actual), np.nanmax(threshold)) > 1.5:
        as_percent = False

    max_value = max(float(np.nanmax(actual)), float(np.nanmax(threshold))) * 1.15
    if as_percent:
        max_value = max(max_value, 1.0)

    for idx, category in enumerate(categories):
        passed = _pass_check(actual[idx], threshold[idx], directions[idx])
        color = COLORS["teal"] if passed else COLORS["coral"]
        ax.barh(idx, max_value, color="#F3F4F6", height=0.58, edgecolor="none")
        ax.barh(idx, actual[idx], color=color, height=0.42, alpha=0.9)
        ax.vlines(threshold[idx], idx - 0.34, idx + 0.34, color=COLORS["amber"], linewidth=2.5)
        ax.text(actual[idx] + max_value * 0.015, idx, _format_number(actual[idx], as_percent), va="center")
        ax.text(
            threshold[idx], idx + 0.42,
            f"{directions[idx]}{_format_number(threshold[idx], as_percent)}",
            ha="center", va="bottom", fontsize=9, color=COLORS["amber"],
        )

    ax.set_yticks(y)
    ax.set_yticklabels(categories)
    ax.set_xlim(0, max_value)
    ax.invert_yaxis()
    if as_percent:
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
    if xlabel:
        ax.set_xlabel(xlabel)
    else:
        ax.set_xlabel("指标值")
    if ylabel:
        ax.set_ylabel(ylabel)
    else:
        ax.set_ylabel("指标")
    if title:
        set_chart_title(ax, title)
    else:
        set_chart_title(ax, "指标阈值达标状态")

    handles = [
        mpatches.Patch(color=COLORS["teal"], label="达标"),
        mpatches.Patch(color=COLORS["coral"], label="未达标"),
        mlines.Line2D([], [], color=COLORS["amber"], linewidth=2.5, label="阈值"),
    ]
    ax.legend(handles=handles, loc="lower right", frameon=False)
    finalize_plot(ax.figure)
    return ax
