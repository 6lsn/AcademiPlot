import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 水平柱状图
def plot_bar_horizontal(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    np.random.seed(42)
    categories = ['地区A', '地区B', '地区C', '地区D', '地区E', '地区F']
    values = np.random.randint(100, 500, len(categories))
    
    plt.figure()
    bars = plt.barh(categories, values, 
                    color=palette(len(categories)), 
                    edgecolor='w', linewidth=1.5)
    
    # 添加数据标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 10, bar.get_y() + bar.get_height()/2.,
                f'{width}', va='center', fontsize=10, fontweight='bold')
    plt.xlabel('销售额', fontsize=12, labelpad=10)
    plt.ylabel('地区', fontsize=12, labelpad=10)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    set_chart_title(plt.gca(), "关键指标水平排序对比")
    plt.tight_layout()
    # plt.show()

    # 运行所有图表

if __name__ == "__main__":
    plot_bar_horizontal()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_bar_horizontal")
