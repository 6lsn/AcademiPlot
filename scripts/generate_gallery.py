"""Generate gallery images for README."""
import sys
sys.path.insert(0, "src")

import matplotlib
matplotlib.use("Agg")

import acadp
from acadp.charts import pareto, contour
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

acadp.set_style("nature")

gallery_dir = Path("gallery/showcase")
gallery_dir.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

# 1. Line plot
x = np.linspace(0, 10, 50)
ax = acadp.lineplot(x=x, y=np.sin(x) * 10 + 50 + np.random.randn(50) * 2,
                     title="经济增长趋势", xlabel="年份", ylabel="GDP（万亿元）")
ax.figure.savefig(gallery_dir / "line.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 2. Bar plot with highlight
ax = acadp.barplot(x=["方案A", "方案B", "方案C", "方案D", "方案E"],
                    y=[85, 92, 78, 95, 88], highlight="max",
                    title="各方案综合评分对比")
ax.figure.savefig(gallery_dir / "bar.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 3. Scatter with trend
np.random.seed(42)
ax = acadp.scatter(x=np.random.randn(80) * 10 + 50,
                    y=np.random.randn(80) * 15 + 80, trend=True,
                    title="投入产出相关性分析", xlabel="投入（万元）", ylabel="产出（万元）")
ax.figure.savefig(gallery_dir / "scatter.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 4. Heatmap
corr = np.array([[1, 0.8, 0.3, -0.2], [0.8, 1, 0.5, -0.1],
                  [0.3, 0.5, 1, 0.4], [-0.2, -0.1, 0.4, 1]])
ax = acadp.heatmap(corr, labels=["成本", "效率", "质量", "风险"],
                    title="指标相关性矩阵")
ax.figure.savefig(gallery_dir / "heatmap.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 5. Box plot
df = pd.DataFrame({"score": np.concatenate([np.random.normal(80, 10, 50),
                                              np.random.normal(70, 15, 50)]),
                    "method": np.repeat(["方法A", "方法B"], 50)})
ax = acadp.boxplot(df, y="score", groupby="method", title="各方法得分分布")
ax.figure.savefig(gallery_dir / "boxplot.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 6. Radar
ax = acadp.radar(["速度", "精度", "成本", "可靠性", "可维护性"],
                  [0.85, 0.92, 0.75, 0.88, 0.80], title="综合评估雷达图")
ax.figure.savefig(gallery_dir / "radar.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 7. Histogram with KDE
ax = acadp.histogram(np.random.normal(100, 15, 500), kde=True, bins=30,
                      title="误差分布", xlabel="误差值")
ax.figure.savefig(gallery_dir / "histogram.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 8. Stacked bar
ax = acadp.stacked_bar(["Q1", "Q2", "Q3", "Q4"],
                        {"材料": [30, 35, 28, 32], "人工": [20, 22, 18, 25],
                         "其他": [10, 12, 8, 15]}, title="季度成本构成")
ax.figure.savefig(gallery_dir / "stacked_bar.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 9. Pareto
ax = pareto(x=[10, 20, 15, 30, 25, 12, 22, 18],
                   y=[0.9, 0.7, 0.8, 0.5, 0.65, 0.85, 0.6, 0.75],
                   frontier=True, title="多目标优化 Pareto 前沿")
ax.figure.savefig(gallery_dir / "pareto.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 10. Contour
x = np.linspace(0, 10, 50); y = np.linspace(0, 10, 50)
X, Y = np.meshgrid(x, y)
Z = -(X - 5)**2 - (Y - 5)**2 + 50
ax = contour(X, Y, Z, optimum=(5, 5), title="参数优化等高线",
                    xlabel="参数A", ylabel="参数B")
ax.figure.savefig(gallery_dir / "contour.png", dpi=150, bbox_inches="tight")
plt.close("all")

print(f"Generated {len(list(gallery_dir.glob('*.png')))} gallery images in {gallery_dir}")
