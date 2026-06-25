import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, _ensure_style, finalize_plot

def scatter(data=None, x=None, y=None, trend=False, title=None,
            xlabel=None, ylabel=None, color=None, alpha=0.7, ax=None, **kwargs):
    """Scatter plot with optional trend line. Returns Axes."""
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
    ax.scatter(x_vals, y_vals, c=color, alpha=alpha, edgecolors="white",
               s=60, linewidth=1.2, **kwargs)

    if trend:
        z = np.polyfit(x_vals, y_vals, 1)
        p = np.poly1d(z)
        x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
        ax.plot(x_line, p(x_line), color=COLORS["crimson"], linewidth=1.5, linestyle="--")
        r = np.corrcoef(x_vals, y_vals)[0, 1]
        ax.annotate(f"R² = {r**2:.3f}", xy=(0.05, 0.95), xycoords="axes fraction",
                    fontsize=10, color=COLORS["crimson"], va="top")

    if xlabel: ax.set_xlabel(xlabel)
    elif data is not None and x: ax.set_xlabel(x)
    if ylabel: ax.set_ylabel(ylabel)
    elif data is not None and y: ax.set_ylabel(y)
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", color=COLORS["text"], pad=10)
    finalize_plot(ax.figure)
    return ax
