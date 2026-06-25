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


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
REVIEW = ROOT / "review"
sys.path.insert(0, str(SCRIPTS))

from utf8_io import utf8_subprocess_env

NON_TEMPLATE_SCRIPTS = {
    "__init__.py",
    "style.py",
    "utf8_io.py",
    "data_profiler.py",
    "chart_planner.py",
    "render_from_spec.py",
    "layout_qa.py",
}
SCRIPT_FILES = sorted(
    path for path in SCRIPTS.glob("*.py") if path.name not in NON_TEMPLATE_SCRIPTS
)


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


def load_review_module():
    spec = importlib.util.spec_from_file_location(
        "chart_reviewer", REVIEW / "chart_reviewer.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_auto_reviser_module():
    spec = importlib.util.spec_from_file_location(
        "chart_auto_reviser", REVIEW / "chart_auto_reviser.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PlotWorkflowTests(unittest.TestCase):
    def test_shared_style_module_sets_paper_defaults(self):
        sys.path.insert(0, str(SCRIPTS))
        try:
            import style

            style.apply_paper_style()
            fig, ax = plt.subplots()
            style.set_chart_title(ax, "测试业务主题")
        finally:
            sys.path.remove(str(SCRIPTS))

        self.assertEqual(
            plt.rcParams["font.sans-serif"][:2], ["Microsoft YaHei", "SimHei"]
        )
        self.assertEqual(
            plt.rcParams["font.serif"][:3],
            ["Times New Roman", "Microsoft YaHei", "SimHei"],
        )
        self.assertFalse(plt.rcParams["axes.unicode_minus"])
        self.assertEqual(plt.rcParams["figure.dpi"], 120)
        self.assertEqual(plt.rcParams["savefig.dpi"], 300)
        self.assertEqual(plt.rcParams["savefig.bbox"], "tight")
        self.assertAlmostEqual(plt.rcParams["savefig.pad_inches"], 0.06)
        self.assertGreaterEqual(ax.title.get_position()[1], 1.08)
        plt.close(fig)

    def test_shared_annotation_helpers_add_research_marks(self):
        sys.path.insert(0, str(SCRIPTS))
        try:
            import style

            fig, ax = plt.subplots()
            x_values = np.array([1, 2, 3, 4])
            y_values = np.array([8.0, 12.5, np.nan, 6.2])
            ax.plot(x_values, np.nan_to_num(y_values, nan=10.0), color=style.COLORS["blue"])

            self.assertIs(
                style.annotate_point(ax, 2, 12.5, "关键拐点", color=style.COLORS["blue"]),
                ax,
            )
            point_note = ax.texts[-1]
            self.assertEqual(point_note.get_text(), "关键拐点")
            self.assertTrue(same_color(point_note.get_bbox_patch().get_facecolor()[:3], "white"))
            self.assertGreater(point_note.get_bbox_patch().get_facecolor()[3], 0.85)
            self.assertTrue(same_color(point_note.arrow_patch.get_edgecolor(), style.COLORS["blue"]))

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
            self.assertEqual(ax.texts[-1].get_text(), "最高值：12.50")

            style.annotate_extreme(ax, x_values, y_values, mode="min", text="阶段低点")
            self.assertEqual(ax.texts[-1].get_text(), "阶段低点")

            with self.assertRaisesRegex(ValueError, "max.*min"):
                style.annotate_extreme(ax, x_values, y_values, mode="median")

            plt.close(fig)
        finally:
            sys.path.remove(str(SCRIPTS))

    def test_annotation_boundaries_are_explicit_and_conservative(self):
        sys.path.insert(0, str(SCRIPTS))
        try:
            import style

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
            with self.assertRaisesRegex(ValueError, "allowed"):
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
        finally:
            sys.path.remove(str(SCRIPTS))

    def test_save_current_figure_writes_metadata_json(self):
        sys.path.insert(0, str(SCRIPTS))
        try:
            import style

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
        finally:
            sys.path.remove(str(SCRIPTS))

    def test_review_module_files_schema_and_single_review(self):
        required_files = [
            "chart_review_rules.md",
            "chart_reviewer.py",
            "review_schema.json",
            "review_report_template.md",
        ]
        for name in required_files:
            self.assertTrue((REVIEW / name).exists(), name)

        rules = (REVIEW / "chart_review_rules.md").read_text(encoding="utf-8")
        for phrase in [
            "不同建模问题适合哪些图",
            "annotation 使用边界",
            "图注与图内标题边界",
            "3D 图、饼图、雷达图、散点矩阵的慎用规则",
        ]:
            self.assertIn(phrase, rules)

        schema = json.loads((REVIEW / "review_schema.json").read_text(encoding="utf-8"))
        for field in [
            "figure",
            "overall_status",
            "scores",
            "major_issues",
            "minor_issues",
            "recommended_action",
            "suggested_caption",
            "suggested_plot_type",
        ]:
            self.assertIn(field, schema["required"])

        reviewer = load_review_module()
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
        review = reviewer.review_figure_metadata(metadata)
        self.assertEqual(set(review["scores"]), set(schema["properties"]["scores"]["required"]))
        self.assertIn(review["overall_status"], ["pass", "revise", "manual_review", "reject"])
        self.assertEqual(review["figure"], "forecast_trend")
        self.assertLessEqual(review["scores"]["annotation_quality"], 100)

    def test_chart_reviewer_cli_writes_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            metadata_dir = tmp_path / "figures"
            output_dir = tmp_path / "review"
            metadata_dir.mkdir()
            metadata = {
                "figure_name": "bad_pie",
                "plot_type": "pie",
                "problem_type": "预测类",
                "modeling_purpose": "展示未来趋势",
                "variables": {"x": "年份", "y": "预测值"},
                "axis_labels": {"x": "", "y": ""},
                "legend_labels": [],
                "caption": "",
                "usage": "paper",
                "annotate": True,
                "annotation_config": {"count": 5, "text": "由于政策导致上涨"},
                "data_summary": {"sample_size": 5, "missing_values": 0},
            }
            (metadata_dir / "bad_pie.metadata.json").write_text(
                json.dumps(metadata, ensure_ascii=False),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(REVIEW / "chart_reviewer.py"),
                    "--metadata-dir",
                    str(metadata_dir),
                    "--output-dir",
                    str(output_dir),
                ],
                text=True,
                capture_output=True,
                encoding="utf-8",
                env=utf8_subprocess_env(),
                check=True,
            )
            self.assertEqual(result.stderr.strip(), "")
            report_json = output_dir / "review_report.json"
            report_md = output_dir / "review_report.md"
            self.assertTrue(report_json.exists())
            self.assertTrue(report_md.exists())
            report = json.loads(report_json.read_text(encoding="utf-8"))
            self.assertEqual(report["summary"]["total"], 1)
            self.assertEqual(report["reviews"][0]["figure"], "bad_pie")
            self.assertIn(report["reviews"][0]["overall_status"], ["revise", "manual_review", "reject"])

    def test_chart_auto_reviser_applies_safe_metadata_repairs_and_reruns_review(self):
        auto_reviser_path = REVIEW / "chart_auto_reviser.py"
        self.assertTrue(auto_reviser_path.exists())

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            metadata_dir = tmp_path / "figures"
            output_dir = tmp_path / "auto_revise"
            metadata_dir.mkdir()
            metadata = {
                "figure_name": "regional_score_bar",
                "plot_type": "bar",
                "problem_type": "评价类",
                "modeling_purpose": "展示地区得分对比",
                "variables": {"x": "地区", "y": "得分"},
                "axis_labels": {"x": "地区", "y": "得分"},
                "legend_labels": [],
                "caption": "",
                "usage": "paper",
                "annotate": True,
                "annotation_config": {"count": 5, "mode": "point"},
                "data_summary": {"sample_size": 5, "missing_values": 0, "min": 72, "max": 95},
            }
            (metadata_dir / "regional_score_bar.metadata.json").write_text(
                json.dumps(metadata, ensure_ascii=False),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(auto_reviser_path),
                    "--metadata-dir",
                    str(metadata_dir),
                    "--output-dir",
                    str(output_dir),
                    "--max-rounds",
                    "2",
                ],
                text=True,
                capture_output=True,
                encoding="utf-8",
                env=utf8_subprocess_env(),
                check=True,
            )

            self.assertEqual(result.stderr.strip(), "")
            plan_path = output_dir / "revision_plan.json"
            final_report_path = output_dir / "final_review" / "review_report.json"
            revised_metadata_path = (
                output_dir
                / "round_1"
                / "revised_metadata"
                / "regional_score_bar.metadata.json"
            )
            self.assertTrue(plan_path.exists())
            self.assertTrue(final_report_path.exists())
            self.assertTrue(revised_metadata_path.exists())

            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            self.assertGreaterEqual(plan["summary"]["applied_fixes"], 2)
            actions = plan["rounds"][0]["figures"][0]["actions"]
            self.assertIn("补全缺失图注", actions)
            self.assertIn("将正文图 annotation 数量限制到 3 个", actions)

            revised_metadata = json.loads(revised_metadata_path.read_text(encoding="utf-8"))
            self.assertEqual(revised_metadata["caption"], "展示地区得分对比")
            self.assertEqual(revised_metadata["annotation_config"]["count"], 3)

            final_report = json.loads(final_report_path.read_text(encoding="utf-8"))
            self.assertEqual(final_report["summary"]["total"], 1)
            self.assertEqual(final_report["reviews"][0]["overall_status"], "pass")

    def test_run_all_examples_supports_review_workflow(self):
        runner = ROOT / "run_all_examples.py"
        self.assertTrue(runner.exists())
        source = runner.read_text(encoding="utf-8")
        self.assertIn("--review", source)
        self.assertIn("--auto-revise", source)
        self.assertIn("chart_reviewer.py", source)
        self.assertIn("chart_auto_reviser.py", source)
        self.assertIn(".metadata.json", source)

    def test_all_plot_scripts_use_shared_style_only(self):
        self.assertEqual(len(SCRIPT_FILES), 50)
        for script in SCRIPT_FILES:
            with self.subTest(script=script.name):
                source = script.read_text(encoding="utf-8")
                self.assertIn("from style import", source)
                self.assertIn("save_current_figure", source)
                self.assertIn("set_chart_title", source)
                self.assertNotIn("plt.rcParams[", source)
                self.assertNotIn("plt.title(", source)
                self.assertNotIn("bbox_to_anchor=(1.", source)
                self.assertNotIn("bbox_to_anchor=(0.5, 1.08)", source)
                for generic_title in ["基础柱状图", "水平柱状图", "雷达图", "环形图", "时间序列图"]:
                    self.assertNotIn(f'"{generic_title}"', source)
                    self.assertNotIn(f"'{generic_title}'", source)
                self.assertNotIn("WenQuanYi Micro Hei", source)
                self.assertNotIn("Heiti TC", source)
                for cmap_name in ["viridis", "plasma", "rainbow", "coolwarm"]:
                    self.assertNotIn(cmap_name, source)

    def test_all_plot_templates_expose_opt_in_annotation_parameters(self):
        self.assertEqual(len(SCRIPT_FILES), 50)
        for script in SCRIPT_FILES:
            with self.subTest(script=script.name):
                tree = ast.parse(script.read_text(encoding="utf-8-sig"))
                functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
                plot_function = next(node for node in functions if node.name == script.stem)
                args = plot_function.args.args
                arg_names = [arg.arg for arg in args[-4:]]
                self.assertEqual(
                    arg_names,
                    [
                        "annotate",
                        "annotation_mode",
                        "annotation_config",
                        "auto_annotation",
                    ],
                )
                defaults = plot_function.args.defaults[-4:]
                self.assertIsInstance(defaults[0], ast.Constant)
                self.assertFalse(defaults[0].value)
                self.assertIsInstance(defaults[1], ast.Constant)
                self.assertIsNone(defaults[1].value)
                self.assertIsInstance(defaults[2], ast.Constant)
                self.assertIsNone(defaults[2].value)
                self.assertIsInstance(defaults[3], ast.Constant)
                self.assertFalse(defaults[3].value)

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

        plot5 = (SCRIPTS / "plot5.py").read_text(encoding="utf-8")
        self.assertTrue("Mosaic" in plot5 or "mosaic" in plot5)
        self.assertIn("proportion", plot5)

        plot7 = (SCRIPTS / "plot7.py").read_text(encoding="utf-8")
        self.assertIn(".twinx(", plot7)
        self.assertIn("累计占比", plot7)
        self.assertIn("80%", plot7)
        self.assertIn("handles1 + handles2", plot7)
        self.assertIn('loc="upper center"', plot7)
        self.assertIn("供应链异常因素帕累托分析", plot7)

        percentage = (SCRIPTS / "plot_percentage_stacked_bar.py").read_text(encoding="utf-8")
        self.assertIn("各地区销售渠道占比", percentage)
        self.assertIn('loc="lower center"', percentage)
        self.assertIn("bbox_to_anchor=(0.5, 1.02)", percentage)
        self.assertNotIn("bbox_to_anchor=(0.5, 1.0)", percentage)

        plot8 = (SCRIPTS / "plot8.py").read_text(encoding="utf-8")
        self.assertIn("dendrogram", plot8)
        self.assertIn("linkage", plot8)

        waterfall = (SCRIPTS / "plot_waterfall.py").read_text(encoding="utf-8")
        self.assertIn("running_total", waterfall)
        self.assertIn("connector", waterfall)

        scatter = (SCRIPTS / "plot_scatter_with_trend.py").read_text(encoding="utf-8")
        self.assertIn("ax.text(", scatter)
        self.assertIn("transform=ax.transAxes", scatter)
        self.assertIn("趋势线: y =", scatter)
        self.assertNotIn("label=f'趋势线", scatter)
        self.assertNotIn('label=f"趋势线', scatter)

        matrix = (SCRIPTS / "plot_matrix_scatter.py").read_text(encoding="utf-8")
        self.assertIn("figsize=(10, 8)", matrix)

        plot6 = (SCRIPTS / "plot6.py").read_text(encoding="utf-8")
        self.assertIn("alpha=0.75", plot6)
        self.assertIn("palette(", plot6)

    def test_skill_doc_uses_progressive_disclosure_for_heavy_reference(self):
        skill_doc = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(skill_doc.split()), 650)
        for rel_path in [
            "references/chart_lookup.md",
            "references/style_metadata.md",
            "references/annotation_rules.md",
            "review/chart_review_rules.md",
        ]:
            self.assertIn(rel_path, skill_doc)
            self.assertTrue((ROOT / rel_path).exists(), rel_path)

    def test_3d_scripts_apply_readable_camera_and_colorbar(self):
        for name in [
            "plot_3d_bar_chart.py",
            "plot_3d_scatter.py",
            "plot_3d_surface.py",
            "plot10.py",
        ]:
            with self.subTest(script=name):
                source = (SCRIPTS / name).read_text(encoding="utf-8")
                self.assertIn(".view_init(", source)
                self.assertIn(".colorbar(", source)
                self.assertIn("style_3d_axis", source)

    def test_key_scripts_generate_pngs(self):
        scripts = [
            "plot5.py",
            "plot7.py",
            "plot8.py",
            "plot_waterfall.py",
            "plot_3d_bar_chart.py",
            "plot_3d_scatter.py",
            "plot_3d_surface.py",
            "plot10.py",
            "plot_violinplot.py",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for name in scripts:
                with self.subTest(script=name):
                    result = subprocess.run(
                        [sys.executable, str(SCRIPTS / name)],
                        cwd=tmp_path,
                        text=True,
                        capture_output=True,
                        encoding="utf-8",
                        env=utf8_subprocess_env(),
                        check=True,
                    )
                    self.assertEqual(result.stderr.strip(), "")
                    png = tmp_path / f"{Path(name).stem}.png"
                    metadata = tmp_path / f"{Path(name).stem}.metadata.json"
                    self.assertTrue(png.exists(), result.stdout + result.stderr)
                    self.assertTrue(metadata.exists(), result.stdout + result.stderr)
                    self.assertGreater(png.stat().st_size, 20_000)
                    self.assertEqual(read_png_dpi(png), (300, 300))


if __name__ == "__main__":
    unittest.main()
