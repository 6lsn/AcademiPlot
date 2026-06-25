import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 带填充区域的折线图
def plot_filled_line_chart(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.plot(x, y1, color=COLORS["blue"], linestyle="-", label='正弦')
    ax.plot(x, y2, color=COLORS["crimson"], linestyle="-", label='余弦')
    ax.fill_between(x, y1, y2, where=(y1 >= y2), color=COLORS["blue"], alpha=0.2)
    ax.fill_between(x, y1, y2, where=(y1 < y2), color=COLORS["crimson"], alpha=0.2)
    ax.set_xlabel('X轴')
    ax.set_ylabel('Y轴')
    ax.legend()
    set_chart_title(plt.gca(), "正弦与余弦差异区间")
    plt.tight_layout()
    # plt.show()

if __name__ == "__main__":
    plot_filled_line_chart()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_filled_line_chart")
