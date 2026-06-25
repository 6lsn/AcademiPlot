import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# 彩色折线图（极简版）
def plot3(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    plt.figure()
    x = np.linspace(0, 10, 200)
    y = np.sin(x)
    plt.scatter(x, y, c=x, cmap=PAPER_CMAP, s=10)
    set_chart_title(plt.gca(), "正弦响应随输入变化的色阶分布")
    plt.tight_layout()

if __name__ == "__main__":
    plot3()
    save_current_figure(Path(__file__).stem)
    print("Done: plot3")
