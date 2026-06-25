import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, PALETTE, _ensure_style, finalize_plot


def boxplot(data=None, x=None, y=None, groupby=None, title=None,
            xlabel=None, ylabel=None, ax=None, **kwargs):
    """Box plot. Accepts DataFrame with groupby or arrays. Returns Axes."""
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    if data is not None and hasattr(data, "columns"):
        if groupby:
            groups = data[groupby].unique()
            plot_data = [data[data[groupby] == g][y].values for g in groups]
            bp = ax.boxplot(plot_data, tick_labels=groups, patch_artist=True, **kwargs)
            for i, patch in enumerate(bp["boxes"]):
                patch.set_facecolor(PALETTE[i % len(PALETTE)])
                patch.set_alpha(0.7)
        else:
            col = y or data.columns[0]
            bp = ax.boxplot(data[col].dropna().values, patch_artist=True, **kwargs)
            for i, patch in enumerate(bp["boxes"]):
                patch.set_facecolor(PALETTE[i % len(PALETTE)])
                patch.set_alpha(0.7)
    else:
        bp = ax.boxplot(np.asarray(data), patch_artist=True, **kwargs)
        for i, patch in enumerate(bp["boxes"]):
            patch.set_facecolor(PALETTE[i % len(PALETTE)])
            patch.set_alpha(0.7)

    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, fontsize=10, fontweight="bold", color="#333333", pad=6)
    finalize_plot(ax.figure)
    return ax
