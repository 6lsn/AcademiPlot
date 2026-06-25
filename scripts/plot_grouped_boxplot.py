import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 分组箱线图
def plot_grouped_boxplot(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    np.random.seed(10)
    data1 = [np.random.normal(0, std, 50) for std in range(1, 4)]
    data2 = [np.random.normal(3, std, 50) for std in range(1, 4)]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    bp1 = ax.boxplot(data1, positions=[1, 2, 3], widths=0.3, 
                    patch_artist=True, boxprops=dict(facecolor="lightblue"))
    bp2 = ax.boxplot(data2, positions=[1.5, 2.5, 3.5], widths=0.3, 
                    patch_artist=True, boxprops=dict(facecolor="lightgreen"))
    ax.set_xlabel('类别')
    ax.set_ylabel('数值')
    ax.set_xticks([1.25, 2.25, 3.25])
    ax.set_xticklabels(['A', 'B', 'C'])
    ax.legend([bp1["boxes"][0], bp2["boxes"][0]], ['组1', '组2'])
    set_chart_title(plt.gca(), "两组分类样本分布对比")
    plt.tight_layout()
    # plt.show()

if __name__ == "__main__":
    plot_grouped_boxplot()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_grouped_boxplot")
