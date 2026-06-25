import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 热图
def plot_heat(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    plt.figure(figsize=(6,5))
    data = np.random.rand(5,5)  # 5x5随机数据
    plt.imshow(data, cmap=DIVERGING_CMAP)
    plt.colorbar(label='值')
    plt.xticks(range(5), [f'X{i}' for i in range(5)])
    plt.yticks(range(5), [f'Y{i}' for i in range(5)])
    set_chart_title(plt.gca(), "样本指标热力分布")
    # plt.show()

    # 相关性热图

if __name__ == "__main__":
    plot_heat()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_heat")
