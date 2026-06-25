import pandas as pd
import numpy as np


def test_auto_plot_returns_result():
    from acadp._suggest import auto_plot, AutoPlotResult
    df = pd.DataFrame({"method": ["A", "B", "C"], "cost": [100, 200, 150]})
    result = auto_plot(df, task="展示各方案的成本对比")
    assert isinstance(result, AutoPlotResult)
    assert result.chart is not None
    assert result.report is not None


def test_auto_plot_report_has_status():
    from acadp._suggest import auto_plot
    df = pd.DataFrame({"x": range(10), "y": range(10)})
    result = auto_plot(df, task="展示趋势")
    assert result.report.status in ("pass", "revise", "manual_review", "reject")


def test_revise_metadata_fixes_caption():
    from acadp._reviser import revise_metadata
    from acadp._reviewer import ReviewResult
    meta = {"caption": "", "variables": {}, "axis_labels": {"x": "year", "y": "gdp"}}
    r = ReviewResult(suggested_caption="GDP trend over years")
    revised, changes, blocked = revise_metadata(meta, r)
    assert revised["caption"] == "GDP trend over years"
    assert len(changes) > 0
