import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 带误差线的折线图
def plot_line_with_error(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    np.random.seed(42)
    x = np.arange(1, 13)  # 12个数据点，例如12个月
    y = np.sin(x/2) * 10 + 50 + np.random.randn(12) * 3
    y_err = np.random.rand(12) * 4 + 1  # 误差值
    
    plt.figure()
    plt.errorbar(x, y, yerr=y_err, fmt='-o', ecolor=COLORS["crimson"], elinewidth=2,
                 capsize=5, capthick=2, color=COLORS["crimson"], linewidth=2.5, 
                 markersize=8, markerfacecolor="white", markeredgewidth=2)
    plt.xlabel('月份', fontsize=12, labelpad=10)
    plt.ylabel('测量值', fontsize=12, labelpad=10)
    plt.xticks(x)  # 显示所有x刻度
    plt.grid(True, linestyle='--', alpha=0.6)
    set_chart_title(plt.gca(), "观测序列均值及误差范围")
    plt.tight_layout()
    # plt.show()

    # 8. 阶梯折线图

if __name__ == "__main__":
    plot_line_with_error()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_line_with_error")
