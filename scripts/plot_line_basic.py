import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 基础折线图
def plot_line_basic(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    np.random.seed(42)
    x = np.linspace(0, 12, 100)
    y = np.sin(x) * 10 + 50 + np.random.randn(100) * 2
    
    plt.figure()
    plt.plot(x, y, color=COLORS["blue"], linewidth=2.5, linestyle='-', 
             marker='o', markersize=6, markerfacecolor=COLORS["amber"], 
             markeredgecolor=COLORS["blue"], markeredgewidth=1.5)
    plt.xlabel('时间', fontsize=12, labelpad=10)
    plt.ylabel('数值', fontsize=12, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    set_chart_title(plt.gca(), "单指标时间变化趋势")
    plt.tight_layout()
    # plt.show()

    # 6. 多系列折线图

if __name__ == "__main__":
    plot_line_basic()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_line_basic")
