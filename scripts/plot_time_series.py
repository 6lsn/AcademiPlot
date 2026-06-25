import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 时间序列图
def plot_time_series(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    plt.figure(figsize=(6,5))
    x = range(12)  # 用数字代替日期，避免日期处理问题
    y1 = np.cumsum(np.random.randn(12)) + 20
    y2 = np.cumsum(np.random.randn(12)) + 10
    
    plt.plot(x, y1, color=COLORS["blue"], linestyle="-", label='序列1')
    plt.plot(x, y2, color=COLORS["crimson"], linestyle="-", label='序列2')
    plt.xticks(x, [f'{i+1}月' for i in x])
    plt.legend(loc="upper right", frameon=False)
    plt.grid(axis='y', linestyle='--')
    set_chart_title(plt.gca(), "两组月度序列变化趋势")
    # plt.show()

    # 绘制所有图表

if __name__ == "__main__":
    plot_time_series()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_time_series")
