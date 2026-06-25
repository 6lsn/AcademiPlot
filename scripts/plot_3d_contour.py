import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 3D等高线图
def plot_3d_contour(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    x = np.linspace(-3, 3, 50)
    y = np.linspace(-3, 3, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, Z, cmap=DIVERGING_CMAP, alpha=0.8)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    set_chart_title(plt.gca(), "空间响应强度三维等高面")
    plt.tight_layout()
    # plt.show()

if __name__ == "__main__":
    plot_3d_contour()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_3d_contour")
