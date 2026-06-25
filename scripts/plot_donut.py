import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 环形图
def plot_donut(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    fig, ax = plt.subplots(figsize=(6, 5.4))
    labels = ['A', 'B', 'C', 'D']
    sizes = [30, 25, 25, 20]
    colors = palette(len(labels))
    
    wedges, _, autotexts = ax.pie(
        sizes,
        labels=None,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.78,
        wedgeprops=dict(width=0.32, edgecolor='w'),
    )
    ax.add_artist(plt.Circle((0, 0), 0.58, fc='white'))
    ax.axis('equal')
    ax.legend(wedges, labels, loc="upper right", frameon=False)
    for text in autotexts:
        text.set_fontsize(10)
        text.set_color(COLORS["text"])
    set_chart_title(plt.gca(), "四类资源占比结构")
    # plt.show()

    # 雷达图

if __name__ == "__main__":
    plot_donut()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_donut")
