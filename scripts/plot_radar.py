import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 雷达图
def plot_radar(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    plt.figure(figsize=(6,6))
    ax = plt.subplot(111, polar=True)
    labels = ['指标1', '指标2', '指标3', '指标4']
    values1 = [80, 90, 70, 60]
    values2 = [60, 70, 80, 90]
    
    angles = np.linspace(0, 2*np.pi, 4, endpoint=False).tolist()
    values1 += values1[:1]
    values2 += values2[:1]
    angles += angles[:1]
    
    ax.plot(angles, values1, color=COLORS["blue"], linestyle="-", linewidth=2, label='数据1')
    ax.fill(angles, values1, color=COLORS["blue"], alpha=0.2)
    ax.plot(angles, values2, color=COLORS["seagreen"], linestyle="-", linewidth=2, label='数据2')
    ax.fill(angles, values2, color=COLORS["seagreen"], alpha=0.2)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    ax.legend(loc="upper right", frameon=False)
    set_chart_title(plt.gca(), "两方案多指标综合评价")
    # plt.show()

    # 热图

if __name__ == "__main__":
    plot_radar()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_radar")
