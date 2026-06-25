"""Generate publication-quality gallery images for AcademiPlot.

Run: python scripts/generate_gallery.py
"""
import sys
sys.path.insert(0, "src")

import acadp
from acadp._style import COLORS, PALETTE, DIVERGING_CMAP, PAPER_CMAP
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

acadp.set_style("nature")
np.random.seed(42)

gallery = Path("gallery/showcase")
gallery.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    fig.savefig(gallery / f"{name}.png", dpi=200, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)


# ── 1. Line plot (multi-series) ──
fig, ax = plt.subplots(figsize=(5, 3.2))
x = np.linspace(0, 10, 80)
colors = [COLORS["navy"], COLORS["coral"], COLORS["teal"]]
labels = ["Wind", "Solar", "Hybrid"]
for c, lbl, shift in zip(colors, labels, [0, 3, 6]):
    ax.plot(x, np.sin(x + shift) * 8 + 50 + np.random.randn(80) * 1.5,
            color=c, label=lbl, linewidth=1.5, alpha=0.9)
ax.set_xlabel("Time (h)")
ax.set_ylabel("Output (MW)")
ax.set_title("Daily Renewable Energy Output")
ax.legend(frameon=False, fontsize=8, loc="upper right")
save(fig, "line")


# ── 2. Bar plot with highlight ──
fig, ax = plt.subplots(figsize=(5, 3.2))
methods = ["Baseline", "Opt-v1", "Opt-v2", "Opt-v3", "Proposed"]
scores = [72, 78, 83, 81, 91]
colors_bar = [COLORS["slate"]] * 4 + [COLORS["coral"]]
bars = ax.barh(methods, scores, color=colors_bar, edgecolor="white", height=0.6)
bars[-1].set_edgecolor(COLORS["amber"])
bars[-1].set_linewidth(2)
ax.set_xlabel("Accuracy (%)")
ax.set_xlim(60, 100)
ax.set_title("Model Performance Comparison")
for bar, s in zip(bars, scores):
    ax.text(s + 0.5, bar.get_y() + bar.get_height()/2, f"{s}%",
            va="center", fontsize=8, color="#555555")
save(fig, "bar")


# ── 3. Scatter with trend ──
fig, ax = plt.subplots(figsize=(5, 3.2))
n = 60
x_sc = np.random.uniform(10, 100, n)
y_sc = 0.8 * x_sc + np.random.randn(n) * 12 + 20
ax.scatter(x_sc, y_sc, c=COLORS["navy"], s=30, alpha=0.7,
           edgecolors="white", linewidth=0.8)
z = np.polyfit(x_sc, y_sc, 1)
p = np.poly1d(z)
x_line = np.linspace(10, 100, 100)
ax.plot(x_line, p(x_line), color=COLORS["coral"],
        linewidth=1.5, linestyle="--")
r = np.corrcoef(x_sc, y_sc)[0, 1]
ax.annotate(f"R² = {r**2:.3f}", xy=(0.05, 0.92), xycoords="axes fraction",
            fontsize=9, color=COLORS["coral"], va="top")
ax.set_xlabel("Investment ($10k)")
ax.set_ylabel("Revenue ($10k)")
ax.set_title("Investment vs Revenue")
save(fig, "scatter")


# ── 4. Heatmap ──
fig, ax = plt.subplots(figsize=(4.5, 3.8))
labels_hm = ["Cost", "Efficiency", "Quality", "Safety", "Reliability"]
corr = np.array([
    [1.00, 0.82, 0.31, -0.15, 0.28],
    [0.82, 1.00, 0.55, -0.08, 0.45],
    [0.31, 0.55, 1.00, 0.42, 0.71],
    [-0.15, -0.08, 0.42, 1.00, 0.35],
    [0.28, 0.45, 0.71, 0.35, 1.00],
])
im = ax.imshow(corr, cmap=DIVERGING_CMAP, vmin=-1, vmax=1, aspect="auto")
ax.set_xticks(range(5))
ax.set_xticklabels(labels_hm, fontsize=7.5, rotation=30, ha="right")
ax.set_yticks(range(5))
ax.set_yticklabels(labels_hm, fontsize=7.5)
for i in range(5):
    for j in range(5):
        val = corr[i, j]
        color = "white" if abs(val) > 0.5 else "#333333"
        ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                fontsize=7.5, color=color)
plt.colorbar(im, ax=ax, shrink=0.8, label="Correlation")
ax.set_title("Indicator Correlation Matrix")
save(fig, "heatmap")


# ── 5. Box plot ──
fig, ax = plt.subplots(figsize=(5, 3.2))
data_bp = {
    "CNN": np.random.normal(85, 8, 40),
    "RNN": np.random.normal(78, 12, 40),
    "Transformer": np.random.normal(91, 6, 40),
    "Baseline": np.random.normal(65, 15, 40),
}
bp = ax.boxplot(data_bp.values(), labels=data_bp.keys(), patch_artist=True,
                widths=0.5, showfliers=False)
for patch, color in zip(bp["boxes"],
                         [COLORS["navy"], COLORS["coral"],
                          COLORS["teal"], COLORS["slate"]]):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
    patch.set_edgecolor("white")
    patch.set_linewidth(0.8)
ax.set_ylabel("Accuracy (%)")
ax.set_title("Model Accuracy Distribution")
save(fig, "boxplot")


# ── 6. Radar ──
fig, ax = plt.subplots(figsize=(4.5, 4), subplot_kw={"projection": "polar"})
categories = ["Speed", "Accuracy", "Memory", "Scalability", "Robustness"]
values = [0.85, 0.92, 0.70, 0.78, 0.88]
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
values_plot = values + [values[0]]
angles += angles[:1]
ax.plot(angles, values_plot, color=COLORS["navy"], linewidth=2, marker="o", markersize=4)
ax.fill(angles, values_plot, color=COLORS["navy"], alpha=0.12)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=8.5)
ax.set_ylim(0, 1)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=7, color="#999999")
ax.set_title("Multi-dimensional Evaluation", y=1.08, fontsize=10, fontweight="bold")
save(fig, "radar")


# ── 7. Histogram with KDE ──
fig, ax = plt.subplots(figsize=(5, 3.2))
vals = np.concatenate([np.random.normal(100, 12, 300),
                        np.random.normal(115, 8, 200)])
ax.hist(vals, bins=35, color=COLORS["navy"], alpha=0.6,
        edgecolor="white", linewidth=0.5, density=True)
from scipy.stats import gaussian_kde
kde = gaussian_kde(vals)
x_range = np.linspace(vals.min(), vals.max(), 200)
ax2 = ax.twinx()
ax2.plot(x_range, kde(x_range), color=COLORS["coral"], linewidth=1.8)
ax2.fill_between(x_range, kde(x_range), alpha=0.08, color=COLORS["coral"])
ax2.set_ylabel("Density", fontsize=8)
ax2.tick_params(labelsize=7.5)
ax2.spines["top"].set_visible(False)
ax.set_xlabel("Error (ms)")
ax.set_ylabel("Frequency")
ax.set_title("Prediction Error Distribution")
save(fig, "histogram")


# ── 8. Stacked bar ──
fig, ax = plt.subplots(figsize=(5, 3.2))
quarters = ["Q1", "Q2", "Q3", "Q4"]
materials = [30, 35, 28, 32]
labor = [20, 22, 18, 25]
overhead = [10, 12, 8, 15]
x_sb = np.arange(len(quarters))
colors_sb = [COLORS["navy"], COLORS["teal"], COLORS["amber"]]
ax.bar(x_sb, materials, label="Materials", color=colors_sb[0], edgecolor="white", width=0.6)
ax.bar(x_sb, labor, bottom=materials, label="Labor", color=colors_sb[1], edgecolor="white", width=0.6)
ax.bar(x_sb, overhead, bottom=[m+l for m, l in zip(materials, labor)],
       label="Overhead", color=colors_sb[2], edgecolor="white", width=0.6)
ax.set_xticks(x_sb)
ax.set_xticklabels(quarters)
ax.set_ylabel("Cost ($10k)")
ax.set_title("Quarterly Cost Breakdown")
ax.legend(frameon=False, fontsize=8)
save(fig, "stacked_bar")


# ── 9. Pareto frontier ──
fig, ax = plt.subplots(figsize=(5, 3.2))
costs = np.array([10, 18, 15, 28, 22, 12, 25, 20, 16, 30])
quality = np.array([0.92, 0.75, 0.83, 0.55, 0.68, 0.88, 0.60, 0.70, 0.80, 0.50])
ax.scatter(costs, quality, c=COLORS["navy"], s=50, alpha=0.8,
           edgecolors="white", linewidth=0.8, zorder=3)
pts = np.column_stack([costs, quality])
mask = np.ones(len(pts), dtype=bool)
for i, p in enumerate(pts):
    dom = np.all(pts <= p, axis=1) & np.any(pts < p, axis=1)
    mask[i] = not np.any(dom & (np.arange(len(pts)) != i))
frontier = pts[mask]
sort_idx = np.argsort(frontier[:, 0])
frontier = frontier[sort_idx]
ax.plot(frontier[:, 0], frontier[:, 1], color=COLORS["coral"],
        linewidth=2, linestyle="--", marker="o", markersize=5,
        markerfacecolor=COLORS["coral"], markeredgecolor="white",
        markeredgewidth=0.8, zorder=4, label="Pareto frontier")
ax.set_xlabel("Cost ($10k)")
ax.set_ylabel("Quality Score")
ax.set_title("Multi-objective Optimization")
ax.legend(frameon=False, fontsize=8)
save(fig, "pareto")


# ── 10. Contour ──
fig, ax = plt.subplots(figsize=(5, 3.8))
x_c = np.linspace(0, 10, 80)
y_c = np.linspace(0, 10, 80)
X, Y = np.meshgrid(x_c, y_c)
Z = -(X - 5)**2 - (Y - 5)**2 + 50 + np.sin(X) * 2
cs = ax.contourf(X, Y, Z, levels=20, cmap=PAPER_CMAP)
plt.colorbar(cs, ax=ax, shrink=0.8, label="Objective Value")
ax.scatter([5], [5], c=COLORS["coral"], s=150, marker="*",
           edgecolors="white", linewidth=1.5, zorder=10, label="Optimum")
ax.set_xlabel("Parameter α")
ax.set_ylabel("Parameter β")
ax.set_title("Parameter Optimization Landscape")
ax.legend(frameon=False, fontsize=8)
save(fig, "contour")


# ── 11. Waterfall ──
fig, ax = plt.subplots(figsize=(6, 3.2))
cats = ["Base", "Material\n+", "Labor\n+", "Overhead\n−", "Savings\n−", "Final"]
vals_w = [100, 20, 15, -8, -12, 115]
bottoms = [0, 100, 120, 120+15-8, 120+15-8-12, 0]
colors_w = [COLORS["navy"], COLORS["teal"], COLORS["teal"],
            COLORS["coral"], COLORS["coral"], COLORS["navy"]]
ax.bar(cats, [abs(v) for v in vals_w], bottom=bottoms,
       color=colors_w, edgecolor="white", width=0.6)
for i, (b, v) in enumerate(zip(bottoms, vals_w)):
    top = b + abs(v)
    ax.text(i, top + 2, f"{'+'if v>=0 else ''}{v}", ha="center", fontsize=8,
            fontweight="bold", color="#333333")
for i in range(len(cats) - 2):
    top = bottoms[i] + abs(vals_w[i])
    ax.plot([i + 0.3, i + 0.7], [top, top], color="#AAAAAA", linewidth=0.6)
ax.set_ylabel("Cost ($10k)")
ax.set_title("Cost Decomposition Waterfall")
save(fig, "waterfall")


# ── 12. Dumbbell ──
fig, ax = plt.subplots(figsize=(5, 3.5))
methods_d = ["Method A", "Method B", "Method C", "Method D"]
before_d = [72, 65, 80, 58]
after_d = [88, 82, 85, 75]
y_pos = np.arange(len(methods_d))
ax.plot([before_d, after_d], [y_pos, y_pos], color="#CCCCCC", linewidth=2, zorder=1)
ax.scatter(before_d, y_pos, c=COLORS["slate"], s=60, zorder=2,
           edgecolors="white", label="Before")
ax.scatter(after_d, y_pos, c=COLORS["coral"], s=60, zorder=2,
           edgecolors="white", label="After")
for i, (b, a) in enumerate(zip(before_d, after_d)):
    ax.annotate(f"{b}", (b, i), xytext=(-12, 6), textcoords="offset points",
                fontsize=7.5, color=COLORS["slate"], ha="center")
    ax.annotate(f"{a}", (a, i), xytext=(12, 6), textcoords="offset points",
                fontsize=7.5, color=COLORS["coral"], ha="center")
ax.set_yticks(y_pos)
ax.set_yticklabels(methods_d, fontsize=9)
ax.set_xlabel("Accuracy (%)")
ax.set_title("Before vs After Optimization")
ax.legend(frameon=False, fontsize=8)
save(fig, "dumbbell")


print(f"Generated {len(list(gallery.glob('*.png')))} gallery images in {gallery}")
