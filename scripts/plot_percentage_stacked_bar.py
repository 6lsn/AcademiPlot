import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 百分比堆叠柱状图
def plot_percentage_stacked_bar(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    categories = ['华东', '华北', '华南', '西部', '东北']
    group1 = [50, 40, 60, 30, 45]
    group2 = [30, 35, 25, 40, 30]
    group3 = [20, 25, 15, 30, 25]
    
    total = np.array(group1) + np.array(group2) + np.array(group3)
    group1_perc = group1 / total * 100
    group2_perc = group2 / total * 100
    group3_perc = group3 / total * 100
    
    fig, ax = plt.subplots()
    colors = palette(3)
    ax.bar(categories, group1_perc, label='线上销售', color=colors[0])
    ax.bar(categories, group2_perc, bottom=group1_perc, label='门店销售', color=colors[1])
    ax.bar(categories, group3_perc, bottom=group1_perc+group2_perc, label='经销商', color=colors[2])
    
    ax.set_xlabel('地区')
    ax.set_ylabel('销售占比 (%)')
    ax.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=3,
        borderaxespad=0,
        frameon=False,
    )
    set_chart_title(ax, "各地区销售渠道占比")
    
    fig.tight_layout()
    # plt.show()

    # 4. 直方图

if __name__ == "__main__":
    plot_percentage_stacked_bar()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_percentage_stacked_bar")
