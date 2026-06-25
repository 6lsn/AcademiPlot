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

| 折线图 | 柱状图 | 散点图 |
|:---:|:---:|:---:|
| ![line](gallery/showcase/line.png) | ![bar](gallery/showcase/bar.png) | ![scatter](gallery/showcase/scatter.png) |

| 热力图 | 箱线图 | 雷达图 |
|:---:|:---:|:---:|
| ![heatmap](gallery/showcase/heatmap.png) | ![boxplot](gallery/showcase/boxplot.png) | ![radar](gallery/showcase/radar.png) |

| 直方图 | 堆叠柱状图 | Pareto 前沿 |
|:---:|:---:|:---:|
| ![hist](gallery/showcase/histogram.png) | ![stacked](gallery/showcase/stacked_bar.png) | ![pareto](gallery/showcase/pareto.png) |

---

## API 参考

### 图表函数

| 函数 | 说明 | 核心参数 |
|------|------|----------|
| `lineplot()` | 折线图 | `x, y, title, trend` |
| `barplot()` | 柱状图 | `x, y, highlight="max"` |
| `scatter()` | 散点图 | `x, y, trend=True` |
| `heatmap()` | 相关性热力图 | `data, labels, annot` |
| `boxplot()` | 箱线图 | `data, groupby` |
| `violinplot()` | 小提琴图 | `data, groupby` |
| `histogram()` | 直方图 + KDE | `data, kde=True` |
| `radar()` | 雷达图 | `labels, values` |
| `area()` | 面积图 | `x, y_dict` |
| `stacked_bar()` | 堆叠柱状图 | `categories, series_dict` |
| `pareto()` | Pareto 前沿 | `x, y, frontier` |
| `contour()` | 等高线图 | `X, Y, Z, optimum` |
| `waterfall()` | 瀑布图 | `categories, values` |
| `dumbbell()` | 前后对比图 | `before, after, labels` |

### 智能函数

| 函数 | 说明 |
|------|------|
| `suggest(data, task)` | 根据数据和描述自动选择最佳图表 |
| `auto_plot(data, task)` | 完整流程：推荐 → 出图 → 审查 → 修正 |
| `review(source)` | 6 维度质量审查 |
| `set_style("nature")` | 切换主题（nature/science/ieee） |

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

---

## 许可证

MIT
