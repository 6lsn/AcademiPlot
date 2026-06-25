import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, PAPER_CMAP, _ensure_style, finalize_plot

def contour(X, Y, Z, optimum=None, title=None, xlabel=None, ylabel=None,
            cmap=None, filled=True, ax=None, **kwargs):
    """Contour plot for parameter optimization. Returns Axes."""
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    cm = cmap or PAPER_CMAP
    if filled:
        cs = ax.contourf(X, Y, Z, cmap=cm, levels=20, **kwargs)
    else:
        cs = ax.contour(X, Y, Z, cmap=cm, levels=20, **kwargs)
    plt.colorbar(cs, ax=ax, shrink=0.8)
    if optimum:
        ax.scatter([optimum[0]], [optimum[1]], c=COLORS["crimson"], s=120,
                   marker="*", edgecolors="white", linewidth=1.5, zorder=10)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    if title: ax.set_title(title, fontsize=13, fontweight="bold", color=COLORS["text"], pad=10)
    finalize_plot(ax.figure)
    return ax
