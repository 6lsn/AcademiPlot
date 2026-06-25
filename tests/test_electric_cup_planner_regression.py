import unittest


ELECTRIC_CUP_CASES = [
    {
        "figure_id": "fig01_power_balance",
        "problem_type": "预测类",
        "purpose": "展示时段内新能源出力、总用电负荷、基础电负荷和净供需差的日内变化，检验典型日供需匹配关系。",
        "data_semantics": {
            "x": "时段",
            "y": "功率",
            "group": "新能源出力、总用电负荷、基础电负荷、净供需差",
        },
        "legend_labels": ["风电出力", "光伏出力", "总用电负荷", "基础电负荷"],
        "expected_recipe": "supply_demand_balance",
        "expected_role": "system_balance",
    },
    {
        "figure_id": "fig02_green_indicators",
        "problem_type": "评价类",
        "purpose": "展示绿电直连指标、指标比例和要求阈值的对比，判断自发自用比例、绿电比例和上网比例是否达标。",
        "data_semantics": {
            "x": "指标比例",
            "y": "绿电直连指标",
            "group": "实际值与要求阈值",
        },
        "legend_labels": ["实际值（达标）", "实际值（未达标）", "要求阈值"],
        "expected_recipe": "bullet_threshold",
        "expected_role": "constraint_compliance",
    },
    {
        "figure_id": "fig03_cost_breakdown",
        "problem_type": "评价类",
        "purpose": "展示日产量水平下购电成本、运维成本、设备折旧和总成本的构成关系，比较成本结构差异。",
        "data_semantics": {
            "x": "日产量水平",
            "y": "日成本",
            "group": "购电成本、运维成本、设备折旧、总成本",
        },
        "legend_labels": ["购电成本", "运维成本", "设备折旧", "总成本"],
        "expected_recipe": "waterfall_cost",
        "expected_role": "cost_decomposition",
    },
    {
        "figure_id": "fig04_sensitivity",
        "problem_type": "优化类",
        "purpose": "展示参数水平与日均成本的敏感性关系，对比风电容量、光伏容量、电价倍率和储能单位成本的影响幅度。",
        "data_semantics": {
            "x": "参数水平",
            "y": "日均成本",
            "group": "风电容量、光伏容量、电价倍率、储能单位成本",
        },
        "legend_labels": [],
        "expected_recipe": "small_multiples_sensitivity",
        "expected_role": "multi_factor_sensitivity",
    },
    {
        "figure_id": "fig05_comparison",
        "problem_type": "评价类",
        "purpose": "展示日产量水平下离散模式、连续模式和吨氨成本的对比，并给出成本节约比例。",
        "data_semantics": {
            "x": "吨氨成本",
            "y": "日产量水平",
            "group": "离散模式、连续模式、成本节约比例",
        },
        "legend_labels": ["离散模式", "连续模式"],
        "expected_recipe": "dumbbell_comparison",
        "expected_role": "paired_scheme_comparison",
    },
    {
        "figure_id": "fig06_annual_compliance",
        "problem_type": "评价类",
        "purpose": "展示日产量水平、年度天数占比和达标类别的结构关系，比较完全满足、部分满足和不满足天数。",
        "data_semantics": {
            "x": "日产量水平",
            "y": "年度天数占比",
            "group": "完全满足、部分满足、不满足",
        },
        "legend_labels": ["完全满足", "部分满足", "不满足"],
        "expected_recipe": "percentage_structure",
        "expected_role": "composition_comparison",
    },
    {
        "figure_id": "fig07_storage_optimization",
        "problem_type": "优化类",
        "purpose": "展示储能容量、储能单位成本和年化总成本之间的优化关系，识别最优容量轨迹和基准成本最优点。",
        "data_semantics": {
            "x": "储能容量",
            "y": "储能单位成本",
            "z": "年化总成本",
        },
        "legend_labels": ["最优容量轨迹", "基准成本最优点"],
        "expected_recipe": "contour_optimization",
        "expected_role": "parameter_optimization",
    },
    {
        "figure_id": "fig08_mode_comparison",
        "problem_type": "评价类",
        "purpose": "展示运行模式、日产氨量和吨氨成本的对比关系，比较联网运行、离网运行和离网加储能方案。",
        "data_semantics": {
            "x": "运行模式",
            "y": "日产氨量和吨氨成本",
            "group": "联网运行、离网运行、离网加储能",
        },
        "legend_labels": [],
        "expected_recipe": "pareto_frontier",
        "expected_role": "multi_objective_tradeoff",
    },
]


@unittest.skip("plan_chart() was removed; acadp._planner now exposes choose_chart(profile, task)")
class ElectricCupPlannerRegressionTests(unittest.TestCase):
    def test_electric_cup_metadata_cases_select_advanced_recipes_without_manual_role(self):

        selected_recipes = set()
        for case in ELECTRIC_CUP_CASES:
            task = {
                key: value
                for key, value in case.items()
                if key not in {"expected_recipe", "expected_role"}
            }
            with self.subTest(figure_id=case["figure_id"]):
                self.assertNotIn("figure_role", task)
                spec = planner.plan_chart(task)
                selected_recipes.add(spec["recipe"])
                self.assertEqual(spec["recipe"], case["expected_recipe"])
                self.assertEqual(spec["figure_role"], case["expected_role"])
                self.assertEqual(spec["usage"], "paper")
                self.assertGreaterEqual(spec["planner_trace"]["score"], 60)

        for required_recipe in [
            "bullet_threshold",
            "dumbbell_comparison",
            "contour_optimization",
            "small_multiples_sensitivity",
        ]:
            self.assertIn(required_recipe, selected_recipes)


if __name__ == "__main__":
    unittest.main()
