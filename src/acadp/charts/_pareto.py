import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, _ensure_style, finalize_plot

def pareto(data=None, x=None, y=None, objectives=None, frontier=True,
           title=None, xlabel=None, ylabel=None, ax=None, **kwargs):
    """Pareto frontier chart for multi-objective optimization. Returns Axes."""
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    if objectives is not None:
        keys = list(objectives.keys())
        x_vals = np.asarray(objectives[keys[0]])
        y_vals = np.asarray(objectives[keys[1]])
    elif data is not None and hasattr(data, "columns"):
        x_vals = data[x].values if x else data.iloc[:, 0].values
        y_vals = data[y].values if y else data.iloc[:, 1].values
    else:
        x_vals = np.asarray(x)
        y_vals = np.asarray(y)

    ax.scatter(x_vals, y_vals, c=COLORS["blue_main"], alpha=0.7, s=60,
               edgecolors="white", linewidth=1.2, **kwargs)

    if frontier and len(x_vals) > 1:
        points = np.column_stack([x_vals, y_vals])
        pareto_mask = np.ones(len(points), dtype=bool)
        for i, p in enumerate(points):
            if pareto_mask[i]:
                dominated = np.all(points <= p, axis=1) & np.any(points < p, axis=1)
                pareto_mask[i] = not np.any(dominated & (np.arange(len(points)) != i))
        pareto_points = points[pareto_mask]
        sort_idx = np.argsort(pareto_points[:, 0])
        pareto_sorted = pareto_points[sort_idx]
        ax.plot(pareto_sorted[:, 0], pareto_sorted[:, 1], color=COLORS["crimson"],
                linewidth=2, linestyle="--", label="Pareto frontier")
        ax.legend(frameon=False)

    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    if title: ax.set_title(title, fontsize=13, fontweight="bold", color=COLORS["text"], pad=10)
    finalize_plot(ax.figure)
    return ax
