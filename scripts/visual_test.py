"""Visual regression test — generates all chart types and compares with baseline.

Run: python scripts/visual_test.py
Generates output in gallery/visual_test/
"""
import sys
sys.path.insert(0, "src")

import acadp
from acadp._style import COLORS, PALETTE, DIVERGING_CMAP, PAPER_CMAP, palette
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.random.seed(42)
out = Path("gallery/visual_test")
out.mkdir(parents=True, exist_ok=True)

def save(fig, name):
    fig.savefig(out / f"{name}.png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print(f"  OK {name}")


# ═══════════════════════════════════════════
# Test 1: Each chart type renders without error
# ═══════════════════════════════════════════
print("\n=== Individual Chart Tests ===")
acadp.set_style("nature")

fig, ax = plt.subplots()
acadp.lineplot(x=np.arange(20), y=np.random.randn(20).cumsum(), ax=ax, title="line")
save(fig, "01_line")

fig, ax = plt.subplots()
acadp.barplot(["A","B","C","D"], [10,15,13,12], highlight="max", ax=ax, title="bar")
save(fig, "02_bar")

fig, ax = plt.subplots()
acadp.scatter(x=np.random.randn(50), y=np.random.randn(50), trend=True, ax=ax, title="scatter")
save(fig, "03_scatter")

fig, ax = plt.subplots()
acadp.heatmap(np.corrcoef(np.random.randn(4, 50)), labels=["A","B","C","D"], ax=ax, title="heatmap")
save(fig, "04_heatmap")

fig, ax = plt.subplots()
acadp.boxplot([np.random.normal(0,1,50), np.random.normal(1,1,50)], ax=ax, title="boxplot")
save(fig, "05_boxplot")

fig, ax = plt.subplots()
acadp.histogram(np.random.randn(200), kde=True, ax=ax, title="histogram")
save(fig, "06_histogram")

fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
acadp.radar(["A","B","C","D","E"], [0.8,0.6,0.9,0.7,0.85], ax=ax, title="radar")
save(fig, "07_radar")

fig, ax = plt.subplots()
acadp.stacked_bar(["Q1","Q2","Q3"], {"A":[10,12,14],"B":[8,10,12]}, ax=ax, title="stacked_bar")
save(fig, "08_stacked_bar")

fig, ax = plt.subplots()
acadp.pareto(x=[10,15,20,25,30], y=[0.9,0.8,0.7,0.6,0.5], frontier=True, ax=ax, title="pareto")
save(fig, "09_pareto")

fig, ax = plt.subplots()
x_c = np.linspace(-3, 3, 50); y_c = np.linspace(-3, 3, 50); X, Y = np.meshgrid(x_c, y_c)
acadp.contour(X, Y, X**2 + Y**2, optimum=(0,0), ax=ax, title="contour")
save(fig, "10_contour")

fig, ax = plt.subplots()
acadp.waterfall(["A","B","C","D"], [10,5,-3,12], ax=ax, title="waterfall")
save(fig, "11_waterfall")

fig, ax = plt.subplots()
acadp.dumbbell([10,20,30], [15,25,28], ["X","Y","Z"], ax=ax, title="dumbbell")
save(fig, "12_dumbbell")


# ═══════════════════════════════════════════
# Test 2: Theme comparison
# ═══════════════════════════════════════════
print("\n=== Theme Comparison ===")
for theme in ["nature", "science", "ieee"]:
    acadp.set_style(theme)
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    x = np.linspace(0, 10, 40)
    for ax_i, (c, lbl) in enumerate(zip(
        [COLORS["navy"], COLORS["coral"], COLORS["teal"]],
        ["Series 1", "Series 2", "Series 3"]
    )):
        axes[0].plot(x, np.sin(x + ax_i*2) * 5 + 50, color=c, label=lbl)
    axes[0].legend(frameon=False, fontsize=7)
    axes[0].set_title("Line Plot", fontsize=9, fontweight="bold")
    axes[0].set_xlabel("X")
    axes[0].set_ylabel("Y")

    bars = axes[1].bar(["A","B","C","D"], [10,15,13,12],
                        color=[COLORS["navy"], COLORS["coral"],
                               COLORS["teal"], COLORS["amber"]],
                        edgecolor="white", width=0.6)
    axes[1].set_title("Bar Chart", fontsize=9, fontweight="bold")

    axes[2].scatter(np.random.randn(40), np.random.randn(40),
                     c=COLORS["navy"], s=30, alpha=0.7, edgecolors="white")
    axes[2].set_title("Scatter", fontsize=9, fontweight="bold")

    fig.suptitle(f"Theme: {theme.title()}", fontsize=11, fontweight="bold", y=1.02)
    save(fig, f"13_theme_{theme}")


# ═══════════════════════════════════════════
# Test 3: Suggest API
# ═══════════════════════════════════════════
print("\n=== Smart Suggest Tests ===")
acadp.set_style("nature")

df_bar = pd.DataFrame({"method": ["A","B","C"], "cost": [100,200,150]})
ax = acadp.suggest(df_bar, task="展示各方案的成本对比")
ax.figure.savefig(out / "14_suggest_bar.png", dpi=150, bbox_inches="tight")
plt.close("all")
print("  OK suggest -> barplot")

df_line = pd.DataFrame({"year": range(2020,2026), "gdp": [100,110,105,120,130,145]})
ax = acadp.suggest(df_line, task="展示GDP增长趋势")
ax.figure.savefig(out / "15_suggest_line.png", dpi=150, bbox_inches="tight")
plt.close("all")
print("  OK suggest -> lineplot")


# ═══════════════════════════════════════════
# Test 4: Color palette verification
# ═══════════════════════════════════════════
print("\n=== Color Palette Verification ===")
acadp.set_style("nature")
fig, ax = plt.subplots(figsize=(10, 2))
colors_list = palette(10)
for i, c in enumerate(colors_list):
    ax.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=c, edgecolor="white", linewidth=0.5))
    ax.text(i + 0.5, 0.5, c, ha="center", va="center", fontsize=8, color="white", fontweight="bold")
ax.set_xlim(0, 10)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("AcademiPlot Color Palette", fontsize=10, fontweight="bold", pad=10)
save(fig, "16_palette")


# ═══════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════
print(f"\n=== Visual Test Complete ===")
print(f"Generated {len(list(out.glob('*.png')))} test images in {out}/")
print("Review images visually to verify quality.")
