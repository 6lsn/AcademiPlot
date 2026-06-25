import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, DIVERGING_CMAP, _ensure_style, finalize_plot

def heatmap(data, annot=True, cmap="diverging", title=None, labels=None, ax=None, **kwargs):
    """Heatmap (typically for correlation matrices). Returns Axes."""
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 6))

    matrix = np.asarray(data, dtype=float)
    cm = DIVERGING_CMAP if cmap == "diverging" else cmap
    im = ax.imshow(matrix, cmap=cm, aspect="auto", **kwargs)

    if labels:
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontsize=9)

    if annot:
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                val = matrix[i, j]
                color = "white" if abs(val) > 0.6 else COLORS["text"]
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=9, color=color)

    plt.colorbar(im, ax=ax, shrink=0.8)
    if title:
        ax.set_title(title, fontsize=10, fontweight="bold", color="#333333", pad=6)
    finalize_plot(ax.figure)
    return ax
