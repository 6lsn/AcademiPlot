# AcademiPlot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the existing math-modeling chart skill into `acadp` — a pip-installable academic chart library with one-line API, smart suggest, and quality review.

**Architecture:** `src/acadp/` layout with `_style.py` foundation, `charts/` modules for each chart type, `_suggest.py` orchestrating planner/profiler/reviewer, and `__init__.py` exporting a flat public API (`acadp.lineplot()`, `acadp.suggest()`, etc.).

**Tech Stack:** Python 3.9+, matplotlib, numpy, pandas, pyyaml. Package via pyproject.toml (setuptools). Tests via pytest.

## Global Constraints

- All Chinese labels/annotations preserved (academic audience is Chinese-first)
- matplotlib only — no plotly, bokeh, or other backends
- Every chart function returns `matplotlib.axes.Axes` for composability
- `set_style()` applied lazily on first chart call, not at import time
- No side effects on `import acadp` — no rcParams mutation until first use
- All tests runnable with `pytest tests/ -v`

---

## Phase 1: Project Skeleton

### Task 1: Create project structure and pyproject.toml

**Files:**
- Create: `pyproject.toml`
- Create: `src/acadp/__init__.py`
- Create: `src/acadp/charts/__init__.py`
- Create: `src/acadp/_recipes/__init__.py`
- Create: `tests/__init__.py`
- Create: `LICENSE`
- Create: `CHANGELOG.md`

**Interfaces:**
- Produces: `pip install -e .` works; `import acadp` succeeds (empty API)

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p src/acadp/charts src/acadp/_recipes tests gallery docs examples
```

- [ ] **Step 2: Write pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "acadp"
version = "0.1.0"
description = "Publication-ready academic figures in one line"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.9"
dependencies = [
    "matplotlib>=3.5",
    "numpy>=1.21",
    "pandas>=1.3",
    "pyyaml>=5.4",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-mpl"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 3: Write src/acadp/__init__.py (minimal)**

```python
"""AcademiPlot — publication-ready academic figures in one line."""

__version__ = "0.1.0"
```

- [ ] **Step 4: Write empty __init__.py for subpackages**

```bash
touch src/acadp/charts/__init__.py
touch src/acadp/_recipes/__init__.py
touch tests/__init__.py
```

- [ ] **Step 5: Write LICENSE (MIT)**

Standard MIT license with year 2026.

- [ ] **Step 6: Verify install works**

```bash
cd /path/to/AcademiPlot
pip install -e ".[dev]"
python -c "import acadp; print(acadp.__version__)"
```
Expected: `0.1.0`

- [ ] **Step 7: Commit**

```bash
git init
git add .
git commit -m "feat: project skeleton with pyproject.toml"
```

---

### Task 2: Style engine — _style.py

**Files:**
- Create: `src/acadp/_style.py`
- Create: `tests/test_style.py`

**Interfaces:**
- Consumes: nothing (foundation module)
- Produces:
  - `apply_paper_style()` — sets matplotlib rcParams
  - `set_style(name: str)` — switch theme ("nature"/"science"/"ieee")
  - `set_dpi(dpi: int)`, `set_font(font: str)`, `set_context(ctx: str)`
  - `get_style() -> dict` — current style config
  - `COLORS: dict`, `PALETTE: list`, `palette(n) -> list`
  - `style_axis(ax, grid=False)`, `finalize_plot(fig=None)`
  - `save_figure(fig, path, dpi=300)` — save without side effects

- [ ] **Step 1: Write failing test for set_style**

```python
# tests/test_style.py
def test_set_style_returns_none():
    """set_style should not raise and should accept known themes."""
    from acadp._style import set_style
    set_style("nature")  # should not raise

def test_get_style_returns_dict():
    from acadp._style import get_style, set_style
    set_style("nature")
    s = get_style()
    assert isinstance(s, dict)
    assert "dpi" in s
    assert "font" in s
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_style.py -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'acadp._style'`

- [ ] **Step 3: Implement _style.py**

Migrate from existing `scripts/style.py`. Key changes:
- Remove module-level `apply_paper_style()` call (line 428) — make it lazy
- Add `set_style(name)` / `get_style()` / `set_dpi()` / `set_font()` / `set_context()`
- Store state in a module-level `_CONFIG` dict
- Keep `COLORS`, `PALETTE`, `palette(n)`, `style_axis()`, `finalize_plot()`
- Add `save_figure(fig, path, dpi)` that only saves, no metadata side effects
- Keep annotation helpers unchanged

```python
# src/acadp/_style.py (skeleton — full migration of scripts/style.py)
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

COLORS = {
    "blue_main": "#3B6BA5", "blue_light": "#6B93C7",
    "teal": "#3D8C6A", "teal_light": "#6AAF8A",
    "amber": "#D4942B", "crimson": "#C44D4D", "crimson_light": "#D97A6B",
    "purple": "#7C5E9E", "purple_light": "#A88FC4",
    "grid": "#E2E6ED", "axis": "#6B7280", "text": "#1F2937",
    "muted": "#9CA3AF", "background": "#FFFFFF",
    "blue_seq": ["#3B6BA5", "#5B8EC9", "#8AB3E0", "#B8D4EF"],
    "green_seq": ["#3D8C6A", "#6AAF8A", "#9ED1B2", "#C8E6D8"],
    "red_seq": ["#C44D4D", "#D97A6B", "#ECA89A", "#F5D6D6"],
}
_OLD_MAP = {"blue": "blue_main", "seagreen": "teal"}
for _old, _new in _OLD_MAP.items():
    if _old not in COLORS:
        COLORS[_old] = COLORS[_new]

PALETTE = [COLORS["blue_main"], COLORS["amber"], COLORS["teal"],
           COLORS["crimson"], COLORS["purple"], COLORS["blue_light"],
           COLORS["teal_light"], COLORS["crimson_light"]]

PAPER_CMAP = LinearSegmentedColormap.from_list(
    "paper_main", [COLORS["blue_main"], COLORS["teal"], COLORS["amber"], COLORS["crimson"]])
DIVERGING_CMAP = LinearSegmentedColormap.from_list(
    "paper_diverging", [COLORS["blue_main"], "#F3F4F6", COLORS["crimson"]])

def palette(n):
    return [PALETTE[i % len(PALETT)] for i in range(n)]

# --- Style config ---
_CONFIG = {"style": "nature", "dpi": 300, "font": None, "context": "paper"}

_STYLES = {
    "nature": {"font.sans-serif": ["Microsoft YaHei", "SimHei", "Arial"],
               "font.family": ["sans-serif"], "axes.unicode_minus": False,
               "figure.dpi": 120, "savefig.dpi": 300, "savefig.bbox": "tight",
               "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
               "legend.frameon": False, "lines.linewidth": 1.8},
    "science": {},  # inherits nature, overrides specific
    "ieee": {},
}
_STYLES["science"] = {**_STYLES["nature"], "font.serif": ["Times New Roman", "SimHei"], "font.family": ["serif"]}
_STYLES["ieee"] = {**_STYLES["nature"], "figure.dpi": 150, "savefig.dpi": 600}

_style_applied = False

def apply_paper_style():
    global _style_applied
    style_name = _CONFIG.get("style", "nature")
    rc = dict(_STYLES.get(style_name, _STYLES["nature"]))
    if _CONFIG.get("font"):
        rc["font.sans-serif"] = [_CONFIG["font"]] + rc.get("font.sans-serif", [])
    rc["savefig.dpi"] = _CONFIG.get("dpi", 300)
    plt.rcParams.update(rc)
    _style_applied = True

def _ensure_style():
    if not _style_applied:
        apply_paper_style()

def set_style(name):
    if name not in _STYLES:
        raise ValueError(f"Unknown style: {name}. Choose from {list(_STYLES.keys())}")
    _CONFIG["style"] = name
    global _style_applied
    _style_applied = False  # force re-apply on next chart

def get_style():
    return dict(_CONFIG)

def set_dpi(dpi):
    _CONFIG["dpi"] = int(dpi)
    plt.rcParams["savefig.dpi"] = _CONFIG["dpi"]

def set_font(font):
    _CONFIG["font"] = font
    global _style_applied
    _style_applied = False

def set_context(ctx):
    if ctx not in ("paper", "presentation", "poster"):
        raise ValueError(f"context must be paper/presentation/poster")
    _CONFIG["context"] = ctx

def style_axis(ax, grid=False, grid_axis="y"):
    # ... (migrate from scripts/style.py lines 120-149)
    pass

def finalize_plot(fig=None, grid=False):
    _ensure_style()
    fig = fig or plt.gcf()
    for ax in fig.get_axes():
        style_axis(ax, grid=grid)
    fig.tight_layout()

def save_figure(fig, path, dpi=None):
    _ensure_style()
    dpi = dpi or _CONFIG.get("dpi", 300)
    finalize_plot(fig)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0.06)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_style.py -v
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/acadp/_style.py tests/test_style.py
git commit -m "feat: style engine with lazy application and theme switching"
```

---

### Task 3: Data profiler — _profiler.py

**Files:**
- Create: `src/acadp/_profiler.py`
- Create: `tests/test_profiler.py`

**Interfaces:**
- Consumes: nothing
- Produces:
  - `profile_data(source) -> dict` — accepts DataFrame / CSV path / Excel path
  - `infer_semantic_type(name, series) -> str`
  - Returns dict with `columns`, `semantic_hints`, `plotting_hints`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_profiler.py
import pandas as pd

def test_profile_dataframe():
    from acadp._profiler import profile_data
    df = pd.DataFrame({"year": [2020, 2021, 2022], "gdp": [100, 110, 120], "type": ["A", "B", "A"]})
    result = profile_data(df)
    assert "columns" in result
    assert result["columns"]["year"]["semantic_type"] == "numeric"
    assert result["columns"]["type"]["semantic_type"] == "category"

def test_infer_semantic_types():
    from acadp._profiler import infer_semantic_type
    import pandas as pd
    assert infer_semantic_type("成本", pd.Series([10, 20, 30])) == "cost"
    assert infer_semantic_type("时间", pd.Series(["2020-01", "2021-01"])) == "time"
    assert infer_semantic_type("状态", pd.Series(["达标", "未达标"])) == "status"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_profiler.py -v
```
Expected: FAIL

- [ ] **Step 3: Migrate data_profiler.py**

Migrate from `scripts/data_profiler.py`. Key changes:
- Remove `argparse` / `main()` CLI (keep as internal module)
- Remove `utf8_io` dependency
- Keep `infer_semantic_type()`, `summarize_column()`, `profile_dataframe()`, `profile_data()`
- Ensure `profile_data()` accepts DataFrame / str path

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_profiler.py -v
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/acadp/_profiler.py tests/test_profiler.py
git commit -m "feat: data profiler with semantic type inference"
```

---

## Phase 2: Core Charts

### Task 4: lineplot + barplot

**Files:**
- Create: `src/acadp/charts/_line.py`
- Create: `src/acadp/charts/_bar.py`
- Create: `tests/test_charts_core.py`

**Interfaces:**
- Consumes: `_style.py` (COLORS, _ensure_style, finalize_plot, save_figure)
- Produces:
  - `lineplot(data, x=None, y=None, title=None, **kwargs) -> Axes`
  - `barplot(data, x=None, y=None, highlight=None, title=None, **kwargs) -> Axes`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_charts_core.py
import numpy as np
import pandas as pd

def test_lineplot_returns_axes():
    import matplotlib.axes
    from acadp.charts._line import lineplot
    ax = lineplot(x=np.arange(10), y=np.arange(10), title="test")
    assert isinstance(ax, matplotlib.axes.Axes)

def test_lineplot_accepts_dataframe():
    from acadp.charts._line import lineplot
    df = pd.DataFrame({"year": range(2020, 2025), "val": [1, 2, 3, 4, 5]})
    ax = lineplot(df, x="year", y="val")
    assert ax.get_xlabel() == "year"

def test_barplot_highlight_max():
    from acadp.charts._bar import barplot
    ax = barplot(["A", "B", "C"], [10, 30, 20], highlight="max", title="test")
    # highlight="max" should annotate the tallest bar
    assert len(ax.patches) == 3
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_charts_core.py -v
```
Expected: FAIL

- [ ] **Step 3: Implement _line.py**

```python
# src/acadp/charts/_line.py
import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, _ensure_style, finalize_plot

def lineplot(data=None, x=None, y=None, title=None, xlabel=None, ylabel=None,
             color=None, linewidth=1.8, marker=None, label=None, ax=None, **kwargs):
    """Plot a line chart. Returns matplotlib Axes.

    Args:
        data: DataFrame (x/y are column names) or None (x/y are arrays)
        x: x values or column name
        y: y values or column name
        title: chart title
        highlight: not used for lineplot
    """
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    # Resolve x, y from DataFrame or direct arrays
    if data is not None:
        if hasattr(data, "columns"):  # DataFrame
            x_vals = data[x] if x else data.iloc[:, 0]
            y_vals = data[y] if y else data.iloc[:, 1]
        else:
            raise ValueError("data must be a DataFrame when provided")
    else:
        x_vals = np.asarray(x)
        y_vals = np.asarray(y)

    color = color or COLORS["blue_main"]
    ax.plot(x_vals, y_vals, color=color, linewidth=linewidth, marker=marker,
            label=label, **kwargs)
    if xlabel:
        ax.set_xlabel(xlabel)
    elif data is not None and x:
        ax.set_xlabel(x)
    if ylabel:
        ax.set_ylabel(ylabel)
    elif data is not None and y:
        ax.set_ylabel(y)
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", color=COLORS["text"], pad=10)
    finalize_plot(ax.figure)
    return ax
```

- [ ] **Step 4: Implement _bar.py**

```python
# src/acadp/charts/_bar.py
import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, PALETTE, _ensure_style, finalize_plot

def barplot(data=None, x=None, y=None, highlight=None, title=None,
            xlabel=None, ylabel=None, horizontal=False, ax=None, **kwargs):
    """Plot a bar chart. Returns matplotlib Axes.

    Args:
        highlight: "max", "min", or None — annotate the highest/lowest bar
    """
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    if data is not None and hasattr(data, "columns"):
        categories = data[x].tolist() if x else data.iloc[:, 0].tolist()
        values = data[y].tolist() if y else data.iloc[:, 1].tolist()
    else:
        categories = list(x) if x is not None else list(range(len(y)))
        values = list(y)

    colors = [PALETTE[i % len(PALETTE)] for i in range(len(categories))]
    bars = ax.bar(categories, values, color=colors, edgecolor="white", linewidth=1.5, **kwargs)

    if highlight in ("max", "min"):
        idx = int(np.argmax(values)) if highlight == "max" else int(np.argmin(values))
        bars[idx].set_edgecolor(COLORS["amber"])
        bars[idx].set_linewidth(2.5)
        ax.annotate(f"{values[idx]}", xy=(idx, values[idx]),
                    xytext=(0, 8), textcoords="offset points",
                    ha="center", fontsize=10, fontweight="bold", color=COLORS["amber"])

    if xlabel:
        ax.set_xlabel(xlabel)
    elif data is not None and x:
        ax.set_xlabel(x)
    if ylabel:
        ax.set_ylabel(ylabel)
    elif data is not None and y:
        ax.set_ylabel(y)
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", color=COLORS["text"], pad=10)
    finalize_plot(ax.figure)
    return ax
```

- [ ] **Step 5: Run tests**

```bash
pytest tests/test_charts_core.py -v
```
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/acadp/charts/_line.py src/acadp/charts/_bar.py tests/test_charts_core.py
git commit -m "feat: lineplot and barplot with one-line API"
```

---

### Task 5: scatter + heatmap

**Files:**
- Create: `src/acadp/charts/_scatter.py`
- Create: `src/acadp/charts/_heatmap.py`
- Modify: `tests/test_charts_core.py`

**Interfaces:**
- Produces:
  - `scatter(data, x, y, trend=False, title=None, **kwargs) -> Axes`
  - `heatmap(data, annot=True, cmap="diverging", title=None, **kwargs) -> Axes`

- [ ] **Step 1: Write failing tests**

```python
# Append to tests/test_charts_core.py
def test_scatter_with_trend():
    from acadp.charts._scatter import scatter
    np.random.seed(42)
    x = np.random.randn(50)
    y = 2 * x + np.random.randn(50)
    ax = scatter(x=x, y=y, trend=True, title="Correlation")
    # trend=True should add a line — check children count
    assert len(ax.lines) >= 1

def test_heatmap_square():
    from acadp.charts._heatmap import heatmap
    matrix = np.corrcoef(np.random.randn(3, 100))
    ax = heatmap(matrix, annot=True, labels=["A", "B", "C"])
    assert ax is not None
```

- [ ] **Step 2: Run tests — FAIL**

- [ ] **Step 3: Implement _scatter.py**

```python
# src/acadp/charts/_scatter.py
import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, _ensure_style, finalize_plot

def scatter(data=None, x=None, y=None, trend=False, title=None,
            xlabel=None, ylabel=None, color=None, alpha=0.7, ax=None, **kwargs):
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    if data is not None and hasattr(data, "columns"):
        x_vals = data[x].values if x else data.iloc[:, 0].values
        y_vals = data[y].values if y else data.iloc[:, 1].values
    else:
        x_vals = np.asarray(x)
        y_vals = np.asarray(y)

    color = color or COLORS["blue_main"]
    ax.scatter(x_vals, y_vals, c=color, alpha=alpha, edgecolors="white",
               s=60, linewidth=1.2, **kwargs)

    if trend:
        z = np.polyfit(x_vals, y_vals, 1)
        p = np.poly1d(z)
        x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
        ax.plot(x_line, p(x_line), color=COLORS["crimson"], linewidth=1.5, linestyle="--")
        r = np.corrcoef(x_vals, y_vals)[0, 1]
        ax.annotate(f"R² = {r**2:.3f}", xy=(0.05, 0.95), xycoords="axes fraction",
                    fontsize=10, color=COLORS["crimson"], va="top")

    if xlabel: ax.set_xlabel(xlabel)
    elif data is not None and x: ax.set_xlabel(x)
    if ylabel: ax.set_ylabel(ylabel)
    elif data is not None and y: ax.set_ylabel(y)
    if title: ax.set_title(title, fontsize=13, fontweight="bold", color=COLORS["text"], pad=10)
    finalize_plot(ax.figure)
    return ax
```

- [ ] **Step 4: Implement _heatmap.py**

```python
# src/acadp/charts/_heatmap.py
import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, DIVERGING_CMAP, _ensure_style, finalize_plot

def heatmap(data, annot=True, cmap="diverging", title=None, labels=None, ax=None, **kwargs):
    _ensure_style()
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 6))

    matrix = np.asarray(data)
    cm = DIVERGING_CMAP if cmap == "diverging" else cmap
    im = ax.imshow(matrix, cmap=cm, aspect="auto", **kwargs)

    if labels:
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontsize=9)

    if annot:
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                val = matrix[i, j]
                color = "white" if abs(val) > 0.6 else COLORS["text"]
                ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                        fontsize=9, color=color)

    plt.colorbar(im, ax=ax, shrink=0.8)
    if title: ax.set_title(title, fontsize=13, fontweight="bold", color=COLORS["text"], pad=10)
    finalize_plot(ax.figure)
    return ax
```

- [ ] **Step 5: Run tests — PASS**

- [ ] **Step 6: Commit**

```bash
git add src/acadp/charts/_scatter.py src/acadp/charts/_heatmap.py tests/test_charts_core.py
git commit -m "feat: scatter (with trend) and heatmap"
```

---

### Task 6: boxplot + violinplot + histogram

**Files:**
- Create: `src/acadp/charts/_box.py`
- Create: `src/acadp/charts/_violin.py`
- Create: `src/acadp/charts/_hist.py`
- Modify: `tests/test_charts_core.py`

- [ ] **Step 1: Write failing tests**

```python
def test_boxplot_groupby():
    from acadp.charts._box import boxplot
    df = pd.DataFrame({"val": np.random.randn(100), "grp": np.repeat(["A", "B"], 50)})
    ax = boxplot(df, y="val", groupby="grp")
    assert len(ax.patches) >= 2

def test_histogram_kde():
    from acadp.charts._hist import histogram
    ax = histogram(np.random.randn(200), kde=True)
    assert len(ax.patches) >= 1
    assert len(ax.lines) >= 1  # KDE line
```

- [ ] **Step 2: Run tests — FAIL**

- [ ] **Step 3: Implement _box.py, _violin.py, _hist.py**

Each follows the same pattern: accept data/x/y/groupby, resolve from DataFrame, plot with academic style, call finalize_plot, return Axes.

- [ ] **Step 4: Run tests — PASS**

- [ ] **Step 5: Commit**

```bash
git add src/acadp/charts/_box.py src/acadp/charts/_violin.py src/acadp/charts/_hist.py tests/test_charts_core.py
git commit -m "feat: boxplot, violinplot, histogram"
```

---

### Task 7: radar + area + stacked_bar

**Files:**
- Create: `src/acadp/charts/_radar.py`
- Create: `src/acadp/charts/_area.py`
- Create: `src/acadp/charts/_stacked_bar.py`
- Modify: `tests/test_charts_core.py`

- [ ] **Step 1: Write failing tests**

```python
def test_radar_returns_axes():
    from acadp.charts._radar import radar
    ax = radar(["Speed", "Power", "Cost"], [0.8, 0.6, 0.9])
    assert ax is not None

def test_stacked_bar():
    from acadp.charts._stacked_bar import stacked_bar
    ax = stacked_bar(["Q1", "Q2"], {"A": [10, 20], "B": [15, 25]})
    assert len(ax.patches) >= 4
```

- [ ] **Step 2: Run tests — FAIL**

- [ ] **Step 3: Implement all three**

- radar: polar axes, polygon fill
- area: stackplot with academic colors
- stacked_bar: bottom-up bar stacking with legend

- [ ] **Step 4: Run tests — PASS**

- [ ] **Step 5: Commit**

```bash
git add src/acadp/charts/_radar.py src/acadp/charts/_area.py src/acadp/charts/_stacked_bar.py tests/test_charts_core.py
git commit -m "feat: radar, area, stacked_bar"
```

---

### Task 8: Register charts in __init__.py

**Files:**
- Modify: `src/acadp/charts/__init__.py`
- Modify: `src/acadp/__init__.py`
- Create: `tests/test_imports.py`

**Interfaces:**
- Produces: `acadp.lineplot()`, `acadp.barplot()`, etc. all importable from top level

- [ ] **Step 1: Write failing test**

```python
# tests/test_imports.py
def test_top_level_imports():
    import acadp
    assert callable(getattr(acadp, "lineplot", None))
    assert callable(getattr(acadp, "barplot", None))
    assert callable(getattr(acadp, "scatter", None))
    assert callable(getattr(acadp, "heatmap", None))
    assert callable(getattr(acadp, "boxplot", None))
    assert callable(getattr(acadp, "violinplot", None))
    assert callable(getattr(acadp, "histogram", None))
    assert callable(getattr(acadp, "radar", None))
    assert callable(getattr(acadp, "area", None))
    assert callable(getattr(acadp, "stacked_bar", None))
```

- [ ] **Step 2: Run test — FAIL**

- [ ] **Step 3: Wire up imports**

```python
# src/acadp/charts/__init__.py
from acadp.charts._line import lineplot
from acadp.charts._bar import barplot
from acadp.charts._scatter import scatter
from acadp.charts._heatmap import heatmap
from acadp.charts._box import boxplot
from acadp.charts._violin import violinplot
from acadp.charts._hist import histogram
from acadp.charts._radar import radar
from acadp.charts._area import area
from acadp.charts._stacked_bar import stacked_bar

__all__ = ["lineplot", "barplot", "scatter", "heatmap", "boxplot",
           "violinplot", "histogram", "radar", "area", "stacked_bar"]
```

```python
# src/acadp/__init__.py
"""AcademiPlot — publication-ready academic figures in one line."""
__version__ = "0.1.0"

from acadp.charts import (
    lineplot, barplot, scatter, heatmap, boxplot,
    violinplot, histogram, radar, area, stacked_bar,
)
from acadp._style import set_style, get_style, set_dpi, set_font, set_context

__all__ = [
    "lineplot", "barplot", "scatter", "heatmap", "boxplot",
    "violinplot", "histogram", "radar", "area", "stacked_bar",
    "set_style", "get_style", "set_dpi", "set_font", "set_context",
]
```

- [ ] **Step 4: Run tests — PASS**

- [ ] **Step 5: Commit**

```bash
git add src/acadp/__init__.py src/acadp/charts/__init__.py tests/test_imports.py
git commit -m "feat: register all charts in top-level API"
```

---

## Phase 3: Smart Layer

### Task 9: Planner + suggest()

**Files:**
- Create: `src/acadp/_planner.py`
- Create: `src/acadp/_suggest.py`
- Create: `tests/test_suggest.py`

**Interfaces:**
- Consumes: `_profiler.py` (profile_data), `charts/*` (all chart functions)
- Produces:
  - `suggest(data, task: str, **kwargs) -> Axes` — smart chart selection + rendering
  - `choose_chart(profile: dict, task: str) -> str` — returns chart function name

- [ ] **Step 1: Write failing tests**

```python
# tests/test_suggest.py
import pandas as pd
import numpy as np

def test_suggest_bar_for_comparison():
    from acadp._suggest import suggest
    df = pd.DataFrame({"method": ["A", "B", "C"], "cost": [100, 200, 150]})
    ax = suggest(df, task="展示各方案的成本对比")
    assert ax is not None

def test_suggest_line_for_trend():
    from acadp._suggest import suggest
    df = pd.DataFrame({"year": range(2020, 2025), "val": [1, 2, 3, 4, 5]})
    ax = suggest(df, task="展示时间趋势变化")
    assert ax is not None

def test_suggest_heatmap_for_correlation():
    from acadp._suggest import suggest
    df = pd.DataFrame(np.random.randn(100, 4), columns=["a", "b", "c", "d"])
    ax = suggest(df, task="分析变量之间的相关性")
    assert ax is not None
```

- [ ] **Step 2: Run tests — FAIL**

- [ ] **Step 3: Implement _planner.py**

Adapt from `scripts/chart_planner.py`. Simplify to a function `choose_chart(profile, task) -> str` that maps data profile + task description to a chart function name. Use keyword scoring on the task string:

```python
# src/acadp/_planner.py
_TASK_KEYWORDS = {
    "barplot": ["对比", "比较", "各方案", "排名", "得分", "评分"],
    "lineplot": ["趋势", "变化", "时间", "增长", "下降", "走势"],
    "scatter": ["相关", "关系", "散点", "回归", "关联"],
    "heatmap": ["相关性", "相关矩阵", "热力", "矩阵"],
    "boxplot": ["分布", "箱线", "离散程度", "异常值"],
    "violinplot": ["分布", "密度", "小提琴"],
    "histogram": ["频率", "分布", "直方", "分组统计"],
    "radar": ["雷达", "综合评估", "多维", "多指标"],
    "area": ["面积", "堆积", "累计", "供需"],
    "stacked_bar": ["堆积", "构成", "结构", "占比"],
}

def choose_chart(profile, task):
    """Choose best chart type based on data profile and task description."""
    task_lower = task.lower()
    scores = {}
    for chart, keywords in _TASK_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in task_lower)
        if score:
            scores[chart] = score

    # Boost based on data shape
    hints = profile.get("plotting_hints", {})
    if hints.get("has_categories") and "barplot" in scores:
        scores["barplot"] += 2
    if hints.get("has_time_axis") and "lineplot" in scores:
        scores["lineplot"] += 2

    if not scores:
        # Default fallback based on data shape
        if hints.get("has_categories"):
            return "barplot"
        if hints.get("has_time_axis"):
            return "lineplot"
        return "lineplot"

    return max(scores, key=scores.get)
```

- [ ] **Step 4: Implement _suggest.py**

```python
# src/acadp/_suggest.py
import pandas as pd
import numpy as np
from acadp._profiler import profile_data
from acadp._planner import choose_chart
from acadp import charts

def _load_data(data):
    """Accept DataFrame / CSV path / Excel path, return DataFrame."""
    if isinstance(data, pd.DataFrame):
        return data
    if isinstance(data, (str,)):
        if data.endswith(".csv"):
            return pd.read_csv(data)
        if data.endswith((".xls", ".xlsx")):
            return pd.read_excel(data)
    raise ValueError(f"Unsupported data type: {type(data)}")

def suggest(data, task, **kwargs):
    """Smart chart selection: analyze data + task → pick best chart → render."""
    df = _load_data(data)
    profile = profile_data(df)
    chart_name = choose_chart(profile, task)
    chart_fn = getattr(charts, chart_name)

    # Auto-detect x/y from profile
    cols = profile.get("columns", {})
    hints = profile.get("plotting_hints", {})
    col_names = list(cols.keys())

    # Heuristic: first category col → x, first numeric col → y
    x_col, y_col = None, None
    for name, info in cols.items():
        if info["semantic_type"] == "category" and x_col is None:
            x_col = name
        if info["semantic_type"] in ("numeric", "cost", "ratio", "objective") and y_col is None:
            y_col = name
    if x_col is None and len(col_names) >= 1:
        x_col = col_names[0]
    if y_col is None and len(col_names) >= 2:
        y_col = col_names[1]

    # Call chart function with appropriate args
    if chart_name in ("heatmap",):
        # For heatmap, compute correlation matrix
        numeric_df = df.select_dtypes(include=[np.number])
        return chart_fn(numeric_df.corr(), labels=list(numeric_df.columns), title=task, **kwargs)
    elif chart_name in ("radar",):
        labels = df[x_col].tolist() if x_col else col_names
        values = df[y_col].tolist() if y_col else [0] * len(labels)
        return chart_fn(labels, values, title=task, **kwargs)
    elif chart_name in ("histogram",):
        return chart_fn(df[y_col].values, title=task, **kwargs)
    else:
        return chart_fn(df, x=x_col, y=y_col, title=task, **kwargs)
```

- [ ] **Step 5: Run tests — PASS**

- [ ] **Step 6: Commit**

```bash
git add src/acadp/_planner.py src/acadp/_suggest.py tests/test_suggest.py
git commit -m "feat: smart suggest() — auto-select chart from data + task"
```

---

### Task 10: Reviewer + review()

**Files:**
- Create: `src/acadp/_reviewer.py`
- Create: `tests/test_reviewer.py`

**Interfaces:**
- Consumes: metadata dict (from save_current_figure or manual)
- Produces:
  - `review(source) -> ReviewResult` — review a single figure
  - `review_dir(path) -> BatchReport` — review all .metadata.json in dir
  - `ReviewResult.score`, `.status`, `.suggestions`, `.to_markdown()`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_reviewer.py
def test_review_pass():
    from acadp._reviewer import review
    result = review("tests/fixtures/good_figure.png")  # we'll create a fixture
    assert result.status == "pass"

def test_review_result_has_fields():
    from acadp._reviewer import ReviewResult
    r = ReviewResult(score=85, status="pass", suggestions=[])
    assert r.score == 85
```

- [ ] **Step 2: Run tests — FAIL**

- [ ] **Step 3: Implement _reviewer.py**

Migrate from `review/chart_reviewer.py`. Key changes:
- Wrap in a `ReviewResult` dataclass
- `review()` accepts PNG path (reads companion .metadata.json) or metadata dict directly
- `review_dir()` accepts directory path
- Remove CLI / argparse
- Keep all scoring logic (6 dimensions)

```python
# src/acadp/_reviewer.py
from dataclasses import dataclass, field
from pathlib import Path
import json

@dataclass
class ReviewResult:
    figure: str = ""
    score: int = 0
    status: str = "unknown"  # pass / revise / manual_review / reject
    scores: dict = field(default_factory=dict)
    major_issues: list = field(default_factory=list)
    minor_issues: list = field(default_factory=list)
    suggested_caption: str = ""
    suggested_plot_type: str = ""
    recommended_action: str = ""

    def to_markdown(self):
        # ... render markdown report
        pass

@dataclass
class BatchReport:
    total: int = 0
    results: list = field(default_factory=list)

    def to_markdown(self, path=None):
        # ... render batch report
        pass

def review(source):
    """Review a figure. source: PNG path, metadata JSON path, or metadata dict."""
    if isinstance(source, dict):
        metadata = source
    else:
        path = Path(source)
        if path.suffix == ".png":
            meta_path = path.with_suffix(".metadata.json")
            # or path.with_name(path.stem + ".metadata.json")
            metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        elif path.suffix == ".json":
            metadata = json.loads(path.read_text(encoding="utf-8"))
    # ... scoring logic from chart_reviewer.py
    return ReviewResult(...)

def review_dir(directory):
    """Review all .metadata.json in a directory."""
    # ... migrate from chart_reviewer.py review_directory()
    return BatchReport(...)
```

- [ ] **Step 4: Run tests — PASS**

- [ ] **Step 5: Commit**

```bash
git add src/acadp/_reviewer.py tests/test_reviewer.py
git commit -m "feat: quality review system with 6-dimension scoring"
```

---

### Task 11: auto_plot() — suggest + review + revise

**Files:**
- Create: `src/acadp/_reviser.py`
- Modify: `src/acadp/_suggest.py` (add auto_plot)
- Create: `tests/test_auto_plot.py`

**Interfaces:**
- Produces:
  - `auto_plot(data, task) -> AutoPlotResult` — full pipeline
  - `AutoPlotResult.chart`, `.report`, `.recipe`

- [ ] **Step 1: Write failing test**

```python
def test_auto_plot_returns_result():
    from acadp._suggest import auto_plot
    import pandas as pd
    df = pd.DataFrame({"method": ["A", "B", "C"], "cost": [100, 200, 150]})
    result = auto_plot(df, task="展示各方案的成本对比")
    assert result.chart is not None
    assert result.report is not None
```

- [ ] **Step 2: Run test — FAIL**

- [ ] **Step 3: Implement _reviser.py + auto_plot()**

Migrate from `review/chart_auto_reviser.py`. Simplify to:
- `_reviser.py`: `revise_metadata(metadata) -> metadata` — apply safe fixes
- `_suggest.py`: add `AutoPlotResult` dataclass and `auto_plot()` function

```python
@dataclass
class AutoPlotResult:
    chart: object  # matplotlib Axes
    report: ReviewResult
    recipe: str

def auto_plot(data, task, **kwargs):
    """Full pipeline: suggest → render → review → revise → re-review."""
    ax = suggest(data, task, **kwargs)
    # ... review the generated figure, apply revisions if needed
    return AutoPlotResult(chart=ax, report=report, recipe=recipe_name)
```

- [ ] **Step 4: Run tests — PASS**

- [ ] **Step 5: Commit**

```bash
git add src/acadp/_reviser.py src/acadp/_suggest.py tests/test_auto_plot.py
git commit -m "feat: auto_plot() — full suggest+review+revise pipeline"
```

---

## Phase 4: Advanced Charts

### Task 12: pareto + contour

**Files:**
- Create: `src/acadp/charts/_pareto.py`
- Create: `src/acadp/charts/_contour.py`
- Modify: `tests/test_charts_core.py`

- [ ] **Step 1: Write failing tests**
- [ ] **Step 2: Run tests — FAIL**
- [ ] **Step 3: Implement (migrate from scripts/plot7.py and scripts/plot_contour.py)**
- [ ] **Step 4: Run tests — PASS**
- [ ] **Step 5: Commit**

```bash
git add src/acadp/charts/_pareto.py src/acadp/charts/_contour.py tests/test_charts_core.py
git commit -m "feat: pareto frontier and contour optimization charts"
```

---

### Task 13: waterfall + dumbbell

**Files:**
- Create: `src/acadp/charts/_waterfall.py`
- Create: `src/acadp/charts/_dumbbell.py`
- Modify: `tests/test_charts_core.py`

- [ ] **Step 1: Write failing tests**
- [ ] **Step 2: Run tests — FAIL**
- [ ] **Step 3: Implement (migrate from scripts/plot_waterfall.py, adapt dumbbell from recipes)**
- [ ] **Step 4: Run tests — PASS**
- [ ] **Step 5: Commit**

```bash
git add src/acadp/charts/_waterfall.py src/acadp/charts/_dumbbell.py tests/test_charts_core.py
git commit -m "feat: waterfall and dumbbell comparison charts"
```

---

## Phase 5: Packaging

### Task 14: README + Gallery

**Files:**
- Create: `README.md`
- Create: `README_CN.md`
- Create: `gallery/before_after/` (generated PNGs)
- Create: `gallery/showcase/` (generated PNGs)

- [ ] **Step 1: Generate gallery images**

```python
# scripts/generate_gallery.py
import acadp
import numpy as np
# Generate before/after comparison and showcase images
```

- [ ] **Step 2: Write README.md**

Structure:
1. One-line description + before/after image
2. `pip install acadp`
3. Quick Start (3 lines)
4. Gallery (10-15 images)
5. Features table
6. Comparison with matplotlib/seaborn
7. Contributing guide

- [ ] **Step 3: Write README_CN.md (Chinese version)**

- [ ] **Step 4: Commit**

```bash
git add README.md README_CN.md gallery/
git commit -m "docs: README with gallery and before/after comparison"
```

---

### Task 15: Examples + Docs

**Files:**
- Create: `examples/quick_start.py`
- Create: `examples/paper_workflow.py`
- Create: `docs/getting_started.md`
- Create: `docs/api_reference.md`

- [ ] **Step 1: Write quick_start.py**

```python
"""AcademiPlot Quick Start — 3 lines to a publication-ready figure."""
import acadp
import numpy as np

# Generate a Nature-style line plot
ax = acadp.lineplot(x=np.linspace(0, 10, 50), y=np.sin(np.linspace(0, 10, 50)),
                     title="Sine Wave", xlabel="x", ylabel="sin(x)")
acadp.save_figure(ax.figure, "quick_start.png")
```

- [ ] **Step 2: Write paper_workflow.py — full example**

- [ ] **Step 3: Write docs**

- [ ] **Step 4: Commit**

```bash
git add examples/ docs/
git commit -m "docs: examples and getting started guide"
```

---

## Phase 6: Release

### Task 16: PyPI + GitHub

**Files:**
- Modify: `pyproject.toml` (final version check)
- Create: `.gitignore`

- [ ] **Step 1: Verify package builds**

```bash
python -m build
```

- [ ] **Step 2: Verify install from wheel**

```bash
pip install dist/acadp-0.1.0-py3-none-any.whl
python -c "import acadp; print(acadp.__version__)"
```

- [ ] **Step 3: Create GitHub repo, push**

- [ ] **Step 4: Tag release**

```bash
git tag v0.1.0
git push origin v0.1.0
```

- [ ] **Step 5: Publish to PyPI (optional)**

```bash
twine upload dist/*
```
