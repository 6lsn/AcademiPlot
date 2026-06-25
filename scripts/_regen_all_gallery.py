"""Regenerate ALL gallery images with updated grid color (#D1D5DB).
Keeps original data, colors, and titles — only grid line color changes.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import math, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from style import (apply_paper_style, COLORS, palette, PAPER_CMAP, DIVERGING_CMAP,
                   set_chart_title, style_axis, style_3d_axis, finalize_plot,
                   save_current_figure)

# Override grid color
COLORS["grid"] = "#D1D5DB"

OUT = Path(__file__).resolve().parents[1] / "gallery" / "showcase"
OUT.mkdir(parents=True, exist_ok=True)
np.random.seed(42)


def save(fig, name):
    path = OUT / f"{name}.png"
    fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print(f"Saved {name}.png")


# ================================================================
# 1. Line
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(0, 12, 100)
y = np.sin(x) * 10 + 50 + np.random.randn(100) * 2
ax.plot(x, y, color=COLORS["blue"], linewidth=2.5, marker="o", markersize=5,
        markerfacecolor=COLORS["amber"], markeredgecolor=COLORS["blue"], markeredgewidth=1.5)
ax.set_xlabel("Time", fontsize=12, labelpad=10)
ax.set_ylabel("Value", fontsize=12, labelpad=10)
set_chart_title(ax, "Daily Renewable Energy Output")
ax.legend(["Wind", "Solar", "Hybrid"], loc="upper right", frameon=False)
style_axis(ax, grid=True, grid_axis="y")
fig.tight_layout()
save(fig, "line")

# ================================================================
# 2. Bar (horizontal)
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5))
methods = ["Proposed", "Opt-v3", "Opt-v2", "Opt-v1", "Baseline"]
scores = [95, 91, 83, 78, 72]
colors = [COLORS["crimson"] if s == max(scores) else COLORS["blue"] for s in scores]
bars = ax.barh(methods, scores, color=colors, edgecolor="white", linewidth=1.5, height=0.6)
for bar, s in zip(bars, scores):
    ax.text(s + 0.5, bar.get_y() + bar.get_height() / 2, f"{s}%",
            va="center", fontsize=10, fontweight="bold")
ax.set_xlabel("Accuracy (%)")
ax.set_xlim(60, 100)
set_chart_title(ax, "Model Performance Comparison")
ax.invert_yaxis()
style_axis(ax, grid=True, grid_axis="x")
fig.tight_layout()
save(fig, "bar")

# ================================================================
# 3. Scatter
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5))
x = np.random.uniform(10, 100, 50)
y = 0.8 * x + np.random.randn(50) * 10 + 10
ax.scatter(x, y, c=COLORS["blue"], alpha=0.7, s=80, edgecolors="w", linewidth=1.5)
z = np.polyfit(x, y, 1); p = np.poly1d(z)
x_line = np.linspace(10, 100, 100)
ax.plot(x_line, p(x_line), color=COLORS["crimson"], linewidth=2, linestyle="--")
r2 = 1 - np.sum((y - p(x)) ** 2) / np.sum((y - y.mean()) ** 2)
ax.text(0.05, 0.92, f"R² = {r2:.3f}", transform=ax.transAxes,
        fontsize=11, color=COLORS["crimson"], fontweight="bold")
ax.set_xlabel("Investment ($10k)")
ax.set_ylabel("Revenue ($10k)")
set_chart_title(ax, "Investment vs Revenue")
style_axis(ax, grid=True, grid_axis="y")
fig.tight_layout()
save(fig, "scatter")

# ================================================================
# 4. Heatmap
# ================================================================
fig, ax = plt.subplots(figsize=(8, 6))
labels = ["Cost", "Efficiency", "Quality", "Safety", "Reliability"]
corr = np.array([
    [1.00, 0.82, 0.31, -0.15, 0.28],
    [0.82, 1.00, 0.55, -0.08, 0.45],
    [0.31, 0.55, 1.00, 0.42, 0.71],
    [-0.15, -0.08, 0.42, 1.00, 0.35],
    [0.28, 0.45, 0.71, 0.35, 1.00],
])
im = ax.imshow(corr, cmap=PAPER_CMAP, vmin=-1, vmax=1)
ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, rotation=45, ha="right")
ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels)
for i in range(len(labels)):
    for j in range(len(labels)):
        ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center", fontsize=10,
                color="white" if abs(corr[i, j]) > 0.5 else "black")
fig.colorbar(im, ax=ax, label="Correlation", shrink=0.8)
set_chart_title(ax, "Indicator Correlation Matrix")
fig.tight_layout()
save(fig, "heatmap")

# ================================================================
# 5. Box Plot
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5))
data = [np.random.normal(85, 5, 30), np.random.normal(78, 10, 30),
        np.random.normal(90, 4, 30), np.random.normal(65, 12, 30)]
bp = ax.boxplot(data, tick_labels=["CNN", "RNN", "Transformer", "Baseline"],
                patch_artist=True, widths=0.5)
box_colors = [COLORS["blue"], COLORS["crimson"], COLORS["seagreen"], COLORS["amber"]]
for patch, c in zip(bp["boxes"], box_colors):
    patch.set_facecolor(c); patch.set_alpha(0.7)
ax.set_ylabel("Accuracy (%)")
set_chart_title(ax, "Model Accuracy Distribution")
style_axis(ax, grid=True, grid_axis="y")
fig.tight_layout()
save(fig, "boxplot")

# ================================================================
# 6. Radar
# ================================================================
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
labels_r = ["Accuracy", "Speed", "Robustness", "Scalability", "Memory"]
angles = np.linspace(0, 2 * np.pi, len(labels_r), endpoint=False).tolist()
values = [0.92, 0.85, 0.78, 0.88, 0.70]
values += values[:1]; angles += angles[:1]
ax.plot(angles, values, color=COLORS["blue"], linewidth=2.5, marker="o", markersize=6)
ax.fill(angles, values, color=COLORS["blue"], alpha=0.15)
ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels_r, fontsize=10)
ax.set_ylim(0, 1)
set_chart_title(ax, "Multi-dimensional Evaluation")
fig.tight_layout()
save(fig, "radar")

# ================================================================
# 7. Histogram
# ================================================================
fig, ax1 = plt.subplots(figsize=(8, 5))
data = np.random.normal(100, 15, 500)
n, bins, patches = ax1.hist(data, bins=30, density=True, alpha=0.7, color=COLORS["blue"],
                             edgecolor="white", linewidth=0.8)
ax1.set_xlabel("Error (ms)")
ax1.set_ylabel("Frequency")
ax2 = ax1.twinx()
from scipy.stats import norm
x_fit = np.linspace(bins.min(), bins.max(), 200)
ax2.plot(x_fit, norm.pdf(x_fit, 100, 15), color=COLORS["crimson"], linewidth=2)
ax2.set_ylabel("Density")
set_chart_title(ax1, "Prediction Error Distribution")
style_axis(ax1, grid=True, grid_axis="y")
fig.tight_layout()
save(fig, "histogram")

# ================================================================
# 8. Stacked Bar
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5))
quarters = ["Q1", "Q2", "Q3", "Q4"]
materials = [30, 35, 28, 32]
labor = [20, 22, 18, 25]
overhead = [10, 12, 9, 11]
x = np.arange(len(quarters))
ax.bar(x, materials, label="Materials", color=COLORS["blue"], edgecolor="white", linewidth=1.2)
ax.bar(x, labor, bottom=materials, label="Labor", color=COLORS["seagreen"], edgecolor="white", linewidth=1.2)
ax.bar(x, overhead, bottom=[m + l for m, l in zip(materials, labor)],
       label="Overhead", color=COLORS["amber"], edgecolor="white", linewidth=1.2)
ax.set_xticks(x); ax.set_xticklabels(quarters)
ax.set_ylabel("Cost ($10k)")
ax.legend(loc="upper right", frameon=False)
set_chart_title(ax, "Quarterly Cost Breakdown")
style_axis(ax, grid=True, grid_axis="y")
fig.tight_layout()
save(fig, "stacked_bar")

# ================================================================
# 9. Pareto
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5))
costs = np.array([10, 12, 15, 17, 20, 22, 25, 27, 30])
quality = np.array([0.92, 0.88, 0.85, 0.80, 0.75, 0.70, 0.65, 0.58, 0.50])
ax.plot(costs, quality, color=COLORS["crimson"], linewidth=2, marker="o",
        markersize=6, markerfacecolor=COLORS["crimson"], markeredgecolor="white",
        label="Pareto frontier")
ax.set_xlabel("Cost ($10k)")
ax.set_ylabel("Quality Score")
set_chart_title(ax, "Multi-objective Optimization")
ax.legend(frameon=False)
style_axis(ax, grid=True, grid_axis="both")
fig.tight_layout()
save(fig, "pareto")

# ================================================================
# 10. Contour
# ================================================================
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(0, 10, 50)
y = np.linspace(0, 10, 50)
X, Y = np.meshgrid(x, y)
Z = (X - 5) ** 2 + (Y - 5) ** 2 + 2 * np.sin(X) * np.cos(Y)
cs = ax.contourf(X, Y, Z, levels=20, cmap=PAPER_CMAP, alpha=0.92)
ax.contour(X, Y, Z, levels=10, colors="white", linewidths=0.5, alpha=0.5)
ax.scatter([5], [5], c="white", s=120, marker="*", edgecolors=COLORS["crimson"],
           linewidth=1.5, zorder=10, label="Optimum")
ax.scatter([3], [7], c="white", s=80, marker="*", edgecolors=COLORS["amber"],
           linewidth=1.2, zorder=10, label="Local min")
fig.colorbar(cs, ax=ax, label="Objective Value", shrink=0.8)
ax.set_xlabel("Parameter α")
ax.set_ylabel("Parameter β")
ax.legend(loc="upper right", frameon=False)
set_chart_title(ax, "Parameter Optimization Landscape")
fig.tight_layout()
save(fig, "contour")

# ================================================================
# 11. Waterfall
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5))
cats = ["Base", "Material\n+", "Labor\n+", "Overhead\n−", "Savings\n−", "Final"]
values = [100, 20, 15, -8, -12, 115]
cumulative = [0, 100, 120, 135, 127, 115]
bar_colors = [COLORS["blue"], COLORS["seagreen"], COLORS["seagreen"],
              COLORS["crimson"], COLORS["crimson"], COLORS["blue"]]
bottoms = [0, 100, 120, 127, 115, 0]
heights = [100, 20, 15, 8, 12, 115]

bars = ax.bar(cats, heights, bottom=bottoms, color=bar_colors, edgecolor="white", linewidth=1.5)
for i, (b, h) in enumerate(zip(bottoms, heights)):
    if i == 0 or i == len(bars) - 1:
        ax.text(i, b + h + 2, f"+{h}" if i == 0 else f"+{h}", ha="center", fontsize=10, fontweight="bold")
    else:
        sign = "+" if values[i] > 0 else ""
        ax.text(i, b + h + 2, f"{sign}{values[i]}", ha="center", fontsize=10, fontweight="bold")
# connector lines
for i in range(len(cats) - 1):
    top = bottoms[i] + heights[i]
    ax.plot([i + 0.4, i + 0.6], [top, top], color=COLORS["axis"], linewidth=0.8)

ax.set_ylabel("Cost ($10k)")
set_chart_title(ax, "Cost Decomposition Waterfall")
style_axis(ax, grid=True, grid_axis="y")
fig.tight_layout()
save(fig, "waterfall")

# ================================================================
# 12. Dumbbell
# ================================================================
fig, ax = plt.subplots(figsize=(8, 5))
methods = ["Method A", "Method B", "Method C", "Method D"]
before = [72, 65, 80, 58]
after = [88, 82, 85, 77]
y_pos = np.arange(len(methods))

for i in range(len(methods)):
    ax.plot([before[i], after[i]], [i, i], color=COLORS["grid"], linewidth=3, solid_capstyle="round", zorder=1)
    saving = (before[i] - after[i]) / before[i] * -100
    ax.text(max(before[i], after[i]) + 1, i, f"+{abs(after[i] - before[i])}",
            va="center", fontsize=9, color=COLORS["seagreen"], fontweight="bold")

ax.scatter(before, y_pos, s=80, color=COLORS["blue"], label="Before", zorder=3, edgecolors="white")
ax.scatter(after, y_pos, s=80, color=COLORS["crimson"], label="After", zorder=3, edgecolors="white")
ax.set_yticks(y_pos); ax.set_yticklabels(methods)
ax.set_xlabel("Accuracy (%)")
ax.legend(loc="lower right", frameon=False)
ax.invert_yaxis()
set_chart_title(ax, "Before vs After Optimization")
style_axis(ax, grid=True, grid_axis="x")
fig.tight_layout()
save(fig, "dumbbell")

print(f"\nAll 12 gallery images regenerated in {OUT}")
