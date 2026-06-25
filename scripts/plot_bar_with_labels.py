import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 带数据标签的柱状图
def plot_bar_with_labels(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    categories = ['一月', '二月', '三月', '四月', '五月']
    values1 = np.random.randint(30, 80, size=5)
    values2 = np.random.randint(20, 60, size=5)
    
    x = np.arange(len(categories))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    rects1 = ax.bar(x - width/2, values1, width, label='系列1', color='lightblue')
    rects2 = ax.bar(x + width/2, values2, width, label='系列2', color='lightgreen')
    
    # 添加标签
    for rect in rects1:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height+1,
                f'{height}', ha='center', va='bottom')
    
    for rect in rects2:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height+1,
                f'{height}', ha='center', va='bottom')
    ax.set_xlabel('月份')
    ax.set_ylabel('数值')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    set_chart_title(plt.gca(), "两组指标精确数值对比")
    plt.tight_layout()
    # plt.show()

if __name__ == "__main__":
    plot_bar_with_labels()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_bar_with_labels")
