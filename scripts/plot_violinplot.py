import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 小提琴图
def plot_violinplot(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    # 固定的三组数据
    data = [
        [ -2, -1, 0, 1, 2 ] * 40,  # 正态分布模拟
        [ 0, 1, 2, 3, 4 ] * 40,    # 偏态分布模拟
        [ -3, -2, -1, 0, 1, 2, 3 ] * 28  # 均匀分布模拟
    ]
    
    fig, ax = plt.subplots()
    parts = ax.violinplot(data, showmedians=True)
    
    # 统一论文主题着色
    for pc, color in zip(parts['bodies'], palette(len(data))):
        pc.set_facecolor(color)
        pc.set_alpha(0.7)
    
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['正态分布', '偏态分布', '均匀分布'])
    ax.set_ylabel('数值')
    set_chart_title(plt.gca(), "不同分布样本密度对比")
    
    plt.tight_layout()
    # plt.show()

    # 9. 点图

if __name__ == "__main__":
    plot_violinplot()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_violinplot")
