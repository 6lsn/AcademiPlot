"""Regenerate gallery images using the old style.py palette and grid."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import math, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from style import apply_paper_style, COLORS, palette, set_chart_title, style_axis

apply_paper_style()
np.random.seed(42)

# ========== 1. Bullet ==========
fig, ax = plt.subplots(figsize=(8.2, 4.9))
categories = ["Efficiency", "Stability", "Cost Control", "Maintainability"]
actual = [85, 72, 91, 78]
threshold = [80, 75, 88, 80]
directions = [">=", ">=", ">=", ">="]
y = np.arange(len(categories))
max_val = max(max(actual), max(threshold)) * 1.15

for idx in range(len(categories)):
    passed = actual[idx] >= threshold[idx]
    color = COLORS["seagreen"] if passed else COLORS["crimson"]
    ax.barh(idx, max_val, color="#F3F4F6", height=0.58, edgecolor="none")
    ax.barh(idx, actual[idx], color=color, height=0.42, alpha=0.9)
    ax.vlines(threshold[idx], idx - 0.34, idx + 0.34, color=COLORS["amber"], linewidth=2.5)
    ax.text(actual[idx] + max_val * 0.015, idx, f"{actual[idx]:.1f}", va="center", fontsize=10)
    ax.text(threshold[idx], idx + 0.42, f"{directions[idx]}{threshold[idx]}",
            ha="center", va="bottom", fontsize=9, color=COLORS["amber"])

ax.set_yticks(y); ax.set_yticklabels(categories); ax.set_xlim(0, max_val); ax.invert_yaxis()
ax.set_xlabel("Metric Value"); ax.set_ylabel("Metric")
set_chart_title(ax, "Threshold Compliance Status")
import matplotlib.patches as mpatches, matplotlib.lines as mlines
handles = [mpatches.Patch(color=COLORS["seagreen"], label="Pass"),
           mpatches.Patch(color=COLORS["crimson"], label="Fail"),
           mlines.Line2D([], [], color=COLORS["amber"], linewidth=2.5, label="Threshold")]
ax.legend(handles=handles, loc="lower right", frameon=False)
style_axis(ax, grid=True, grid_axis="x")
fig.tight_layout()
fig.savefig("gallery/showcase/bullet.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
plt.close("all"); print("Saved bullet.png")

# ========== 2. Supply-Demand ==========
time = np.arange(24)
wind = np.abs(np.sin(time / 4) * 40 + np.random.randn(24) * 5)
solar = np.abs(np.cos(time / 3) * 25 + np.random.randn(24) * 3)
demand = wind + solar + np.random.randn(24) * 8
net = wind + solar - demand

fig = plt.figure(figsize=(10.8, 6.4))
gs = fig.add_gridspec(2, 1, height_ratios=[3.2, 1.15], hspace=0.1)
ax_top = fig.add_subplot(gs[0])
ax_bot = fig.add_subplot(gs[1], sharex=ax_top)

ax_top.stackplot(time, wind, solar, labels=["Wind", "Solar"],
                 colors=[COLORS["blue"], COLORS["amber"]], alpha=0.72)
ax_top.plot(time, demand, color=COLORS["crimson"], linewidth=2.4, label="Demand")
ax_top.set_ylabel("Power / Quantity")
set_chart_title(ax_top, "Supply-Demand Balance")
ax_top.legend(loc="upper left", ncol=4, frameon=False)
plt.setp(ax_top.get_xticklabels(), visible=False)
style_axis(ax_top, grid=True, grid_axis="y")

bar_colors = [COLORS["seagreen"] if v >= 0 else COLORS["crimson"] for v in net]
ax_bot.bar(time, net, color=bar_colors, alpha=0.85, width=0.72)
ax_bot.axhline(0, color=COLORS["axis"], linewidth=0.9)
ax_bot.set_xlabel("Time"); ax_bot.set_ylabel("Net Balance")
style_axis(ax_bot, grid=True, grid_axis="y")

fig.savefig("gallery/showcase/supply_demand.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
plt.close("all"); print("Saved supply_demand.png")

# ========== 3. Small Multiples ==========
factors = [
    {"name": "Temperature", "x": [15, 20, 25, 30, 35], "y": [60, 75, 82, 78, 65]},
    {"name": "Humidity", "x": [30, 40, 50, 60, 70], "y": [70, 78, 85, 80, 72]},
    {"name": "Wind Speed", "x": [0, 2, 4, 6, 8], "y": [50, 65, 80, 75, 55]},
    {"name": "Solar Irradiance", "x": [200, 400, 600, 800, 1000], "y": [40, 60, 78, 85, 82]},
]
cols = 2; rows = math.ceil(len(factors) / cols)
fig, axes = plt.subplots(rows, cols, figsize=(11.5, 4.0 * rows))
axes = np.asarray(axes).reshape(-1)
p = palette(4)

for idx, factor in enumerate(factors):
    ax = axes[idx]
    x = np.asarray(factor["x"]); y = np.asarray(factor["y"])
    ax.plot(x, y, marker="o", color=p[idx % 4], linewidth=2.2)
    if len(x) >= 2:
        trend = np.poly1d(np.polyfit(x, y, 1))(x)
        ax.plot(x, trend, linestyle="--", linewidth=1.2, color=COLORS["muted"])
    ax.set_xlabel(factor["name"]); ax.set_ylabel("Efficiency (%)")
    set_chart_title(ax, factor["name"])
    style_axis(ax, grid=True, grid_axis="y")

for ax in axes[len(factors):]: ax.set_visible(False)
fig.tight_layout()
fig.savefig("gallery/showcase/small_multiples.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
plt.close("all"); print("Saved small_multiples.png")

# ========== 4. 2-panel ==========
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

ax1 = axes[0]
x = np.linspace(0, 10, 50)
ax1.plot(x, np.sin(x) * 10 + 50, color=COLORS["blue"], linewidth=2.2, label="Predicted")
ax1.plot(x, np.cos(x) * 8 + 52, color=COLORS["crimson"], linewidth=2.2, linestyle="--", label="Actual")
ax1.fill_between(x, np.sin(x) * 10 + 47, np.sin(x) * 10 + 53, alpha=0.15, color=COLORS["blue"])
ax1.set_xlabel("Time"); ax1.set_ylabel("Metric")
ax1.legend(frameon=False, fontsize=8)
set_chart_title(ax1, "A. Trend Comparison")
style_axis(ax1, grid=True, grid_axis="y")

ax2 = axes[1]
cats = ["Method A", "Method B", "Method C", "Method D", "Method E"]
vals = [85, 72, 91, 68, 78]
colors = [COLORS["blue"] if v == max(vals) else COLORS["blue_light"] for v in vals]
bars = ax2.bar(cats, vals, color=colors, edgecolor="white", linewidth=1.2)
ax2.set_ylabel("Score"); ax2.set_ylim(0, 100)
for bar, v in zip(bars, vals):
    ax2.text(bar.get_x() + bar.get_width() / 2, v + 1.5, str(v), ha="center", fontsize=9, fontweight="bold")
set_chart_title(ax2, "B. Method Comparison")
style_axis(ax2, grid=True, grid_axis="y")

fig.tight_layout()
fig.savefig("gallery/showcase/multipanel_2panel.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
plt.close("all"); print("Saved multipanel_2panel.png")

# ========== 5. 3-panel ==========
fig = plt.figure(figsize=(14, 4.5))

ax1 = fig.add_subplot(131)
x_s = np.linspace(0, 8, 60)
y_s = np.sin(x_s) * 10 + 50 + np.random.randn(60) * 3
ax1.scatter(x_s, y_s, s=25, alpha=0.7, color=COLORS["blue"])
z = np.polyfit(x_s, y_s, 1); p_fit = np.poly1d(z)
ax1.plot(x_s, p_fit(x_s), color=COLORS["crimson"], linewidth=2, linestyle="--",
         label=f"y={z[0]:.1f}x+{z[1]:.1f}")
ax1.legend(frameon=False, fontsize=8)
ax1.set_xlabel("X"); ax1.set_ylabel("Y")
set_chart_title(ax1, "A. Correlation Analysis")
style_axis(ax1, grid=True, grid_axis="y")

ax2 = fig.add_subplot(132)
data_groups = [np.random.normal(80, 5, 30), np.random.normal(75, 8, 30), np.random.normal(85, 4, 30)]
bp = ax2.boxplot(data_groups, tick_labels=["Method A", "Method B", "Method C"], patch_artist=True)
box_colors = [COLORS["blue"], COLORS["crimson"], COLORS["seagreen"]]
for patch, color in zip(bp["boxes"], box_colors):
    patch.set_facecolor(color); patch.set_alpha(0.7)
ax2.set_ylabel("Score")
set_chart_title(ax2, "B. Distribution Comparison")
style_axis(ax2, grid=True, grid_axis="y")

ax3 = fig.add_subplot(133, polar=True)
labels_r = ["Accuracy", "Stability", "Efficiency", "Interpretability", "Generalization"]
angles = np.linspace(0, 2 * np.pi, len(labels_r), endpoint=False).tolist()
values_r = [85, 78, 92, 70, 82]; values_r += values_r[:1]; angles += angles[:1]
ax3.plot(angles, values_r, color=COLORS["blue"], linewidth=2, marker="o", markersize=5)
ax3.fill(angles, values_r, color=COLORS["blue"], alpha=0.15)
ax3.set_xticks(angles[:-1]); ax3.set_xticklabels(labels_r, fontsize=8)
ax3.set_ylim(0, 100)
set_chart_title(ax3, "C. Multi-dimensional Evaluation")

fig.subplots_adjust(wspace=0.35)
fig.savefig("gallery/showcase/multipanel_3panel.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
plt.close("all"); print("Saved multipanel_3panel.png")
