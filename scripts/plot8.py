import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from style import COLORS, apply_paper_style, finalize_plot, palette, save_current_figure, set_chart_title

apply_paper_style()


def linkage(data):
    active = {i: [i] for i in range(len(data))}
    heights = {i: 0.0 for i in active}
    centers = {i: float(i) for i in active}
    next_id = len(data)
    merges = []

    while len(active) > 1:
        keys = list(active)
        best_pair = None
        best_distance = float("inf")
        for i, left in enumerate(keys[:-1]):
            for right in keys[i + 1 :]:
                left_points = data[active[left]]
                right_points = data[active[right]]
                distance = np.linalg.norm(left_points.mean(axis=0) - right_points.mean(axis=0))
                if distance < best_distance:
                    best_distance = distance
                    best_pair = (left, right)

        left, right = best_pair
        merged_members = active[left] + active[right]
        merges.append(
            {
                "left": left,
                "right": right,
                "height": best_distance,
                "left_height": heights[left],
                "right_height": heights[right],
                "center": (centers[left] + centers[right]) / 2,
                "left_center": centers[left],
                "right_center": centers[right],
            }
        )
        active[next_id] = merged_members
        centers[next_id] = (centers[left] + centers[right]) / 2
        heights[next_id] = best_distance
        del active[left], active[right]
        next_id += 1

    return merges


def dendrogram(ax, merges, labels):
    colors = palette(len(merges))
    max_height = max(item["height"] for item in merges)
    for index, item in enumerate(merges):
        color = colors[index]
        ax.plot(
            [item["left_center"], item["left_center"]],
            [item["left_height"], item["height"]],
            color=color,
            linewidth=1.8,
        )
        ax.plot(
            [item["right_center"], item["right_center"]],
            [item["right_height"], item["height"]],
            color=color,
            linewidth=1.8,
        )
        ax.plot(
            [item["left_center"], item["right_center"]],
            [item["height"], item["height"]],
            color=color,
            linewidth=1.8,
        )
        ax.text(
            item["center"],
            item["height"] + max_height * 0.03,
            f"{item['height']:.2f}",
            ha="center",
            va="bottom",
            fontsize=8,
            color=COLORS["axis"],
        )

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=11, rotation=20, ha="right")
    ax.set_ylabel("聚类距离")
    ax.set_ylim(0, max_height * 1.18)


# 树状图
def plot8(annotate=False, annotation_mode=None, annotation_config=None, auto_annotation=False):
    labels = ["城市A", "城市B", "城市C", "城市D", "城市E", "城市F"]
    data = np.array(
        [
            [0.82, 0.35, 0.68],
            [0.78, 0.38, 0.64],
            [0.31, 0.81, 0.42],
            [0.35, 0.77, 0.39],
            [0.58, 0.51, 0.86],
            [0.62, 0.48, 0.82],
        ]
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    dendrogram(ax, linkage(data), labels)
    set_chart_title(plt.gca(), "城市综合指标层次聚类结果")
    return fig, ax


if __name__ == "__main__":
    plot8()
    save_current_figure(Path(__file__).stem)
    print("Done: plot8")
