import pandas as pd
import numpy as np
import pytest


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
    np.random.seed(42)
    df = pd.DataFrame(np.random.randn(100, 4), columns=["a", "b", "c", "d"])
    ax = suggest(df, task="分析变量之间的相关性")
    assert ax is not None


def test_choose_chart_returns_string():
    from acadp._planner import choose_chart
    profile = {"plotting_hints": {"has_categories": True}, "columns": {}}
    result = choose_chart(profile, "对比各方案")
    assert isinstance(result, str)
    assert result in [
        "lineplot", "barplot", "scatter", "heatmap", "boxplot",
        "violinplot", "histogram", "radar", "area", "stacked_bar",
    ]


def test_choose_chart_default_fallback_categories():
    from acadp._planner import choose_chart
    profile = {"plotting_hints": {"has_categories": True}, "columns": {}}
    result = choose_chart(profile, "some unrelated text")
    assert result == "barplot"


def test_choose_chart_default_fallback_time():
    from acadp._planner import choose_chart
    profile = {"plotting_hints": {"has_time_axis": True}, "columns": {}}
    result = choose_chart(profile, "some unrelated text")
    assert result == "lineplot"


def test_choose_chart_default_fallback_heatmap():
    from acadp._planner import choose_chart
    profile = {
        "plotting_hints": {},
        "columns": {
            "a": {"semantic_type": "numeric"},
            "b": {"semantic_type": "cost"},
            "c": {"semantic_type": "ratio"},
        },
    }
    result = choose_chart(profile, "some unrelated text")
    assert result == "heatmap"


def test_suggest_scatter():
    from acadp._suggest import suggest
    np.random.seed(42)
    df = pd.DataFrame({"x": np.random.randn(50), "y": np.random.randn(50)})
    ax = suggest(df, task="分析x和y的散点关系")
    assert ax is not None


def test_suggest_radar():
    from acadp._suggest import suggest
    df = pd.DataFrame({"指标": ["A", "B", "C", "D"], "得分": [80, 90, 70, 85]})
    ax = suggest(df, task="综合评估雷达图")
    assert ax is not None


def test_suggest_histogram():
    from acadp._suggest import suggest
    np.random.seed(42)
    df = pd.DataFrame({"value": np.random.randn(200)})
    ax = suggest(df, task="查看数据的频率分布直方图")
    assert ax is not None
