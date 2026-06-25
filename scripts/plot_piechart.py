import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 基础饼图
def plot_piechart(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    labels = ['直接访问', '搜索引擎', '社交媒体', '广告推广', '外部链接']
    sizes = np.array([30, 25, 20, 15, 10])
    
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    order = np.argsort(sizes)
    bars = ax.barh(
        np.array(labels)[order],
        sizes[order],
        color=palette(len(labels))[::-1],
        height=0.58,
    )
    ax.set_xlabel("占比 (%)")
    ax.set_xlim(0, sizes.max() * 1.22)
    for bar, value in zip(bars, sizes[order]):
        ax.text(
            value + sizes.max() * 0.025,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.0f}%",
            va="center",
            ha="left",
            fontsize=10,
            color=COLORS["axis"],
        )
    set_chart_title(plt.gca(), "网站流量来源占比排序")
    
    plt.tight_layout()
    # plt.show()

    # 运行所有图表

if __name__ == "__main__":
    plot_piechart()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_piechart")
