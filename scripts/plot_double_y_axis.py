import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 双Y轴折线图
def plot_double_y_axis(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    x = np.linspace(0, 10, 100)
    y1 = np.exp(x/10)
    y2 = np.sin(x) * 10 + 30

    fig, ax1 = plt.subplots(figsize=(8, 5))

    # 第一个Y轴
    line1, = ax1.plot(x, y1, color=COLORS["blue"], linestyle="-", linewidth=2, label="系列1")
    ax1.set_xlabel('X轴')
    ax1.set_ylabel('系列1', color=COLORS["blue"])
    ax1.tick_params('y', colors=COLORS["blue"])

    # 第二个Y轴
    ax2 = ax1.twinx()
    line2, = ax2.plot(x, y2, color=COLORS["crimson"], linestyle="--", linewidth=2, label="系列2")
    ax2.set_ylabel('系列2', color=COLORS["crimson"])
    ax2.tick_params('y', colors=COLORS["crimson"])
    ax1.legend(
        [line1, line2],
        ["系列1", "系列2"],
        loc="upper center",
        bbox_to_anchor=(0.5, 1.0),
        ncol=2,
        frameon=False,
    )
    line1.set_label("_nolegend_")
    line2.set_label("_nolegend_")
    set_chart_title(plt.gca(), "指数增长与周期波动双轴对比")
    plt.tight_layout()
    # plt.show()

if __name__ == "__main__":
    plot_double_y_axis()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_double_y_axis")
