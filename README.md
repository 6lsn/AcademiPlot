# AcademiPlot

> **Publication-ready academic figures in one line.**
> **一行代码，论文图表直达 Nature 级。**

[![PyPI version](https://img.shields.io/pypi/v/acadp.svg)](https://pypi.org/project/acadp/)
[![Python](https://img.shields.io/pypi/pyversions/acadp.svg)](https://pypi.org/project/acadp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | [中文](README_CN.md)

---

## Why AcademiPlot? / 为什么选择 AcademiPlot？

<table>
<tr>
<td align="center"><b>Before (matplotlib default) / 默认样式</b></td>
<td align="center"><b>After (AcademiPlot) / 学术级样式</b></td>
</tr>
<tr>
<td><img src="gallery/before_after/before.png" width="400"></td>
<td><img src="gallery/before_after/after.png" width="400"></td>
</tr>
</table>

**What makes it different: / 核心优势：**

- **Nature/Science-grade styles / Nature/Science 级样式** — not just colors, but complete academic figure standards / 不只是换颜色，而是完整的学术图表规范
- **Smart suggest / 智能推荐** — describe your goal, it picks the best chart type / 描述你想展示的内容，自动选择最佳图表类型
- **Quality review / 质量审查** — 6-dimension scoring checks if your figure meets academic standards / 6 维度评分，检查图表是否符合学术标准
- **17 chart types / 17 种图表** — from line plots to bullet charts & supply-demand balance / 从折线图到子弹图与供需平衡图

---

## Quick Start / 快速开始

```bash
pip install acadp
```

```python
import acadp
import numpy as np

# One-line chart / 一行代码出图
x = np.linspace(0, 10, 50)
ax = acadp.lineplot(x=x, y=np.sin(x), title="示例曲线", xlabel="X", ylabel="Y")

# Smart suggest — describe what you want to show / 智能推荐
ax = acadp.suggest(df, task="展示各方案的成本对比")

# Full pipeline — suggest + render + quality review / 完整流程
result = acadp.auto_plot(df, task="展示成本分解与优化空间")
print(result.report.status)  # "pass"
```

---

## Gallery / 图表示例

### Single Charts / 单图

| Line / 折线图 | Bar / 柱状图 | Scatter / 散点图 |
|:---:|:---:|:---:|
| ![line](gallery/showcase/line.png) | ![bar](gallery/showcase/bar.png) | ![scatter](gallery/showcase/scatter.png) |

| Heatmap / 热力图 | Box Plot / 箱线图 | Radar / 雷达图 |
|:---:|:---:|:---:|
| ![heatmap](gallery/showcase/heatmap.png) | ![boxplot](gallery/showcase/boxplot.png) | ![radar](gallery/showcase/radar.png) |

| Histogram / 直方图 | Stacked Bar / 堆叠柱状图 | Pareto / Pareto 前沿 |
|:---:|:---:|:---:|
| ![hist](gallery/showcase/histogram.png) | ![stacked](gallery/showcase/stacked_bar.png) | ![pareto](gallery/showcase/pareto.png) |

| Contour / 等高线图 | Waterfall / 瀑布图 | Dumbbell / 前后对比图 |
|:---:|:---:|:---:|
| ![contour](gallery/showcase/contour.png) | ![waterfall](gallery/showcase/waterfall.png) | ![dumbbell](gallery/showcase/dumbbell.png) |

| Bullet | Supply-Demand Balance | Small Multiples |
|:---:|:---:|:---:|
| ![bullet](gallery/showcase/bullet.png) | ![supply_demand](gallery/showcase/supply_demand.png) | ![small_multiples](gallery/showcase/small_multiples.png) |

### Multi-panel Figures / 多面板组合图

| 2-panel (1x2) / 2 面板 | 3-panel (1x3) / 3 面板 |
|:---:|:---:|
| ![2panel](gallery/showcase/multipanel_2panel.png) | ![3panel](gallery/showcase/multipanel_3panel.png) |

| 4-panel (2x2) / 4 面板 | 6-panel (2x3) / 6 面板 |
|:---:|:---:|
| ![4panel](gallery/showcase/multipanel_4panel.png) | ![6panel](gallery/showcase/multipanel_6panel.png) |

---

## Usage Guide / 使用指南

### 1. Direct API / 直接调用 API

When you know what chart you want / 明确知道自己要什么图时：

```python
import acadp

# Line chart / 折线图
ax = acadp.lineplot(x=[1,2,3,4,5], y=[2,4,1,5,3],
                     title="增长趋势", xlabel="年份", ylabel="GDP")

# Bar chart with highlight / 柱状图 + 高亮最大值
ax = acadp.barplot(["方法A", "方法B", "方法C"], [85, 92, 78],
                    highlight="max", title="性能对比")

# Scatter with trend + R² / 散点图 + 趋势线
ax = acadp.scatter(x=var1, y=var2, trend=True, title="相关性分析")

# Correlation heatmap / 相关性热力图
ax = acadp.heatmap(corr_matrix, labels=["指标1","指标2","指标3"],
                    title="指标相关性矩阵")

# Box plot with grouping / 箱线图（按分组）
ax = acadp.boxplot(df, y="得分", groupby="方法")

# Histogram + KDE / 直方图 + 密度曲线
ax = acadp.histogram(values, kde=True, title="误差分布")

# Radar chart / 雷达图
ax = acadp.radar(["速度","精度","成本","可靠性"],
                  [0.85, 0.92, 0.75, 0.88], title="综合评估")

# Stacked bar / 堆叠柱状图
ax = acadp.stacked_bar(["Q1","Q2","Q3","Q4"],
                        {"材料": [30,35,28,32], "人工": [20,22,18,25]},
                        title="季度成本构成")

# Pareto frontier / Pareto 前沿
ax = acadp.pareto(x=costs, y=quality, frontier=True,
                   title="多目标优化 Pareto 前沿")

# Contour + optimum / 等高线图 + 最优点
ax = acadp.contour(X, Y, Z, optimum=(5, 5), title="参数优化等高线")

# Waterfall / 瀑布图
ax = acadp.waterfall(["基础","材料+","人工+","节省−","最终"],
                      [100, 20, 15, -12, 123], title="成本分解瀑布图")

# Dumbbell (before/after) / 前后对比图
ax = acadp.dumbbell([72, 65, 80], [88, 82, 85], ["方法A","方法B","方法C"],
                     title="优化前后对比")

# Bullet (threshold compliance) / 子弹图（达标状态）
ax = acadp.bullet(categories=["效率", "稳定性", "成本"],
                  actual=[85, 72, 91], threshold=[80, 75, 88],
                  directions=[">=", ">=", ">="], title="指标达标状态")

# Supply-demand balance / 供需平衡图
fig = acadp.supply_demand(
    time=np.arange(24),
    supply_components={"风电": wind, "光伏": solar},
    demand=demand, title="供需匹配与净差"
)

# Small multiples (sensitivity) / 小多图（敏感性分析）
fig = acadp.small_multiples([
    {"name": "温度", "x": [20,25,30,35], "y": [10,15,12,8]},
    {"name": "湿度", "x": [30,40,50,60], "y": [20,25,22,18]},
], title="多因素敏感性分析")
```

### 2. Smart Suggest / 智能推荐

When you're not sure which chart to use / 不确定用什么图时：

```python
import pandas as pd

df = pd.read_csv("data.csv")

# Just describe what you want to show / 只需描述你想展示什么
ax = acadp.suggest(df, task="展示各方案的成本对比")
# -> Auto-selects barplot, detects cost column / 自动选择柱状图，检测到成本列

ax = acadp.suggest(df, task="分析变量之间的相关性")
# -> Auto-selects heatmap, computes correlation / 自动选择热力图，计算相关矩阵

ax = acadp.suggest(df, task="展示时间趋势变化")
# -> Auto-selects lineplot, uses time as x-axis / 自动选择折线图

ax = acadp.suggest(df, task="对比各方法的性能分布")
# -> Auto-selects boxplot with groupby / 自动选择箱线图并分组
```

### 3. Full Pipeline / 完整流程

Suggest + render + quality review + auto-fix / 推荐 + 出图 + 审查 + 自动修正：

```python
result = acadp.auto_plot(df, task="展示成本分解与优化空间")

# result.chart  — the generated matplotlib Axes / 生成的图表
# result.report — ReviewResult with scores and status / 审查结果
# result.changes — list of auto-applied fixes / 自动修正内容

print(f"Status / 状态: {result.report.status}")    # "pass"
print(f"Score / 评分: {result.report.scores}")     # 6-dimension scores
print(f"Changes / 修正: {result.changes}")         # auto-fixed items
```

### 4. Quality Review / 质量审查

```python
# Review from metadata dict / 从元数据字典审查
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
print(report.to_markdown())   # formatted review report

# Batch review / 批量审查
batch = acadp.review_dir("figures/")
batch.to_markdown("审查报告.md")
```

### 5. Style Themes / 切换主题风格

```python
# Nature journal style (default) / Nature 期刊风格（默认）
acadp.set_style("nature")

# Science journal style / Science 期刊风格（衬线字体）
acadp.set_style("science")

# IEEE conference style / IEEE 会议风格（紧凑、高 DPI）
acadp.set_style("ieee")

# Customize / 自定义配置
acadp.set_dpi(600)         # high-res output / 高分辨率输出
acadp.set_font("SimHei")   # Chinese font / 中文字体
acadp.set_context("paper") # paper / presentation / poster
```

### 6. CLI Review / 命令行审查

```bash
# Batch review figures / 批量审查图表
acadp-review --metadata-dir figures/ --output-dir review_output/

# Skip file routing / 跳过文件路由
acadp-review --metadata-dir figures/ --output-dir review_output/ --no-route
```

### 6. Data Input / 数据输入格式

```python
# Direct arrays / 直接传数组
ax = acadp.lineplot(x=[1,2,3], y=[4,5,6])

# Pandas DataFrame
import pandas as pd
df = pd.read_csv("data.csv")
ax = acadp.barplot(df, x="类别", y="数值")

# Excel file / Excel 文件
df = pd.read_excel("结果.xlsx")
ax = acadp.scatter(df, x="投入", y="产出", trend=True)

# Smart suggest accepts file paths / 智能推荐支持文件路径
ax = acadp.suggest("data.csv", task="展示趋势变化")
ax = acadp.suggest("results.xlsx", task="对比各方案")
```

### 7. Multi-panel Figures / 多面板组合图（进阶）

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

### 8. Export for Papers / 导出论文用图

```python
# Standard export (300 DPI) / 标准导出
ax = acadp.lineplot(x, y, title="我的图表")
ax.figure.savefig("图1.png", dpi=300, bbox_inches="tight")

# Built-in helper / 内置辅助函数
acadp.save_figure(ax.figure, "图1.png", dpi=300)

# Vector format for LaTeX / LaTeX 友好的矢量格式
ax.figure.savefig("图1.pdf", bbox_inches="tight")
ax.figure.savefig("图1.svg", bbox_inches="tight")
```

---

## API Reference / API 参考

### Chart Functions / 图表函数

| Function / 函数 | Description / 说明 | Key Args / 核心参数 |
|----------|-------------|----------|
| `lineplot()` | Line chart / 折线图 | `x, y, title, color, marker` |
| `barplot()` | Bar chart / 柱状图 | `x, y, highlight="max"` |
| `scatter()` | Scatter plot / 散点图 | `x, y, trend=True` |
| `heatmap()` | Correlation heatmap / 热力图 | `data, labels, annot` |
| `boxplot()` | Box plot / 箱线图 | `data, groupby` |
| `violinplot()` | Violin plot / 小提琴图 | `data, groupby` |
| `histogram()` | Histogram + KDE / 直方图 | `data, kde=True` |
| `radar()` | Radar chart / 雷达图 | `labels, values` |
| `area()` | Stacked area / 面积图 | `x, y_dict` |
| `stacked_bar()` | Stacked bar / 堆叠柱状图 | `categories, series_dict` |
| `pareto()` | Pareto frontier / Pareto 前沿 | `x, y, frontier` |
| `contour()` | Contour plot / 等高线图 | `X, Y, Z, optimum` |
| `waterfall()` | Waterfall / 瀑布图 | `categories, values` |
| `dumbbell()` | Before/after / 前后对比图 | `before, after, labels` |
| `bullet()` | Threshold compliance / 子弹图 | `categories, actual, threshold` |
| `supply_demand()` | Supply-demand balance / 供需平衡 | `time, supply_components, demand` |
| `small_multiples()` | Multi-factor sensitivity / 小多图 | `factors, y_label` |

### Smart Functions / 智能函数

| Function / 函数 | Description / 说明 |
|----------|-------------|
| `suggest(data, task)` | Auto-select best chart / 自动选择最佳图表 |
| `auto_plot(data, task)` | Full pipeline / 完整流程：推荐 → 出图 → 审查 → 修正 |
| `review(source)` | 6-dimension review / 6 维度质量审查 |
| `review_dir(path)` | Batch review / 批量审查 |
| `set_style("nature")` | Switch theme / 切换主题 |
| `set_dpi(n)` | Set DPI / 设置输出 DPI |
| `set_font(name)` | Set font / 设置字体 |
| `set_context(ctx)` | Set context / 设置场景 |

---

## Comparison / 对比

| Feature / 功能 | matplotlib | seaborn | **AcademiPlot** |
|---------|:---:|:---:|:---:|
| Academic styles / 学术样式 | no / 无 | no / 无 | Nature/Science/IEEE |
| Smart selection / 智能选图 | no / 无 | no / 无 | yes / 有 |
| Quality review / 质量审查 | no / 无 | no / 无 | 6-dimension / 6 维度 |
| One-line API / 一行 API | no / 无 | yes / 有 | yes / 有 |
| 17 chart types / 17 种图表 | manual / 手动 | 部分 | all built-in / 全内置 |
| CLI review / 命令行审查 | no / 无 | no / 无 | yes / 有 |
| Chinese labels / 中文标签 | manual / 手动 | manual / 手动 | built-in / 内置 |
| Multi-panel / 多面板图 | manual / 手动 | no / 无 | yes / 有 |

---

## License / 许可证

MIT
