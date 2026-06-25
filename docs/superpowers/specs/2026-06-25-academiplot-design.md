# AcademiPlot 设计规格

> "一行代码，论文图表直达 Nature 级"

## 1. 项目定位

**名称：** AcademiPlot
**定位：** 学术论文图表一站式工具
**目标用户：** 研究生、科研人员、数据分析师、数学建模参赛者
**Star 目标：** 500-1000

### 核心价值主张
1. **开箱即用** — `import acadp` 即获得 Nature/Science 级图表样式
2. **智能推荐** — `suggest(data, task)` 根据数据和目的自动选图
3. **质量审查** — `review()` 自动检测图表是否符合学术规范

## 2. API 设计

### 2.1 智能推荐模式（核心卖点）

```python
import acadp

# 只传数据 + 一句话描述目的，系统自动选图
ax = acadp.suggest(df, task="展示各方案的成本对比")

# 完整流程：推荐 → 审查 → 修正
result = acadp.auto_plot(df, task="展示成本分解与优化空间")
# result.chart  — 生成的图表
# result.report — 审查报告
# result.recipe — 推荐的图表类型及理由
```

### 2.2 显式指定模式

```python
ax = acadp.lineplot(df, x="year", y="gdp", title="经济增长趋势")
ax = acadp.barplot(df, x="method", y="cost", highlight="max")
ax = acadp.scatter(df, x="var1", y="var2", trend=True)
ax = acadp.heatmap(matrix, annot=True, cmap="diverging")
ax = acadp.boxplot(df, groupby="method")
ax = acadp.violinplot(df, groupby="method")
ax = acadp.histogram(values, kde=True)
ax = acadp.radar(labels, values)
ax = acadp.stacked_bar(categories, series_dict)
ax = acadp.area(x, y_dict)
ax = acadp.pareto(objectives, frontier=True)
ax = acadp.contour(X, Y, Z, optimum=True)
ax = acadp.waterfall(categories, values)
ax = acadp.dumbbell(before, after, labels)
```

### 2.3 质量审查 API

```python
report = acadp.review("figure1.png")
report = acadp.review_dir("figures/")
report.to_markdown("review_report.md")
```

### 2.4 样式控制

```python
acadp.set_style("nature")     # Nature 期刊风格（默认）
acadp.set_style("science")    # Science 期刊风格
acadp.set_style("ieee")       # IEEE 会议风格
acadp.set_dpi(300)
acadp.set_font("SimHei")
acadp.set_context("paper")    # paper / presentation / poster
```

### 2.5 数据输入

统一接受 DataFrame / CSV 路径 / Excel 路径，利用 data_profiler 自动识别列类型。

## 3. 项目结构

```
AcademiPlot/
├── README.md
├── README_CN.md
├── pyproject.toml
├── LICENSE (MIT)
├── CHANGELOG.md
├── src/acadp/
│   ├── __init__.py          # 导出顶层 API
│   ├── _style.py            # 样式引擎
│   ├── _profiler.py         # 数据分析器
│   ├── _planner.py          # 图表规划器
│   ├── _suggest.py          # suggest() + auto_plot() 入口
│   ├── _reviewer.py         # 质量审查
│   ├── _reviser.py          # 自动修正
│   ├── _layout_qa.py        # 布局检测
│   ├── _recipes/            # 高级配方 YAML
│   └── charts/              # 15 个精选图表
│       ├── _line.py
│       ├── _bar.py
│       ├── _scatter.py
│       ├── _heatmap.py
│       ├── _box.py
│       ├── _violin.py
│       ├── _hist.py
│       ├── _radar.py
│       ├── _area.py
│       ├── _stacked_bar.py
│       ├── _pareto.py
│       ├── _contour.py
│       ├── _waterfall.py
│       └── _dumbbell.py
├── gallery/                 # 展示图库
├── docs/                    # 文档
├── examples/                # 示例脚本 + 数据
└── tests/                   # 测试
```

## 4. 从现有代码迁移

| 现有文件 | 新位置 |
|---------|--------|
| scripts/style.py | src/acadp/_style.py |
| scripts/data_profiler.py | src/acadp/_profiler.py |
| scripts/chart_planner.py | src/acadp/_planner.py |
| review/chart_reviewer.py | src/acadp/_reviewer.py |
| review/chart_auto_reviser.py | src/acadp/_reviser.py |
| scripts/layout_qa.py | src/acadp/_layout_qa.py |
| recipes/*.yaml | src/acadp/_recipes/*.yaml |
| scripts/plot_*.py | src/acadp/charts/_*.py（合并重构） |

## 5. 视觉策略

README 必须包含：
- Before/After 对比图（matplotlib 默认 vs AcademiPlot）
- 一行代码 Quick Start
- 10-15 张精选 Gallery
- 与 matplotlib/seaborn 对比表

## 6. 实施路线图

| 阶段 | 内容 | 工作量 |
|------|------|--------|
| Phase 1 | 项目骨架：结构、pyproject.toml、__init__.py、style 引擎 | 1-2 天 |
| Phase 2 | 10 个核心图表：line/bar/scatter/heatmap/box/violin/hist/radar/area/stacked_bar | 3-4 天 |
| Phase 3 | 智能层：suggest() + auto_plot() + review() | 2-3 天 |
| Phase 4 | 4 个高级图表：pareto/contour/waterfall/dumbbell | 1-2 天 |
| Phase 5 | 包装：README、Gallery、examples、文档 | 2-3 天 |
| Phase 6 | 发布：GitHub、PyPI、内容营销 | 1 天 |
