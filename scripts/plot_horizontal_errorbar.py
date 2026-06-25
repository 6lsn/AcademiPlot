import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 横向误差棒图
def plot_horizontal_errorbar(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    y = np.arange(8)
    x = np.random.rand(8) * 100
    xerr = np.random.rand(8) * 8 + 2
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.errorbar(x, y, xerr=xerr, fmt='o', ecolor=COLORS["crimson"], capsize=5,
                markerfacecolor=COLORS["blue"])
    ax.set_xlabel('测量值')
    ax.set_ylabel('样本')
    ax.set_yticks(y)
    ax.set_yticklabels([f'样本{i+1}' for i in y])
    set_chart_title(plt.gca(), "多指标估计值及横向误差范围")
    plt.tight_layout()
    # plt.show()

if __name__ == "__main__":
    plot_horizontal_errorbar()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_horizontal_errorbar")
