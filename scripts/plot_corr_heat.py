import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 相关性热图
def plot_corr_heat(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    plt.figure(figsize=(6,5))
    data = np.random.randn(5, 30)  # 5个变量，30个样本
    corr = np.corrcoef(data)
    plt.imshow(corr, cmap=DIVERGING_CMAP, vmin=-1, vmax=1)
    plt.colorbar(label='相关系数')
    plt.xticks(range(5), [f'变量{i}' for i in range(5)])
    plt.yticks(range(5), [f'变量{i}' for i in range(5)])
    set_chart_title(plt.gca(), "多指标相关系数矩阵")
    # plt.show()

    # 3D散点图

if __name__ == "__main__":
    plot_corr_heat()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_corr_heat")
