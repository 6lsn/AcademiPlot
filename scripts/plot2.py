import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 分组点图（极简版）
def plot2(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    plt.figure()
    for i in range(3):
        x = np.random.normal(i, 0.5, 30)
        y = np.random.normal(i, 0.5, 30)
        plt.scatter(x, y, label=f'组{i+1}')
    plt.legend()
    set_chart_title(plt.gca(), "三类样本二维特征分布")
    plt.tight_layout()

if __name__ == "__main__":
    plot2()
    save_current_figure(Path(__file__).stem)
    print("Done: plot2")
