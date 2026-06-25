import unittest


@unittest.skip("scripts/layout_qa.py was deleted in v0.2.0 architecture unification")
class LayoutQATests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_clean_legend_and_text_pass_layout_qa(self):
        layout_qa = load_layout_qa()
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot([1, 2, 3], [2, 3, 4], label="forecast")
        ax.set_xlabel("year")
        ax.set_ylabel("indicator")
        ax.set_title("forecast trend")
        ax.legend(loc="upper left")
        fig.tight_layout()

        report = layout_qa.qa_figure_layout(fig)

        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["summary"]["total_issues"], 0)

    def test_detects_legend_obviously_outside_figure(self):
        layout_qa = load_layout_qa()
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot([1, 2, 3], [2, 3, 4], label="far legend")
        ax.legend(loc="upper left", bbox_to_anchor=(1.45, 1.0))

        report = layout_qa.qa_figure_layout(fig, tolerance=0.03)

        self.assertEqual(report["status"], "fail")
        self.assertTrue(any(issue["kind"] == "legend" for issue in report["issues"]))

    def test_detects_text_obviously_outside_figure(self):
        layout_qa = load_layout_qa()
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot([1, 2, 3], [2, 3, 4])
        fig.text(1.25, 0.5, "overflow note", transform=fig.transFigure)

        report = layout_qa.qa_figure_layout(fig, tolerance=0.03)

        self.assertEqual(report["status"], "fail")
        self.assertTrue(any(issue["kind"] == "text" for issue in report["issues"]))

    def test_cli_writes_json_report_for_demo_figure(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "layout_report.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(LAYOUT_QA),
                    "--demo",
                    "overflow",
                    "--output",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=utf8_subprocess_env(),
            )

            self.assertEqual(result.stderr.strip(), "")
            report = json.loads(output_path.read_text(encoding="utf-8"))
            stdout_report = json.loads(result.stdout)
            self.assertEqual(report["status"], "fail")
            self.assertEqual(stdout_report["status"], "fail")
            self.assertGreaterEqual(report["summary"]["legend_issues"], 1)
            self.assertGreaterEqual(report["summary"]["text_issues"], 1)


if __name__ == "__main__":
    unittest.main()
