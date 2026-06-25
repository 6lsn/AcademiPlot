import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 分组柱状图
def plot_grouped_bar(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    categories = ['产品A', '产品B', '产品C', '产品D', '产品E']
    group1 = [80, 95, 75, 110, 90]
    group2 = [65, 85, 70, 95, 80]
    group3 = [50, 70, 60, 85, 75]
    
    x = np.arange(len(categories))
    width = 0.25
    
    fig, ax = plt.subplots()
    ax.bar(x - width, group1, width, label='2021年')
    ax.bar(x, group2, width, label='2022年')
    ax.bar(x + width, group3, width, label='2023年')
    
    ax.set_xlabel('产品类别')
    ax.set_ylabel('销售额 (万元)')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    set_chart_title(plt.gca(), "不同年份各产品销售额对比")
    
    plt.tight_layout()
    # plt.show()

    # 2. 堆叠柱状图

if __name__ == "__main__":
    plot_grouped_bar()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_grouped_bar")
