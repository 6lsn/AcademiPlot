"""Generate multi-panel figures (Fig. 1 style) for README.

Run: python scripts/generate_multipanel.py
"""
import sys
sys.path.insert(0, "src")

import acadp
from acadp._style import COLORS, PALETTE, DIVERGING_CMAP, PAPER_CMAP
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

acadp.set_style("nature")
np.random.seed(42)

gallery = Path("gallery/showcase")
gallery.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════
# Multi-panel 1: 4-panel data exploration (2x2)
# ═══════════════════════════════════════════
fig = plt.figure(figsize=(7, 5.5))
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

# Panel A: Multi-series line
ax1 = fig.add_subplot(gs[0, 0])
x = np.linspace(0, 10, 60)
for c, lbl, shift in zip(
    [COLORS["navy"], COLORS["coral"], COLORS["teal"]],
    ["Scenario A", "Scenario B", "Scenario C"], [0, 2, 4]
):
    ax1.plot(x, np.sin(x + shift) * 5 + 50, color=c, label=lbl, linewidth=1.3)
ax1.set_xlabel("Time")
ax1.set_ylabel("Value")
ax1.set_title("A. Multi-scenario Comparison", fontsize=9, fontweight="bold", loc="left")
ax1.legend(frameon=False, fontsize=7)

# Panel B: Bar + error bars
ax2 = fig.add_subplot(gs[0, 1])
categories = ["Exp-1", "Exp-2", "Exp-3", "Exp-4"]
means = [82, 88, 76, 91]
stds = [5, 3, 7, 4]
ax2.bar(categories, means, yerr=stds, capsize=3,
        color=[COLORS["navy"], COLORS["coral"],
               COLORS["teal"], COLORS["amber"]],
        edgecolor="white", width=0.6, error_kw={"linewidth": 0.8, "color": "#555555"})
ax2.set_ylabel("Accuracy (%)")
ax2.set_title("B. Experimental Results", fontsize=9, fontweight="bold", loc="left")

# Panel C: Scatter + trend
ax3 = fig.add_subplot(gs[1, 0])
n = 50
x_sc = np.random.uniform(0, 100, n)
y_sc = 0.6 * x_sc + np.random.randn(n) * 15 + 20
ax3.scatter(x_sc, y_sc, c=COLORS["navy"], s=25, alpha=0.7, edgecolors="white", linewidth=0.6)
z = np.polyfit(x_sc, y_sc, 1)
ax3.plot(np.sort(x_sc), np.poly1d(z)(np.sort(x_sc)), color=COLORS["coral"], linewidth=1.5, linestyle="--")
ax3.set_xlabel("Variable X")
ax3.set_ylabel("Variable Y")
r = np.corrcoef(x_sc, y_sc)[0, 1]
ax3.annotate(f"R² = {r**2:.3f}", xy=(0.05, 0.9), xycoords="axes fraction", fontsize=8, color=COLORS["coral"])
ax3.set_title("C. Correlation Analysis", fontsize=9, fontweight="bold", loc="left")

# Panel D: Box plot
ax4 = fig.add_subplot(gs[1, 1])
data_bp = {
    "Control": np.random.normal(70, 10, 30),
    "Treatment": np.random.normal(85, 8, 30),
    "Combined": np.random.normal(78, 12, 30),
}
bp = ax4.boxplot(data_bp.values(), labels=data_bp.keys(), patch_artist=True, widths=0.5, showfliers=False)
for patch, color in zip(bp["boxes"], [COLORS["slate"], COLORS["coral"], COLORS["teal"]]):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
    patch.set_edgecolor("white")
ax4.set_ylabel("Score")
ax4.set_title("D. Group Comparison", fontsize=9, fontweight="bold", loc="left")

fig.suptitle("Figure 1. Comprehensive Data Analysis", fontsize=11, fontweight="bold", y=1.02)
fig.savefig(gallery / "multipanel_4panel.png", dpi=200, bbox_inches="tight",
            facecolor=fig.get_facecolor(), edgecolor="none")
plt.close(fig)
print("Generated: multipanel_4panel.png")


# ═══════════════════════════════════════════
# Multi-panel 2: 6-panel (2 rows × 3 cols)
# ═══════════════════════════════════════════
fig = plt.figure(figsize=(9, 5.5))
gs = GridSpec(2, 3, figure=fig, hspace=0.38, wspace=0.35)

# (0,0) Line with confidence band
ax = fig.add_subplot(gs[0, 0])
x = np.linspace(0, 8, 50)
y = np.sin(x) * 10 + 50
noise = np.random.randn(50) * 3
ax.plot(x, y, color=COLORS["navy"], linewidth=1.3)
ax.fill_between(x, y - 6, y + 6, color=COLORS["navy"], alpha=0.1)
ax.set_xlabel("Time (h)")
ax.set_ylabel("Output")
ax.set_title("A", fontsize=9, fontweight="bold", loc="left", pad=4)

# (0,1) Stacked area
ax = fig.add_subplot(gs[0, 1])
x = np.linspace(0, 10, 50)
ax.stackplot(x, np.sin(x)*3+20, np.cos(x)*4+15, np.sin(x+1)*2+10,
             labels=["Source A", "Source B", "Source C"],
             colors=[COLORS["navy"], COLORS["teal"], COLORS["amber"]], alpha=0.7)
ax.legend(frameon=False, fontsize=6.5)
ax.set_xlabel("Time")
ax.set_ylabel("Energy (MWh)")
ax.set_title("B", fontsize=9, fontweight="bold", loc="left", pad=4)

# (0,2) Heatmap
ax = fig.add_subplot(gs[0, 2])
matrix = np.random.randn(5, 5)
im = ax.imshow(matrix, cmap=DIVERGING_CMAP, aspect="auto", vmin=-2, vmax=2)
labels_hm = ["Var A", "Var B", "Var C", "Var D", "Var E"]
ax.set_xticks(range(5))
ax.set_xticklabels(labels_hm, fontsize=6.5, rotation=45, ha="right")
ax.set_yticks(range(5))
ax.set_yticklabels(labels_hm, fontsize=6.5)
plt.colorbar(im, ax=ax, shrink=0.75, label="Value")
ax.set_title("C", fontsize=9, fontweight="bold", loc="left", pad=4)

# (1,0) Scatter with color coding
ax = fig.add_subplot(gs[1, 0])
for i, (c, lbl) in enumerate(zip(
    [COLORS["navy"], COLORS["coral"], COLORS["teal"]],
    ["Class 1", "Class 2", "Class 3"]
)):
    x = np.random.randn(30) * 10 + (i + 1) * 20
    y = np.random.randn(30) * 8 + (i + 1) * 15
    ax.scatter(x, y, c=c, s=20, alpha=0.7, edgecolors="white", linewidth=0.5, label=lbl)
ax.legend(frameon=False, fontsize=6.5, markerscale=0.8)
ax.set_xlabel("Feature 1")
ax.set_ylabel("Feature 2")
ax.set_title("D", fontsize=9, fontweight="bold", loc="left", pad=4)

# (1,1) Histogram comparison
ax = fig.add_subplot(gs[1, 1])
ax.hist(np.random.normal(80, 10, 200), bins=25, alpha=0.5, color=COLORS["navy"], label="Group A", density=True)
ax.hist(np.random.normal(90, 8, 200), bins=25, alpha=0.5, color=COLORS["coral"], label="Group B", density=True)
ax.legend(frameon=False, fontsize=6.5)
ax.set_xlabel("Value")
ax.set_ylabel("Density")
ax.set_title("E", fontsize=9, fontweight="bold", loc="left", pad=4)

# (1,2) Pareto
ax = fig.add_subplot(gs[1, 2])
costs = np.array([10, 15, 20, 25, 30, 12, 18, 22, 28, 35])
quality = np.array([0.9, 0.8, 0.75, 0.65, 0.55, 0.85, 0.72, 0.68, 0.58, 0.45])
ax.scatter(costs, quality, c=COLORS["navy"], s=30, alpha=0.8, edgecolors="white", linewidth=0.6)
# frontier
pts = np.column_stack([costs, quality])
mask = np.ones(len(pts), dtype=bool)
for i, p in enumerate(pts):
    dom = np.all(pts <= p, axis=1) & np.any(pts < p, axis=1)
    mask[i] = not np.any(dom & (np.arange(len(pts)) != i))
frontier = pts[mask]
sort_idx = np.argsort(frontier[:, 0])
frontier = frontier[sort_idx]
ax.plot(frontier[:, 0], frontier[:, 1], color=COLORS["coral"], linewidth=1.5, linestyle="--", marker="o", markersize=4, markerfacecolor=COLORS["coral"], markeredgecolor="white", markeredgewidth=0.6)
ax.set_xlabel("Cost")
ax.set_ylabel("Quality")
ax.set_title("F", fontsize=9, fontweight="bold", loc="left", pad=4)

fig.suptitle("Figure 2. Multi-view Analysis Dashboard", fontsize=11, fontweight="bold", y=1.02)
fig.savefig(gallery / "multipanel_6panel.png", dpi=200, bbox_inches="tight",
            facecolor=fig.get_facecolor(), edgecolor="none")
plt.close(fig)
print("Generated: multipanel_6panel.png")
print("Done!")
