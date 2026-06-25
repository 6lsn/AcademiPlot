import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "references" / "recipe_index.yaml"
RECIPES = ROOT / "recipes"


EXPECTED_RECIPES = {
    "bullet_threshold": {
        "figure_role": "constraint_compliance",
        "plot_type": "bar",
        "layers": {"actual_bar", "threshold_marker", "pass_fail_color"},
    },
    "contour_optimization": {
        "figure_role": "parameter_optimization",
        "plot_type": "contour",
        "layers": {"filled_contour", "contour_lines", "optimum_path", "baseline_marker"},
    },
    "dumbbell_comparison": {
        "figure_role": "paired_scheme_comparison",
        "plot_type": "dotplot",
        "layers": {"baseline_points", "candidate_points", "gap_segments", "saving_labels"},
    },
    "supply_demand_balance": {
        "figure_role": "system_balance",
        "plot_type": "time_series",
        "layers": {"stacked_supply", "demand_line", "net_balance_bar"},
    },
    "small_multiples_sensitivity": {
        "figure_role": "multi_factor_sensitivity",
        "plot_type": "scatter_with_trend",
        "layers": {"factor_panels", "trend_line", "baseline_reference"},
    },
    "waterfall_cost": {
        "figure_role": "cost_decomposition",
        "plot_type": "waterfall",
        "layers": {"starting_value", "increment_bars", "decrement_bars", "connector_lines"},
    },
    "pareto_frontier": {
        "figure_role": "multi_objective_tradeoff",
        "plot_type": "scatter_with_trend",
        "layers": {"candidate_points", "frontier_line", "efficient_set"},
    },
    "percentage_structure": {
        "figure_role": "composition_comparison",
        "plot_type": "percentage_stacked_bar",
        "layers": {"percentage_segments", "category_totals", "segment_labels"},
    },
}


class RecipeCatalogTests(unittest.TestCase):
    def load_index(self):
        self.assertTrue(INDEX.exists(), "references/recipe_index.yaml must exist")
        data = yaml.safe_load(INDEX.read_text(encoding="utf-8"))
        self.assertIsInstance(data, dict)
        self.assertIn("recipes", data)
        return data

    def load_recipe(self, recipe_id):
        path = RECIPES / f"{recipe_id}.yaml"
        self.assertTrue(path.exists(), f"{path} must exist")
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertIsInstance(data, dict)
        return data

    def test_recipe_index_lists_exactly_the_eight_advanced_recipes(self):
        index = self.load_index()
        listed = {entry["id"] for entry in index["recipes"]}
        self.assertEqual(listed, set(EXPECTED_RECIPES))
        for entry in index["recipes"]:
            self.assertEqual(entry["path"], f"recipes/{entry['id']}.yaml")
            self.assertIn("trigger_roles", entry)
            self.assertIn("recommended_plot_type", entry)
            self.assertIn("summary", entry)
            self.assertTrue((ROOT / entry["path"]).exists(), entry["path"])

    def test_each_recipe_has_planner_ready_schema(self):
        for recipe_id, expected in EXPECTED_RECIPES.items():
            with self.subTest(recipe=recipe_id):
                recipe = self.load_recipe(recipe_id)
                self.assertEqual(recipe["id"], recipe_id)
                self.assertEqual(recipe["figure_role"], expected["figure_role"])
                self.assertEqual(recipe["output"]["plot_type"], expected["plot_type"])
                self.assertEqual(recipe["output"]["usage"], "paper")
                self.assertTrue(expected["layers"].issubset(set(recipe["visual_layers"])))
                for field in [
                    "name",
                    "problem_types",
                    "use_when",
                    "avoid_when",
                    "required_semantics",
                    "planner_rules",
                    "metadata_defaults",
                    "quality_checks",
                ]:
                    self.assertIn(field, recipe)
                self.assertIn("prefer_when", recipe["planner_rules"])
                self.assertIn("avoid_templates", recipe["planner_rules"])
                self.assertIn("caption_pattern", recipe["metadata_defaults"])
                self.assertIn("variables", recipe["metadata_defaults"])

    def test_recipe_catalog_covers_current_red_case_roles(self):
        index = self.load_index()
        role_to_recipe = {
            role: entry["id"]
            for entry in index["recipes"]
            for role in entry["trigger_roles"]
        }
        self.assertEqual(role_to_recipe["constraint_compliance"], "bullet_threshold")
        self.assertEqual(role_to_recipe["parameter_optimization"], "contour_optimization")
        self.assertEqual(role_to_recipe["paired_scheme_comparison"], "dumbbell_comparison")
        self.assertEqual(role_to_recipe["system_balance"], "supply_demand_balance")
        self.assertEqual(role_to_recipe["multi_factor_sensitivity"], "small_multiples_sensitivity")
