import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from style import COLORS, PAPER_CMAP, apply_paper_style, finalize_plot, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()


# 3D柱状图
def plot_3d_bar_chart(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    x_labels = ["A", "B", "C", "D"]
    y_labels = ["指标1", "指标2", "指标3"]
    values = np.array(
        [
            [12, 18, 10, 15],
            [9, 14, 20, 17],
            [16, 11, 13, 19],
        ],
        dtype=float,
    )
    y, x = np.indices(values.shape)
    x = x.ravel()
    y = y.ravel()
    dz = values.ravel()
    z = np.zeros_like(dz)
    dx = np.full_like(dz, 0.58, dtype=float)
    dy = np.full_like(dz, 0.58, dtype=float)

    fig = plt.figure(figsize=(8, 5.6))
    ax = fig.add_subplot(111, projection="3d")
    norm = plt.Normalize(dz.min(), dz.max())
    bars = ax.bar3d(
        x,
        y,
        z,
        dx,
        dy,
        dz,
        color=PAPER_CMAP(norm(dz)),
        alpha=0.86,
        shade=True,
    )

    ax.set_xticks(np.arange(len(x_labels)) + 0.3)
    ax.set_xticklabels(x_labels)
    ax.set_yticks(np.arange(len(y_labels)) + 0.3)
    ax.set_yticklabels(y_labels)
    ax.set_zlabel("得分")
    ax.view_init(elev=26, azim=-48)
    style_3d_axis(ax, elev=26, azim=-48)

    mappable = plt.cm.ScalarMappable(norm=norm, cmap=PAPER_CMAP)
    mappable.set_array(dz)
    fig.colorbar(mappable, ax=ax, shrink=0.68, pad=0.12, label="得分")
    set_chart_title(plt.gca(), "多方案多指标三维得分对比")
    return fig, ax


if __name__ == "__main__":
    plot_3d_bar_chart()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_3d_bar_chart")
