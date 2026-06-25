import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 3D网格图（极简版）
def plot4(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.linspace(-3, 3, 10)
    y = np.linspace(-3, 3, 10)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) + np.cos(Y)
    ax.plot_wireframe(X, Y, Z)
    set_chart_title(plt.gca(), "空间网格响应曲面结构")
    plt.tight_layout()

if __name__ == "__main__":
    plot4()
    save_current_figure(Path(__file__).stem)
    print("Done: plot4")
