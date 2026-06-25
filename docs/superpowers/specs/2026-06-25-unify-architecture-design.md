# AcademiPlot v0.2.0 — 统一架构优化设计

**日期：** 2026-06-25
**状态：** 待实施
**范围：** 消除双轨并行，统一为 src/acadp/ 单一实现

---

## 1. 背景与问题

项目存在两套平行实现：

| 组件 | scripts/（旧） | src/acadp/（新） |
|------|----------------|------------------|
| 样式引擎 | `scripts/style.py` | `src/acadp/_style.py` |
| 数据分析 | `scripts/data_profiler.py` | `src/acadp/_profiler.py` |
| 图表规划 | `scripts/chart_planner.py` | `src/acadp/_planner.py` |
| 质量审查 | `review/chart_reviewer.py` | `src/acadp/_reviewer.py` |
| 自动修复 | `review/chart_auto_reviser.py` | `src/acadp/_reviser.py` |
| 高级图渲染 | `scripts/render_from_spec.py` | `src/acadp/` 各 chart 模块 |
| 图表脚本 | `scripts/plot_*.py`（50 个） | `src/acadp/charts/`（14 个） |

**已出现的分歧：**
- 配色不同：scripts 用 `#3B6BA5`（blue_main），acadp 用 `#003049`（navy）
- annotation 标签不同：scripts 用中文（"最高："），acadp 用英文（"Peak:"）
- reviser 功能不同：scripts 版有完整 safe/unsafe 边界，acadp 版只有 4 个修复
- suggest 用硬编码 if/elif 链，扩展性差

**目标：** src/acadp/ 成为唯一实现，scripts/ 精简为示例脚本，review/ 目录删除。

---

## 2. 目标架构

```
AcademiPlot/
├── pyproject.toml              # NEW — 打包配置
├── src/acadp/
│   ├── __init__.py             # 公开 API（14 charts + style + suggest + review）
│   ├── _style.py              # 唯一样式引擎（合并 scripts/style.py）
│   ├── _profiler.py           # 数据分析（已有）
│   ├── _planner.py            # 图表选择逻辑（已有）
│   ├── _suggest.py            # 智能建议（重构 dispatch 表）
│   ├── _reviewer.py           # 质量审查（合并 CLI 功能）
│   ├── _reviser.py            # 自动修复（合并完整 safe revision）
│   ├── _recipes/              # 高级图 recipe 定义
│   └── charts/                # 14 个图表函数
│       ├── _line.py, _bar.py, _scatter.py, _heatmap.py
│       ├── _box.py, _violin.py, _hist.py, _radar.py
│       ├── _area.py, _stacked_bar.py, _pareto.py
│       ├── _contour.py, _waterfall.py, _dumbbell.py
│       └── __init__.py
├── scripts/                   # 精简为示例脚本
│   ├── examples/              # 50 个示例（分批迁移到 acadp API）
│   ├── run_all_examples.py    # 改为遍历 scripts/examples/
│   └── utf8_io.py             # 保留（subprocess 编码工具）
├── tests/                     # 统一测试
├── references/                # 保留 — 文档参考
├── recipes/                   # 保留 — 高级图 YAML 定义
└── review/                    # 删除（功能移入 acadp/_reviewer.py）
```

**迁移后删除的文件：**
- `scripts/style.py`（合并到 acadp/_style.py）
- `scripts/data_profiler.py`（已在 acadp/_profiler.py）
- `scripts/chart_planner.py`（已在 acadp/_planner.py）
- `scripts/layout_qa.py`（功能合并到 acadp/_reviewer.py 的布局检查）
- `scripts/render_from_spec.py`（8 个高级图渲染器迁移到 acadp/charts/ 对应模块）
- `review/chart_reviewer.py`（合并到 acadp/_reviewer.py）
- `review/chart_auto_reviser.py`（合并到 acadp/_reviser.py）
- `review/chart_review_rules.md`、`review/review_schema.json`、`review/review_report_template.md`（移入 docs/ 或删除）

**render_from_spec.py 的 8 个渲染器迁移目标：**

| 渲染器 | 迁移到 |
|--------|--------|
| `render_bullet_threshold` | `acadp/charts/_bullet.py`（新增） |
| `render_contour_optimization` | `acadp/charts/_contour.py`（已有，合并） |
| `render_dumbbell_comparison` | `acadp/charts/_dumbbell.py`（已有，合并） |
| `render_supply_demand_balance` | `acadp/charts/_supply_demand.py`（新增） |
| `render_small_multiples_sensitivity` | `acadp/charts/_small_multiples.py`（新增） |
| `render_waterfall_cost` | `acadp/charts/_waterfall.py`（已有，合并） |
| `render_pareto_frontier` | `acadp/charts/_pareto.py`（已有，合并） |
| `render_percentage_structure` | `acadp/charts/_stacked_bar.py`（已有，合并） |

---

## 3. 配色统一

### 3.1 采用 Nature NMI 色板

以 `src/acadp/_style.py` 的色板为唯一标准：

```python
COLORS = {
    # 主色系 — 10 色高对比、色盲友好
    "navy":      "#003049",
    "coral":     "#E07A5F",
    "teal":      "#2A9D8F",
    "amber":     "#E9C46A",
    "slate":     "#264653",
    "lavender":  "#81B29A",
    "rose":      "#F4845F",
    "sky":       "#457B9D",
    "mauve":     "#B5838D",
    "sand":      "#D4A373",

    # 向后兼容别名
    "blue":       "#003049",   # → navy
    "seagreen":   "#2A9D8F",   # → teal
    "blue_main":  "#003049",   # → navy
    "blue_light": "#457B9D",   # → sky
    "teal_light": "#2A9D8F",   # → teal
    "crimson":    "#E07A5F",   # → coral
    "crimson_light": "#F4845F", # → rose
    "purple":     "#81B29A",   # → lavender
    "purple_light": "#B5838D", # → mauve

    # 中性色
    "grid":       "#E8E8E8",
    "axis":       "#555555",
    "text":       "#333333",
    "muted":      "#999999",
    "background": "#FFFFFF",
}
```

### 3.2 Annotation 标签统一为中文

```python
def annotate_extreme(ax, x_values, y_values, mode="max", text=None, ...):
    if mode == "max":
        default_text = f"最高：{y_values[idx]:.2f}"
    elif mode == "min":
        default_text = f"最低：{y_values[idx]:.2f}"
```

---

## 4. 图表函数 API

### 4.1 统一签名

所有 14 个图表函数遵循：

```python
def chart_fn(data=None, x=None, y=None, *, title=None, xlabel=None, ylabel=None,
             color=None, ax=None, **kwargs) -> matplotlib.axes.Axes
```

**调用方式：**
```python
# DataFrame 方式
acadp.lineplot(df, x="year", y="value", title="趋势")

# 数组方式
acadp.lineplot(x=[1,2,3], y=[4,5,6])

# 组合子图
fig, axes = plt.subplots(1, 2)
acadp.barplot(df, x="cat", y="val", ax=axes[0])
acadp.lineplot(df, x="year", y="val", ax=axes[1])
```

### 4.2 suggest() 重构

将 if/elif 链改为分发表：

```python
_CHART_RENDERERS = {
    "heatmap": _render_heatmap,
    "radar": _render_radar,
    "histogram": _render_histogram,
    "stacked_bar": _render_stacked_bar,
    "area": _render_area,
    "pareto": _render_pareto,
    "contour": _render_contour,
    "waterfall": _render_waterfall,
    "dumbbell": _render_dumbbell,
}
_DEFAULT_RENDERER = _render_generic  # lineplot, barplot, scatter, boxplot, violinplot

def suggest(data, task, **kwargs):
    df = _load_data(data)
    profile = profile_data(df)
    chart_name = choose_chart(profile, task)
    renderer = _CHART_RENDERERS.get(chart_name, _DEFAULT_RENDERER)
    return renderer(df, profile, chart_name, task, **kwargs)
```

### 4.3 _reviser.py 增强

从 `review/chart_auto_reviser.py` 合并：

```python
UNSAFE_REVIEW_MARKERS = (
    "不匹配", "不宜使用饼图", "缺乏证据支撑的因果性解释",
)
ANNOTATION_CAUTION_NAMES = {
    "3d", "3d_surface", "3d_scatter", "3d_contour",
    "heat", "heatmap", "corr_heat", "matrix_scatter",
    "scatter_matrix", "radar", "polar",
}

def _has_unsafe_issue(review_result):
    issues = review_result.major_issues + review_result.minor_issues
    return any(m in issue for issue in issues for m in UNSAFE_REVIEW_MARKERS)

def revise_metadata(metadata, review_result):
    """Apply only low-risk metadata fixes. Returns (revised, changes, blocked)."""
    changes = []
    blocked = []
    meta = dict(metadata)

    # 安全检查 — 涉及图型选择或因果解释的不自动修复
    if _has_unsafe_issue(review_result):
        blocked.append("涉及图型选择、建模含义或因果解释，需人工复核")
        return meta, changes, blocked

    # 1. 补全缺失图注
    if not meta.get("caption") and review_result.suggested_caption:
        meta["caption"] = review_result.suggested_caption
        changes.append("补全缺失图注")

    # 2. 根据 axis_labels 补全 variables
    axis_labels = meta.get("axis_labels") or {}
    if not meta.get("variables") and axis_labels:
        inferred = {k: v for k, v in axis_labels.items() if v}
        if inferred:
            meta["variables"] = inferred
            changes.append("根据坐标轴标签补全变量含义")

    # 3. 根据 variables 补全 axis_labels
    variables = meta.get("variables") or {}
    axis_labels = dict(meta.get("axis_labels") or {})
    updated = False
    for key in ("x", "y", "z"):
        if not axis_labels.get(key) and variables.get(key):
            axis_labels[key] = variables[key]
            updated = True
    if updated:
        meta["axis_labels"] = axis_labels
        changes.append("根据变量含义补全坐标轴标签")

    # 4. 关闭慎用图型的 annotation
    plot_type = meta.get("plot_type", "")
    if any(ct in plot_type for ct in ANNOTATION_CAUTION_NAMES):
        if meta.get("annotate"):
            meta["annotate"] = False
            meta["annotation_config"] = None
            changes.append("关闭慎用图型的 annotation")

    # 5. 限制 annotation 数量
    if meta.get("annotate"):
        usage = meta.get("usage", "paper")
        limit = {"paper": 3, "presentation": 4, "appendix": 1}.get(usage, 3)
        config = meta.get("annotation_config") or {}
        count = config.get("count", 0) if isinstance(config, dict) else 0
        if count > limit:
            meta["annotation_config"] = {"count": limit, **{k: v for k, v in config.items() if k != "count"}}
            changes.append(f"将 annotation 数量从 {count} 限制到 {limit}")

    return meta, changes, blocked
```

---

## 5. 审查系统整合

### 5.1 合并到 acadp/_reviewer.py

新增 CLI 入口和文件路由：

```python
def _route_artifacts(metadata_path, review, output_dir):
    """将审查通过/未通过的文件路由到对应目录"""
    status_dir = output_dir / STATUS_DIR[review.status]
    status_dir.mkdir(parents=True, exist_ok=True)
    # copy PNG + metadata to status_dir

def review_cli(metadata_dir, output_dir, route_files=True):
    """审查并路由文件"""
    report = review_dir(metadata_dir)
    if route_files:
        for meta_path in sorted(Path(metadata_dir).glob("*.metadata.json")):
            r = review(meta_path)
            _route_artifacts(meta_path, r, output_dir)
    _write_reports(report, output_dir)
    return report

def main():
    """CLI 入口"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--no-route", action="store_true")
    args = parser.parse_args()
    review_cli(args.metadata_dir, args.output_dir, route_files=not args.no_route)
```

### 5.2 CLI 注册

```toml
[project.scripts]
acadp-review = "acadp._reviewer:main"
```

---

## 6. 打包配置

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "acadp"
version = "0.2.0"
description = "Publication-ready academic figures in one line"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
dependencies = [
    "matplotlib>=3.5",
    "numpy>=1.21",
    "pandas>=1.3",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "pillow>=9.0"]

[project.scripts]
acadp-review = "acadp._reviewer:main"

[tool.setuptools.packages.find]
where = ["src"]
```

---

## 7. 测试策略

### 7.1 保留的测试

- `test_plot_workflow.py` — 更新 import 路径，保留核心断言
- `test_recipe_catalog.py` — 保留
- `test_data_profiler.py` — 更新 import 路径
- `test_chart_reviewer_recipe_fit.py` — 更新 import 路径
- `test_render_from_spec.py` — 更新为调用 acadp charts
- `test_chart_planner_red_cases.py` — 更新 import 路径

### 7.2 删除的测试

- 引用已删除模块的测试用例

### 7.3 新增的测试

- 每个 chart 函数的 smoke test（生成 Axes 不报错）
- suggest() dispatch 测试
- _reviser.py safe revision 测试
- 配色一致性测试（COLORS 别名指向正确颜色）

---

## 8. 分批实施计划

| 阶段 | 内容 | 预计文件变更 |
|------|------|-------------|
| Phase 1 | 合并 style、配色统一、pyproject.toml | _style.py, pyproject.toml |
| Phase 2 | 合并 reviewer/reviser、重构 suggest | _reviewer.py, _reviser.py, _suggest.py |
| Phase 3 | 迁移 10 个核心示例脚本 | scripts/examples/ 下 10 个文件 |
| Phase 4 | 迁移剩余 40 个示例、删除旧文件 | scripts/examples/ 下 40 个文件，删除 scripts/style.py 等 |
| Phase 5 | 更新所有测试、文档 | tests/ 下所有文件，README.md |

---

## 9. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 50 个示例脚本迁移工作量大 | 高 | 分批迁移，先改 10 个核心 |
| 配色改变影响已有图表外观 | 中 | 保留向后兼容别名，用户可手动切换 |
| 测试在迁移过程中 broken | 中 | 每阶段都跑测试，逐步更新 |
| render_from_spec.py 的 8 个高级图渲染器 | 中 | 逐一迁移到 charts/ 各模块 |
