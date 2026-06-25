import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 核密度图
def plot_kde(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    # 使用固定数据点
    x1 = np.linspace(-3, 3, 100)
    kde1 = np.exp(-0.5 * x1**2) / np.sqrt(2 * np.pi)  # 标准正态分布
    
    x2 = np.linspace(0, 6, 100)
    kde2 = np.exp(-0.5 * ((x2 - 3) / 1.5)**2) / (1.5 * np.sqrt(2 * np.pi))  # 偏移正态分布
    
    fig, ax = plt.subplots()
    ax.plot(x1, kde1, label='组A')
    ax.plot(x2, kde2, label='组B')
    ax.fill_between(x1, kde1, alpha=0.3)
    ax.fill_between(x2, kde2, alpha=0.3)
    
    ax.set_xlabel('值')
    ax.set_ylabel('密度')
    ax.legend()
    set_chart_title(plt.gca(), "两组样本核密度分布对比")
    
    plt.tight_layout()
    # plt.show()

    # 6. 直方图 + 核密度图

if __name__ == "__main__":
    plot_kde()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_kde")
