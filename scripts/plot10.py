import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from pathlib import Path

from style import PAPER_CMAP, apply_paper_style, finalize_plot, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()


# 3D曲面图（带光照）
def plot10(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    x = np.linspace(-2.5, 2.5, 80)
    y = np.linspace(-2.5, 2.5, 80)
    X, Y = np.meshgrid(x, y)
    Z = 1.2 * np.exp(-(X**2 + Y**2) / 2) + 0.25 * X - 0.18 * Y

    fig = plt.figure(figsize=(8, 5.6))
    ax = fig.add_subplot(111, projection="3d")
    light = LightSource(azdeg=315, altdeg=40)
    facecolors = light.shade(Z, cmap=PAPER_CMAP, vert_exag=0.7, blend_mode="soft")
    surface = ax.plot_surface(
        X,
        Y,
        Z,
        facecolors=facecolors,
        linewidth=0,
        antialiased=True,
        shade=False,
    )
    ax.contour(
        X,
        Y,
        Z,
        zdir="z",
        offset=Z.min() - 0.1,
        cmap=PAPER_CMAP,
        levels=10,
        linewidths=0.8,
    )
    ax.set_xlabel("变量X")
    ax.set_ylabel("变量Y")
    ax.set_zlabel("目标函数")
    ax.view_init(elev=28, azim=-54)
    style_3d_axis(ax, elev=28, azim=-54)

    mappable = plt.cm.ScalarMappable(cmap=PAPER_CMAP)
    mappable.set_array(Z)
    fig.colorbar(mappable, ax=ax, shrink=0.68, pad=0.12, label="目标函数")
    set_chart_title(plt.gca(), "目标函数响应曲面与光照渲染")
    return fig, ax


if __name__ == "__main__":
    plot10()
    save_current_figure(Path(__file__).stem)
    print("Done: plot10")
