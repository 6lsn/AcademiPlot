"""Regenerate the 7 new gallery images with ORIGINAL color scheme."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Original colors from scripts/style.py (6a59ebf)
C = {
    "blue": "#3B6BA5", "blue_light": "#6B93C7", "teal": "#3D8C6A",
    "teal_light": "#6AAF8A", "amber": "#D4942B", "crimson": "#C44D4D",
    "crimson_light": "#D97A6B", "purple": "#7C5E9E", "purple_light": "#A88FC4",
    "grid": "#D1D5DB", "axis": "#6B7280", "text": "#1F2937", "muted": "#9CA3AF",
}
PALETTE = [C["blue"], C["amber"], C["teal"], C["crimson"], C["purple"],
           C["blue_light"], C["teal_light"], C["crimson_light"]]

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DengXian", "Arial"],
    "font.family": ["sans-serif"], "axes.unicode_minus": False,
    "figure.dpi": 120, "savefig.dpi": 300, "savefig.bbox": "tight",
    "savefig.pad_inches": 0.06, "figure.facecolor": "#FFFFFF",
    "axes.facecolor": "#FFFFFF", "axes.edgecolor": "#6B7280",
    "axes.labelcolor": "#1F2937", "axes.labelsize": 11,
    "axes.titlesize": 13, "axes.titleweight": "bold",
    "axes.grid": False, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "legend.fontsize": 9.5,
    "xtick.color": "#6B7280", "ytick.color": "#6B7280",
})


def style_ax(ax, grid_axis="y"):
    ax.set_axisbelow(True)
    ax.grid(True, axis=grid_axis, color="#D1D5DB", linestyle="-", linewidth=0.4, alpha=0.7)
    for s in ("top", "right"):
        if s in ax.spines:
            ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        if s in ax.spines:
            ax.spines[s].set_color("#D1D5DB")
            ax.spines[s].set_linewidth(0.7)


def ttl(ax, t):
    ax.set_title(t, fontsize=13, fontweight="bold", color="#1F2937", y=1.06, pad=10)


np.random.seed(42)

# ===== Violinplot =====
fig, ax = plt.subplots(figsize=(8, 5))
d1 = np.random.normal(80, 8, 50)
d2 = np.random.normal(75, 12, 50)
d3 = np.random.normal(88, 6, 50)
parts = ax.violinplot([d1, d2, d3], positions=[1, 2, 3], showmeans=True, showmedians=True)
for i, pc in enumerate(parts["bodies"]):
    pc.set_facecolor(PALETTE[i])
    pc.set_alpha(0.7)
parts["cmeans"].set_color(C["crimson"])
parts["cmedians"].set_color(C["amber"])
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(["Method A", "Method B", "Method C"])
ax.set_ylabel("Accuracy (%)")
ttl(ax, "Model Accuracy Distribution")
style_ax(ax)
fig.tight_layout()
fig.savefig("gallery/showcase/chart_violinplot.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
plt.close("all")
print("Saved violinplot")

# ===== Area =====
fig, ax = plt.subplots(figsize=(8, 5))
x = list(range(1, 13))
y1 = [45, 42, 50, 55, 60, 58, 62, 65, 55, 48, 44, 46]
y2 = [20, 25, 35, 45, 55, 60, 58, 50, 40, 30, 22, 18]
y3 = [10, 12, 15, 18, 20, 22, 25, 28, 22, 18, 14, 11]
ax.stackplot(x, y1, y2, y3, labels=["Wind", "Solar", "Hybrid"],
             colors=[C["blue"], C["amber"], C["teal"]], alpha=0.75)
ax.set_xlabel("Month")
ax.set_ylabel("Output (MWh)")
ax.legend(loc="upper left", frameon=False)
ttl(ax, "Monthly Energy Output")
style_ax(ax)
fig.tight_layout()
fig.savefig("gallery/showcase/chart_area.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
plt.close("all")
print("Saved area")

# ===== Bullet =====
fig, ax = plt.subplots(figsize=(8.2, 4.9))
cats = ["Efficiency", "Stability", "Cost Control", "Maintainability"]
actual = [85, 72, 91, 78]
threshold = [80, 75, 88, 80]
dirs = [">=", ">=", ">=", ">="]
y = np.arange(len(cats))
mx = max(max(actual), max(threshold)) * 1.15
for i in range(len(cats)):
    passed = actual[i] >= threshold[i]
    color = C["teal"] if passed else C["crimson"]
    ax.barh(i, mx, color="#F3F4F6", height=0.58, edgecolor="none")
    ax.barh(i, actual[i], color=color, height=0.42, alpha=0.9)
    ax.vlines(threshold[i], i - 0.34, i + 0.34, color=C["amber"], linewidth=2.5)
    ax.text(actual[i] + mx * 0.015, i, f"{actual[i]:.1f}", va="center", fontsize=10)
    ax.text(threshold[i], i + 0.42, f"{dirs[i]}{threshold[i]}",
            ha="center", va="bottom", fontsize=9, color=C["amber"])
ax.set_yticks(y)
ax.set_yticklabels(cats)
ax.set_xlim(0, mx)
ax.invert_yaxis()
ax.set_xlabel("Metric Value")
ax.set_ylabel("Metric")
ttl(ax, "Threshold Compliance Status")
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

ax.legend(handles=[
    mpatches.Patch(color=C["teal"], label="Pass"),
    mpatches.Patch(color=C["crimson"], label="Fail"),
    mlines.Line2D([], [], color=C["amber"], linewidth=2.5, label="Threshold"),
], loc="lower right", frameon=False)
style_ax(ax, grid_axis="x")
fig.tight_layout()
fig.savefig("gallery/showcase/chart_bullet.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
plt.close("all")
print("Saved bullet")

# ===== 3D Surface =====
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))
surf = ax.plot_surface(X, Y, Z, cmap="YlGnBu_r", alpha=0.9, edgecolor="none")
fig.colorbar(surf, ax=ax, shrink=0.5, pad=0.1)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.view_init(elev=25, azim=-60)
ttl(ax, "3D Surface Plot")
fig.savefig("gallery/showcase/chart_3d_surface.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
plt.close("all")
print("Saved 3d_surface")

# ===== 3D Scatter =====
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")
n = 80
x = np.random.randn(n)
y = np.random.randn(n)
z = x**2 + y**2 + np.random.randn(n) * 2
ax.scatter(x, y, z, c=z, cmap="YlGnBu_r", s=50, alpha=0.8, edgecolors="white", linewidth=0.5)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.view_init(elev=25, azim=-60)
ttl(ax, "3D Scatter Plot")
fig.savefig("gallery/showcase/chart_3d_scatter.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
plt.close("all")
print("Saved 3d_scatter")

# ===== 3D Bar =====
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")
xp = [0, 1, 2, 0, 1, 2]
yp = [0, 0, 0, 1, 1, 1]
zp = [0] * 6
dx = [0.4] * 6
dy = [0.4] * 6
dz = [5, 8, 6, 7, 9, 4]
colors = [C["blue"], C["teal"], C["amber"], C["crimson"], C["purple"], C["blue_light"]]
ax.bar3d(xp, yp, zp, dx, dy, dz, color=colors, alpha=0.85, edgecolor="white", linewidth=0.5)
ax.set_xlabel("Group A")
ax.set_ylabel("Group B")
ax.set_zlabel("Value")
ax.view_init(elev=25, azim=-60)
ttl(ax, "3D Bar Chart")
fig.savefig("gallery/showcase/chart_3d_bar.png", dpi=300, bbox_inches="tight", pad_inches=0.06)
plt.close("all")
print("Saved 3d_bar")
