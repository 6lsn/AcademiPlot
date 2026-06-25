import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 极坐标折线图
def plot_polar_line(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    theta = np.linspace(0, 2*np.pi, 100)
    r1 = 2 + np.sin(theta)*2
    r2 = 1 + np.cos(theta)*2
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    ax.plot(theta, r1, color=COLORS["blue"], linestyle="-", label='曲线1')
    ax.plot(theta, r2, color=COLORS["crimson"], linestyle="--", label='曲线2')
    ax.legend(loc="upper right", frameon=False)
    set_chart_title(plt.gca(), "周期性指标极坐标对比")
    plt.tight_layout()
    # plt.show()

if __name__ == "__main__":
    plot_polar_line()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_polar_line")
