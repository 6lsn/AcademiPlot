import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 箱线图
def plot_boxplot(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    # 固定的四组数据
    data = [
        [45, 50, 55, 60, 65, 48, 52, 58, 62, 53],
        [55, 60, 65, 70, 75, 58, 62, 68, 72, 63],
        [35, 40, 45, 50, 55, 38, 42, 48, 52, 43],
        [65, 70, 75, 80, 85, 68, 72, 78, 82, 73]
    ]
    
    fig, ax = plt.subplots()
    bp = ax.boxplot(data, patch_artist=True)
    
    # 简单着色
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
    
    ax.set_xticklabels(['A组', 'B组', 'C组', 'D组'])
    ax.set_ylabel('测量值')
    set_chart_title(plt.gca(), "四组样本分布差异对比")
    
    plt.tight_layout()
    # plt.show()

    # 8. 小提琴图

if __name__ == "__main__":
    plot_boxplot()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_boxplot")
