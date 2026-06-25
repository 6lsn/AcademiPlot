import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
RENDERER = SCRIPTS / "render_from_spec.py"
sys.path.insert(0, str(SCRIPTS))

from utf8_io import utf8_subprocess_env


def load_renderer():
    if not RENDERER.exists():
        raise AssertionError("Expected scripts/render_from_spec.py to exist")
    spec = importlib.util.spec_from_file_location("render_from_spec", RENDERER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def spec_for(recipe_id):
    base = {
        "figure_id": f"{recipe_id}_demo",
        "recipe": recipe_id,
        "figure_role": "demo",
        "problem_type": "评价类",
        "plot_type": "bar",
        "usage": "paper",
        "metadata": {
            "caption": f"{recipe_id} 示例图",
            "variables": {"x": "横轴变量", "y": "纵轴变量"},
            "axis_labels": {"x": "横轴", "y": "纵轴"},
            "modeling_purpose": f"渲染 {recipe_id} recipe 的测试图。",
        },
    }
    if recipe_id == "bullet_threshold":
        base.update(
            {
                "figure_role": "constraint_compliance",
                "plot_type": "bar",
                "data": {
                    "category": ["自发自用比例", "绿电比例", "上网比例"],
                    "actual": [0.28, 0.69, 0.36],
                    "threshold": [0.60, 0.30, 0.20],
                    "direction": [">=", ">=", "<="],
                    "unit": "ratio",
                },
            }
        )
    elif recipe_id == "contour_optimization":
        base.update(
            {
                "figure_role": "parameter_optimization",
                "problem_type": "优化类",
                "plot_type": "contour",
                "data": {
                    "x": [0, 15, 30, 45],
                    "y": [500, 1000, 1500],
                    "z": [[14, 10, 12, 18], [16, 8, 9, 15], [20, 13, 11, 14]],
                    "baseline": {"x": 30, "y": 1000},
                },
            }
        )
    elif recipe_id == "dumbbell_comparison":
        base.update(
            {
                "figure_role": "paired_scheme_comparison",
                "plot_type": "dotplot",
                "data": {
                    "category": ["72 t/d", "63 t/d", "54 t/d"],
                    "baseline": [6281, 5495, 4795],
                    "candidate": [4787, 4077, 3393],
                    "baseline_label": "离散模式",
                    "candidate_label": "连续模式",
                    "unit": "元/吨",
                },
            }
        )
    elif recipe_id == "supply_demand_balance":
        base.update(
            {
                "figure_role": "system_balance",
                "problem_type": "预测类",
                "plot_type": "time_series",
                "data": {
                    "time": [0, 1, 2, 3, 4],
                    "supply_components": {"风电": [8, 10, 12, 9, 6], "光伏": [0, 4, 12, 16, 8]},
                    "demand": [12, 15, 20, 22, 18],
                    "secondary": {"基础负荷": [3, 4, 5, 4, 3]},
                },
            }
        )
    elif recipe_id == "small_multiples_sensitivity":
        base.update(
            {
                "figure_role": "multi_factor_sensitivity",
                "problem_type": "优化类",
                "plot_type": "scatter_with_trend",
                "data": {
                    "factors": [
                        {"name": "风电容量", "x": [20, 40, 60], "y": [29, 25, 21], "baseline": 40},
                        {"name": "光伏容量", "x": [32, 64, 96], "y": [26, 25, 24], "baseline": 64},
                        {"name": "电价倍率", "x": [0.8, 1.0, 1.2], "y": [23, 25, 27], "baseline": 1.0},
                        {"name": "储能成本", "x": [500, 1000, 1500], "y": [24, 25, 26], "baseline": 1000},
                    ],
                    "y_label": "日均成本 (万元)",
                },
            }
        )
    elif recipe_id == "waterfall_cost":
        base.update(
            {
                "figure_role": "cost_decomposition",
                "problem_type": "优化类",
                "plot_type": "waterfall",
                "data": {
                    "start_label": "基准",
                    "start": 100,
                    "changes": [
                        {"label": "购电增加", "value": 25},
                        {"label": "运维增加", "value": 10},
                        {"label": "储能节省", "value": -18},
                    ],
                    "final_label": "最终",
                },
            }
        )
    elif recipe_id == "pareto_frontier":
        base.update(
            {
                "figure_role": "multi_objective_tradeoff",
                "problem_type": "优化类",
                "plot_type": "scatter_with_trend",
                "data": {
                    "objective_x": [100, 85, 70, 65, 55],
                    "objective_y": [30, 38, 42, 46, 44],
                    "labels": ["A", "B", "C", "D", "E"],
                    "efficient": [True, True, True, True, False],
                    "x_direction": "min",
                    "y_direction": "max",
                },
            }
        )
    elif recipe_id == "percentage_structure":
        base.update(
            {
                "figure_role": "composition_comparison",
                "plot_type": "percentage_stacked_bar",
                "data": {
                    "category": ["72", "63", "54"],
                    "components": {
                        "完全满足": [360, 300, 225],
                        "部分满足": [0, 60, 135],
                        "不满足": [0, 0, 0],
                    },
                    "unit": "天",
                },
            }
        )
    else:
        raise ValueError(recipe_id)
    return base


class RenderFromSpecTests(unittest.TestCase):
    def test_renders_all_eight_advanced_recipes_to_png_and_metadata(self):
        renderer = load_renderer()
        recipe_ids = [
            "bullet_threshold",
            "contour_optimization",
            "dumbbell_comparison",
            "supply_demand_balance",
            "small_multiples_sensitivity",
            "waterfall_cost",
            "pareto_frontier",
            "percentage_structure",
        ]
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            for recipe_id in recipe_ids:
                with self.subTest(recipe=recipe_id):
                    result = renderer.render_from_spec(spec_for(recipe_id), output_dir)
                    image_path = Path(result["image_path"])
                    metadata_path = Path(result["metadata_path"])
                    self.assertTrue(image_path.exists(), image_path)
                    self.assertGreater(image_path.stat().st_size, 1000)
                    self.assertTrue(metadata_path.exists(), metadata_path)
                    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                    self.assertEqual(metadata["figure_name"], f"{recipe_id}_demo")
                    self.assertEqual(metadata["plot_type"], spec_for(recipe_id)["plot_type"])
                    self.assertEqual(metadata["usage"], "paper")
                    self.assertTrue(metadata["caption"])
                    self.assertTrue(metadata["variables"])

    def test_cli_renders_json_spec_and_prints_summary(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            spec_path = tmp_path / "spec.json"
            spec_path.write_text(
                json.dumps(spec_for("bullet_threshold"), ensure_ascii=False),
                encoding="utf-8-sig",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    str(spec_path),
                    "--output-dir",
                    str(tmp_path),
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=utf8_subprocess_env(),
            )
            summary = json.loads(result.stdout)
            self.assertEqual(summary["recipe"], "bullet_threshold")
            self.assertTrue(Path(summary["image_path"]).exists())
            self.assertTrue(Path(summary["metadata_path"]).exists())
