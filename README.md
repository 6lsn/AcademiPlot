<div align="center">

# 🎨 AcademiPlot

**Publication-ready academic figures in one line.**
**一行代码，论文图表直达 Nature 级。**

[![PyPI](https://img.shields.io/pypi/v/acadp?color=blue)](https://pypi.org/project/acadp/)
[![Python](https://img.shields.io/pypi/pyversions/acadp)](https://pypi.org/project/acadp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/acadp)](https://pypi.org/project/acadp/)

[Quick Start](#-quick-start) • [Gallery](#-gallery) • [API](#-api-reference) • [Installation](#-installation)

</div>

---

## 🚀 Why AcademiPlot?

<table>
<tr>
<td align="center"><b>Before (matplotlib default)</b></td>
<td align="center"><b>After (AcademiPlot)</b></td>
</tr>
<tr>
<td><img src="gallery/before_after/before.png" width="400"></td>
<td><img src="gallery/before_after/after.png" width="400"></td>
</tr>
</table>

> 🎯 **Nature/Science-grade styles** — not just colors, but complete academic figure standards / 不只是换颜色，而是完整的学术图表规范
> 🤖 **Smart suggest** — describe your goal, it picks the best chart / 描述你想展示的内容，自动选择最佳图表类型
> ✅ **Quality review** — 6-dimension scoring checks academic compliance / 6 维度评分，检查图表是否符合学术标准
> 📊 **17 chart types** — from line plots to bullet charts / 从折线图到子弹图与供需平衡图

---

## ⚡ Quick Start

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

## 📊 Gallery

**[Basic](#basic-charts) • [Statistical](#statistical-charts) • [Advanced](#advanced-charts) • [3D](#3d-charts) • [Multi-panel](#multi-panel-figures)**

### Basic Charts

| Line / 折线图 | Bar / 柱状图 | Scatter / 散点图 | Area / 面积图 |
|:---:|:---:|:---:|:---:|
| ![line](gallery/showcase/v2_chart_line.png) | ![bar](gallery/showcase/v2_chart_bar.png) | ![scatter](gallery/showcase/v2_chart_scatter.png) | ![area](gallery/showcase/v2_chart_area.png) |

### Statistical Charts

| Heatmap / 热力图 | Box Plot / 箱线图 | Radar / 雷达图 | Histogram / 直方图 | Violinplot / 小提琴图 |
|:---:|:---:|:---:|:---:|:---:|
| ![heatmap](gallery/showcase/v2_chart_heatmap.png) | ![boxplot](gallery/showcase/v2_chart_boxplot.png) | ![radar](gallery/showcase/v2_chart_radar.png) | ![hist](gallery/showcase/v2_chart_histogram.png) | ![violin](gallery/showcase/v2_chart_violinplot.png) |

### Advanced Charts

| Pareto / 前沿 | Contour / 等高线 | Waterfall / 瀑布图 | Dumbbell / 对比图 | Bullet / 子弹图 |
|:---:|:---:|:---:|:---:|:---:|
| ![pareto](gallery/showcase/v2_chart_pareto.png) | ![contour](gallery/showcase/v2_chart_contour.png) | ![waterfall](gallery/showcase/v2_chart_waterfall.png) | ![dumbbell](gallery/showcase/v2_chart_dumbbell.png) | ![bullet](gallery/showcase/v2_chart_bullet.png) |

### 3D Charts

| Surface / 曲面图 | Scatter / 散点图 | Bar / 柱状图 |
|:---:|:---:|:---:|
| ![3d_surface](gallery/showcase/v2_chart_3d_surface.png) | ![3d_scatter](gallery/showcase/v2_chart_3d_scatter.png) | ![3d_bar](gallery/showcase/v2_chart_3d_bar.png) |

### Multi-panel Figures / 多面板组合图

| 2-panel (1x2) | 3-panel (1x3) | 4-panel (2x2) | 6-panel (2x3) |
|:---:|:---:|:---:|:---:|
| ![2panel](gallery/showcase/v2_chart_multipanel_2panel.png) | ![3panel](gallery/showcase/v2_chart_multipanel_3panel.png) | ![4panel](gallery/showcase/multipanel_4panel.png) | ![6panel](gallery/showcase/multipanel_6panel.png) |

---

## ✨ Features

| Feature / 功能 | Description / 说明 |
|---------|-------------|
| 🎨 **3 Theme Styles** | Nature / Science / IEEE — one-line switch / 一键切换期刊风格 |
| 🤖 **Smart Suggest** | Describe your goal → auto-select best chart / 描述目标，自动选图 |
| ✅ **Quality Review** | 6-dimension scoring + auto-fix / 6 维度评分 + 自动修正 |
| 📊 **17 Chart Types** | All academic essentials built-in / 学术常用图表全覆盖 |
| 🖼️ **Multi-panel** | Combine charts with GridSpec / 灵活组合多面板 |
| 🌐 **Bilingual Labels** | Chinese & English built-in / 中英文标签内置 |
| 💾 **Multi-format** | PNG, PDF, SVG — LaTeX-ready / LaTeX 友好 |
| ⌨️ **CLI Review** | `acadp-review` batch quality check / 命令行批量审查 |

---

## 📖 Usage

### Smart Suggest / 智能推荐

```python
ax = acadp.suggest(df, task="展示各方案的成本对比")     # → barplot
ax = acadp.suggest(df, task="分析变量之间的相关性")     # → heatmap
ax = acadp.suggest(df, task="展示时间趋势变化")         # → lineplot
ax = acadp.suggest(df, task="对比各方法的性能分布")     # → boxplot
```

### Style Themes / 切换主题

```python
acadp.set_style("nature")   # Nature 期刊风格（默认）
acadp.set_style("science")  # Science 期刊风格（衬线字体）
acadp.set_style("ieee")     # IEEE 会议风格（紧凑、高 DPI）

acadp.set_dpi(600)          # 高分辨率输出
acadp.set_font("SimHei")    # 中文字体
```

### Quality Review / 质量审查

```python
result = acadp.auto_plot(df, task="展示成本分解与优化空间")
print(result.report.status)   # "pass" / "revise" / "reject"
print(result.report.scores)   # {theme_fit: 95, readability: 88, ...}
print(result.changes)         # auto-fixed items
```

### Multi-panel / 多面板组合

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
acadp.lineplot(x=x, y=y1, ax=axes[0], title="A. Trend")
acadp.barplot(cats, vals, ax=axes[1], title="B. Comparison")
fig.savefig("multi_panel.png", dpi=300, bbox_inches="tight")
```

### Data Input / 数据输入

```python
# Arrays / 数组
ax = acadp.lineplot(x=[1,2,3], y=[4,5,6])

# DataFrame
ax = acadp.barplot(df, x="类别", y="数值")

# File path (suggest only) / 文件路径（仅 suggest）
ax = acadp.suggest("data.csv", task="展示趋势变化")
```

---

## 🔍 API Reference

<details>
<summary><b>📊 Chart Functions (17)</b></summary>

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

</details>

<details>
<summary><b>🤖 Smart Functions</b></summary>

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

</details>

---

## 📦 Installation

```bash
# PyPI
pip install acadp

# From source / 从源码安装
git clone https://github.com/6lsn/AcademiPlot.git
cd AcademiPlot
pip install -e .
```

---

## 📈 Comparison

| Feature / 功能 | matplotlib | seaborn | **AcademiPlot** |
|---------|:---:|:---:|:---:|
| Academic styles / 学术样式 | ❌ | ❌ | ✅ Nature/Science/IEEE |
| Smart selection / 智能选图 | ❌ | ❌ | ✅ |
| Quality review / 质量审查 | ❌ | ❌ | ✅ 6-dimension |
| One-line API / 一行 API | ❌ | ✅ | ✅ |
| 17 chart types / 17 种图表 | manual | partial | ✅ built-in |
| CLI review / 命令行审查 | ❌ | ❌ | ✅ |
| Chinese labels / 中文标签 | manual | manual | ✅ built-in |
| Multi-panel / 多面板图 | manual | ❌ | ✅ |

---

<div align="center">

**MIT License** • [GitHub](https://github.com/6lsn/AcademiPlot) • [PyPI](https://pypi.org/project/acadp/)

</div>
