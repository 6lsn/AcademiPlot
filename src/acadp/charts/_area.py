"""Stacked area chart."""

import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, PALETTE, _ensure_style, finalize_plot


def area(x, y=None, title=None, xlabel=None, ylabel=None, labels=None, ax=None, **kwargs):
    """Stacked area chart. y can be dict of series or 2D array. Returns Axes."""
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    if isinstance(y, dict):
        ys = list(y.values())
        labels = labels or list(y.keys())
    else:
        ys = np.asarray(y)
        if ys.ndim == 1:
            ys = [ys]

    colors = [PALETTE[i % len(PALETTE)] for i in range(len(ys))]
    ax.stackplot(np.asarray(x), *ys, labels=labels, colors=colors, alpha=0.7, **kwargs)
    if labels:
        ax.legend(loc="upper left", frameon=False)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", color=COLORS["text"], pad=10)
    finalize_plot(ax.figure)
    return ax
