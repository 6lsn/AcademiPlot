import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 基础柱状图
def plot_bar_basic(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    np.random.seed(42)
    categories = ['产品A', '产品B', '产品C', '产品D', '产品E', '产品F']
    values = np.random.randint(50, 200, len(categories))
    
    plt.figure()
    bars = plt.bar(categories, values, 
                   color=palette(len(categories)), 
                   edgecolor='w', linewidth=1.5)
    
    # 添加数据标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 3,
                f'{height}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    plt.xlabel('产品类别', fontsize=12, labelpad=10)
    plt.ylabel('销量', fontsize=12, labelpad=10)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    set_chart_title(plt.gca(), "不同类别综合评分对比")
    plt.tight_layout()
    # plt.show()

    # 10. 水平柱状图

if __name__ == "__main__":
    plot_bar_basic()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_bar_basic")
