import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, _ensure_style, finalize_plot


def _numpy_kde(values, x_range):
    """Simple Gaussian KDE using numpy (no scipy dependency)."""
    n = len(values)
    std = np.std(values, ddof=1)
    bandwidth = 1.06 * std * n ** (-1 / 5)
    if bandwidth <= 0:
        bandwidth = 1.0
    diffs = (x_range[:, None] - values[None, :]) / bandwidth
    kernel = np.exp(-0.5 * diffs ** 2) / (bandwidth * np.sqrt(2 * np.pi))
    return kernel.mean(axis=1)


def histogram(data, bins=30, kde=False, title=None, xlabel=None, ylabel=None,
              color=None, ax=None, **kwargs):
    """Histogram with optional KDE overlay. Returns Axes."""
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    values = np.asarray(data).flatten()
    values = values[np.isfinite(values)]
    color = color or COLORS["blue_main"]
    ax.hist(values, bins=bins, color=color, edgecolor="white", alpha=0.7, **kwargs)

    if kde:
        try:
            from scipy.stats import gaussian_kde
            kde_func = gaussian_kde(values)
        except ImportError:
            kde_func = None

        x_range = np.linspace(values.min(), values.max(), 200)
        if kde_func is not None:
            density = kde_func(x_range)
        else:
            density = _numpy_kde(values, x_range)

        ax2 = ax.twinx()
        ax2.plot(x_range, density, color=COLORS["crimson"], linewidth=1.5)
        ax2.set_ylabel("Density")
        ax2.spines["top"].set_visible(False)

    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, fontsize=10, fontweight="bold", color="#333333", pad=6)
    finalize_plot(ax.figure)
    return ax
