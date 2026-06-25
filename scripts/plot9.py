import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 彩色散点图（极简版）
def plot9(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    plt.figure()
    x = np.random.randn(100)
    y = np.random.randn(100)
    c = x + y
    plt.scatter(x, y, c=c)
    set_chart_title(plt.gca(), "双变量综合色阶散点分布")
    plt.tight_layout()

if __name__ == "__main__":
    plot9()
    save_current_figure(Path(__file__).stem)
    print("Done: plot9")
