import unittest

import acadp._reviewer as reviewer


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
        result = reviewer.review(
            self.metadata_for("bullet_threshold", figure_role="constraint_compliance")
        )

        self.assertEqual(result.status, "pass")
        issues = " ".join(result.major_issues + result.minor_issues)
        self.assertNotIn("recipe", issues.lower())

    def test_wrong_recipe_for_threshold_purpose_requires_revision(self):
        result = reviewer.review(
            self.metadata_for("dumbbell_comparison", plot_type="dotplot")
        )

        self.assertEqual(result.status, "revise")
        issues = " ".join(result.major_issues)
        self.assertTrue("recipe" in issues.lower() or "表达范式" in issues)

    def test_unknown_recipe_id_requires_revision(self):
        result = reviewer.review(self.metadata_for("made_up_recipe"))

        self.assertEqual(result.status, "revise")
        self.assertIn("recipe", " ".join(result.major_issues).lower())


if __name__ == "__main__":
    unittest.main()
