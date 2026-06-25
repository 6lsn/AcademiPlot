import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 点图
def plot_dotplot(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    categories = ['方法A', '方法B', '方法C', '方法D']
    # 固定的四组数据点
    data = [
        [5, 5.2, 5.4, 5.6, 5.8, 6.0, 6.2],
        [7, 7.2, 7.4, 7.6, 7.8, 8.0, 8.2],
        [9, 9.2, 9.4, 9.6, 9.8, 10.0, 10.2],
        [11, 11.2, 11.4, 11.6, 11.8, 12.0, 12.2]
    ]
    
    fig, ax = plt.subplots()
    for i, values in enumerate(data):
        y = [i + np.random.normal(0, 0.05) for _ in values]
        ax.scatter(values, y, alpha=0.7)
    
    # 平均值
    means = [np.mean(values) for values in data]
    ax.scatter(means, range(len(categories)), color=COLORS["crimson"], s=100, marker='X', label='平均值')
    
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories)
    ax.set_xlabel('性能指标')
    ax.legend()
    set_chart_title(plt.gca(), "不同方法性能点估计对比")
    
    plt.tight_layout()
    # plt.show()

    # 10. 基础饼图

if __name__ == "__main__":
    plot_dotplot()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_dotplot")
