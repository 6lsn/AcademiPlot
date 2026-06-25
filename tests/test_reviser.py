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
