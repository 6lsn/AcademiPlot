import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, PALETTE, _ensure_style, finalize_plot

def barplot(data=None, x=None, y=None, highlight=None, title=None,
            xlabel=None, ylabel=None, horizontal=False, ax=None, **kwargs):
    """Plot a bar chart. Returns matplotlib Axes.

    Args:
        highlight: "max", "min", or None — annotate the highest/lowest bar
    """
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    if data is not None and hasattr(data, "columns"):
        categories = data[x].tolist() if x else data.iloc[:, 0].tolist()
        values = data[y].tolist() if y else data.iloc[:, 1].tolist()
    else:
        categories = list(x) if x is not None else list(range(len(y) if hasattr(y, '__len__') else 0))
        values = list(y)

    colors = [PALETTE[i % len(PALETTE)] for i in range(len(categories))]
    bars = ax.bar(categories, values, color=colors, edgecolor="white", linewidth=1.5, **kwargs)

    if highlight in ("max", "min"):
        idx = int(np.argmax(values)) if highlight == "max" else int(np.argmin(values))
        bars[idx].set_edgecolor(COLORS["amber"])
        bars[idx].set_linewidth(2.5)
        ax.annotate(f"{values[idx]}", xy=(idx, values[idx]),
                    xytext=(0, 8), textcoords="offset points",
                    ha="center", fontsize=10, fontweight="bold", color=COLORS["amber"])

    if xlabel: ax.set_xlabel(xlabel)
    elif data is not None and x: ax.set_xlabel(x)
    if ylabel: ax.set_ylabel(ylabel)
    elif data is not None and y: ax.set_ylabel(y)
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", color=COLORS["text"], pad=10)
    finalize_plot(ax.figure)
    return ax
