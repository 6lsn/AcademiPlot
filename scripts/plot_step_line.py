import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 阶梯折线图
def plot_step_line(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    np.random.seed(42)
    x = np.linspace(0, 10, 20)
    y = np.cumsum(np.random.randn(20) * 2 + 5)  # 累积和，模拟某种指标变化
    
    plt.figure()
    plt.step(x, y, where='mid', color=COLORS["amber"], linewidth=2.5, 
             marker='s', markersize=8, markerfacecolor=COLORS["amber"], 
             markeredgecolor=COLORS["amber"], markeredgewidth=2)
    plt.xlabel('时间点', fontsize=12, labelpad=10)
    plt.ylabel('累计值', fontsize=12, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    set_chart_title(plt.gca(), "过程累计值阶梯变化")
    plt.tight_layout()
    # plt.show()

    # 9. 基础柱状图

if __name__ == "__main__":
    plot_step_line()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_step_line")
