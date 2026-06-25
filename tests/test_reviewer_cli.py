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
        meta_path = tmp_path / "test_chart.metadata.json"
        png_path = tmp_path / "test_chart.png"
        meta_path.write_text(json.dumps({
            "figure_name": "test_chart", "plot_type": "bar",
            "problem_type": "评价类", "modeling_purpose": "测试",
            "variables": {"x": "类别", "y": "值"},
            "axis_labels": {"x": "类别", "y": "值"},
            "legend_labels": [], "caption": "测试图",
            "usage": "paper", "annotate": False, "annotation_config": None,
        }), encoding="utf-8")
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
