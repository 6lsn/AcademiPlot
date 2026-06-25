import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from style import COLORS, apply_paper_style, finalize_plot, save_current_figure, set_chart_title

apply_paper_style()


# 帕累托图
def plot7(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    factors = np.array(["运输延迟", "库存不足", "设备故障", "计划变更", "人工误差"])
    values = np.array([43, 27, 14, 9, 7], dtype=float)
    order = np.argsort(values)[::-1]
    factors = factors[order]
    values = values[order]
    cumulative = np.cumsum(values) / values.sum() * 100
    x = np.arange(len(factors))

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(x, values, color=COLORS["seagreen"], width=0.62, label="频数")
    ax.set_ylabel("频数")
    ax.set_xticks(x)
    ax.set_xticklabels(factors, rotation=15, ha="right")

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + values.max() * 0.02,
            f"{value:.0f}",
            ha="center",
            va="bottom",
            fontsize=9,
            color=COLORS["axis"],
        )

    ax2 = ax.twinx()
    ax2.plot(
        x,
        cumulative,
        color=COLORS["crimson"],
        marker="o",
        linewidth=2.4,
        label="累计占比",
    )
    ax2.axhline(80, color=COLORS["blue"], linestyle="--", linewidth=1.4, label="80%阈值")
    ax2.set_ylabel("累计占比")
    ax2.set_ylim(0, 110)
    ax2.set_yticks(np.arange(0, 101, 20))
    ax2.set_yticklabels([f"{tick}%" for tick in range(0, 101, 20)])

    for xi, pct in zip(x, cumulative):
        ax2.text(
            xi,
            pct + 3,
            f"{pct:.1f}%",
            ha="center",
            va="bottom",
            fontsize=8,
            color=COLORS["crimson"],
        )

    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(
        handles1 + handles2,
        labels1 + labels2,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.0),
        ncol=3,
        borderaxespad=0,
        frameon=False,
    )
    for handle in handles1 + handles2:
        handle.set_label("_nolegend_")
    set_chart_title(plt.gca(), "供应链异常因素帕累托分析")
    return fig, (ax, ax2)


if __name__ == "__main__":
    plot7()
    save_current_figure(Path(__file__).stem)
    print("Done: plot7")
