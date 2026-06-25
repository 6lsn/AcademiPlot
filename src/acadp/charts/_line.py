import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, _ensure_style, finalize_plot

def lineplot(data=None, x=None, y=None, title=None, xlabel=None, ylabel=None,
             color=None, linewidth=1.8, marker=None, label=None, ax=None, **kwargs):
    """Plot a line chart. Returns matplotlib Axes.

    Args:
        data: DataFrame (x/y are column names) or None (x/y are arrays)
        x: x values or column name
        y: y values or column name
        title: chart title
    """
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    if data is not None and hasattr(data, "columns"):
        x_vals = data[x].values if x else data.iloc[:, 0].values
        y_vals = data[y].values if y else data.iloc[:, 1].values
    else:
        x_vals = np.asarray(x)
        y_vals = np.asarray(y)

    color = color or COLORS["blue_main"]
    ax.plot(x_vals, y_vals, color=color, linewidth=linewidth, marker=marker,
            label=label, **kwargs)
    if xlabel: ax.set_xlabel(xlabel)
    elif data is not None and x: ax.set_xlabel(x)
    if ylabel: ax.set_ylabel(ylabel)
    elif data is not None and y: ax.set_ylabel(y)
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", color=COLORS["text"], pad=10)
    finalize_plot(ax.figure)
    return ax
