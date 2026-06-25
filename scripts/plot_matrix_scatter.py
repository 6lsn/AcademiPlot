import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 矩阵散点图
def plot_matrix_scatter(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    np.random.seed(42)
    n = 50
    v1 = np.random.normal(0, 1, n)
    v2 = np.random.normal(2, 1, n)
    v3 = np.random.normal(-1, 0.8, n)
    vars = [v1, v2, v3]
    names = ['变量1', '变量2', '变量3']
    
    fig, axes = plt.subplots(3, 3, figsize=(10, 8))
    
    for i in range(3):
        for j in range(3):
            ax = axes[i, j]
            if i != j:
                ax.scatter(vars[j], vars[i], alpha=0.62, s=18, color=COLORS["blue"])
            else:
                ax.hist(vars[i], bins=10, alpha=0.75, color=COLORS["seagreen"])
            
            if i == 2:
                ax.set_xlabel(names[j])
            if j == 0:
                ax.set_ylabel(names[i])
    set_chart_title(plt.gca(), "多变量联合分布矩阵")
    
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.18, hspace=0.18)
    # plt.show()

if __name__ == "__main__":
    plot_matrix_scatter()
    save_current_figure(Path(__file__).stem)
    print("Done: plot_matrix_scatter")
