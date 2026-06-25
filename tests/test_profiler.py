"""Tests for src/acadp/_profiler.py — semantic type inference and profiling."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest

from acadp._profiler import (
    infer_semantic_type,
    profile_dataframe,
    profile_data,
    _plotting_hints,
)


class TestProfileDataframe:
    """profile_dataframe() with year / gdp / type columns."""

    def test_profile_dataframe(self):
        df = pd.DataFrame(
            {
                "year": [2020, 2021, 2022, 2023],
                "gdp": [100.5, 110.2, 115.8, 120.3],
                "type": ["A", "B", "A", "C"],
            }
        )
        profile = profile_dataframe(df)

        assert profile["source"]["type"] == "dataframe"
        assert profile["shape"] == {"rows": 4, "columns": 3}
        assert profile["columns"]["year"]["semantic_type"] == "numeric"
        assert profile["columns"]["gdp"]["semantic_type"] == "numeric"
        assert profile["columns"]["type"]["semantic_type"] == "category"


class TestInferCostType:
    """Column named '成本' with numeric values must infer cost."""

    def test_infer_cost_type(self):
        series = pd.Series([1000, 2000, 3000], name="成本")
        result = infer_semantic_type("成本", series)
        assert result == "cost"


class TestProfileCsvPath:
    """profile_data() accepts a CSV file path and detects columns."""

    def test_profile_csv_path(self):
        df = pd.DataFrame(
            {
                "city": ["Beijing", "Shanghai", "Guangzhou"],
                "population": [21_540_000, 24_870_000, 18_680_000],
                "gdp_billion": [3610.0, 3870.0, 2500.0],
            }
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "cities.csv"
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")

            profile = profile_data(str(csv_path))

        assert profile["source"]["type"] == "csv"
        assert profile["source"]["name"] == "cities.csv"
        assert profile["shape"]["columns"] == 3
        assert "city" in profile["columns"]
        assert "population" in profile["columns"]
        assert "gdp_billion" in profile["columns"]


class TestPlottingHints:
    """_plotting_hints() reflects column type presence."""

    def test_plotting_hints_with_time_and_categories(self):
        hints = {
            "time_columns": ["hour"],
            "category_columns": ["mode"],
            "cost_columns": ["cost_a", "cost_b"],
            "capacity_columns": ["cap"],
            "threshold_columns": [],
            "status_columns": [],
            "objective_columns": [],
            "ratio_columns": [],
            "numeric_columns": [],
            "boolean_columns": [],
        }
        result = _plotting_hints(hints)

        assert result["has_time_axis"] is True
        assert result["has_categories"] is True
        assert result["has_costs"] is True
        assert result["has_capacity"] is True
        assert result["has_thresholds"] is False
        assert result["has_objectives"] is False
        assert result["has_ratios"] is False
        # has_optimization_surface_candidates: capacity + >=2 cost columns
        assert result["has_optimization_surface_candidates"] is True

    def test_plotting_hints_empty(self):
        hints = {
            "time_columns": [],
            "category_columns": [],
            "cost_columns": [],
            "capacity_columns": [],
            "threshold_columns": [],
            "status_columns": [],
            "objective_columns": [],
            "ratio_columns": [],
            "numeric_columns": [],
            "boolean_columns": [],
        }
        result = _plotting_hints(hints)

        assert result["has_time_axis"] is False
        assert result["has_categories"] is False
        assert result["has_optimization_surface_candidates"] is False
