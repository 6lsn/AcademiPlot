import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from style import DIVERGING_CMAP, apply_paper_style, finalize_plot, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()


# 3D曲面图
def plot_3d_surface(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    x = np.linspace(-3, 3, 70)
    y = np.linspace(-3, 3, 70)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.08 * (X**2 + Y**2))

    fig = plt.figure(figsize=(9.5, 4.8))
    ax3d = fig.add_subplot(121, projection="3d")
    surface = ax3d.plot_surface(
        X,
        Y,
        Z,
        cmap=DIVERGING_CMAP,
        linewidth=0,
        antialiased=True,
        alpha=0.9,
    )
    ax3d.contour(
        X,
        Y,
        Z,
        zdir="z",
        offset=Z.min() - 0.08,
        cmap=DIVERGING_CMAP,
        linewidths=0.8,
    )
    ax3d.set_xlabel("X")
    ax3d.set_ylabel("Y")
    ax3d.set_zlabel("响应值")
    ax3d.view_init(elev=27, azim=-50)
    style_3d_axis(ax3d, elev=27, azim=-50)

    ax2d = fig.add_subplot(122)
    contour = ax2d.contourf(X, Y, Z, levels=16, cmap=DIVERGING_CMAP)
    ax2d.contour(X, Y, Z, levels=8, colors="white", linewidths=0.55, alpha=0.75)
    ax2d.set_xlabel("X")
    ax2d.set_ylabel("Y")

    fig.colorbar(surface, ax=[ax3d, ax2d], shrink=0.82, pad=0.04, label="响应值")
    set_chart_title(plt.gca(), "响应曲面及等高线投影")
    return fig, (ax3d, ax2d)


if __name__ == "__main__":
    plot_3d_surface()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_3d_surface")
