import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, PALETTE, _ensure_style, finalize_plot


def violinplot(data=None, x=None, y=None, groupby=None, title=None,
               xlabel=None, ylabel=None, showmedians=True, ax=None, **kwargs):
    """Violin plot. Accepts DataFrame with groupby or arrays. Returns Axes."""
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    if data is not None and hasattr(data, "columns"):
        if groupby:
            groups = data[groupby].unique()
            plot_data = [data[data[groupby] == g][y].values for g in groups]
            parts = ax.violinplot(plot_data, showmedians=showmedians, **kwargs)
            ax.set_xticks(range(1, len(groups) + 1))
            ax.set_xticklabels(groups)
        else:
            col = y or data.columns[0]
            values = data[col].dropna().values
            parts = ax.violinplot([values], showmedians=showmedians, **kwargs)
    else:
        arr = np.asarray(data)
        if arr.ndim == 1:
            arr = [arr]
        parts = ax.violinplot(arr, showmedians=showmedians, **kwargs)

    for i, body in enumerate(parts["bodies"]):
        body.set_facecolor(PALETTE[i % len(PALETTE)])
        body.set_alpha(0.7)

    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", color=COLORS["text"], pad=10)
    finalize_plot(ax.figure)
    return ax
