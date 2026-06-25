"""Small multiples for sensitivity analysis."""
import math
import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, palette, _ensure_style, finalize_plot, set_chart_title


def small_multiples(factors, y_label="结果指标", cols=2,
                    title=None, figsize=None, **kwargs):
    """Small multiples chart for multi-factor sensitivity analysis.

    Args:
        factors: list of dicts, each with "name", "x", "y", optional "baseline"
        y_label: shared y-axis label
        cols: number of columns
        title: overall title (unused -- each panel gets its own)
        figsize: tuple or None

    Returns:
        matplotlib.figure.Figure
    """
    _ensure_style()
    rows = math.ceil(len(factors) / cols)
    if figsize is None:
        figsize = (11.5, 4.0 * rows)
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    axes = np.asarray(axes).reshape(-1)
    colors = palette(4)

    for idx, factor in enumerate(factors):
        ax = axes[idx]
        x = np.asarray(factor["x"])
        y = np.asarray(factor["y"])
        ax.plot(x, y, marker="o", color=colors[idx % len(colors)], linewidth=2.2)
        if len(x) >= 2:
            trend = np.poly1d(np.polyfit(x, y, 1))(x)
            ax.plot(x, trend, linestyle="--", linewidth=1.2, color=COLORS["muted"])
        if "baseline" in factor:
            ax.axvline(factor["baseline"], color=COLORS["muted"], linestyle=":", linewidth=1.2)
        ax.set_xlabel(factor["name"])
        ax.set_ylabel(y_label)
        set_chart_title(ax, factor["name"])

    for ax in axes[len(factors):]:
        ax.set_visible(False)

    finalize_plot(fig)
    return fig
