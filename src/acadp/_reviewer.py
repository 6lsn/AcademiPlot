"""Chart quality reviewer -- 6-dimension scoring system.

Migrated from review/chart_reviewer.py. Provides programmatic review API
without CLI or file-routing dependencies.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from functools import lru_cache

try:
    import yaml
except ImportError:
    yaml = None


# ============================================================
# Constants
# ============================================================

SCORE_KEYS = [
    "theme_fit",
    "chart_suitability",
    "readability",
    "annotation_quality",
    "caption_consistency",
    "paper_style",
]

STATUS_DIR = {
    "pass": "final_figures",
    "revise": "revise",
    "manual_review": "manual_review",
    "reject": "reject",
}

PROBLEM_CHARTS = {
    "评价类": {"bar", "grouped_bar", "stacked_bar", "percentage_stacked_bar", "boxplot", "heat", "corr_heat", "radar", "dotplot"},
    "预测类": {"time_series", "line", "line_basic", "scatter_with_trend", "area", "filled_line_chart", "contour"},
    "优化类": {"pareto", "waterfall", "contour", "3d_surface", "3d_contour", "bar", "scatter_with_trend"},
    "聚类分类类": {"scatter_grouped", "grouped_scatter", "dendrogram", "3d_scatter", "dotplot"},
    "物理工程空间类": {"vector_field", "3d_surface", "3d_wireframe", "contour", "3d_contour"},
    "统计处理类": {"histogram", "kde", "histogram_with_kde", "boxplot", "violinplot", "corr_heat", "heat", "matrix_scatter"},
}

CAUTION_CHARTS = {"3d", "3d_surface", "3d_scatter", "3d_contour", "pie", "piechart", "donut", "radar", "matrix_scatter", "scatter_matrix"}
ANNOTATION_CAUTION_CHARTS = {"3d", "3d_surface", "3d_scatter", "heat", "heatmap", "corr_heat", "matrix_scatter", "scatter_matrix", "radar", "polar"}
CAUSAL_WORDS = ["导致", "由于", "因果", "cause", "caused", "because", "therefore"]

SKILL_ROOT = Path(__file__).resolve().parents[2]
RECIPE_INDEX_PATH = SKILL_ROOT / "references" / "recipe_index.yaml"

PURPOSE_ROLE_KEYWORDS = {
    "constraint_compliance": ["达标", "阈值", "约束", "合规", "满足要求", "要求阈值", "compliance", "threshold", "constraint"],
    "threshold_comparison": ["阈值", "目标线", "警戒线", "标准值", "要求值", "target line"],
    "indicator_evaluation": ["指标评价", "评价指标", "指标值", "综合得分", "得分排名"],
    "parameter_optimization": ["参数寻优", "参数优化", "最优", "寻优", "优化路径", "optimum", "optimization"],
    "surface_search": ["响应面", "等高线", "二维参数", "parameter surface"],
    "paired_scheme_comparison": ["双方案", "两种方案", "方案对比", "基准方案", "对比方案", "节约率", "改进率"],
    "before_after_comparison": ["前后对比", "改造前", "改造后", "before", "after"],
    "two_series_gap": ["差异", "差距", "gap", "saving", "improvement"],
    "system_balance": ["供需", "平衡", "净差", "缺口", "盈余", "balance"],
    "supply_demand_matching": ["供给", "需求", "匹配", "supply", "demand"],
    "power_balance": ["电力平衡", "负荷", "出力", "发电", "用电"],
    "multi_factor_sensitivity": ["敏感性", "扰动", "多因素", "sensitivity"],
    "parameter_sensitivity": ["参数敏感", "参数扰动"],
    "scenario_sensitivity": ["情景", "场景", "scenario"],
    "cost_decomposition": ["成本拆解", "成本构成", "费用构成", "cost breakdown"],
    "incremental_change": ["增量", "边际", "逐步变化", "incremental"],
    "contribution_breakdown": ["贡献", "分解", "构成"],
    "multi_objective_tradeoff": ["多目标", "权衡", "tradeoff", "trade-off"],
    "pareto_frontier": ["帕累托", "pareto", "前沿"],
    "efficiency_frontier": ["效率前沿", "efficient frontier"],
    "composition_comparison": ["占比", "组成", "结构", "构成比例"],
    "share_structure": ["份额", "比例结构", "share"],
    "annual_status_structure": ["年度", "年际", "annual"],
}

PLOT_TYPE_ALIASES = {
    "bar": {"bar", "horizontal_bar", "grouped_bar", "stacked_bar", "percentage_stacked_bar"},
    "contour": {"contour", "heat", "heatmap", "3d_contour"},
    "dotplot": {"dotplot", "dumbbell", "lollipop"},
    "time_series": {"time_series", "line", "line_basic", "area", "filled_line_chart"},
    "scatter_with_trend": {"scatter", "scatter_with_trend", "pareto"},
    "waterfall": {"waterfall"},
    "percentage_stacked_bar": {"percentage_stacked_bar", "stacked_bar"},
}


# ============================================================
# Dataclasses
# ============================================================

@dataclass
class ReviewResult:
    """Result of reviewing a single figure."""
    figure: str = ""
    score: int = 0
    status: str = "unknown"
    scores: dict = field(default_factory=dict)
    major_issues: list = field(default_factory=list)
    minor_issues: list = field(default_factory=list)
    suggested_caption: str = ""
    suggested_plot_type: str = ""
    recommended_action: str = ""

    def to_markdown(self) -> str:
        lines = [f"## {self.figure}", ""]
        lines.append(f"- Status: `{self.status}`")
        lines.append(f"- Score: {self.score}/100")
        score_text = ", ".join(f"{k}={v}" for k, v in self.scores.items())
        lines.append(f"- Dimensions: {score_text}")
        if self.major_issues:
            lines.append("- Major issues:")
            for issue in self.major_issues:
                lines.append(f"  - {issue}")
        if self.minor_issues:
            lines.append("- Minor issues:")
            for issue in self.minor_issues:
                lines.append(f"  - {issue}")
        if self.suggested_caption:
            lines.append(f"- Suggested caption: {self.suggested_caption}")
        if self.suggested_plot_type:
            lines.append(f"- Suggested plot type: {self.suggested_plot_type}")
        return "\n".join(lines)


@dataclass
class BatchReport:
    """Aggregated report from reviewing a directory of figures."""
    total: int = 0
    pass_count: int = 0
    revise_count: int = 0
    manual_count: int = 0
    reject_count: int = 0
    results: list = field(default_factory=list)

    def to_markdown(self, path=None) -> str:
        lines = ["# Chart Review Report", ""]
        lines.append(f"- Total: {self.total}")
        lines.append(f"- Pass: {self.pass_count}")
        lines.append(f"- Revise: {self.revise_count}")
        lines.append(f"- Manual review: {self.manual_count}")
        lines.append(f"- Reject: {self.reject_count}")
        lines.append("")
        for r in self.results:
            lines.append(r.to_markdown())
            lines.append("")
        md = "\n".join(lines)
        if path:
            Path(path).write_text(md, encoding="utf-8")
        return md


# ============================================================
# Helpers
# ============================================================

def _clamp(value):
    return max(0, min(100, int(round(value))))


def _normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _as_list(value):
    if not value:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


def _normalize_role_set(values):
    return {_normalize_text(value).strip() for value in _as_list(values) if _normalize_text(value).strip()}


@lru_cache(maxsize=1)
def _load_recipe_catalog():
    if yaml is None or not RECIPE_INDEX_PATH.exists():
        return {}
    index = yaml.safe_load(RECIPE_INDEX_PATH.read_text(encoding="utf-8")) or {}
    catalog = {}
    for entry in index.get("recipes", []):
        recipe_id = _normalize_text(entry.get("id")).strip()
        if not recipe_id:
            continue
        recipe = dict(entry)
        recipe_path = SKILL_ROOT / _normalize_text(entry.get("path"))
        if recipe_path.exists():
            detail = yaml.safe_load(recipe_path.read_text(encoding="utf-8")) or {}
            if isinstance(detail, dict):
                recipe.update(detail)
        roles = _normalize_role_set(entry.get("trigger_roles"))
        roles.update(_normalize_role_set(recipe.get("trigger_roles")))
        if recipe.get("figure_role"):
            roles.add(_normalize_text(recipe.get("figure_role")).strip())
        output = recipe.get("output") or {}
        catalog[recipe_id] = {
            "id": recipe_id,
            "roles": roles,
            "plot_type": _normalize_text(output.get("plot_type") or entry.get("recommended_plot_type")).strip(),
            "problem_types": set(_as_list(recipe.get("problem_types"))),
            "summary": _normalize_text(entry.get("summary") or recipe.get("name")),
        }
    return catalog


def _infer_purpose_roles(metadata):
    text = " ".join(
        [
            _normalize_text(metadata.get("modeling_purpose")),
            _normalize_text(metadata.get("caption")),
            _normalize_text(metadata.get("figure_role")),
            _normalize_text(metadata.get("variables")),
        ]
    ).lower()
    roles = set()
    for role, keywords in PURPOSE_ROLE_KEYWORDS.items():
        if any(keyword.lower() in text for keyword in keywords):
            roles.add(role)
    return roles


def _format_roles(roles):
    return "、".join(sorted(roles)) if roles else "未识别"


def _plot_type_matches_expected(actual, expected):
    actual = _normalize_text(actual).lower()
    expected = _normalize_text(expected).lower()
    if not expected or not actual:
        return True
    if expected in actual or actual in expected:
        return True
    expected_aliases = PLOT_TYPE_ALIASES.get(expected, {expected})
    actual_aliases = PLOT_TYPE_ALIASES.get(actual, {actual})
    return bool(expected_aliases & actual_aliases)


def _plot_matches_problem(plot_type, problem_type):
    plot_type = _normalize_text(plot_type).lower()
    suitable = PROBLEM_CHARTS.get(problem_type, set())
    return any(name in plot_type for name in suitable)


def _suggest_plot_type(problem_type):
    return {
        "评价类": "bar / grouped_bar / boxplot",
        "预测类": "time_series / line / scatter_with_trend",
        "优化类": "pareto / waterfall / contour",
        "聚类分类类": "scatter_grouped / dendrogram",
        "物理工程空间类": "contour / vector_field / 3d_surface",
        "统计处理类": "histogram / boxplot / corr_heat",
    }.get(problem_type, "bar / line")


def _has_causal_claim(metadata):
    text = " ".join(
        [
            _normalize_text(metadata.get("caption")),
            _normalize_text(metadata.get("annotation_config")),
            _normalize_text(metadata.get("modeling_purpose")),
        ]
    ).lower()
    return any(word.lower() in text for word in CAUSAL_WORDS)


def _count_annotations(metadata):
    config = metadata.get("annotation_config") or {}
    if isinstance(config, dict):
        if "count" in config:
            try:
                return int(config["count"])
            except (TypeError, ValueError):
                return 1
        if "items" in config and isinstance(config["items"], list):
            return len(config["items"])
    return 1 if metadata.get("annotate") else 0


def _build_suggested_caption(metadata):
    purpose = _normalize_text(metadata.get("modeling_purpose"))
    figure = _normalize_text(metadata.get("figure_name"))
    if purpose:
        return purpose
    return f"{figure} 的建模结果可视化" if figure else ""


# ============================================================
# Recipe fit review
# ============================================================

def _review_recipe_fit(metadata, plot_type):
    recipe_id = _normalize_text(metadata.get("recipe")).strip()
    if not recipe_id:
        return [], []

    catalog = _load_recipe_catalog()
    recipe = catalog.get(recipe_id)
    if not recipe:
        return [f"未知 recipe：{recipe_id}，请检查 references/recipe_index.yaml 或 metadata.recipe。"], []

    major_issues = []
    minor_issues = []
    expected_plot_type = recipe.get("plot_type")
    if expected_plot_type and not _plot_type_matches_expected(plot_type, expected_plot_type):
        major_issues.append(
            f"recipe {recipe_id} 预期输出图型为 {expected_plot_type}，但 metadata.plot_type 为 {plot_type}。"
        )

    allowed_roles = recipe.get("roles") or set()
    figure_role = _normalize_text(metadata.get("figure_role")).strip()
    if figure_role and allowed_roles and figure_role not in allowed_roles:
        major_issues.append(
            f"recipe {recipe_id} 的表达范式适合 {_format_roles(allowed_roles)}，但 figure_role 为 {figure_role}。"
        )

    inferred_roles = _infer_purpose_roles(metadata)
    if inferred_roles and allowed_roles and not (inferred_roles & allowed_roles):
        major_issues.append(
            f"recipe {recipe_id} 与论文目的不匹配：目的更像 {_format_roles(inferred_roles)}，该表达范式适合 {_format_roles(allowed_roles)}。"
        )

    problem_type = _normalize_text(metadata.get("problem_type")).strip()
    problem_types = recipe.get("problem_types") or set()
    if problem_type and problem_types and problem_type not in problem_types:
        minor_issues.append(
            f"recipe {recipe_id} 通常用于 {_format_roles(problem_types)}，当前 problem_type 为 {problem_type}，需人工确认。"
        )

    return major_issues, minor_issues


# ============================================================
# Core review logic
# ============================================================

def _review_metadata(metadata, figure=""):
    """Compute 6-dimension scores for a metadata dict. Returns ReviewResult."""
    plot_type = _normalize_text(metadata.get("plot_type")).lower()
    problem_type = metadata.get("problem_type", "")
    purpose = _normalize_text(metadata.get("modeling_purpose"))
    variables = metadata.get("variables") or {}
    axis_labels = metadata.get("axis_labels") or {}
    legend_labels = metadata.get("legend_labels") or []
    caption = _normalize_text(metadata.get("caption"))
    usage = metadata.get("usage", "paper")
    data_summary = metadata.get("data_summary") or {}
    annotate = bool(metadata.get("annotate"))
    annotation_count = _count_annotations(metadata)

    major_issues = []
    minor_issues = []
    scores = {key: 100 for key in SCORE_KEYS}

    # --- theme_fit & chart_suitability ---
    if not problem_type or not purpose:
        scores["theme_fit"] -= 35
        major_issues.append("缺少 problem_type 或 modeling_purpose，无法判断图是否服务建模主题。")
    elif not _plot_matches_problem(plot_type, problem_type):
        scores["theme_fit"] -= 20
        scores["chart_suitability"] -= 30
        major_issues.append(f"图型 {plot_type} 与 {problem_type} 的常用建模表达不匹配。")

    # recipe fit
    recipe_major_issues, recipe_minor_issues = _review_recipe_fit(metadata, plot_type)
    if recipe_major_issues:
        scores["theme_fit"] -= min(35, 20 * len(recipe_major_issues))
        scores["chart_suitability"] -= min(30, 15 * len(recipe_major_issues))
        major_issues.extend(recipe_major_issues)
    if recipe_minor_issues:
        scores["chart_suitability"] -= min(15, 5 * len(recipe_minor_issues))
        minor_issues.extend(recipe_minor_issues)

    # caution charts
    if any(name in plot_type for name in CAUTION_CHARTS) and usage == "paper":
        scores["chart_suitability"] -= 15
        minor_issues.append(f"{plot_type} 属于正文慎用图型，需确认是否优于二维或表格表达。")

    # pie for prediction
    if "pie" in plot_type and problem_type == "预测类":
        scores["chart_suitability"] -= 35
        major_issues.append("预测类问题通常不宜使用饼图表达趋势。")

    # --- readability ---
    if not variables:
        scores["readability"] -= 20
        major_issues.append("缺少 variables 字段，变量含义不清。")

    needs_axes = not any(name in plot_type for name in ["pie", "donut", "radar"])
    if needs_axes:
        if not axis_labels.get("x"):
            scores["readability"] -= 10
            minor_issues.append("缺少 x 轴标签。")
        if not axis_labels.get("y") and "3d" not in plot_type:
            scores["readability"] -= 10
            minor_issues.append("缺少 y 轴标签。")

    if variables.get("group") and not legend_labels:
        scores["readability"] -= 12
        minor_issues.append("存在分组变量但图例信息缺失。")

    # --- caption_consistency ---
    if not caption:
        scores["caption_consistency"] -= 35
        major_issues.append("缺少图注，无法判断图中信息是否被准确概括。")
    else:
        missing_terms = []
        for value in variables.values():
            value_text = _normalize_text(value)
            if value_text and value_text not in caption and value_text not in purpose:
                missing_terms.append(value_text)
        if missing_terms:
            scores["caption_consistency"] -= min(25, 8 * len(missing_terms))
            minor_issues.append("图注未覆盖部分变量含义：" + "、".join(missing_terms[:3]))

    # --- annotation_quality ---
    if annotate:
        if annotation_count > 3 and usage == "paper":
            scores["annotation_quality"] -= 35
            major_issues.append("正文图 annotation 超过 3 个。")
        elif annotation_count > 0:
            scores["annotation_quality"] -= max(0, annotation_count - 2) * 8
        if any(name in plot_type for name in ANNOTATION_CAUTION_CHARTS):
            scores["annotation_quality"] -= 25
            major_issues.append("高密度图、3D 图、热力图、雷达图或极坐标图应慎用 annotation。")
    else:
        scores["annotation_quality"] -= 0

    # causal claims
    if _has_causal_claim(metadata):
        scores["annotation_quality"] -= 25
        major_issues.append("图注或标注中疑似存在缺乏证据支撑的因果性解释。")

    # --- paper_style ---
    if metadata.get("internal_title"):
        scores["paper_style"] -= 10
        minor_issues.append("检测到图内标题，需确认没有替代正式图注或占用图内空间。")

    # missing values
    if data_summary.get("missing_values", 0):
        scores["theme_fit"] -= 5
        minor_issues.append("数据摘要显示存在缺失值，论文中需说明处理方式。")

    # clamp all scores
    for key in scores:
        scores[key] = _clamp(scores[key])

    # --- status determination ---
    min_score = min(scores.values())
    if any("不宜使用饼图" in issue for issue in major_issues) or min_score < 45:
        status = "reject"
    elif major_issues:
        status = "revise"
    elif min_score < 70:
        status = "manual_review"
    else:
        status = "pass"

    suggested_caption = caption or _build_suggested_caption(metadata)
    suggested_type = "" if _plot_matches_problem(plot_type, problem_type) else _suggest_plot_type(problem_type)
    action = {
        "pass": "可直接进入 final_figures/。",
        "revise": "根据 major_issues 修改绘图脚本或 metadata 后复审。",
        "manual_review": "进入 manual_review/，由建模负责人判断是否保留。",
        "reject": "建议更换图型或重画。",
    }[status]

    overall_score = int(round(sum(scores.values()) / len(scores)))

    return ReviewResult(
        figure=figure,
        score=overall_score,
        status=status,
        scores=scores,
        major_issues=major_issues,
        minor_issues=minor_issues,
        suggested_caption=suggested_caption,
        suggested_plot_type=suggested_type,
        recommended_action=action,
    )


# ============================================================
# Public API
# ============================================================

def review(source):
    """Review a figure.

    Parameters
    ----------
    source : str or Path or dict
        - PNG path: reads the companion .metadata.json
        - JSON path: reads the metadata directly
        - dict: uses the metadata dict as-is

    Returns
    -------
    ReviewResult
    """
    if isinstance(source, dict):
        metadata = source
        figure = source.get("figure_name", "unknown")
    else:
        path = Path(source)
        if path.suffix == ".png":
            meta_path = path.with_name(path.stem + ".metadata.json")
            if not meta_path.exists():
                meta_path = path.with_suffix(".metadata.json")
            if not meta_path.exists():
                return ReviewResult(
                    figure=path.stem,
                    status="reject",
                    score=0,
                    scores={k: 0 for k in SCORE_KEYS},
                    major_issues=[f"找不到 metadata 文件：{meta_path}"],
                    recommended_action="请提供 metadata 文件后重新审查。",
                )
            metadata = json.loads(meta_path.read_text(encoding="utf-8"))
            figure = path.stem
        elif path.suffix == ".json":
            metadata = json.loads(path.read_text(encoding="utf-8"))
            figure = path.stem.replace(".metadata", "")
        else:
            return ReviewResult(
                figure=str(path),
                status="reject",
                score=0,
                scores={k: 0 for k in SCORE_KEYS},
                major_issues=[f"不支持的文件类型：{path.suffix}"],
                recommended_action="请提供 .png 或 .json 文件。",
            )
    return _review_metadata(metadata, figure)


def review_dir(directory):
    """Review all .metadata.json files in a directory.

    Returns
    -------
    BatchReport
    """
    directory = Path(directory)
    results = []
    for meta_path in sorted(directory.glob("*.metadata.json")):
        r = review(meta_path)
        results.append(r)

    report = BatchReport(total=len(results), results=results)
    for r in results:
        if r.status == "pass":
            report.pass_count += 1
        elif r.status == "revise":
            report.revise_count += 1
        elif r.status == "manual_review":
            report.manual_count += 1
        elif r.status == "reject":
            report.reject_count += 1
    return report


# ============================================================
# CLI and file routing
# ============================================================

import argparse
import shutil


def _route_artifacts(metadata_path, review, output_dir):
    """Copy PNG and metadata to status-specific directory."""
    metadata_path = Path(metadata_path)
    status_dir = output_dir / STATUS_DIR.get(review.status, "manual_review")
    status_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(metadata_path, status_dir / metadata_path.name)
    png_path = metadata_path.with_name(
        metadata_path.name.replace(".metadata.json", ".png")
    )
    if png_path.exists():
        shutil.copy2(png_path, status_dir / png_path.name)


def _write_reports(report, output_dir):
    """Write review_report.json and review_report.md."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "review_report.json").write_text(
        json.dumps({
            "summary": {
                "total": report.total,
                "pass": report.pass_count,
                "revise": report.revise_count,
                "manual_review": report.manual_count,
                "reject": report.reject_count,
            },
            "reviews": [
                {
                    "figure": r.figure,
                    "overall_status": r.status,
                    "score": r.score,
                    "scores": r.scores,
                    "major_issues": r.major_issues,
                    "minor_issues": r.minor_issues,
                    "recommended_action": r.recommended_action,
                    "suggested_caption": r.suggested_caption,
                    "suggested_plot_type": r.suggested_plot_type,
                }
                for r in report.results
            ],
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "review_report.md").write_text(report.to_markdown(), encoding="utf-8")


def review_cli(metadata_dir, output_dir, route_files=True):
    """Review all metadata files and optionally route artifacts.

    Parameters
    ----------
    metadata_dir : str or Path
        Directory containing *.metadata.json files.
    output_dir : str or Path
        Directory for review reports and routed figures.
    route_files : bool
        If True, copy files to status-specific subdirectories.

    Returns
    -------
    BatchReport
    """
    metadata_dir = Path(metadata_dir)
    output_dir = Path(output_dir)
    report = review_dir(metadata_dir)
    if route_files:
        for meta_path in sorted(metadata_dir.glob("*.metadata.json")):
            r = review(meta_path)
            _route_artifacts(meta_path, r, output_dir)
    _write_reports(report, output_dir)
    return report


def main():
    """CLI entry point for acadp-review."""
    parser = argparse.ArgumentParser(description="Review generated chart metadata.")
    parser.add_argument("--metadata-dir", required=True, help="Directory with *.metadata.json files.")
    parser.add_argument("--output-dir", required=True, help="Directory for review reports.")
    parser.add_argument("--no-route", action="store_true", help="Skip file routing.")
    args = parser.parse_args()
    report = review_cli(args.metadata_dir, args.output_dir, route_files=not args.no_route)
    print(json.dumps({
        "total": report.total,
        "pass": report.pass_count,
        "revise": report.revise_count,
        "manual_review": report.manual_count,
        "reject": report.reject_count,
    }, ensure_ascii=False))
