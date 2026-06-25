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
