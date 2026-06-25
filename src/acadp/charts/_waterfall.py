import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, PALETTE, _ensure_style, finalize_plot

def waterfall(categories, values, title=None, xlabel=None, ylabel=None,
              color_increase=None, color_decrease=None, ax=None, **kwargs):
    """Waterfall chart showing incremental changes. Returns Axes."""
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))

    color_inc = color_increase or COLORS["teal"]
    color_dec = color_decrease or COLORS["crimson"]

    cumulative = [0]
    for v in values[:-1]:
        cumulative.append(cumulative[-1] + v)

    bar_colors = []
    for i, v in enumerate(values):
        if i == 0 or i == len(values) - 1:
            bar_colors.append(COLORS["blue_main"])
        elif v >= 0:
            bar_colors.append(color_inc)
        else:
            bar_colors.append(color_dec)

    bottoms = []
    for i, v in enumerate(values):
        if i == 0 or i == len(values) - 1:
            bottoms.append(0)
        elif v >= 0:
            bottoms.append(cumulative[i])
        else:
            bottoms.append(cumulative[i] + v)

    bars = ax.bar(categories, [abs(v) for v in values], bottom=bottoms,
                  color=bar_colors, edgecolor="white", linewidth=1.5, **kwargs)

    # Connect bars with lines
    for i in range(len(values) - 1):
        top = bottoms[i] + abs(values[i])
        ax.plot([i + 0.4, i + 0.6], [top, top], color=COLORS["axis"],
                linewidth=0.8, linestyle="-")

    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    if title: ax.set_title(title, fontsize=10, fontweight="bold", color="#333333", pad=6)
    finalize_plot(ax.figure)
    return ax
