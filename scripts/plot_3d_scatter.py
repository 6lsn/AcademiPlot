import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from style import COLORS, PAPER_CMAP, apply_paper_style, finalize_plot, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()


# 3D散点图
def plot_3d_scatter(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    rng = np.random.default_rng(42)
    x = rng.normal(0, 1.0, 80)
    y = 0.65 * x + rng.normal(0, 0.55, 80)
    z = 0.45 * x - 0.35 * y + rng.normal(0, 0.4, 80)
    score = x + y + z

    fig = plt.figure(figsize=(8, 5.6))
    ax = fig.add_subplot(111, projection="3d")
    scatter = ax.scatter(
        x,
        y,
        z,
        c=score,
        cmap=PAPER_CMAP,
        s=44,
        alpha=0.88,
        edgecolors="white",
        linewidth=0.35,
    )
    ax.set_xlabel("指标X")
    ax.set_ylabel("指标Y")
    ax.set_zlabel("指标Z")
    ax.view_init(elev=24, azim=-48)
    style_3d_axis(ax, elev=24, azim=-48)
    fig.colorbar(scatter, ax=ax, shrink=0.68, pad=0.12, label="综合得分")
    set_chart_title(plt.gca(), "三维聚类特征综合得分分布")
    return fig, ax


if __name__ == "__main__":
    plot_3d_scatter()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_3d_scatter")
