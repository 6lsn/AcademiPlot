import runpy
import ast
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from struct import unpack

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import same_color

import acadp._style as style
from acadp._reviewer import review as review_figure, ReviewResult, SCORE_KEYS


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
EXAMPLES = ROOT / "scripts" / "examples"
sys.path.insert(0, str(SCRIPTS))

from utf8_io import utf8_subprocess_env

EXAMPLE_FILES = sorted(EXAMPLES.glob("*.py"))


def read_png_dpi(path):
    data = path.read_bytes()
    offset = 8
    while offset < len(data):
        length = unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_data = data[offset + 8 : offset + 8 + length]
        if chunk_type == b"pHYs":
            ppm_x, ppm_y, unit = unpack(">IIB", chunk_data[:9])
            if unit == 1:
                return round(ppm_x * 0.0254), round(ppm_y * 0.0254)
        offset += 12 + length
    return None



class PlotWorkflowTests(unittest.TestCase):
    def test_shared_style_module_sets_paper_defaults(self):
        style._apply_paper_style()
        fig, ax = plt.subplots()
        style.set_chart_title(ax, "测试业务主题")

        self.assertEqual(
            plt.rcParams["font.sans-serif"][:2], ["Microsoft YaHei", "SimHei"]
        )
        self.assertEqual(
            plt.rcParams["font.serif"][:3],
            ["Times New Roman", "Microsoft YaHei", "SimHei"],
        )
        self.assertFalse(plt.rcParams["axes.unicode_minus"])
        self.assertEqual(plt.rcParams["figure.dpi"], 150)
        self.assertEqual(plt.rcParams["savefig.dpi"], 300)
        self.assertEqual(plt.rcParams["savefig.bbox"], "tight")
        self.assertAlmostEqual(plt.rcParams["savefig.pad_inches"], 0.05)
        self.assertGreaterEqual(ax.title.get_position()[1], 1.04)
        plt.close(fig)

    def test_shared_annotation_helpers_add_research_marks(self):
        fig, ax = plt.subplots()
        x_values = np.array([1, 2, 3, 4])
        y_values = np.array([8.0, 12.5, np.nan, 6.2])
        ax.plot(x_values, np.nan_to_num(y_values, nan=10.0), color=style.COLORS["blue_main"])

        self.assertIs(
            style.annotate_point(ax, 2, 12.5, "关键拐点", color=style.COLORS["blue_main"]),
            ax,
        )
        point_note = ax.texts[-1]
        self.assertEqual(point_note.get_text(), "关键拐点")
        self.assertTrue(same_color(point_note.get_bbox_patch().get_facecolor()[:3], "white"))
        self.assertGreater(point_note.get_bbox_patch().get_facecolor()[3], 0.85)
        self.assertTrue(same_color(point_note.arrow_patch.get_edgecolor(), style.COLORS["blue_main"]))

        style.add_event_line(ax, 3, "政策出台")
        event_note = ax.texts[-1]
        self.assertEqual(event_note.get_text(), "政策出台")
        self.assertGreater(event_note.get_position()[1], 1.0)
        self.assertFalse(event_note.get_clip_on())
        self.assertTrue(same_color(ax.lines[-1].get_color(), style.COLORS["amber"]))

        style.add_threshold_line(ax, 10, "目标线")
        threshold_note = ax.texts[-1]
        self.assertEqual(threshold_note.get_text(), "目标线")
        self.assertFalse(threshold_note.get_clip_on())
        self.assertTrue(same_color(ax.lines[-1].get_color(), style.COLORS["crimson"]))

        style.add_phase_span(ax, 1.5, 2.5, "试点期")
        span_note = ax.texts[-1]
        self.assertEqual(span_note.get_text(), "试点期")
        self.assertGreater(span_note.get_position()[1], 1.0)
        self.assertFalse(span_note.get_clip_on())
        self.assertAlmostEqual(ax.patches[-1].get_alpha(), 0.08)

        style.annotate_extreme(ax, x_values, y_values, mode="max")
        self.assertEqual(ax.texts[-1].get_text(), "最高：12.50")

        style.annotate_extreme(ax, x_values, y_values, mode="min", text="阶段低点")
        self.assertEqual(ax.texts[-1].get_text(), "阶段低点")

        with self.assertRaisesRegex(ValueError, "max.*min"):
            style.annotate_extreme(ax, x_values, y_values, mode="median")

        plt.close(fig)

    def test_annotation_boundaries_are_explicit_and_conservative(self):
        self.assertEqual(
            set(style.ANNOTATION_ALLOWED_MODES),
            {"point", "extreme", "event", "threshold", "phase"},
        )
        self.assertEqual(style.ANNOTATION_LIMITS["paper"], 3)
        self.assertEqual(style.ANNOTATION_LIMITS["presentation"], 4)
        self.assertEqual(style.ANNOTATION_LIMITS["appendix"], 1)
        self.assertIn("time_series", style.ANNOTATION_SUITABLE_CHARTS)
        self.assertIn("heatmap", style.ANNOTATION_CAUTION_CHARTS)
        self.assertIn("3d", style.AUTO_ANNOTATION_DISABLED_CHARTS)

        self.assertIsNone(style.validate_annotation_config())
        self.assertIsNone(
            style.validate_annotation_config(
                annotate=False,
                annotation_mode="extreme",
                annotation_config={"count": 1},
            )
        )

        config = style.validate_annotation_config(
            annotate=True,
            annotation_mode="extreme",
            annotation_config={"count": 2},
            chart_type="time_series",
            figure_context="paper",
        )
        self.assertTrue(config["enabled"])
        self.assertEqual(config["mode"], "extreme")
        self.assertEqual(config["count"], 2)
        self.assertFalse(config["caution"])
        self.assertFalse(config["suggested_only"])

        suggested = style.validate_annotation_config(
            auto_annotation=True,
            annotation_mode="event",
            annotation_config={"count": 1},
            chart_type="time_series",
            suggested_annotations=[{"mode": "event", "label": "政策出台"}],
            figure_context="paper",
        )
        self.assertFalse(suggested["enabled"])
        self.assertTrue(suggested["suggested_only"])
        self.assertTrue(suggested["auto_annotation"])
        self.assertEqual(len(suggested["suggested_annotations"]), 1)

        auto_disabled = style.validate_annotation_config(
            auto_annotation=True,
            annotation_mode="event",
            annotation_config={"count": 1},
            chart_type="heatmap",
            figure_context="paper",
        )
        self.assertFalse(auto_disabled["enabled"])
        self.assertTrue(auto_disabled["auto_disabled"])

        caution = style.validate_annotation_config(
            annotate=True,
            annotation_mode="event",
            annotation_config={"count": 1},
            chart_type="heatmap",
            figure_context="paper",
        )
        self.assertTrue(caution["caution"])

        with self.assertRaisesRegex(ValueError, "annotation_mode"):
            style.validate_annotation_config(annotate=True)
        with self.assertRaisesRegex(ValueError, "annotation_config"):
            style.validate_annotation_config(annotate=True, annotation_mode="point")
        with self.assertRaisesRegex(ValueError, "annotation_mode must be one of"):
            style.validate_annotation_config(
                annotate=True,
                annotation_mode="label_every_point",
                annotation_config={"count": 1},
            )
        with self.assertRaisesRegex(ValueError, "paper"):
            style.validate_annotation_config(
                annotate=True,
                annotation_mode="point",
                annotation_config={"count": 4},
                figure_context="paper",
            )
        with self.assertRaisesRegex(ValueError, "presentation"):
            style.validate_annotation_config(
                auto_annotation=True,
                annotation_mode="point",
                annotation_config={"count": 5},
                figure_context="presentation",
            )

    def test_save_current_figure_writes_metadata_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            old_cwd = Path.cwd()
            try:
                import os

                os.chdir(tmp_path)
                fig, ax = plt.subplots()
                x = np.array([1, 2, 3])
                y = np.array([2.0, 5.0, np.nan])
                ax.plot(x, np.nan_to_num(y, nan=0.0), label="预测值")
                ax.set_xlabel("时间")
                ax.set_ylabel("指标")
                ax.legend()
                path = style.save_current_figure(
                    "metadata_demo",
                    fig,
                    metadata={
                        "figure_name": "metadata_demo",
                        "plot_type": "line",
                        "problem_type": "预测类",
                        "modeling_purpose": "展示预测指标变化趋势",
                        "variables": {"x": "时间", "y": "指标"},
                        "caption": "预测指标随时间变化",
                        "usage": "paper",
                        "annotate": False,
                        "annotation_config": None,
                        "data": {"x": x.tolist(), "y": y.tolist()},
                    },
                )
            finally:
                os.chdir(old_cwd)

            metadata_path = tmp_path / "metadata_demo.metadata.json"
            self.assertTrue(path.exists())
            self.assertTrue(metadata_path.exists())
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            for field in [
                "figure_name",
                "plot_type",
                "problem_type",
                "modeling_purpose",
                "variables",
                "axis_labels",
                "legend_labels",
                "caption",
                "usage",
                "annotate",
                "annotation_config",
                "data_summary",
            ]:
                self.assertIn(field, metadata)
            self.assertEqual(metadata["axis_labels"], {"x": "时间", "y": "指标"})
            self.assertEqual(metadata["legend_labels"], ["预测值"])
            self.assertEqual(metadata["data_summary"]["sample_size"], 3)
            self.assertEqual(metadata["data_summary"]["missing_values"], 1)
            self.assertEqual(metadata["data_summary"]["max"], 5.0)

    def test_review_module_reviews_metadata_via_api(self):
        """Test the acadp._reviewer.review() API with a metadata dict."""
        metadata = {
            "figure_name": "forecast_trend",
            "plot_type": "time_series",
            "problem_type": "预测类",
            "modeling_purpose": "展示预测指标的时间变化趋势",
            "variables": {"x": "年份", "y": "预测指标"},
            "axis_labels": {"x": "年份", "y": "预测指标"},
            "legend_labels": ["预测值"],
            "caption": "预测指标随年份变化趋势",
            "usage": "paper",
            "annotate": True,
            "annotation_config": {"count": 2, "mode": "event"},
            "data_summary": {"sample_size": 12, "missing_values": 0, "min": 1, "max": 9},
        }
        result = review_figure(metadata)
        self.assertIsInstance(result, ReviewResult)
        self.assertEqual(set(result.scores.keys()), set(SCORE_KEYS))
        self.assertIn(result.status, ["pass", "revise", "manual_review", "reject"])
        self.assertEqual(result.figure, "forecast_trend")
        self.assertLessEqual(result.scores["annotation_quality"], 100)

    @unittest.skip("review/chart_reviewer.py CLI deleted; use acadp._reviewer.review_cli() instead")
    def test_chart_reviewer_cli_writes_reports(self):
        pass

    @unittest.skip("review/chart_auto_reviser.py deleted; use acadp._reviser.revise_metadata() instead")
    def test_chart_auto_reviser_applies_safe_metadata_repairs_and_reruns_review(self):
        pass

    def test_run_all_examples_supports_review_workflow(self):
        runner = ROOT / "run_all_examples.py"
        self.assertTrue(runner.exists())
        source = runner.read_text(encoding="utf-8")
        self.assertIn("--review", source)
        self.assertIn("--auto-revise", source)
        self.assertIn("acadp-review", source)
        self.assertIn(".metadata.json", source)

    @unittest.skip("Old scripts/plot_*.py replaced by scripts/examples/*.py using acadp API")
    def test_all_plot_scripts_use_shared_style_only(self):
        pass

    @unittest.skip("Old scripts/plot_*.py replaced by scripts/examples/*.py using acadp API")
    def test_all_plot_templates_expose_opt_in_annotation_parameters(self):
        pass

    def test_required_plot_scripts_have_research_grade_structure(self):
        skill_doc = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        style_guide = (ROOT / "STYLE_GUIDE.md").read_text(encoding="utf-8")
        annotation_rules = (ROOT / "references" / "annotation_rules.md").read_text(encoding="utf-8")
        for required_phrase in [
            "annotation 是解释性增强，不是装饰",
            "正文图标注应克制",
            "高密度图慎用标注",
            "一张图只保留 1 个主标注逻辑",
            "默认 annotate=False",
            "模板可以根据数据返回 suggested_annotations，但不得直接写入图中",
            "只有当用户显式设置 annotate=True，并提供 annotation_config 时，才写入标注",
            "auto_annotation=True",
            "3D 图、热力图、散点矩阵、雷达图、极坐标图默认不自动标注",
        ]:
            self.assertTrue(required_phrase in style_guide or required_phrase in annotation_rules)
        self.assertIn("调用对应模板函数，优先传入 DataFrame 或数组数据", skill_doc)
        self.assertIn("不要直接修改模板源码", skill_doc)
        for helper_name in [
            "annotate_point",
            "add_event_line",
            "add_threshold_line",
            "add_phase_span",
            "annotate_extreme",
        ]:
            self.assertIn(helper_name, annotation_rules)
        self.assertIn("一张图建议只添加 1-3 个关键标注", annotation_rules)

    def test_skill_doc_uses_progressive_disclosure_for_heavy_reference(self):
        skill_doc = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(skill_doc.split()), 650)
        for rel_path in [
            "references/chart_lookup.md",
            "references/style_metadata.md",
            "references/annotation_rules.md",
        ]:
            self.assertIn(rel_path, skill_doc)
            self.assertTrue((ROOT / rel_path).exists(), rel_path)

    @unittest.skip("Old scripts/plot_*.py replaced by scripts/examples/*.py using acadp API")
    def test_3d_scripts_apply_readable_camera_and_colorbar(self):
        pass

    @unittest.skip("Old scripts/plot_*.py replaced by scripts/examples/*.py using acadp API")
    def test_key_scripts_generate_pngs(self):
        pass


if __name__ == "__main__":
    unittest.main()
