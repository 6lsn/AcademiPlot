import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path

from style import COLORS, DIVERGING_CMAP, PAPER_CMAP, apply_paper_style, finalize_plot, palette, style_3d_axis, save_current_figure, set_chart_title

apply_paper_style()

# Andrews曲线（极简版）
def plot6(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    fig, ax = plt.subplots(figsize=(9, 5))
    t = np.linspace(-np.pi, np.pi, 100)
    colors = palette(10)
    for i in range(10):
        coeffs = np.random.randn(4)
        curve = coeffs[0] + coeffs[1]*np.sin(t) + coeffs[2]*np.cos(t) + coeffs[3]*np.sin(2*t)
        ax.plot(t, curve, color=colors[i], linewidth=1.25, alpha=0.75, label=f"样本{i+1}")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.22), ncol=5, frameon=False)
    ax.set_xlabel("t")
    ax.set_ylabel("曲线值")
    set_chart_title(plt.gca(), "多样本 Andrews 曲线特征对比")
    plt.tight_layout()

if __name__ == "__main__":
    plot6()
    save_current_figure(Path(__file__).stem)
    print("Done: plot6")
