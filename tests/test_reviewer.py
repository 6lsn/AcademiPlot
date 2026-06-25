"""Tests for acadp._reviewer -- 6-dimension chart quality review system."""

import json
import tempfile
from pathlib import Path

from acadp._reviewer import (
    ReviewResult,
    BatchReport,
    review,
    review_dir,
    _review_metadata,
    _count_annotations,
    _has_causal_claim,
    _plot_matches_problem,
    _normalize_text,
    SCORE_KEYS,
)


# ============================================================
# ReviewResult dataclass
# ============================================================

class TestReviewResult:
    def test_defaults(self):
        r = ReviewResult()
        assert r.figure == ""
        assert r.score == 0
        assert r.status == "unknown"
        assert r.scores == {}
        assert r.major_issues == []
        assert r.minor_issues == []

    def test_to_markdown_basic(self):
        r = ReviewResult(
            figure="fig_cost",
            score=85,
            status="pass",
            scores={"theme_fit": 90, "chart_suitability": 80, "readability": 85,
                    "annotation_quality": 80, "caption_consistency": 85, "paper_style": 90},
            major_issues=[],
            minor_issues=["缺少 x 轴标签"],
        )
        md = r.to_markdown()
        assert "fig_cost" in md
        assert "pass" in md
        assert "85/100" in md
        assert "缺少 x 轴标签" in md

    def test_to_markdown_with_major_issues(self):
        r = ReviewResult(
            figure="fig_bad",
            score=30,
            status="reject",
            scores={k: 30 for k in SCORE_KEYS},
            major_issues=["缺少 problem_type", "饼图不适合预测类"],
            minor_issues=[],
            suggested_caption="建议添加图注",
        )
        md = r.to_markdown()
        assert "reject" in md
        assert "缺少 problem_type" in md
        assert "建议添加图注" in md


# ============================================================
# BatchReport dataclass
# ============================================================

class TestBatchReport:
    def test_defaults(self):
        r = BatchReport()
        assert r.total == 0
        assert r.pass_count == 0
        assert r.results == []

    def test_to_markdown(self):
        report = BatchReport(
            total=3,
            pass_count=2,
            revise_count=1,
            results=[
                ReviewResult(figure="fig1", status="pass", score=90, scores={k: 90 for k in SCORE_KEYS}),
                ReviewResult(figure="fig2", status="pass", score=85, scores={k: 85 for k in SCORE_KEYS}),
                ReviewResult(figure="fig3", status="revise", score=60, scores={k: 60 for k in SCORE_KEYS}),
            ],
        )
        md = report.to_markdown()
        assert "Total: 3" in md
        assert "Pass: 2" in md
        assert "Revise: 1" in md
        assert "fig1" in md
        assert "fig3" in md

    def test_to_markdown_with_path(self):
        report = BatchReport(total=1, pass_count=1, results=[
            ReviewResult(figure="x", status="pass", score=90, scores={k: 90 for k in SCORE_KEYS}),
        ])
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w") as f:
            path = f.name
        md = report.to_markdown(path=path)
        written = Path(path).read_text(encoding="utf-8")
        assert written == md
        Path(path).unlink()


# ============================================================
# Helper functions
# ============================================================

class TestHelpers:
    def test_normalize_text_none(self):
        assert _normalize_text(None) == ""

    def test_normalize_text_dict(self):
        result = _normalize_text({"a": 1})
        assert isinstance(result, str)
        assert "a" in result

    def test_normalize_text_str(self):
        assert _normalize_text("hello") == "hello"

    def test_count_annotations_with_count(self):
        assert _count_annotations({"annotation_config": {"count": 3}}) == 3

    def test_count_annotations_with_items(self):
        items = [{"text": "a"}, {"text": "b"}]
        assert _count_annotations({"annotation_config": {"items": items}}) == 2

    def test_count_annotations_annotate_flag(self):
        assert _count_annotations({"annotate": True}) == 1

    def test_count_annotations_none(self):
        assert _count_annotations({}) == 0

    def test_has_causal_claim_true(self):
        metadata = {"caption": "温度导致产量下降"}
        assert _has_causal_claim(metadata) is True

    def test_has_causal_claim_false(self):
        metadata = {"caption": "温度与产量关系"}
        assert _has_causal_claim(metadata) is False

    def test_plot_matches_problem(self):
        assert _plot_matches_problem("bar", "评价类") is True
        assert _plot_matches_problem("line", "预测类") is True
        assert _plot_matches_problem("pie", "预测类") is False

    def test_plot_matches_problem_empty(self):
        assert _plot_matches_problem("", "") is False


# ============================================================
# review() with metadata dict
# ============================================================

class TestReviewFromDict:
    def test_basic_bar_chart(self):
        metadata = {
            "figure_name": "test_fig",
            "plot_type": "bar",
            "problem_type": "评价类",
            "modeling_purpose": "展示各方案成本对比",
            "variables": {"x": "方案", "y": "成本"},
            "axis_labels": {"x": "方案", "y": "成本"},
            "legend_labels": [],
            "caption": "各方案成本对比",
            "usage": "paper",
        }
        result = review(metadata)
        assert isinstance(result, ReviewResult)
        assert result.figure == "test_fig"
        assert result.status in ("pass", "revise", "manual_review", "reject")
        assert isinstance(result.scores, dict)
        for key in SCORE_KEYS:
            assert key in result.scores

    def test_missing_problem_type(self):
        metadata = {
            "figure_name": "test_fig",
            "plot_type": "bar",
            "modeling_purpose": "展示数据",
            "variables": {"x": "a", "y": "b"},
            "axis_labels": {"x": "a", "y": "b"},
            "caption": "测试图注",
            "usage": "paper",
        }
        result = review(metadata)
        assert any("problem_type" in issue for issue in result.major_issues)
        assert result.scores["theme_fit"] < 100

    def test_pie_for_prediction(self):
        metadata = {
            "figure_name": "bad_pie",
            "plot_type": "pie",
            "problem_type": "预测类",
            "modeling_purpose": "预测趋势",
            "variables": {"x": "时间", "y": "值"},
            "caption": "预测饼图",
            "usage": "paper",
        }
        result = review(metadata)
        assert result.status in ("revise", "reject")
        assert any("饼图" in issue for issue in result.major_issues)

    def test_causal_claim_penalized(self):
        metadata = {
            "figure_name": "causal_fig",
            "plot_type": "bar",
            "problem_type": "评价类",
            "modeling_purpose": "评价方案",
            "variables": {"x": "方案", "y": "成本"},
            "axis_labels": {"x": "方案", "y": "成本"},
            "caption": "方案A导致成本下降",
            "usage": "paper",
        }
        result = review(metadata)
        assert any("因果" in issue for issue in result.major_issues)
        assert result.scores["annotation_quality"] < 100

    def test_no_caption_penalized(self):
        metadata = {
            "figure_name": "no_caption",
            "plot_type": "line",
            "problem_type": "预测类",
            "modeling_purpose": "预测趋势",
            "variables": {"x": "时间", "y": "值"},
            "axis_labels": {"x": "时间", "y": "值"},
            "caption": "",
            "usage": "paper",
        }
        result = review(metadata)
        assert any("图注" in issue for issue in result.major_issues)
        assert result.scores["caption_consistency"] < 100

    def test_caution_chart_for_paper(self):
        metadata = {
            "figure_name": "3d_fig",
            "plot_type": "3d_surface",
            "problem_type": "优化类",
            "modeling_purpose": "展示响应面",
            "variables": {"x": "a", "y": "b", "z": "c"},
            "axis_labels": {"x": "a", "y": "b"},
            "caption": "响应面",
            "usage": "paper",
        }
        result = review(metadata)
        assert any("慎用" in issue for issue in result.minor_issues)

    def test_internal_title_penalized(self):
        metadata = {
            "figure_name": "titled",
            "plot_type": "bar",
            "problem_type": "评价类",
            "modeling_purpose": "评价",
            "variables": {"x": "a", "y": "b"},
            "axis_labels": {"x": "a", "y": "b"},
            "caption": "图注",
            "internal_title": "图内标题",
            "usage": "paper",
        }
        result = review(metadata)
        assert any("图内标题" in issue for issue in result.minor_issues)
        assert result.scores["paper_style"] < 100

    def test_annotation_overflow(self):
        metadata = {
            "figure_name": "annotated",
            "plot_type": "line",
            "problem_type": "预测类",
            "modeling_purpose": "趋势",
            "variables": {"x": "t", "y": "v"},
            "axis_labels": {"x": "t", "y": "v"},
            "caption": "趋势图",
            "annotate": True,
            "annotation_config": {"count": 5},
            "usage": "paper",
        }
        result = review(metadata)
        assert any("annotation" in issue.lower() for issue in result.major_issues)

    def test_missing_axis_labels(self):
        metadata = {
            "figure_name": "no_axes",
            "plot_type": "bar",
            "problem_type": "评价类",
            "modeling_purpose": "评价",
            "variables": {"x": "a", "y": "b"},
            "axis_labels": {},
            "caption": "图注",
            "usage": "paper",
        }
        result = review(metadata)
        assert any("x 轴标签" in issue for issue in result.minor_issues)
        assert result.scores["readability"] < 100

    def test_scores_in_range(self):
        """All scores must be 0..100."""
        metadata = {
            "figure_name": "worst",
            "plot_type": "pie",
            "problem_type": "预测类",
            "modeling_purpose": "",
            "variables": {},
            "axis_labels": {},
            "caption": "",
            "annotate": True,
            "annotation_config": {"count": 10},
            "usage": "paper",
        }
        result = review(metadata)
        for key, val in result.scores.items():
            assert 0 <= val <= 100, f"{key}={val} out of range"


# ============================================================
# review() with JSON file
# ============================================================

class TestReviewFromFile:
    def test_review_json_path(self):
        metadata = {
            "figure_name": "file_fig",
            "plot_type": "bar",
            "problem_type": "评价类",
            "modeling_purpose": "评价方案",
            "variables": {"x": "方案", "y": "成本"},
            "axis_labels": {"x": "方案", "y": "成本"},
            "caption": "方案对比",
            "usage": "paper",
        }
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w", encoding="utf-8") as f:
            json.dump(metadata, f)
            path = f.name
        try:
            result = review(path)
            assert isinstance(result, ReviewResult)
            assert result.status in ("pass", "revise", "manual_review", "reject")
        finally:
            Path(path).unlink()

    def test_review_png_with_missing_metadata(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name
        try:
            result = review(path)
            assert result.status == "reject"
            assert any("metadata" in issue.lower() for issue in result.major_issues)
        finally:
            Path(path).unlink()


# ============================================================
# review_dir()
# ============================================================

class TestReviewDir:
    def test_review_dir_basic(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            for i, status_hint in enumerate(["bar", "line"]):
                meta = {
                    "figure_name": f"fig_{i}",
                    "plot_type": status_hint,
                    "problem_type": "评价类",
                    "modeling_purpose": "评价方案",
                    "variables": {"x": "方案", "y": "成本"},
                    "axis_labels": {"x": "方案", "y": "成本"},
                    "caption": f"图注 {i}",
                    "usage": "paper",
                }
                p = Path(tmpdir) / f"fig_{i}.metadata.json"
                p.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")

            report = review_dir(tmpdir)
            assert isinstance(report, BatchReport)
            assert report.total == 2
            assert len(report.results) == 2
            assert report.pass_count + report.revise_count + report.manual_count + report.reject_count == report.total

    def test_review_dir_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            report = review_dir(tmpdir)
            assert report.total == 0
            assert report.results == []
