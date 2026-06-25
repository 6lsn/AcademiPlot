# AcademiPlot v0.2.0 — 统一架构实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 消除 scripts/ 和 src/acadp/ 的双轨并行，统一为 src/acadp/ 单一实现，添加 pyproject.toml 打包配置。

**Architecture:** src/acadp/ 成为唯一实现层。scripts/style.py 的配色和 annotation 逻辑合并到 acadp/_style.py；review/ 的 CLI 和文件路由合并到 acadp/_reviewer.py；render_from_spec.py 的 8 个高级图渲染器迁移到 acadp/charts/ 对应模块；_suggest.py 从 if/elif 链重构为 dispatch 表。

**Tech Stack:** Python 3.9+, matplotlib, numpy, pandas, pyyaml, setuptools

## Global Constraints

- 配色以 `src/acadp/_style.py` 的 Nature NMI 色板为唯一标准
- 向后兼容别名：blue→navy, seagreen→teal, blue_main→navy, crimson→coral
- annotation 标签统一为中文（"最高：" / "最低："）
- 所有图表函数返回 `matplotlib.axes.Axes`
- `annotate_extreme` 默认文本使用中文
- pyproject.toml 版本号为 0.2.0

---

### Task 1: 创建 pyproject.toml 打包配置

**Files:**
- Create: `pyproject.toml`

**Interfaces:**
- Produces: `pyproject.toml` — 定义包名 acadp, 版本 0.2.0, 依赖 matplotlib/numpy/pandas/pyyaml, CLI 入口 acadp-review

- [ ] **Step 1: 创建 pyproject.toml**

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

- [ ] **Step 2: 验证包可安装**

Run: `cd c:/Users/6sn/.codex/skills/plotting && pip install -e .`
Expected: 成功安装，`python -c "import acadp; print(acadp.__version__)"` 输出 `0.2.0`

- [ ] **Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "feat: add pyproject.toml for package installation"
```

---

### Task 2: 统一 _style.py — 合并配色与 annotation 标签

**Files:**
- Modify: `src/acadp/_style.py:139-175` — COLORS 字典，补充缺失别名
- Modify: `src/acadp/_style.py:488-504` — annotate_extreme 函数，改中文标签

**Interfaces:**
- Consumes: 现有 `src/acadp/_style.py` 的 COLORS 字典和 annotate_extreme 函数
- Produces: 统一后的 COLORS（含所有别名）和中文 annotation 标签

- [ ] **Step 1: 编写配色一致性测试**

创建 `tests/test_style_consistency.py`：

```python
"""Tests for unified color palette and annotation labels."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from acadp._style import COLORS, annotate_extreme
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def test_backward_compat_aliases_point_to_correct_colors():
    """Legacy aliases must resolve to the same hex as their canonical name."""
    pairs = {
        "blue": "navy",
        "seagreen": "teal",
        "blue_main": "navy",
        "blue_light": "sky",
        "teal_light": "teal",
        "crimson": "coral",
        "crimson_light": "rose",
        "purple": "lavender",
        "purple_light": "mauve",
    }
    for alias, canonical in pairs.items():
        assert COLORS[alias] == COLORS[canonical], (
            f"COLORS['{alias}'] = {COLORS[alias]!r} != "
            f"COLORS['{canonical}'] = {COLORS[canonical]!r}"
        )


def test_all_primary_colors_exist():
    """The 10 primary colors must all be present."""
    primary = ["navy", "coral", "teal", "amber", "slate",
               "lavender", "rose", "sky", "mauve", "sand"]
    for name in primary:
        assert name in COLORS, f"Missing primary color: {name}"
        assert COLORS[name].startswith("#"), f"COLORS['{name}'] is not a hex color"


def test_neutral_colors_exist():
    """Neutral colors must be present."""
    for name in ["grid", "axis", "text", "muted", "background"]:
        assert name in COLORS, f"Missing neutral color: {name}"


def test_annotate_extreme_uses_chinese_labels():
    """annotate_extreme default text must be in Chinese."""
    fig, ax = plt.subplots()
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([10.0, 50.0, 30.0])

    annotate_extreme(ax, x, y, mode="max")
    texts = [t.get_text() for t in ax.texts]
    assert any("最高" in t for t in texts), f"Expected '最高' in texts, got: {texts}"

    annotate_extreme(ax, x, y, mode="min")
    texts = [t.get_text() for t in ax.texts]
    assert any("最低" in t for t in texts), f"Expected '最低' in texts, got: {texts}"
    plt.close(fig)
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd c:/Users/6sn/.codex/skills/plotting && python -m pytest tests/test_style_consistency.py -v`
Expected: FAIL — `test_annotate_extreme_uses_chinese_labels` 失败（当前输出 "Peak:" / "Low:"）

- [ ] **Step 3: 修改 _style.py 补充缺失的别名**

在 `src/acadp/_style.py` 的 COLORS 字典中，确认以下别名存在（检查是否已有，没有则添加）：

```python
# 在 COLORS 字典的 "向后兼容别名" 部分确认或添加：
"blue":         "#003049",   # → navy
"seagreen":     "#2A9D8F",   # → teal
"blue_main":    "#003049",   # → navy
"blue_light":   "#457B9D",   # → sky
"teal_light":   "#2A9D8F",   # → teal
"crimson":      "#E07A5F",   # → coral
"crimson_light":"#F4845F",   # → rose
"purple":       "#81B29A",   # → lavender
"purple_light": "#B5838D",   # → mauve
```

- [ ] **Step 4: 修改 annotate_extreme 使用中文标签**

将 `src/acadp/_style.py` 的 `annotate_extreme` 函数中的默认文本从英文改为中文：

```python
def annotate_extreme(ax, x_values, y_values, mode="max", text=None,
                     color=None, xytext=(18, 18)):
    x_values = np.asarray(x_values)
    y_values = np.asarray(y_values)
    if mode == "max":
        idx = np.nanargmax(y_values)
        default_text = f"最高：{y_values[idx]:.2f}"      # 改自 "Peak: ..."
        color = color or COLORS["amber"]
    elif mode == "min":
        idx = np.nanargmin(y_values)
        default_text = f"最低：{y_values[idx]:.2f}"      # 改自 "Low: ..."
        color = color or COLORS["crimson"]
    else:
        raise ValueError("mode must be 'max' or 'min'")
    annotate_point(ax, x_values[idx], y_values[idx],
                   text or default_text, xytext=xytext, color=color)
    return ax
```

- [ ] **Step 5: 运行测试确认通过**

Run: `cd c:/Users/6sn/.codex/skills/plotting && python -m pytest tests/test_style_consistency.py -v`
Expected: 4 passed

- [ ] **Step 6: Commit**

```bash
git add src/acadp/_style.py tests/test_style_consistency.py
git commit -m "feat: unify color palette aliases and Chinese annotation labels"
```

---

### Task 3: 增强 _reviser.py — 合并完整 safe revision 逻辑

**Files:**
- Modify: `src/acadp/_reviser.py` — 重写为完整实现

**Interfaces:**
- Consumes: `acadp._reviewer.ReviewResult` (有 `.major_issues`, `.minor_issues`, `.suggested_caption`, `.status` 属性)
- Produces: `revise_metadata(metadata, review_result)` → `(revised_metadata, changes_list, blocked_list)`

- [ ] **Step 1: 编写 reviser 测试**

创建 `tests/test_reviser.py`：

```python
"""Tests for the enhanced _reviser module."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from acadp._reviser import revise_metadata
from acadp._reviewer import ReviewResult


def _make_review(**overrides):
    defaults = {
        "figure": "test", "score": 80, "status": "revise",
        "scores": {}, "major_issues": [], "minor_issues": [],
        "suggested_caption": "建议图注", "suggested_plot_type": "",
        "recommended_action": "修改",
    }
    defaults.update(overrides)
    return ReviewResult(**defaults)


def test_adds_missing_caption():
    meta = {"plot_type": "bar", "caption": ""}
    review = _make_review()
    revised, changes, blocked = revise_metadata(meta, review)
    assert revised["caption"] == "建议图注"
    assert "补全缺失图注" in changes
    assert blocked == []


def test_infers_variables_from_axis_labels():
    meta = {"plot_type": "bar", "variables": {}, "axis_labels": {"x": "年份", "y": "得分"}}
    review = _make_review()
    revised, changes, _ = revise_metadata(meta, review)
    assert revised["variables"] == {"x": "年份", "y": "得分"}
    assert "根据坐标轴标签补全变量含义" in changes


def test_infers_axis_labels_from_variables():
    meta = {"plot_type": "bar", "variables": {"x": "时间", "y": "温度"}, "axis_labels": {"x": "", "y": ""}}
    review = _make_review()
    revised, changes, _ = revise_metadata(meta, review)
    assert revised["axis_labels"]["x"] == "时间"
    assert revised["axis_labels"]["y"] == "温度"
    assert "根据变量含义补全坐标轴标签" in changes


def test_disables_annotation_on_caution_chart():
    meta = {"plot_type": "heatmap", "annotate": True, "annotation_config": {"count": 2}}
    review = _make_review()
    revised, changes, _ = revise_metadata(meta, review)
    assert revised["annotate"] is False
    assert revised["annotation_config"] is None
    assert "关闭慎用图型的 annotation" in changes


def test_trims_annotation_count():
    meta = {"plot_type": "line", "annotate": True, "annotation_config": {"count": 5}, "usage": "paper"}
    review = _make_review()
    revised, changes, _ = revise_metadata(meta, review)
    assert revised["annotation_config"]["count"] == 3
    assert any("限制" in c for c in changes)


def test_blocks_unsafe_issues():
    meta = {"plot_type": "bar", "caption": ""}
    review = _make_review(minor_issues=["图型 bar 与 预测类 不匹配"])
    revised, changes, blocked = revise_metadata(meta, review)
    assert len(blocked) > 0
    assert changes == []


def test_blocks_pie_warning():
    meta = {"plot_type": "pie", "caption": ""}
    review = _make_review(major_issues=["不宜使用饼图表达趋势"])
    revised, changes, blocked = revise_metadata(meta, review)
    assert len(blocked) > 0


def test_blocks_causal_claim():
    meta = {"plot_type": "line", "caption": ""}
    review = _make_review(major_issues=["缺乏证据支撑的因果性解释"])
    revised, changes, blocked = revise_metadata(meta, review)
    assert len(blocked) > 0
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd c:/Users/6sn/.codex/skills/plotting && python -m pytest tests/test_reviser.py -v`
Expected: FAIL — 当前 _reviser.py 只有 4 个简单修复，不支持 blocked 返回值

- [ ] **Step 3: 重写 _reviser.py**

用以下完整实现替换 `src/acadp/_reviser.py`：

```python
"""Auto-reviser — applies safe metadata fixes after review.

Only applies low-risk fixes. Returns (revised_metadata, changes, blocked).
Blocked items require human review and are NOT auto-fixed.
"""


UNSAFE_REVIEW_MARKERS = (
    "不匹配",
    "不宜使用饼图",
    "缺乏证据支撑的因果性解释",
)

ANNOTATION_CAUTION_NAMES = {
    "3d", "3d_surface", "3d_scatter", "3d_contour",
    "heat", "heatmap", "corr_heat", "matrix_scatter",
    "scatter_matrix", "radar", "polar",
}

USAGE_ANNOTATION_LIMITS = {
    "paper": 3,
    "presentation": 4,
    "appendix": 1,
}


def _has_unsafe_issue(review_result):
    """Check if review has issues that require human judgment."""
    issues = review_result.major_issues + review_result.minor_issues
    return any(marker in issue for issue in issues for marker in UNSAFE_REVIEW_MARKERS)


def revise_metadata(metadata, review_result):
    """Apply low-risk fixes to metadata based on review feedback.

    Only fixes:
    - Missing caption -> use suggested_caption from review
    - Missing variables -> infer from axis_labels
    - Missing axis_labels -> infer from variables
    - Annotations on caution chart types -> disable
    - Annotation count too high -> reduce to limit

    Does NOT change: data, chart type, variable meanings, causal explanations.

    Returns: (revised_metadata, changes_list, blocked_list)
    """
    changes = []
    blocked = []
    meta = dict(metadata)

    # Safety check — do not auto-fix chart selection or causal issues
    if _has_unsafe_issue(review_result):
        blocked.append("涉及图型选择、建模含义或因果解释，需人工复核")
        return meta, changes, blocked

    # 1. Fix missing caption
    if not meta.get("caption") and review_result.suggested_caption:
        meta["caption"] = review_result.suggested_caption
        changes.append("补全缺失图注")

    # 2. Infer variables from axis_labels
    axis_labels = meta.get("axis_labels") or {}
    if not meta.get("variables") and axis_labels:
        inferred = {k: v for k, v in axis_labels.items() if v}
        if inferred:
            meta["variables"] = inferred
            changes.append("根据坐标轴标签补全变量含义")

    # 3. Infer axis_labels from variables
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

    # 4. Disable annotations on caution chart types
    plot_type = str(meta.get("plot_type", "")).lower()
    if any(ct in plot_type for ct in ANNOTATION_CAUTION_NAMES):
        if meta.get("annotate"):
            meta["annotate"] = False
            meta["annotation_config"] = None
            changes.append("关闭慎用图型的 annotation")

    # 5. Trim annotation count
    if meta.get("annotate"):
        usage = meta.get("usage", "paper")
        limit = USAGE_ANNOTATION_LIMITS.get(usage, 3)
        config = meta.get("annotation_config") or {}
        count = config.get("count", 0) if isinstance(config, dict) else 0
        if count > limit:
            new_config = {k: v for k, v in config.items() if k != "count"}
            new_config["count"] = limit
            meta["annotation_config"] = new_config
            changes.append(f"将 annotation 数量从 {count} 限制到 {limit}")

    return meta, changes, blocked
```

- [ ] **Step 4: 运行测试确认通过**

Run: `cd c:/Users/6sn/.codex/skills/plotting && python -m pytest tests/test_reviser.py -v`
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
git add src/acadp/_reviser.py tests/test_reviser.py
git commit -m "feat: enhance _reviser with full safe revision logic and unsafe boundary"
```

---

### Task 4: 增强 _reviewer.py — 添加 CLI 入口和文件路由

**Files:**
- Modify: `src/acadp/_reviewer.py` — 添加 `_route_artifacts`, `_write_reports`, `review_cli`, `main` 函数

**Interfaces:**
- Consumes: 现有 `review()`, `review_dir()`, `ReviewResult`, `BatchReport`
- Produces: `review_cli(metadata_dir, output_dir, route_files=True)`, `main()` CLI 入口

- [ ] **Step 1: 编写 reviewer CLI 测试**

创建 `tests/test_reviewer_cli.py`：

```python
"""Tests for the reviewer CLI and file routing."""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from acadp._reviewer import review_cli, _route_artifacts, ReviewResult
import matplotlib
matplotlib.use("Agg")


def test_route_artifacts_copies_to_status_dir():
    """Files should be routed to status-specific directories."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        # Create a fake metadata + PNG
        meta_path = tmp_path / "test_chart.metadata.json"
        png_path = tmp_path / "test_chart.png"
        meta_path.write_text(json.dumps({"figure_name": "test_chart", "plot_type": "bar",
                                          "problem_type": "评价类", "modeling_purpose": "测试",
                                          "variables": {"x": "类别", "y": "值"},
                                          "axis_labels": {"x": "类别", "y": "值"},
                                          "legend_labels": [], "caption": "测试图",
                                          "usage": "paper", "annotate": False,
                                          "annotation_config": None}),
                             encoding="utf-8")
        png_path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

        output_dir = tmp_path / "output"
        review = ReviewResult(
            figure="test_chart", score=85, status="pass",
            scores={}, major_issues=[], minor_issues=[],
            suggested_caption="", suggested_plot_type="",
            recommended_action="可直接进入 final_figures/。",
        )
        _route_artifacts(meta_path, review, output_dir)
        assert (output_dir / "final_figures" / "test_chart.metadata.json").exists()
        assert (output_dir / "final_figures" / "test_chart.png").exists()


def test_review_cli_generates_reports():
    """review_cli should create review_report.json and review_report.md."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        meta_dir = tmp_path / "figures"
        output_dir = tmp_path / "review"
        meta_dir.mkdir()

        meta = {
            "figure_name": "test_fig", "plot_type": "bar",
            "problem_type": "评价类", "modeling_purpose": "展示得分",
            "variables": {"x": "地区", "y": "得分"},
            "axis_labels": {"x": "地区", "y": "得分"},
            "legend_labels": [], "caption": "各地区得分对比",
            "usage": "paper", "annotate": False, "annotation_config": None,
        }
        (meta_dir / "test_fig.metadata.json").write_text(
            json.dumps(meta, ensure_ascii=False), encoding="utf-8"
        )

        report = review_cli(str(meta_dir), str(output_dir), route_files=False)
        assert report.total == 1
        assert (output_dir / "review_report.json").exists()
        assert (output_dir / "review_report.md").exists()
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd c:/Users/6sn/.codex/skills/plotting && python -m pytest tests/test_reviewer_cli.py -v`
Expected: FAIL — `review_cli` 和 `_route_artifacts` 不存在

- [ ] **Step 3: 添加 CLI 功能到 _reviewer.py**

在 `src/acadp/_reviewer.py` 末尾（`review_dir` 函数之后）添加：

```python
import argparse
import shutil


STATUS_DIR = {
    "pass": "final_figures",
    "revise": "revise",
    "manual_review": "manual_review",
    "reject": "reject",
}


def _route_artifacts(metadata_path, review, output_dir):
    """Copy PNG and metadata to status-specific directory."""
    metadata_path = Path(metadata_path)
    status_dir = output_dir / STATUS_DIR.get(review.status, "manual_review")
    status_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(metadata_path, status_dir / metadata_path.name)
    png_path = metadata_path.with_name(
        metadata_path.name.replace(".metadata.json", ".png")
    )
    if png_path.exists():
        shutil.copy2(png_path, status_dir / png_path.name)


def _write_reports(report, output_dir):
    """Write review_report.json and review_report.md."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "review_report.json").write_text(
        json.dumps({
            "summary": {
                "total": report.total,
                "pass": report.pass_count,
                "revise": report.revise_count,
                "manual_review": report.manual_count,
                "reject": report.reject_count,
            },
            "reviews": [
                {
                    "figure": r.figure,
                    "overall_status": r.status,
                    "score": r.score,
                    "scores": r.scores,
                    "major_issues": r.major_issues,
                    "minor_issues": r.minor_issues,
                    "recommended_action": r.recommended_action,
                    "suggested_caption": r.suggested_caption,
                    "suggested_plot_type": r.suggested_plot_type,
                }
                for r in report.results
            ],
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "review_report.md").write_text(report.to_markdown(), encoding="utf-8")


def review_cli(metadata_dir, output_dir, route_files=True):
    """Review all metadata files and optionally route artifacts.

    Parameters
    ----------
    metadata_dir : str or Path
        Directory containing *.metadata.json files.
    output_dir : str or Path
        Directory for review reports and routed figures.
    route_files : bool
        If True, copy files to status-specific subdirectories.

    Returns
    -------
    BatchReport
    """
    metadata_dir = Path(metadata_dir)
    output_dir = Path(output_dir)
    report = review_dir(metadata_dir)
    if route_files:
        for meta_path in sorted(metadata_dir.glob("*.metadata.json")):
            r = review(meta_path)
            _route_artifacts(meta_path, r, output_dir)
    _write_reports(report, output_dir)
    return report


def main():
    """CLI entry point for acadp-review."""
    parser = argparse.ArgumentParser(description="Review generated chart metadata.")
    parser.add_argument("--metadata-dir", required=True, help="Directory with *.metadata.json files.")
    parser.add_argument("--output-dir", required=True, help="Directory for review reports.")
    parser.add_argument("--no-route", action="store_true", help="Skip file routing.")
    args = parser.parse_args()
    report = review_cli(args.metadata_dir, args.output_dir, route_files=not args.no_route)
    print(json.dumps({
        "total": report.total,
        "pass": report.pass_count,
        "revise": report.revise_count,
        "manual_review": report.manual_count,
        "reject": report.reject_count,
    }, ensure_ascii=False))
```

- [ ] **Step 4: 运行测试确认通过**

Run: `cd c:/Users/6sn/.codex/skills/plotting && python -m pytest tests/test_reviewer_cli.py -v`
Expected: 2 passed

- [ ] **Step 5: 验证 CLI 入口**

Run: `cd c:/Users/6sn/.codex/skills/plotting && python -c "from acadp._reviewer import main; print('CLI import OK')"`
Expected: `CLI import OK`

- [ ] **Step 6: Commit**

```bash
git add src/acadp/_reviewer.py tests/test_reviewer_cli.py
git commit -m "feat: add CLI entry point and file routing to _reviewer"
```

---

### Task 5: 重构 _suggest.py — dispatch 表替代 if/elif 链

**Files:**
- Modify: `src/acadp/_suggest.py` — 重构 suggest() 函数

**Interfaces:**
- Consumes: `acadp.charts` 模块的所有图表函数, `acadp._profiler.profile_data`, `acadp._planner.choose_chart`
- Produces: `suggest(data, task, **kwargs)` → Axes, `_CHART_RENDERERS` dispatch 表

- [ ] **Step 1: 编写 suggest dispatch 测试**

创建 `tests/test_suggest_dispatch.py`：

```python
"""Tests for suggest() dispatch table."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib
matplotlib.use("Agg")

from acadp._suggest import _CHART_RENDERERS, _DEFAULT_RENDERER, suggest


def test_dispatch_table_contains_all_special_charts():
    """All charts with custom rendering logic must be in the dispatch table."""
    expected = {"heatmap", "radar", "histogram", "stacked_bar", "area",
                "pareto", "contour", "waterfall", "dumbbell"}
    assert set(_CHART_RENDERERS.keys()) == expected


def test_default_renderer_exists():
    """_DEFAULT_RENDERER must be callable."""
    assert callable(_DEFAULT_RENDERER)


def test_suggest_returns_axes():
    """suggest() should return a matplotlib Axes."""
    df = pd.DataFrame({"year": [2020, 2021, 2022], "value": [10, 20, 15]})
    ax = suggest(df, "展示年份趋势")
    assert hasattr(ax, "plot"), "suggest should return matplotlib Axes"
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd c:/Users/6sn/.codex/skills/plotting && python -m pytest tests/test_suggest_dispatch.py -v`
Expected: FAIL — `_CHART_RENDERERS` 不存在

- [ ] **Step 3: 重构 _suggest.py**

用以下实现替换 `src/acadp/_suggest.py` 的 `suggest` 函数及相关代码：

```python
"""Smart chart suggestion — analyze data + task → pick best chart → render."""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from acadp._profiler import profile_data
from acadp._planner import choose_chart
from acadp._reviewer import review, ReviewResult
from acadp._reviser import revise_metadata
from acadp import charts


def _load_data(data):
    """Accept DataFrame / CSV path / Excel path, return DataFrame."""
    if isinstance(data, pd.DataFrame):
        return data
    if isinstance(data, str):
        if data.endswith(".csv"):
            return pd.read_csv(data)
        if data.endswith((".xls", ".xlsx")):
            return pd.read_excel(data)
    raise ValueError(f"Unsupported data type: {type(data)}")


def _render_generic(df, profile, chart_name, task, **kwargs):
    """Render lineplot, barplot, scatter, boxplot, violinplot."""
    cols = profile.get("columns", {})
    col_names = list(cols.keys())
    x_col, y_col = None, None
    for name, info in cols.items():
        stype = info.get("semantic_type", "")
        if stype == "category" and x_col is None:
            x_col = name
        if stype in ("numeric", "cost", "ratio", "objective") and y_col is None:
            y_col = name
    if x_col is None and len(col_names) >= 1:
        x_col = col_names[0]
    if y_col is None and len(col_names) >= 2:
        y_col = col_names[1]
    chart_fn = getattr(charts, chart_name)
    return chart_fn(df, x=x_col, y=y_col, title=task, **kwargs)


def _render_heatmap(df, profile, chart_name, task, **kwargs):
    numeric_df = df.select_dtypes(include=[np.number])
    return charts.heatmap(numeric_df.corr(), labels=list(numeric_df.columns), title=task, **kwargs)


def _render_radar(df, profile, chart_name, task, **kwargs):
    cols = profile.get("columns", {})
    col_names = list(cols.keys())
    x_col, y_col = None, None
    for name, info in cols.items():
        if info.get("semantic_type") == "category" and x_col is None:
            x_col = name
        if info.get("semantic_type") in ("numeric", "cost", "ratio", "objective") and y_col is None:
            y_col = name
    labels = df[x_col].tolist() if x_col else col_names
    values = df[y_col].tolist() if y_col else [0] * len(labels)
    return charts.radar(labels, values, title=task, **kwargs)


def _render_histogram(df, profile, chart_name, task, **kwargs):
    cols = profile.get("columns", {})
    y_col = None
    for name, info in cols.items():
        if info.get("semantic_type") in ("numeric", "cost", "ratio", "objective"):
            y_col = name
            break
    if y_col is None:
        y_col = list(cols.keys())[-1] if cols else df.columns[0]
    return charts.histogram(df[y_col].values, title=task, **kwargs)


def _render_stacked_bar(df, profile, chart_name, task, **kwargs):
    cols = profile.get("columns", {})
    col_names = list(cols.keys())
    x_col, y_col = None, None
    for name, info in cols.items():
        if info.get("semantic_type") == "category" and x_col is None:
            x_col = name
        if info.get("semantic_type") in ("numeric", "cost", "ratio") and y_col is None:
            y_col = name
    if x_col and y_col:
        return charts.stacked_bar(df[x_col].tolist(), {y_col: df[y_col].tolist()}, title=task, **kwargs)
    return charts.stacked_bar(
        df.iloc[:, 0].tolist(),
        {df.columns[1]: df.iloc[:, 1].tolist()},
        title=task, **kwargs,
    )


def _render_area(df, profile, chart_name, task, **kwargs):
    cols = profile.get("columns", {})
    col_names = list(cols.keys())
    x_col = None
    for name, info in cols.items():
        if info.get("semantic_type") == "category" and x_col is None:
            x_col = name
    x_vals = df[x_col].tolist() if x_col else list(range(len(df)))
    y_dict = {}
    for name, info in cols.items():
        if info.get("semantic_type") in ("numeric", "cost", "ratio", "objective"):
            y_dict[name] = df[name].tolist()
    if not y_dict:
        y_col = col_names[1] if len(col_names) >= 2 else col_names[0]
        y_dict = {y_col: df[y_col].tolist()}
    return charts.area(x_vals, y_dict, title=task, **kwargs)


def _render_pareto(df, profile, chart_name, task, **kwargs):
    cols = profile.get("columns", {})
    col_names = list(cols.keys())
    x_col, y_col = None, None
    for name, info in cols.items():
        if info.get("semantic_type") in ("numeric", "cost", "ratio", "objective"):
            if x_col is None:
                x_col = name
            elif y_col is None:
                y_col = name
    if x_col is None:
        x_col = col_names[0]
    if y_col is None:
        y_col = col_names[1] if len(col_names) >= 2 else col_names[0]
    return charts.pareto(df, x=x_col, y=y_col, title=task, **kwargs)


def _render_contour(df, profile, chart_name, task, **kwargs):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) >= 3:
        x_vals = df[numeric_cols[0]].values
        y_vals = df[numeric_cols[1]].values
        z_vals = df[numeric_cols[2]].values
        xi = np.linspace(x_vals.min(), x_vals.max(), 30)
        yi = np.linspace(y_vals.min(), y_vals.max(), 30)
        Xi, Yi = np.meshgrid(xi, yi)
        from scipy.interpolate import griddata
        Zi = griddata((x_vals, y_vals), z_vals, (Xi, Yi), method="linear")
        return charts.contour(Xi, Yi, Zi, title=task, **kwargs)
    return _render_generic(df, profile, "lineplot", task, **kwargs)


def _render_waterfall(df, profile, chart_name, task, **kwargs):
    cols = list(df.columns)
    categories = df.iloc[:, 0].tolist()
    values = df.iloc[:, 1].tolist()
    return charts.waterfall(categories, values, title=task, **kwargs)


def _render_dumbbell(df, profile, chart_name, task, **kwargs):
    cols = list(df.columns)
    if len(cols) >= 3:
        labels = df.iloc[:, 0].tolist()
        before = df.iloc[:, 1].values
        after = df.iloc[:, 2].values
        return charts.dumbbell(before, after, labels, title=task, **kwargs)
    return _render_generic(df, profile, "barplot", task, **kwargs)


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

_DEFAULT_RENDERER = _render_generic


def suggest(data, task, **kwargs):
    """Smart chart selection: analyze data + task → pick best chart → render.

    Args:
        data: DataFrame, CSV path, or Excel path
        task: str describing what to show (e.g., "展示各方案的成本对比")
        **kwargs: passed to the chosen chart function

    Returns:
        matplotlib.axes.Axes
    """
    df = _load_data(data)
    profile = profile_data(df)
    chart_name = choose_chart(profile, task)
    renderer = _CHART_RENDERERS.get(chart_name, _DEFAULT_RENDERER)
    return renderer(df, profile, chart_name, task, **kwargs)


# ============================================================
# Auto-plot pipeline
# ============================================================

@dataclass
class AutoPlotResult:
    chart: object  # matplotlib Axes
    report: ReviewResult = None
    recipe: str = ""
    changes: list = field(default_factory=list)


def auto_plot(data, task, max_rounds=2, **kwargs):
    """Full pipeline: suggest -> render -> review -> revise -> re-review.

    Args:
        data: DataFrame, CSV path, or Excel path
        task: str describing what to show
        max_rounds: max revision rounds (default 2)
        **kwargs: passed to chart function

    Returns:
        AutoPlotResult with .chart, .report, .recipe, .changes
    """
    ax = suggest(data, task, **kwargs)

    from acadp._style import build_figure_metadata
    meta = build_figure_metadata(task, fig=ax.figure)

    all_changes = []
    for _ in range(max_rounds):
        r = review(meta)
        if r.status in ("pass", "manual_review"):
            break
        meta, changes, blocked = revise_metadata(meta, r)
        if not changes:
            break
        all_changes.extend(changes)

    final_report = review(meta)
    return AutoPlotResult(
        chart=ax,
        report=final_report,
        recipe=task,
        changes=all_changes,
    )
```

- [ ] **Step 4: 运行测试确认通过**

Run: `cd c:/Users/6sn/.codex/skills/plotting && python -m pytest tests/test_suggest_dispatch.py -v`
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add src/acadp/_suggest.py tests/test_suggest_dispatch.py
git commit -m "feat: refactor suggest() to use dispatch table instead of if/elif chain"
```

---

### Task 6: 新增高级图模块 — _bullet.py, _supply_demand.py, _small_multiples.py

**Files:**
- Create: `src/acadp/charts/_bullet.py`
- Create: `src/acadp/charts/_supply_demand.py`
- Create: `src/acadp/charts/_small_multiples.py`
- Modify: `src/acadp/charts/__init__.py` — 添加新模块导出
- Modify: `src/acadp/__init__.py` — 添加新模块导出

**Interfaces:**
- Produces:
  - `bullet(categories, actual, threshold, directions=None, title=None, ax=None, **kwargs)` → Axes
  - `supply_demand(time, supply_components, demand, title=None, ax=None, **kwargs)` → Axes
  - `small_multiples(factors, y_label="结果指标", title=None, **kwargs)` → Figure

- [ ] **Step 1: 编写 smoke 测试**

创建 `tests/test_advanced_charts.py`：

```python
"""Smoke tests for advanced chart modules."""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from acadp.charts import bullet, supply_demand, small_multiples


def test_bullet_returns_axes():
    ax = bullet(
        categories=["指标A", "指标B", "指标C"],
        actual=[85, 72, 91],
        threshold=[80, 75, 88],
        directions=[">=", ">=", ">="],
        title="指标达标状态",
    )
    assert hasattr(ax, "barh")
    plt.close("all")


def test_supply_demand_returns_figure():
    time = np.arange(24)
    supply = {"风电": np.random.rand(24) * 50, "光伏": np.random.rand(24) * 30}
    demand = np.random.rand(24) * 60 + 20
    fig = supply_demand(time, supply, demand, title="供需匹配")
    assert hasattr(fig, "savefig")
    plt.close("all")


def test_small_multiples_returns_figure():
    factors = [
        {"name": "温度", "x": [20, 25, 30, 35], "y": [10, 15, 12, 8]},
        {"name": "湿度", "x": [30, 40, 50, 60], "y": [20, 25, 22, 18]},
    ]
    fig = small_multiples(factors, title="敏感性分析")
    assert hasattr(fig, "savefig")
    plt.close("all")
```

- [ ] **Step 2: 运行测试确认失败**

Run: `cd c:/Users/6sn/.codex/skills/plotting && python -m pytest tests/test_advanced_charts.py -v`
Expected: FAIL — `bullet`, `supply_demand`, `small_multiples` 不存在

- [ ] **Step 3: 创建 _bullet.py**

```python
"""Bullet chart — threshold compliance visualization."""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.ticker import PercentFormatter
from acadp._style import COLORS, _ensure_style, finalize_plot, set_chart_title


def _pass_check(actual, threshold, direction):
    direction = str(direction).strip()
    if direction.startswith("<"):
        return actual <= threshold
    if direction.startswith(">"):
        return actual >= threshold
    return abs(actual - threshold) <= 1e-9


def _format_number(value, as_percent=False):
    if as_percent:
        return f"{value * 100:.1f}%"
    return f"{value:.1f}"


def bullet(categories, actual, threshold, directions=None, unit="",
           title=None, xlabel=None, ylabel=None, ax=None, **kwargs):
    """Bullet chart showing threshold compliance status.

    Args:
        categories: list of category labels
        actual: array of actual values
        threshold: array of threshold values
        directions: list of direction strings (e.g., [">=", ">="])
        unit: "ratio"/"percent"/"%" for percentage formatting
        title: chart title
        ax: existing Axes or None

    Returns:
        matplotlib.axes.Axes
    """
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8.2, 4.9))

    categories = [str(c) for c in categories]
    actual = np.asarray(actual, dtype=float)
    threshold = np.asarray(threshold, dtype=float)
    if directions is None:
        directions = [">="] * len(categories)
    y = np.arange(len(categories))

    as_percent = unit.lower() in {"ratio", "percent", "%"} or unit == ""
    if as_percent and max(np.nanmax(actual), np.nanmax(threshold)) > 1.5:
        as_percent = False

    max_value = max(float(np.nanmax(actual)), float(np.nanmax(threshold))) * 1.15
    if as_percent:
        max_value = max(max_value, 1.0)

    for idx, category in enumerate(categories):
        passed = _pass_check(actual[idx], threshold[idx], directions[idx])
        color = COLORS["teal"] if passed else COLORS["coral"]
        ax.barh(idx, max_value, color="#F3F4F6", height=0.58, edgecolor="none")
        ax.barh(idx, actual[idx], color=color, height=0.42, alpha=0.9)
        ax.vlines(threshold[idx], idx - 0.34, idx + 0.34, color=COLORS["amber"], linewidth=2.5)
        ax.text(actual[idx] + max_value * 0.015, idx, _format_number(actual[idx], as_percent), va="center")
        ax.text(
            threshold[idx], idx + 0.42,
            f"{directions[idx]}{_format_number(threshold[idx], as_percent)}",
            ha="center", va="bottom", fontsize=9, color=COLORS["amber"],
        )

    ax.set_yticks(y)
    ax.set_yticklabels(categories)
    ax.set_xlim(0, max_value)
    ax.invert_yaxis()
    if as_percent:
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
    if xlabel:
        ax.set_xlabel(xlabel)
    else:
        ax.set_xlabel("指标值")
    if ylabel:
        ax.set_ylabel(ylabel)
    else:
        ax.set_ylabel("指标")
    if title:
        set_chart_title(ax, title)
    else:
        set_chart_title(ax, "指标阈值达标状态")

    handles = [
        mpatches.Patch(color=COLORS["teal"], label="达标"),
        mpatches.Patch(color=COLORS["coral"], label="未达标"),
        mlines.Line2D([], [], color=COLORS["amber"], linewidth=2.5, label="阈值"),
    ]
    ax.legend(handles=handles, loc="lower right", frameon=False)
    finalize_plot(ax.figure)
    return ax
```

- [ ] **Step 4: 创建 _supply_demand.py**

```python
"""Supply-demand balance chart."""
import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, palette, _ensure_style, finalize_plot, set_chart_title


def supply_demand(time, supply_components, demand, secondary=None,
                  title=None, xlabel=None, ylabel=None, ax=None, **kwargs):
    """Stacked area + demand line + net balance bar chart.

    Args:
        time: array of time values
        supply_components: dict mapping supply name → value array
        demand: array of demand values
        secondary: optional dict of secondary line series
        title: chart title
        ax: existing Axes (ignored — creates 2-panel figure)

    Returns:
        matplotlib.figure.Figure (2-panel: stacked area + net balance)
    """
    _ensure_style()
    time = np.asarray(time)
    supply = {name: np.asarray(values) for name, values in supply_components.items()}
    demand = np.asarray(demand)
    supply_total = np.sum(np.vstack(list(supply.values())), axis=0)
    net = supply_total - demand

    fig = plt.figure(figsize=(10.8, 6.4))
    gs = fig.add_gridspec(2, 1, height_ratios=[3.2, 1.15], hspace=0.1)
    ax_top = fig.add_subplot(gs[0])
    ax_bottom = fig.add_subplot(gs[1], sharex=ax_top)

    colors = palette(len(supply))
    ax_top.stackplot(time, list(supply.values()), labels=list(supply.keys()),
                     colors=colors, alpha=0.72)
    ax_top.plot(time, demand, color=COLORS["coral"], linewidth=2.4, label="需求")

    if secondary:
        for name, values in secondary.items():
            ax_top.plot(time, np.asarray(values), color=COLORS["muted"],
                        linestyle="--", linewidth=1.6, label=name)

    ax_top.set_ylabel(ylabel or "功率/数量")
    if title:
        set_chart_title(ax_top, title)
    else:
        set_chart_title(ax_top, "供需匹配与净差")
    ax_top.legend(loc="upper left", ncol=4, frameon=False)
    plt.setp(ax_top.get_xticklabels(), visible=False)

    bar_colors = [COLORS["teal"] if v >= 0 else COLORS["coral"] for v in net]
    ax_bottom.bar(time, net, color=bar_colors, alpha=0.85, width=0.72)
    ax_bottom.axhline(0, color=COLORS["axis"], linewidth=0.9)
    ax_bottom.set_xlabel(xlabel or "时间")
    ax_bottom.set_ylabel("净差")

    finalize_plot(fig)
    return fig
```

- [ ] **Step 5: 创建 _small_multiples.py**

```python
"""Small multiples for sensitivity analysis."""
import math
import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, palette, _ensure_style, finalize_plot, set_chart_title


def small_multiples(factors, y_label="结果指标", cols=2,
                    title=None, figsize=None, **kwargs):
    """Small multiples chart for multi-factor sensitivity analysis.

    Args:
        factors: list of dicts, each with "name", "x", "y", optional "baseline"
        y_label: shared y-axis label
        cols: number of columns
        title: overall title (unused — each panel gets its own)
        figsize: tuple or None

    Returns:
        matplotlib.figure.Figure
    """
    _ensure_style()
    rows = math.ceil(len(factors) / cols)
    if figsize is None:
        figsize = (11.5, 4.0 * rows)
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    axes = np.asarray(axes).reshape(-1)
    colors = palette(4)

    for idx, factor in enumerate(factors):
        ax = axes[idx]
        x = np.asarray(factor["x"])
        y = np.asarray(factor["y"])
        ax.plot(x, y, marker="o", color=colors[idx % len(colors)], linewidth=2.2)
        if len(x) >= 2:
            trend = np.poly1d(np.polyfit(x, y, 1))(x)
            ax.plot(x, trend, linestyle="--", linewidth=1.2, color=COLORS["muted"])
        if "baseline" in factor:
            ax.axvline(factor["baseline"], color=COLORS["muted"], linestyle=":", linewidth=1.2)
        ax.set_xlabel(factor["name"])
        ax.set_ylabel(y_label)
        set_chart_title(ax, factor["name"])

    for ax in axes[len(factors):]:
        ax.set_visible(False)

    finalize_plot(fig)
    return fig
```

- [ ] **Step 6: 更新 __init__.py 导出**

在 `src/acadp/charts/__init__.py` 中添加：

```python
from acadp.charts._bullet import bullet
from acadp.charts._supply_demand import supply_demand
from acadp.charts._small_multiples import small_multiples
```

并在 `__all__` 中添加 `"bullet"`, `"supply_demand"`, `"small_multiples"`。

在 `src/acadp/__init__.py` 的 import 列表和 `__all__` 中同样添加。

- [ ] **Step 7: 运行测试确认通过**

Run: `cd c:/Users/6sn/.codex/skills/plotting && python -m pytest tests/test_advanced_charts.py -v`
Expected: 3 passed

- [ ] **Step 8: Commit**

```bash
git add src/acadp/charts/_bullet.py src/acadp/charts/_supply_demand.py \
       src/acadp/charts/_small_multiples.py src/acadp/charts/__init__.py \
       src/acadp/__init__.py tests/test_advanced_charts.py
git commit -m "feat: add bullet, supply_demand, small_multiples chart modules"
```

---

### Task 7: 迁移 10 个核心示例脚本到 acadp API

**Files:**
- Create: `scripts/examples/` 目录
- Modify/Create: 10 个核心示例脚本

**Interfaces:**
- Consumes: `acadp.lineplot`, `acadp.barplot`, `acadp.scatter`, `acadp.heatmap`, `acadp.boxplot`, `acadp.violinplot`, `acadp.histogram`, `acadp.radar`, `acadp.area`, `acadp.stacked_bar`

- [ ] **Step 1: 创建 scripts/examples/ 目录**

```bash
mkdir -p scripts/examples
```

- [ ] **Step 2: 迁移 plot_line_basic.py → examples/line_basic.py**

```python
"""示例：基础折线图"""
import numpy as np
import acadp

np.random.seed(42)
x = np.linspace(0, 12, 100)
y = np.sin(x) * 10 + 50 + np.random.randn(100) * 2

ax = acadp.lineplot(x=x, y=y, title="单指标时间变化趋势",
                    xlabel="时间", ylabel="数值")
print("Done: line_basic")
```

- [ ] **Step 3: 迁移 plot_scatter_basic.py → examples/scatter_basic.py**

```python
"""示例：基础散点图"""
import numpy as np
import acadp

np.random.seed(42)
x = np.random.randn(100) * 10
y = 2 * x + np.random.randn(100) * 15 + 50

ax = acadp.scatter(x=x, y=y, title="双变量线性关系散点分布",
                   xlabel="X轴数据", ylabel="Y轴数据")
print("Done: scatter_basic")
```

- [ ] **Step 4: 迁移 plot_bar_basic.py → examples/bar_basic.py**

```python
"""示例：基础柱状图"""
import acadp

categories = ["方案A", "方案B", "方案C", "方案D", "方案E"]
values = [85, 72, 91, 68, 78]

ax = acadp.barplot(x=categories, y=values, title="各方案得分对比",
                   xlabel="方案", ylabel="得分", highlight="max")
print("Done: bar_basic")
```

- [ ] **Step 5: 迁移 plot_corr_heat.py → examples/heatmap_corr.py**

```python
"""示例：相关性热力图"""
import numpy as np
import pandas as pd
import acadp

np.random.seed(42)
df = pd.DataFrame(np.random.randn(100, 5), columns=["指标A", "指标B", "指标C", "指标D", "指标E"])

ax = acadp.heatmap(df.corr(), labels=list(df.columns), title="指标相关性矩阵")
print("Done: heatmap_corr")
```

- [ ] **Step 6: 迁移 plot_boxplot.py → examples/boxplot.py**

```python
"""示例：箱线图"""
import numpy as np
import pandas as pd
import acadp

np.random.seed(42)
df = pd.DataFrame({
    "方案": (["方案A"] * 30 + ["方案B"] * 30 + ["方案C"] * 30),
    "得分": np.concatenate([
        np.random.normal(80, 5, 30),
        np.random.normal(75, 8, 30),
        np.random.normal(85, 4, 30),
    ]),
})

ax = acadp.boxplot(df, x="方案", y="得分", title="各方案得分分布")
print("Done: boxplot")
```

- [ ] **Step 7: 迁移 plot_violinplot.py → examples/violinplot.py**

```python
"""示例：小提琴图"""
import numpy as np
import pandas as pd
import acadp

np.random.seed(42)
df = pd.DataFrame({
    "组别": (["对照组"] * 50 + ["实验组"] * 50),
    "测量值": np.concatenate([
        np.random.normal(100, 15, 50),
        np.random.normal(110, 12, 50),
    ]),
})

ax = acadp.violinplot(df, x="组别", y="测量值", title="对照组与实验组测量值分布")
print("Done: violinplot")
```

- [ ] **Step 8: 迁移 plot_histogram.py → examples/histogram.py**

```python
"""示例：直方图"""
import numpy as np
import acadp

np.random.seed(42)
data = np.random.normal(100, 15, 200)

ax = acadp.histogram(data, title="测量值频率分布", xlabel="测量值", ylabel="频数")
print("Done: histogram")
```

- [ ] **Step 9: 迁移 plot_radar.py → examples/radar.py**

```python
"""示例：雷达图"""
import acadp

labels = ["准确性", "稳定性", "效率", "可解释性", "泛化能力"]
values = [85, 78, 92, 70, 82]

ax = acadp.radar(labels, values, title="模型综合评估雷达图")
print("Done: radar")
```

- [ ] **Step 10: 迁移 plot_area.py → examples/area.py**

```python
"""示例：面积图"""
import numpy as np
import acadp

x = list(range(1, 13))
y_dict = {
    "风电": [45, 42, 50, 55, 60, 58, 62, 65, 55, 48, 44, 46],
    "光伏": [20, 25, 35, 45, 55, 60, 58, 50, 40, 30, 22, 18],
}

ax = acadp.area(x, y_dict, title="月度发电量变化", xlabel="月份", ylabel="发电量 (MWh)")
print("Done: area")
```

- [ ] **Step 11: 迁移 plot_stacked_bar.py → examples/stacked_bar.py**

```python
"""示例：堆积柱状图"""
import acadp

categories = ["Q1", "Q2", "Q3", "Q4"]
components = {
    "产品A": [30, 35, 40, 38],
    "产品B": [20, 25, 22, 28],
    "产品C": [15, 18, 20, 22],
}

ax = acadp.stacked_bar(categories, components, title="季度销售构成",
                       xlabel="季度", ylabel="销售额 (万元)")
print("Done: stacked_bar")
```

- [ ] **Step 12: 验证所有示例可运行**

Run: `cd c:/Users/6sn/.codex/skills/plotting && for f in scripts/examples/*.py; do echo "=== $f ===" && python "$f" || break; done`
Expected: 所有 10 个示例输出 "Done: ..." 无报错

- [ ] **Step 13: Commit**

```bash
git add scripts/examples/
git commit -m "feat: migrate 10 core example scripts to acadp API"
```

---

### Task 8: 清理旧文件与更新测试

**Files:**
- Delete: `scripts/style.py`, `scripts/data_profiler.py`, `scripts/chart_planner.py`, `scripts/layout_qa.py`, `scripts/render_from_spec.py`
- Delete: `review/chart_reviewer.py`, `review/chart_auto_reviser.py`, `review/chart_review_rules.md`, `review/review_schema.json`, `review/review_report_template.md`
- Modify: `run_all_examples.py` — 改为遍历 scripts/examples/
- Modify: `tests/test_plot_workflow.py` — 更新 import 路径

**Interfaces:**
- Consumes: 所有已完成的 acadp 模块
- Produces: 干净的项目结构，无重复代码

- [ ] **Step 1: 更新 run_all_examples.py**

将 `run_all_examples.py` 的 `plot_scripts()` 函数改为遍历 `scripts/examples/`：

```python
def plot_scripts():
    examples_dir = ROOT / "scripts" / "examples"
    return sorted(examples_dir.glob("*.py"))
```

同时更新 `NON_EXAMPLE_SCRIPTS` 集合（不再需要，因为 examples/ 目录只包含示例脚本）。

- [ ] **Step 2: 更新 test_plot_workflow.py 的 import 路径**

将测试中引用 `SCRIPTS / "style.py"` 的路径改为 `ROOT / "src" / "acadp" / "_style.py"`，引用 `REVIEW / "chart_reviewer.py"` 改为导入 `acadp._reviewer`。

- [ ] **Step 3: 删除旧文件**

```bash
# 删除 scripts/ 下的旧模块
git rm scripts/style.py scripts/data_profiler.py scripts/chart_planner.py \
       scripts/layout_qa.py scripts/render_from_spec.py

# 删除 review/ 目录
git rm -r review/
```

- [ ] **Step 4: 运行所有测试**

Run: `cd c:/Users/6sn/.codex/skills/plotting && python -m pytest tests/ -v`
Expected: 所有测试通过（可能需要根据实际 import 错误做微调）

- [ ] **Step 5: 运行所有示例验证**

Run: `cd c:/Users/6sn/.codex/skills/plotting && python run_all_examples.py --output-dir /tmp/test_outputs`
Expected: `PNG_COUNT=10`, `METADATA_COUNT=10`, 无 FAILED

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "chore: remove duplicate scripts/ and review/ modules, update tests and run_all_examples"
```
