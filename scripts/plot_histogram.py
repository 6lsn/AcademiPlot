import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 直方图
def plot_histogram(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    # 使用固定数据而非随机生成
    data = np.array([55, 62, 68, 72, 75, 78, 82, 85, 88, 92] * 50)
    data = np.append(data, [65, 68, 70, 73, 76, 80, 83, 86, 89, 95] * 35)
    
    fig, ax = plt.subplots()
    ax.hist(data, bins=20, alpha=0.7)
    
    ax.set_xlabel('分数')
    ax.set_ylabel('频数')
    set_chart_title(plt.gca(), "学生成绩频数分布")
    
    plt.tight_layout()
    # plt.show()

    # 5. 核密度图

if __name__ == "__main__":
    plot_histogram()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_histogram")
