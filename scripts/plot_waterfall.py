import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from style import COLORS, apply_paper_style, finalize_plot, save_current_figure, set_chart_title

apply_paper_style()


# 瀑布图
def plot_waterfall(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    labels = ["基准", "效率提升", "材料节约", "维护增加", "调度优化", "最终"]
    changes = np.array([120, 28, 16, -22, 18], dtype=float)
    final_value = changes.sum()
    values = np.r_[changes, final_value]

    running_total = np.r_[0, np.cumsum(changes[:-1]), 0]
    colors = []
    for index, value in enumerate(values):
        if index == 0 or index == len(values) - 1:
            colors.append(COLORS["blue"])
        elif value >= 0:
            colors.append(COLORS["seagreen"])
        else:
            colors.append(COLORS["crimson"])

    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(x, values, bottom=running_total, color=colors, width=0.62)

    connector = []
    cumulative = np.cumsum(changes)
    for index in range(len(changes) - 1):
        y = cumulative[index]
        connector.append(
            ax.plot(
                [index + 0.31, index + 1 - 0.31],
                [y, y],
                color=COLORS["muted"],
                linestyle="--",
                linewidth=1.0,
            )[0]
        )

    for bar, value, bottom in zip(bars, values, running_total):
        y = bottom + value
        va = "bottom" if value >= 0 else "top"
        offset = 4 if value >= 0 else -4
        ax.annotate(
            f"{value:+.0f}" if bar != bars[-1] else f"{value:.0f}",
            xy=(bar.get_x() + bar.get_width() / 2, y),
            xytext=(0, offset),
            textcoords="offset points",
            ha="center",
            va=va,
            fontsize=9,
            color=COLORS["axis"],
        )

    ax.axhline(0, color=COLORS["axis"], linewidth=0.9)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha="right")
    ax.set_ylabel("综合收益")
    set_chart_title(plt.gca(), "优化方案收益分解")
    return fig, ax


if __name__ == "__main__":
    plot_waterfall()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_waterfall")
