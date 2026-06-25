import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 直方图 + 核密度图
def plot_histogram_with_kde(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    # 固定数据
    data = np.array([30, 35, 40, 45, 50, 55, 60, 65, 70, 75] * 40)
    
    # 固定的核密度曲线
    x = np.linspace(20, 85, 100)
    kde = np.exp(-0.5 * ((x - 50) / 15)**2) / (15 * np.sqrt(2 * np.pi))
    
    fig, ax = plt.subplots()
    ax.hist(data, bins=15, density=True, alpha=0.6)
    ax.plot(x, kde, color=COLORS["crimson"], linewidth=2)
    
    ax.set_xlabel('数值')
    ax.set_ylabel('密度')
    set_chart_title(plt.gca(), "样本分布与核密度估计")
    
    plt.tight_layout()
    # plt.show()

    # 7. 箱线图

if __name__ == "__main__":
    plot_histogram_with_kde()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_histogram_with_kde")
