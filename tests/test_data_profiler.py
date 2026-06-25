import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

import acadp._profiler as profiler


class DataProfilerTests(unittest.TestCase):
    def test_profiles_dataframe_with_modeling_semantics(self):
        df = pd.DataFrame(
            {
                "时段(h)": [0, 1, 2, 3],
                "实际绿电比例": [0.2816, 0.6921, 0.31, 0.8],
                "要求阈值": [0.60, 0.30, 0.30, 0.20],
                "运行模式": ["联网", "离网", "离网+储能", "联网"],
                "吨氨成本(元/吨)": [4787, 1471, 1546, np.nan],
            }
        )

        profile = profiler.profile_data(df, source_name="demo_dataframe")

        self.assertEqual(profile["source"]["type"], "dataframe")
        self.assertEqual(profile["source"]["name"], "demo_dataframe")
        self.assertEqual(profile["shape"], {"rows": 4, "columns": 5})
        self.assertEqual(profile["columns"]["时段(h)"]["semantic_type"], "time")
        self.assertEqual(profile["columns"]["实际绿电比例"]["semantic_type"], "ratio")
        self.assertEqual(profile["columns"]["要求阈值"]["semantic_type"], "threshold")
        self.assertEqual(profile["columns"]["运行模式"]["semantic_type"], "category")
        self.assertEqual(profile["columns"]["吨氨成本(元/吨)"]["semantic_type"], "cost")
        self.assertEqual(profile["columns"]["吨氨成本(元/吨)"]["missing"], 1)
        self.assertEqual(profile["columns"]["吨氨成本(元/吨)"]["numeric"]["min"], 1471.0)
        self.assertIn("时段(h)", profile["semantic_hints"]["time_columns"])
        self.assertIn("要求阈值", profile["semantic_hints"]["threshold_columns"])
        self.assertIn("吨氨成本(元/吨)", profile["semantic_hints"]["cost_columns"])
        self.assertTrue(profile["plotting_hints"]["has_thresholds"])
        self.assertTrue(profile["plotting_hints"]["has_time_axis"])

    def test_profiles_csv_path_with_utf8_columns(self):
        df = pd.DataFrame(
            {
                "储能容量(MWh)": [0, 15, 30, 45],
                "储能单位成本(元/kWh)": [500, 1000, 1500, 2000],
                "年化总成本(万元)": [2850, 980, 750, 1350],
                "是否最优": [False, False, True, False],
            }
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "storage_profile.csv"
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")

            profile = profiler.profile_data(csv_path)

        self.assertEqual(profile["source"]["type"], "csv")
        self.assertEqual(profile["source"]["name"], "storage_profile.csv")
        self.assertEqual(profile["shape"], {"rows": 4, "columns": 4})
        self.assertEqual(profile["columns"]["储能容量(MWh)"]["semantic_type"], "capacity")
        self.assertEqual(profile["columns"]["储能单位成本(元/kWh)"]["semantic_type"], "cost")
        self.assertEqual(profile["columns"]["年化总成本(万元)"]["semantic_type"], "cost")
        self.assertIn("储能容量(MWh)", profile["semantic_hints"]["capacity_columns"])
        self.assertIn("年化总成本(万元)", profile["semantic_hints"]["cost_columns"])
        self.assertTrue(profile["plotting_hints"]["has_optimization_surface_candidates"])

    def test_profiles_excel_path_and_sheet_name(self):
        df = pd.DataFrame(
            {
                "方案": ["A", "B", "C"],
                "目标函数值": [12.5, 9.2, 10.1],
                "排放量": [100, 80, 95],
                "达标状态": ["不满足", "完全满足", "部分满足"],
            }
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            xlsx_path = Path(tmp_dir) / "scenario_summary.xlsx"
            df.to_excel(xlsx_path, sheet_name="summary", index=False)

            profile = profiler.profile_data(xlsx_path, sheet_name="summary")

        self.assertEqual(profile["source"]["type"], "excel")
        self.assertEqual(profile["source"]["sheet_name"], "summary")
        self.assertEqual(profile["shape"], {"rows": 3, "columns": 4})
        self.assertEqual(profile["columns"]["方案"]["semantic_type"], "category")
        self.assertEqual(profile["columns"]["目标函数值"]["semantic_type"], "objective")
        self.assertEqual(profile["columns"]["达标状态"]["semantic_type"], "status")
        self.assertIn("目标函数值", profile["semantic_hints"]["objective_columns"])
        self.assertIn("达标状态", profile["semantic_hints"]["status_columns"])
        self.assertTrue(profile["plotting_hints"]["has_categories"])
