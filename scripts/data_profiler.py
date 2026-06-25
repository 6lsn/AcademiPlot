import argparse
import json
import math
import re
import sys
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from utf8_io import configure_utf8_stdio


configure_utf8_stdio()

SEMANTIC_BUCKETS = [
    "time",
    "ratio",
    "threshold",
    "category",
    "cost",
    "capacity",
    "objective",
    "status",
    "numeric",
    "boolean",
]


def _json_safe(value):
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        try:
            return _json_safe(value.item())
        except (TypeError, ValueError):
            pass
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return float(value)
    return value


def _column_text(name):
    return str(name).strip().lower()


def _extract_unit(name):
    text = str(name)
    matches = re.findall(r"[（(]([^（）()]+)[）)]", text)
    return matches[-1].strip() if matches else ""


def _is_numeric(series):
    return pd.api.types.is_numeric_dtype(series)


def _is_datetime(series):
    if pd.api.types.is_datetime64_any_dtype(series):
        return True
    if not pd.api.types.is_object_dtype(series):
        return False
    sample = series.dropna().astype(str).head(8)
    if sample.empty:
        return False
    parsed = pd.to_datetime(sample, errors="coerce")
    return bool(parsed.notna().mean() >= 0.75)


def _values_between_zero_and_one(series):
    if not _is_numeric(series):
        return False
    values = pd.to_numeric(series.dropna(), errors="coerce").dropna()
    if values.empty:
        return False
    return bool((values >= 0).all() and (values <= 1).all())


def infer_semantic_type(name, series):
    text = _column_text(name)

    if _is_datetime(series) or any(token in text for token in ["时段", "时间", "日期", "hour", "time"]):
        return "time"
    if any(token in text for token in ["阈值", "要求", "标准", "目标线", "threshold", "target"]):
        return "threshold"
    if any(token in text for token in ["状态", "达标", "是否", "status", "satisfied"]):
        return "status"
    if any(token in text for token in ["目标函数", "目标值", "objective", "loss", "score"]):
        return "objective"
    if any(token in text for token in ["容量", "capacity", "cap"]):
        return "capacity"
    if any(token in text for token in ["成本", "费用", "价格", "电价", "cost", "price", "元/"]):
        return "cost"
    if any(token in text for token in ["比例", "占比", "比率", "率", "ratio", "percent", "%"]) or _values_between_zero_and_one(series):
        return "ratio"
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if _is_numeric(series):
        return "numeric"
    return "category"


def summarize_column(name, series):
    non_null = int(series.notna().sum())
    missing = int(series.isna().sum())
    total = int(len(series))
    examples = [_json_safe(value) for value in series.dropna().drop_duplicates().head(3).tolist()]
    summary = {
        "name": str(name),
        "dtype": str(series.dtype),
        "semantic_type": infer_semantic_type(name, series),
        "unit": _extract_unit(name),
        "non_null": non_null,
        "missing": missing,
        "missing_ratio": round(missing / total, 6) if total else 0.0,
        "unique_count": int(series.nunique(dropna=True)),
        "examples": examples,
    }

    if _is_numeric(series):
        numeric = pd.to_numeric(series, errors="coerce").dropna()
        summary["numeric"] = {
            "min": _json_safe(numeric.min()) if not numeric.empty else None,
            "max": _json_safe(numeric.max()) if not numeric.empty else None,
            "mean": _json_safe(numeric.mean()) if not numeric.empty else None,
            "median": _json_safe(numeric.median()) if not numeric.empty else None,
        }
    return summary


def _read_source(source, sheet_name=0):
    if isinstance(source, pd.DataFrame):
        return source.copy(), {"type": "dataframe", "name": "dataframe"}

    path = Path(source)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, encoding="utf-8-sig"), {"type": "csv", "name": path.name, "path": str(path)}
    if suffix in {".xls", ".xlsx"}:
        return (
            pd.read_excel(path, sheet_name=sheet_name),
            {"type": "excel", "name": path.name, "path": str(path), "sheet_name": sheet_name},
        )
    raise ValueError(f"Unsupported data source suffix: {suffix}")


def _semantic_hints(column_profiles):
    hints = {f"{bucket}_columns": [] for bucket in SEMANTIC_BUCKETS}
    for name, profile in column_profiles.items():
        key = f"{profile['semantic_type']}_columns"
        hints.setdefault(key, []).append(name)
    return hints


def _plotting_hints(hints):
    return {
        "has_time_axis": bool(hints.get("time_columns")),
        "has_thresholds": bool(hints.get("threshold_columns")),
        "has_categories": bool(hints.get("category_columns") or hints.get("status_columns")),
        "has_costs": bool(hints.get("cost_columns")),
        "has_capacity": bool(hints.get("capacity_columns")),
        "has_objectives": bool(hints.get("objective_columns")),
        "has_ratios": bool(hints.get("ratio_columns")),
        "has_optimization_surface_candidates": bool(
            hints.get("capacity_columns") and len(hints.get("cost_columns", [])) >= 2
        ),
    }


def profile_dataframe(df, source=None):
    columns = {str(name): summarize_column(name, df[name]) for name in df.columns}
    hints = _semantic_hints(columns)
    return _json_safe(
        {
            "source": source or {"type": "dataframe", "name": "dataframe"},
            "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
            "columns": columns,
            "semantic_hints": hints,
            "plotting_hints": _plotting_hints(hints),
        }
    )


def profile_data(source, *, source_name=None, sheet_name=0):
    df, source_meta = _read_source(source, sheet_name=sheet_name)
    if source_name:
        source_meta["name"] = source_name
    return profile_dataframe(df, source=source_meta)


def main():
    parser = argparse.ArgumentParser(description="Profile CSV/Excel data for plotting planner inputs.")
    parser.add_argument("source", help="CSV, XLS, or XLSX file path.")
    parser.add_argument("--sheet-name", default=0, help="Excel sheet name or index. Defaults to 0.")
    args = parser.parse_args()
    sheet_name = int(args.sheet_name) if str(args.sheet_name).isdigit() else args.sheet_name
    profile = profile_data(args.source, sheet_name=sheet_name)
    print(json.dumps(profile, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
