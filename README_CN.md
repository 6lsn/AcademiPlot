# AcademiPlot

> **一行代码，论文图表直达 Nature 级。**
>
> Publication-ready academic figures in one line.

[![PyPI version](https://img.shields.io/pypi/v/acadp.svg)](https://pypi.org/project/acadp/)
[![Python](https://img.shields.io/pypi/pyversions/acadp.svg)](https://pypi.org/project/acadp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | 中文

---

## 为什么选择 AcademiPlot？

<table>
<tr>
<td align="center"><b>Before（matplotlib 默认样式）</b></td>
<td align="center"><b>After（AcademiPlot）</b></td>
</tr>
<tr>
<td><img src="gallery/before_after/before.png" width="400"></td>
<td><img src="gallery/before_after/after.png" width="400"></td>
</tr>
</table>

**核心优势：**

- **Nature/Science 级样式** — 不只是换颜色，而是完整的学术图表规范
- **智能推荐** — 描述你想展示的内容，自动选择最佳图表类型
- **质量审查** — 6 维度评分，检查图表是否符合学术标准
- **14 种图表** — 从折线图到 Pareto 前沿，覆盖常见学术场景

---

## 快速开始

```bash
pip install acadp
```

```python
import acadp
import numpy as np

# 一行代码出图
x = np.linspace(0, 10, 50)
ax = acadp.lineplot(x=x, y=np.sin(x), title="示例曲线", xlabel="X", ylabel="Y")

# 智能推荐 — 描述你想展示的内容
ax = acadp.suggest(df, task="展示各方案的成本对比")

# 完整流程 — 推荐 + 出图 + 质量审查
result = acadp.auto_plot(df, task="展示成本分解与优化空间")
print(result.report.status)  # "pass"
```

---

## 图表示例

### 单图

| 折线图 | 柱状图 | 散点图 |
|:---:|:---:|:---:|
| ![line](gallery/showcase/line.png) | ![bar](gallery/showcase/bar.png) | ![scatter](gallery/showcase/scatter.png) |

| 热力图 | 箱线图 | 雷达图 |
|:---:|:---:|:---:|
| ![heatmap](gallery/showcase/heatmap.png) | ![boxplot](gallery/showcase/boxplot.png) | ![radar](gallery/showcase/radar.png) |

| 直方图 | 堆叠柱状图 | Pareto 前沿 |
|:---:|:---:|:---:|
| ![hist](gallery/showcase/histogram.png) | ![stacked](gallery/showcase/stacked_bar.png) | ![pareto](gallery/showcase/pareto.png) |

| 等高线图 | 瀑布图 | 前后对比图 |
|:---:|:---:|:---:|
| ![contour](gallery/showcase/contour.png) | ![waterfall](gallery/showcase/waterfall.png) | ![dumbbell](gallery/showcase/dumbbell.png) |

### 多面板组合图

| 4 面板（2x2） | 6 面板（2x3） |
|:---:|:---:|
| ![4panel](gallery/showcase/multipanel_4panel.png) | ![6panel](gallery/showcase/multipanel_6panel.png) |

---

## 使用指南

### 1. 直接调用 API — 明确知道自己要什么图

```python
import acadp

# 折线图
ax = acadp.lineplot(x=[1,2,3,4,5], y=[2,4,1,5,3],
                     title="增长趋势", xlabel="年份", ylabel="GDP")

# 柱状图 + 高亮最大值
ax = acadp.barplot(["方法A", "方法B", "方法C"], [85, 92, 78],
                    highlight="max", title="性能对比")

# 散点图 + 趋势线 + R²
ax = acadp.scatter(x=var1, y=var2, trend=True, title="相关性分析")

# 相关性热力图
ax = acadp.heatmap(corr_matrix, labels=["指标1","指标2","指标3"],
                    title="指标相关性矩阵")

# 箱线图（按分组）
ax = acadp.boxplot(df, y="得分", groupby="方法")

# 直方图 + KDE 密度曲线
ax = acadp.histogram(values, kde=True, title="误差分布")

# 雷达图
ax = acadp.radar(["速度","精度","成本","可靠性"],
                  [0.85, 0.92, 0.75, 0.88], title="综合评估")

# 堆叠柱状图
ax = acadp.stacked_bar(["Q1","Q2","Q3","Q4"],
                        {"材料": [30,35,28,32], "人工": [20,22,18,25]},
                        title="季度成本构成")

# Pareto 前沿
ax = acadp.pareto(x=costs, y=quality, frontier=True,
                   title="多目标优化 Pareto 前沿")

# 等高线图 + 最优点
ax = acadp.contour(X, Y, Z, optimum=(5, 5), title="参数优化等高线")

# 瀑布图
ax = acadp.waterfall(["基础","材料+","人工+","节省−","最终"],
                      [100, 20, 15, -12, 123], title="成本分解瀑布图")

# 前后对比图（哑铃图）
ax = acadp.dumbbell([72, 65, 80], [88, 82, 85], ["方法A","方法B","方法C"],
                     title="优化前后对比")
```

### 2. 智能推荐 — 不确定用什么图时

```python
import pandas as pd

df = pd.read_csv("data.csv")

# 只需描述你想展示什么
ax = acadp.suggest(df, task="展示各方案的成本对比")
# -> 自动选择 barplot，检测到成本列，添加标签

ax = acadp.suggest(df, task="分析变量之间的相关性")
# -> 自动选择 heatmap，计算相关矩阵

ax = acadp.suggest(df, task="展示时间趋势变化")
# -> 自动选择 lineplot，用时间列作为 x 轴

ax = acadp.suggest(df, task="对比各方法的性能分布")
# -> 自动选择 boxplot，按方法分组
```

### 3. 完整流程 — 推荐 + 审查 + 自动修正

```python
result = acadp.auto_plot(df, task="展示成本分解与优化空间")

# result.chart   — 生成的 matplotlib Axes
# result.report  — ReviewResult，含评分和状态
# result.changes — 自动修正的内容列表

print(f"状态: {result.report.status}")    # "pass" / "revise" / "manual_review"
print(f"评分: {result.report.scores}")    # 6 维度评分
print(f"修正: {result.changes}")          # 自动修正的内容
```

### 4. 质量审查

```python
# 从元数据字典审查
metadata = {
    "figure_name": "图1",
    "plot_type": "bar",
    "problem_type": "评价类",
    "modeling_purpose": "展示各方案成本对比",
    "variables": {"x": "方法", "y": "成本"},
    "axis_labels": {"x": "方法", "y": "成本（万元）"},
    "caption": "各方案成本对比",
    "usage": "paper",
}
report = acadp.review(metadata)
print(report.status)          # "pass"
print(report.to_markdown())   # 格式化审查报告

# 批量审查目录下所有图表
batch = acadp.review_dir("figures/")
batch.to_markdown("审查报告.md")
```

### 5. 切换主题风格

```python
# Nature 期刊风格（默认）
acadp.set_style("nature")

# Science 期刊风格（衬线字体）
acadp.set_style("science")

# IEEE 会议风格（紧凑、高 DPI）
acadp.set_style("ieee")

# 自定义配置
acadp.set_dpi(600)         # 高分辨率输出
acadp.set_font("SimHei")   # 中文字体
acadp.set_context("paper") # paper / presentation / poster
```

### 6. 数据输入格式

```python
# 直接传数组
ax = acadp.lineplot(x=[1,2,3], y=[4,5,6])

# Pandas DataFrame
import pandas as pd
df = pd.read_csv("data.csv")
ax = acadp.barplot(df, x="类别", y="数值")

# Excel 文件
df = pd.read_excel("结果.xlsx")
ax = acadp.scatter(df, x="投入", y="产出", trend=True)

# 智能推荐直接传文件路径
ax = acadp.suggest("data.csv", task="展示趋势变化")
ax = acadp.suggest("results.xlsx", task="对比各方案")
```

### 7. 多面板组合图（进阶）

```python
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(10, 6))
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])
acadp.lineplot(x=x, y=y1, ax=ax1, title="A. 趋势分析")

ax2 = fig.add_subplot(gs[0, 1])
acadp.barplot(categories, values, ax=ax2, title="B. 方案对比")

ax3 = fig.add_subplot(gs[1, 0])
acadp.scatter(x=x, y=y, trend=True, ax=ax3, title="C. 相关性分析")

ax4 = fig.add_subplot(gs[1, 1])
acadp.boxplot(data, ax=ax4, title="D. 分布分析")

fig.savefig("多面板图.png", dpi=300, bbox_inches="tight")
```

### 8. 导出论文用图

```python
# 标准导出（300 DPI，紧凑边距）
ax = acadp.lineplot(x, y, title="我的图表")
ax.figure.savefig("图1.png", dpi=300, bbox_inches="tight")

# 使用内置辅助函数
acadp.save_figure(ax.figure, "图1.png", dpi=300)

# LaTeX 友好的矢量格式
ax.figure.savefig("图1.pdf", bbox_inches="tight")
ax.figure.savefig("图1.svg", bbox_inches="tight")
```

---

## API 参考

### 图表函数

| 函数 | 说明 | 核心参数 |
|------|------|----------|
| `lineplot()` | 折线图 | `x, y, title, color, marker` |
| `barplot()` | 柱状图 | `x, y, highlight="max", horizontal` |
| `scatter()` | 散点图 | `x, y, trend=True, alpha` |
| `heatmap()` | 相关性热力图 | `data, labels, annot, cmap` |
| `boxplot()` | 箱线图 | `data, groupby` |
| `violinplot()` | 小提琴图 | `data, groupby` |
| `histogram()` | 直方图 + KDE | `data, bins, kde=True` |
| `radar()` | 雷达图 | `labels, values, fill` |
| `area()` | 面积图 | `x, y_dict, labels` |
| `stacked_bar()` | 堆叠柱状图 | `categories, series_dict` |
| `pareto()` | Pareto 前沿 | `x, y, frontier=True` |
| `contour()` | 等高线图 | `X, Y, Z, optimum, filled` |
| `waterfall()` | 瀑布图 | `categories, values` |
| `dumbbell()` | 前后对比图 | `before, after, labels` |

### 智能函数

| 函数 | 说明 |
|------|------|
| `suggest(data, task)` | 根据数据和描述自动选择最佳图表 |
| `auto_plot(data, task)` | 完整流程：推荐 → 出图 → 审查 → 修正 |
| `review(source)` | 6 维度质量审查 |
| `review_dir(path)` | 批量审查目录下所有图表 |
| `set_style("nature")` | 切换主题（nature / science / ieee） |
| `set_dpi(n)` | 设置输出 DPI（默认：300） |
| `set_font(name)` | 覆盖字体族 |
| `set_context(ctx)` | 设置场景（paper / presentation / poster） |

---

## 对比 seaborn/matplotlib

| 功能 | matplotlib | seaborn | **AcademiPlot** |
|------|:---:|:---:|:---:|
| 学术样式 | 无 | 无 | Nature/Science/IEEE |
| 智能选图 | 无 | 无 | 有 |
| 质量审查 | 无 | 无 | 6 维度评分 |
| 一行 API | 无 | 有 | 有 |
| Pareto/等高线/瀑布图 | 手动 | 无 | 有 |
| 中文标签 | 手动 | 手动 | 内置 |
| 多面板组合图 | 手动 | 无 | 有 |

---

## 许可证

MIT
