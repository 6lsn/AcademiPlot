import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 堆叠柱状图
def plot_stacked_bar(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    categories = ['一月', '二月', '三月', '四月', '五月', '六月']
    group1 = [40, 50, 45, 60, 55, 70]
    group2 = [20, 30, 25, 35, 30, 40]
    group3 = [10, 15, 12, 20, 18, 25]
    
    fig, ax = plt.subplots()
    ax.bar(categories, group1, label='产品X')
    ax.bar(categories, group2, bottom=group1, label='产品Y')
    ax.bar(categories, group3, bottom=np.array(group1)+np.array(group2), label='产品Z')
    
    ax.set_xlabel('月份')
    ax.set_ylabel('销量 (件)')
    ax.legend()
    set_chart_title(plt.gca(), "各月份产品销量构成")
    
    plt.tight_layout()
    # plt.show()

    # 3. 百分比堆叠柱状图

if __name__ == "__main__":
    plot_stacked_bar()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_stacked_bar")
