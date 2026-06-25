import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 面积图
def plot_area(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    plt.figure(figsize=(6,5))
    x = [1,2,3,4,5,6]
    y1 = [10,15,12,18,20,25]
    y2 = [5,8,10,12,15,18]
    
    plt.fill_between(x, y1, alpha=0.4, color=COLORS["blue"], label='数据1')
    plt.fill_between(x, y2, alpha=0.4, color=COLORS["seagreen"], label='数据2')
    plt.plot(x, y1, color=COLORS["blue"], linestyle="-")
    plt.plot(x, y2, color=COLORS["seagreen"], linestyle="-")
    plt.legend()
    set_chart_title(plt.gca(), "两类指标累计变化范围")
    # plt.show()

    # 时间序列图

if __name__ == "__main__":
    plot_area()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_area")
