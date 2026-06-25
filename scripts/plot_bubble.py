import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 气泡图
def plot_bubble(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    np.random.seed(42)
    n = 50
    x = np.random.rand(n) * 100  # X坐标
    y = np.random.rand(n) * 100  # Y坐标
    sizes = np.random.rand(n) * 500 + 50  # 气泡大小
    colors = np.random.rand(n)  # 颜色值
    
    plt.figure()
    scatter = plt.scatter(x, y, s=sizes, c=colors, alpha=0.7, 
                         edgecolors='w', linewidth=1, cmap=PAPER_CMAP)
    
    # 添加颜色条
    cbar = plt.colorbar(scatter)
    cbar.set_label('重要程度', fontsize=12, labelpad=10)
    plt.xlabel('市场份额 (%)', fontsize=12, labelpad=10)
    plt.ylabel('增长率 (%)', fontsize=12, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    set_chart_title(plt.gca(), "变量关系与规模权重气泡分布")
    plt.tight_layout()
    # plt.show()

    # 5. 基础折线图

if __name__ == "__main__":
    plot_bubble()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_bubble")
