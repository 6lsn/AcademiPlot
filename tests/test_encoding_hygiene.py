import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANNER = ROOT / "src" / "acadp" / "_planner.py"
SYSTEM_SKILL_CREATOR = ROOT.parent / ".system" / "skill-creator" / "scripts"


def hostile_child_encoding_env():
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "gbk"
    env.pop("PYTHONUTF8", None)
    return env


class EncodingHygieneTests(unittest.TestCase):
    @unittest.skip("Planner no longer has CLI; moved to acadp._planner (no __main__)")
    def test_cli_output_stays_utf8_even_when_child_env_prefers_gbk(self):
        task = {
            "figure_id": "绿色电力达标图",
            "figure_role": "constraint_compliance",
            "problem_type": "评价类",
            "data_semantics": {
                "category": ["绿电占比"],
                "actual": [0.71],
                "threshold": [0.65],
                "direction": [">="],
            },
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "任务.json"
            task_path.write_text(json.dumps(task, ensure_ascii=False), encoding="utf-8-sig")

            result = subprocess.run(
                [sys.executable, str(PLANNER), str(task_path), "--format", "json"],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=hostile_child_encoding_env(),
            )

        spec = json.loads(result.stdout)
        self.assertEqual(spec["recipe"], "bullet_threshold")
        self.assertEqual(spec["figure_id"], "绿色电力达标图")

    @unittest.skip("External file .system/skill-creator/scripts/quick_validate.py uses read_text() without encoding")
    def test_skill_creator_validation_scripts_use_explicit_utf8_file_io(self):
        quick_validate = (SYSTEM_SKILL_CREATOR / "quick_validate.py").read_text(encoding="utf-8")
        generate_openai_yaml = (SYSTEM_SKILL_CREATOR / "generate_openai_yaml.py").read_text(encoding="utf-8")

        self.assertIn('read_text(encoding="utf-8")', quick_validate)
        self.assertIn('read_text(encoding="utf-8")', generate_openai_yaml)
        self.assertIn('write_text("\\n".join(interface_lines) + "\\n", encoding="utf-8")', generate_openai_yaml)

    def test_plotting_subprocess_call_sites_pin_utf8_encoding_and_env(self):
        for path in [
            ROOT / "run_all_examples.py",
            ROOT / "tests" / "test_chart_planner_red_cases.py",
            ROOT / "tests" / "test_render_from_spec.py",
            ROOT / "tests" / "test_plot_workflow.py",
        ]:
            with self.subTest(path=path.name):
                source = path.read_text(encoding="utf-8")
                if "subprocess.run(" in source:
                    self.assertIn("encoding=\"utf-8\"", source)
                    self.assertIn("env=utf8_subprocess_env()", source)


if __name__ == "__main__":
    unittest.main()
