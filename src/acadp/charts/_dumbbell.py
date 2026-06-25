import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, _ensure_style, finalize_plot

def dumbbell(before, after, labels, title=None, xlabel=None,
             color_before=None, color_after=None, ax=None, **kwargs):
    """Dumbbell chart comparing before/after values. Returns Axes."""
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    before = np.asarray(before)
    after = np.asarray(after)
    y_pos = np.arange(len(labels))

    c_before = color_before or COLORS["blue_light"]
    c_after = color_after or COLORS["crimson"]

    # Draw connecting lines
    for i in range(len(labels)):
        ax.plot([before[i], after[i]], [i, i], color=COLORS["grid"],
                linewidth=2, zorder=1)

    # Draw dots
    ax.scatter(before, y_pos, c=c_before, s=80, zorder=2, label="Before", edgecolors="white")
    ax.scatter(after, y_pos, c=c_after, s=80, zorder=2, label="After", edgecolors="white")

    # Add value labels
    for i in range(len(labels)):
        ax.annotate(f"{before[i]:.1f}", (before[i], i), xytext=(-10, 8),
                    textcoords="offset points", fontsize=8, color=c_before, ha="center")
        ax.annotate(f"{after[i]:.1f}", (after[i], i), xytext=(10, 8),
                    textcoords="offset points", fontsize=8, color=c_after, ha="center")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.legend(frameon=False)
    if xlabel: ax.set_xlabel(xlabel)
    if title: ax.set_title(title, fontsize=10, fontweight="bold", color="#333333", pad=6)
    finalize_plot(ax.figure)
    return ax
