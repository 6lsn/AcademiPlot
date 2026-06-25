import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from style import COLORS, apply_paper_style, finalize_plot, palette, save_current_figure, set_chart_title

apply_paper_style()


# Mosaic plot / 马赛克图
def plot5(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    row_labels = ["方案A", "方案B", "方案C"]
    col_labels = ["低风险", "中风险", "高风险"]
    data = np.array(
        [
            [42, 28, 10],
            [22, 46, 18],
            [18, 25, 31],
        ],
        dtype=float,
    )

    row_totals = data.sum(axis=1)
    total = row_totals.sum()
    row_widths = row_totals / total
    within_row_proportion = data / row_totals[:, None]

    fig, ax = plt.subplots(figsize=(8, 5))
    x_left = 0.0
    colors = palette(len(col_labels))

    for row_index, row_name in enumerate(row_labels):
        y_bottom = 0.0
        for col_index, col_name in enumerate(col_labels):
            height = within_row_proportion[row_index, col_index]
            rect = plt.Rectangle(
                (x_left, y_bottom),
                row_widths[row_index],
                height,
                facecolor=colors[col_index],
                edgecolor="white",
                linewidth=1.4,
                alpha=0.88,
                label=col_name if row_index == 0 else None,
            )
            ax.add_patch(rect)
            proportion = data[row_index, col_index] / total
            if proportion >= 0.08:
                ax.text(
                    x_left + row_widths[row_index] / 2,
                    y_bottom + height / 2,
                    f"{proportion:.0%}",
                    ha="center",
                    va="center",
                    color="white" if col_index in (0, 2) else COLORS["text"],
                    fontsize=9,
                    weight="bold",
                )
            y_bottom += height

        ax.text(
            x_left + row_widths[row_index] / 2,
            -0.06,
            f"{row_name}\n{row_totals[row_index]:.0f}",
            ha="center",
            va="top",
            fontsize=10,
            color=COLORS["axis"],
        )
        x_left += row_widths[row_index]

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.14, 1)
    ax.set_ylabel("组内构成比例")
    ax.set_xticks([])
    ax.set_yticks(np.linspace(0, 1, 6))
    ax.set_yticklabels([f"{value:.0%}" for value in np.linspace(0, 1, 6)])
    ax.legend(title="风险等级")
    set_chart_title(plt.gca(), "不同方案风险等级构成")
    return fig, ax


if __name__ == "__main__":
    plot5()
    save_current_figure(Path(__file__).stem)
    print("Done: plot5")
