import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 分组散点图
def plot_scatter_grouped(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    np.random.seed(42)
    groups = 4
    points_per_group = 50
    
    # 生成四组不同的数据
    x = [np.random.normal(i*3, 1.2, points_per_group) for i in range(groups)]
    y = [np.random.normal(i*2 + 5, 1.0, points_per_group) for i in range(groups)]
    labels = ['组A', '组B', '组C', '组D']
    colors = [COLORS["blue"], COLORS["blue"], COLORS["seagreen"], COLORS["seagreen"]]
    markers = ['o', 's', '^', 'D']
    
    plt.figure()
    for i in range(groups):
        plt.scatter(x[i], y[i], c=colors[i], label=labels[i], alpha=0.7, 
                   edgecolors='w', s=70, marker=markers[i], linewidth=1.5)
    plt.xlabel('X轴指标', fontsize=12, labelpad=10)
    plt.ylabel('Y轴指标', fontsize=12, labelpad=10)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    set_chart_title(plt.gca(), "四组样本聚类散点分布")
    plt.tight_layout()
    # plt.show()

    # 4. 气泡图

if __name__ == "__main__":
    plot_scatter_grouped()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_scatter_grouped")
