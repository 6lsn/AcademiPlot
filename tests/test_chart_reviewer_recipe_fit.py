import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review"


def load_review_module():
    spec = importlib.util.spec_from_file_location(
        "chart_reviewer", REVIEW / "chart_reviewer.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ChartReviewerRecipeFitTests(unittest.TestCase):
    def metadata_for(self, recipe, plot_type="bar", purpose=None, figure_role=None):
        purpose = purpose or (
            "展示指标值、指标名称、实际值、要求阈值、达标状态，判断各绿色电力约束是否达标。"
        )
        metadata = {
            "figure_name": "green_power_compliance",
            "recipe": recipe,
            "plot_type": plot_type,
            "problem_type": "评价类",
            "modeling_purpose": purpose,
            "variables": {
                "x": "指标值",
                "y": "指标名称",
                "group": "实际值、要求阈值、达标状态",
            },
            "axis_labels": {"x": "指标值", "y": "指标名称"},
            "legend_labels": ["实际值", "要求阈值", "达标状态"],
            "caption": purpose,
            "usage": "paper",
            "annotate": False,
            "data_summary": {"sample_size": 4, "missing_values": 0},
        }
        if figure_role:
            metadata["figure_role"] = figure_role
        return metadata

    def test_threshold_recipe_matches_threshold_paper_purpose(self):
        reviewer = load_review_module()
        review = reviewer.review_figure_metadata(
            self.metadata_for("bullet_threshold", figure_role="constraint_compliance")
        )

        self.assertEqual(review["overall_status"], "pass")
        issues = " ".join(review["major_issues"] + review["minor_issues"])
        self.assertNotIn("recipe", issues.lower())

    def test_wrong_recipe_for_threshold_purpose_requires_revision(self):
        reviewer = load_review_module()
        review = reviewer.review_figure_metadata(
            self.metadata_for("dumbbell_comparison", plot_type="dotplot")
        )

        self.assertEqual(review["overall_status"], "revise")
        issues = " ".join(review["major_issues"])
        self.assertTrue("recipe" in issues.lower() or "表达范式" in issues)

    def test_unknown_recipe_id_requires_revision(self):
        reviewer = load_review_module()
        review = reviewer.review_figure_metadata(self.metadata_for("made_up_recipe"))

        self.assertEqual(review["overall_status"], "revise")
        self.assertIn("recipe", " ".join(review["major_issues"]).lower())


if __name__ == "__main__":
    unittest.main()
