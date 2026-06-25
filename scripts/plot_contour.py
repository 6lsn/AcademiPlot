import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 等高线图
def plot_contour(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    plt.figure(figsize=(6,5))
    x = np.linspace(-3,3,30)
    y = np.linspace(-3,3,30)
    x, y = np.meshgrid(x, y)
    z = np.sin(np.sqrt(x**2 + y**2))
    plt.contourf(x, y, z, 10, cmap=DIVERGING_CMAP)
    plt.colorbar(label='值')
    set_chart_title(plt.gca(), "二维参数空间响应等高线")
    # plt.show()

    # 瀑布图（已修复形状不匹配问题）

if __name__ == "__main__":
    plot_contour()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_contour")
