import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 基础散点图
def plot_scatter_basic(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    np.random.seed(42)
    x = np.random.randn(100) * 10
    y = 2 * x + np.random.randn(100) * 15 + 50
    
    plt.figure()
    plt.scatter(x, y, c=COLORS["blue"], alpha=0.7, edgecolors='w', s=80, linewidth=1.5)
    plt.xlabel('X轴数据', fontsize=12, labelpad=10)
    plt.ylabel('Y轴数据', fontsize=12, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    set_chart_title(plt.gca(), "双变量线性关系散点分布")
    plt.tight_layout()
    # plt.show()

    # 2. 带趋势线的散点图

if __name__ == "__main__":
    plot_scatter_basic()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_scatter_basic")
