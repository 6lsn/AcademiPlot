"""Stacked bar chart."""

import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, PALETTE, _ensure_style, finalize_plot


def stacked_bar(categories, series_dict, title=None, xlabel=None, ylabel=None, ax=None, **kwargs):
    """Stacked bar chart. series_dict: {label: [values]}. Returns Axes."""
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    x = np.arange(len(categories))
    bottom = np.zeros(len(categories))
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(series_dict))]

    for i, (label, values) in enumerate(series_dict.items()):
        ax.bar(x, values, bottom=bottom, label=label, color=colors[i],
               edgecolor="white", linewidth=1.5, **kwargs)
        bottom += np.asarray(values)

    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend(frameon=False)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, fontsize=10, fontweight="bold", color="#333333", pad=6)
    finalize_plot(ax.figure)
    return ax
