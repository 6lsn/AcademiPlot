import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 带趋势线的散点图
def plot_scatter_with_trend(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    y = 3 * x + 15 + np.random.randn(100) * 5
    
    # 计算趋势线
    slope, intercept = np.polyfit(x, y, 1)
    r_value = np.corrcoef(x, y)[0, 1]
    trend_line = slope * x + intercept
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y, c=COLORS["crimson"], alpha=0.6, edgecolors='w', s=60, linewidth=1, label='数据点')
    ax.plot(x, trend_line, color=COLORS["blue"], linestyle="--", linewidth=2.5, label="趋势线")
    ax.text(
        0.62,
        0.12,
        f"趋势线: y = {slope:.2f}x + {intercept:.2f}\nR² = {r_value**2:.4f}",
        transform=ax.transAxes,
        fontsize=10.5,
        ha="left",
        va="bottom",
        bbox=dict(
            boxstyle="round,pad=0.25",
            facecolor="white",
            edgecolor="#D1D5DB",
            alpha=0.85,
        ),
    )
    ax.set_xlabel('X轴', fontsize=12, labelpad=10)
    ax.set_ylabel('Y轴', fontsize=12, labelpad=10)
    ax.legend(loc="upper left", frameon=False)
    ax.grid(True, linestyle='--', alpha=0.6)
    set_chart_title(plt.gca(), "变量关系拟合趋势分析")
    plt.tight_layout()
    # plt.show()

    # 3. 分组散点图

if __name__ == "__main__":
    plot_scatter_with_trend()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_scatter_with_trend")
