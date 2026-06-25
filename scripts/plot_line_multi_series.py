import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 多系列折线图
def plot_line_multi_series(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    np.random.seed(42)
    x = np.linspace(0, 10, 50)
    
    # 生成三个不同的系列
    y1 = np.sin(x) * 10 + 50 + np.random.randn(50) * 1.5
    y2 = np.cos(x) * 8 + 30 + np.random.randn(50) * 1.2
    y3 = (np.sin(x) + np.cos(x)) * 5 + 20 + np.random.randn(50) * 1.0
    
    plt.figure()
    plt.plot(x, y1, label='系列一', color=COLORS["crimson"], linewidth=2, 
             marker='o', markersize=5, alpha=0.8)
    plt.plot(x, y2, label='系列二', color=COLORS["blue"], linewidth=2, 
             linestyle='--', marker='s', markersize=5, alpha=0.8)
    plt.plot(x, y3, label='系列三', color=COLORS["seagreen"], linewidth=2, 
             linestyle='-.', marker='^', markersize=5, alpha=0.8)
    plt.xlabel('时间', fontsize=12, labelpad=10)
    plt.ylabel('数值', fontsize=12, labelpad=10)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    set_chart_title(plt.gca(), "多系列指标趋势对比")
    plt.tight_layout()
    # plt.show()

    # 7. 带误差线的折线图

if __name__ == "__main__":
    plot_line_multi_series()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_line_multi_series")
