import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

import acadp._planner as planner_mod


ROOT = Path(__file__).resolve().parents[1]
PLANNER = ROOT / "src" / "acadp" / "_planner.py"

sys.path.insert(0, str(ROOT / "scripts"))
from utf8_io import utf8_subprocess_env


@unittest.skip("plan_chart() was removed; acadp._planner now exposes choose_chart(profile, task)")
class ChartPlannerRedCases(unittest.TestCase):
    def assert_plans_recipe(self, task, expected):
        self.assertTrue(
            hasattr(planner, "plan_chart"),
            "chart_planner.py must expose plan_chart(task: dict) -> dict",
        )
        chart_spec = planner.plan_chart(task)
        self.assertIsInstance(chart_spec, dict)
        self.assertEqual(chart_spec.get("recipe"), expected["recipe"])
        self.assertEqual(chart_spec.get("plot_type"), expected["plot_type"])
        self.assertEqual(chart_spec.get("figure_role"), expected["figure_role"])
        self.assertEqual(chart_spec.get("usage"), "paper")
        for layer in expected["visual_layers"]:
            self.assertIn(layer, chart_spec.get("visual_layers", []))
        for weak_template in expected["avoid_templates"]:
            self.assertNotEqual(chart_spec.get("template"), weak_template)
            self.assertNotIn(weak_template, chart_spec.get("fallback_templates", []))
        metadata = chart_spec.get("metadata", {})
        for field in [
            "problem_type",
            "modeling_purpose",
            "variables",
            "axis_labels",
            "caption",
        ]:
            self.assertIn(field, metadata)

    def test_green_compliance_thresholds_choose_bullet_threshold(self):
        task = {
            "figure_id": "fig_green_compliance",
            "problem_type": "评价类",
            "figure_role": "constraint_compliance",
            "purpose": "判断绿电直连指标是否达标，并突出实际值与要求阈值的差距。",
            "data_semantics": {
                "category": ["自发自用比例", "绿电比例", "上网比例"],
                "actual": [0.2816, 0.6921, 0.3592],
                "threshold": [0.60, 0.30, 0.20],
                "direction": [">=", ">=", "<="],
                "unit": "ratio",
            },
            "available_templates": ["plot_grouped_bar", "plot_bar_basic"],
        }
        expected = {
            "recipe": "bullet_threshold",
            "plot_type": "bar",
            "figure_role": "constraint_compliance",
            "visual_layers": ["actual_bar", "threshold_marker", "pass_fail_color"],
            "avoid_templates": ["plot_grouped_bar", "plot_bar_basic"],
        }
        self.assert_plans_recipe(task, expected)

    def test_storage_capacity_search_chooses_contour_optimization(self):
        task = {
            "figure_id": "fig_storage_optimization",
            "problem_type": "优化类",
            "figure_role": "parameter_optimization",
            "purpose": "展示储能容量、储能单位成本与年化总成本的寻优关系。",
            "data_semantics": {
                "x": "储能容量",
                "y": "储能单位成本",
                "z": "年化总成本",
                "grid": True,
                "baseline": {"储能单位成本": 1000},
            },
            "available_templates": ["plot_line_basic", "plot_3d_surface", "plot_contour"],
        }
        expected = {
            "recipe": "contour_optimization",
            "plot_type": "contour",
            "figure_role": "parameter_optimization",
            "visual_layers": [
                "filled_contour",
                "contour_lines",
                "optimum_path",
                "baseline_marker",
            ],
            "avoid_templates": ["plot_line_basic", "plot_3d_surface"],
        }
        self.assert_plans_recipe(task, expected)

    def test_discrete_vs_continuous_costs_choose_dumbbell_comparison(self):
        task = {
            "figure_id": "fig_mode_cost_comparison",
            "problem_type": "评价类",
            "figure_role": "paired_scheme_comparison",
            "purpose": "比较离散模式和连续模式在不同日产量水平下的吨氨成本差异。",
            "data_semantics": {
                "category": ["72 t/d", "63 t/d", "54 t/d", "45 t/d", "36 t/d"],
                "baseline_series": "离散模式吨氨成本",
                "candidate_series": "连续模式吨氨成本",
                "derived_metric": "节约率",
                "unit": "元/吨",
            },
            "available_templates": ["plot_grouped_bar", "plot_bar_with_labels", "plot_dotplot"],
        }
        expected = {
            "recipe": "dumbbell_comparison",
            "plot_type": "dotplot",
            "figure_role": "paired_scheme_comparison",
            "visual_layers": ["baseline_points", "candidate_points", "gap_segments", "saving_labels"],
            "avoid_templates": ["plot_grouped_bar", "plot_bar_with_labels"],
        }
        self.assert_plans_recipe(task, expected)

    def test_power_balance_chooses_supply_demand_net_balance(self):
        task = {
            "figure_id": "fig_power_balance",
            "problem_type": "预测类",
            "figure_role": "system_balance",
            "purpose": "检验典型日新能源出力与用电负荷的时段匹配关系。",
            "data_semantics": {
                "time_axis": "24小时",
                "supply_components": ["风电出力", "光伏出力"],
                "demand_series": "总用电负荷",
                "secondary_series": "基础电负荷",
                "derived_metric": "净供需差",
            },
            "available_templates": ["plot_line_multi_series", "plot_area", "plot_time_series"],
        }
        expected = {
            "recipe": "supply_demand_balance",
            "plot_type": "time_series",
            "figure_role": "system_balance",
            "visual_layers": ["stacked_supply", "demand_line", "net_balance_bar"],
            "avoid_templates": ["plot_line_multi_series"],
        }
        self.assert_plans_recipe(task, expected)

    def test_multi_factor_sensitivity_chooses_small_multiples(self):
        task = {
            "figure_id": "fig_sensitivity",
            "problem_type": "优化类",
            "figure_role": "multi_factor_sensitivity",
            "purpose": "比较多个参数扰动对日均成本的方向和幅度影响。",
            "data_semantics": {
                "factors": ["风电容量", "光伏容量", "电价倍率", "储能单位成本"],
                "x_per_factor": "参数水平",
                "y": "日均成本",
                "baseline_per_factor": True,
            },
            "available_templates": ["plot_line_multi_series", "plot_scatter_with_trend"],
        }
        expected = {
            "recipe": "small_multiples_sensitivity",
            "plot_type": "scatter_with_trend",
            "figure_role": "multi_factor_sensitivity",
            "visual_layers": ["factor_panels", "trend_line", "baseline_reference"],
            "avoid_templates": ["plot_line_multi_series"],
        }
        self.assert_plans_recipe(task, expected)

    def test_cli_outputs_json_and_yaml_specs(self):
        task = {
            "figure_id": "fig_green_compliance",
            "problem_type": "评价类",
            "figure_role": "constraint_compliance",
            "purpose": "判断绿电直连指标是否达标。",
            "data_semantics": {
                "category": ["自发自用比例", "绿电比例", "上网比例"],
                "actual": [0.2816, 0.6921, 0.3592],
                "threshold": [0.60, 0.30, 0.20],
                "direction": [">=", ">=", "<="],
            },
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "task.json"
            task_path.write_text(json.dumps(task, ensure_ascii=False), encoding="utf-8-sig")

            json_result = subprocess.run(
                [sys.executable, str(PLANNER), str(task_path), "--format", "json"],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=utf8_subprocess_env(),
            )
            json_spec = json.loads(json_result.stdout)
            self.assertEqual(json_spec["recipe"], "bullet_threshold")

            yaml_result = subprocess.run(
                [sys.executable, str(PLANNER), str(task_path), "--format", "yaml"],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=utf8_subprocess_env(),
            )
            yaml_spec = yaml.safe_load(yaml_result.stdout)
            self.assertEqual(yaml_spec["recipe"], "bullet_threshold")
