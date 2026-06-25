import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 堆叠面积图
def plot_stacked_area(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    x = np.arange(2010, 2021)
    data = np.random.randint(5, 30, size=(3, len(x)))
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.stackplot(x, data, labels=['A', 'B', 'C'], 
                colors=[COLORS["blue"], COLORS["seagreen"], COLORS["amber"]], alpha=0.8)
    ax.set_xlabel('年份')
    ax.set_ylabel('数值')
    ax.legend()
    set_chart_title(plt.gca(), "三类资源年度累积变化")
    plt.tight_layout()
    # plt.show()

if __name__ == "__main__":
    plot_stacked_area()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_stacked_area")
