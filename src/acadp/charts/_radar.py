"""Radar / spider chart."""

import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, _ensure_style, finalize_plot


def radar(labels, values, title=None, fill=True, color=None, ax=None, **kwargs):
    """Radar/spider chart. Returns Axes (polar projection)."""
    _ensure_style()
    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    values_plot = list(values) + [values[0]]  # close the polygon
    angles += angles[:1]

    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"projection": "polar"})

    color = color or COLORS["blue_main"]
    ax.plot(angles, values_plot, color=color, linewidth=2, **kwargs)
    if fill:
        ax.fill(angles, values_plot, color=color, alpha=0.15)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylim(0, max(values) * 1.2)
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", color=COLORS["text"], pad=20)
    return ax
