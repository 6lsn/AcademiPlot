import argparse
import importlib.util
import json
import shutil
import sys
from copy import deepcopy
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from utf8_io import configure_utf8_stdio


configure_utf8_stdio()

USAGE_LIMITS = {
    "paper": 3,
    "presentation": 4,
    "appendix": 1,
}

ANNOTATION_CAUTION_NAMES = {
    "3d",
    "3d_surface",
    "3d_scatter",
    "3d_contour",
    "heat",
    "heatmap",
    "corr_heat",
    "matrix_scatter",
    "scatter_matrix",
    "radar",
    "polar",
}

UNSAFE_REVIEW_MARKERS = (
    "不匹配",
    "不宜使用饼图",
    "缺乏证据支撑的因果性解释",
)


def load_reviewer():
    path = Path(__file__).with_name("chart_reviewer.py")
    spec = importlib.util.spec_from_file_location("chart_reviewer_for_auto_revise", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REVIEWER = load_reviewer()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, payload):
    Path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def copy_png_if_present(source_metadata_path, output_dir):
    source_metadata_path = Path(source_metadata_path)
    png_path = source_metadata_path.with_name(
        source_metadata_path.name.replace(".metadata.json", ".png")
    )
    if png_path.exists():
        shutil.copy2(png_path, output_dir / png_path.name)


def usage_limit(usage):
    return USAGE_LIMITS.get(usage or "paper", USAGE_LIMITS["paper"])


def annotation_limit_action(usage, limit):
    if usage == "paper":
        return f"将正文图 annotation 数量限制到 {limit} 个"
    if usage == "presentation":
        return f"将汇报图 annotation 数量限制到 {limit} 个"
    if usage == "appendix":
        return f"将附录图 annotation 数量限制到 {limit} 个"
    return f"将 annotation 数量限制到 {limit} 个"


def trim_annotation_config(config, limit):
    config = deepcopy(config or {})
    if isinstance(config.get("items"), list):
        config["items"] = config["items"][:limit]
    config["count"] = min(int(config.get("count", limit + 1)), limit)
    return config


def is_annotation_caution_plot(plot_type):
    plot_type = str(plot_type or "").lower()
    return any(name in plot_type for name in ANNOTATION_CAUTION_NAMES)


def has_unsafe_issue(review):
    issues = review.get("major_issues", []) + review.get("minor_issues", [])
    return any(marker in issue for issue in issues for marker in UNSAFE_REVIEW_MARKERS)


def safe_revise_metadata(metadata, review):
    """Apply only low-risk metadata fixes that do not change data meaning."""
    revised = deepcopy(metadata)
    actions = []
    blocked = []

    if has_unsafe_issue(review):
        blocked.append("涉及图型选择、建模含义或因果解释，需人工复核")

    if not revised.get("caption") and review.get("suggested_caption"):
        revised["caption"] = review["suggested_caption"]
        actions.append("补全缺失图注")

    axis_labels = revised.get("axis_labels") or {}
    variables = revised.get("variables") or {}
    if not variables and axis_labels:
        inferred = {key: value for key, value in axis_labels.items() if value}
        if inferred:
            revised["variables"] = inferred
            actions.append("根据坐标轴标签补全变量含义")

    variables = revised.get("variables") or {}
    axis_labels = dict(revised.get("axis_labels") or {})
    axis_updated = False
    for key in ("x", "y", "z"):
        if not axis_labels.get(key) and variables.get(key):
            axis_labels[key] = variables[key]
            axis_updated = True
    if axis_updated:
        revised["axis_labels"] = axis_labels
        actions.append("根据变量含义补全坐标轴标签")

    if revised.get("annotate"):
        plot_type = revised.get("plot_type", "")
        if is_annotation_caution_plot(plot_type):
            revised["annotate"] = False
            revised["annotation_config"] = None
            actions.append("关闭慎用图型的 annotation")
        else:
            limit = usage_limit(revised.get("usage", "paper"))
            annotation_count = REVIEWER.count_annotations(revised)
            if annotation_count > limit:
                revised["annotation_config"] = trim_annotation_config(
                    revised.get("annotation_config") or {}, limit
                )
                actions.append(annotation_limit_action(revised.get("usage", "paper"), limit))

    return revised, actions, blocked


def metadata_paths(directory):
    return sorted(Path(directory).glob("*.metadata.json"))


def review_by_figure(report):
    return {review["figure"]: review for review in report.get("reviews", [])}


def figure_name_from_metadata(path, metadata):
    return metadata.get("figure_name") or Path(path).name.replace(".metadata.json", "")


def copy_or_write_metadata(source_path, destination_dir, metadata):
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination_path = destination_dir / Path(source_path).name
    write_json(destination_path, metadata)
    copy_png_if_present(source_path, destination_dir)
    return destination_path


def run_revision_round(current_dir, output_dir, round_number):
    round_dir = output_dir / f"round_{round_number}"
    review_dir = round_dir / "review"
    revised_dir = round_dir / "revised_metadata"
    report = REVIEWER.review_directory(current_dir, review_dir)
    reviews = review_by_figure(report)
    round_record = {
        "round": round_number,
        "review_summary": report["summary"],
        "figures": [],
    }

    applied_count = 0
    for metadata_path in metadata_paths(current_dir):
        metadata = read_json(metadata_path)
        figure = figure_name_from_metadata(metadata_path, metadata)
        review = reviews.get(figure) or REVIEWER.review_figure_metadata(metadata)
        revised, actions, blocked = safe_revise_metadata(metadata, review)
        copy_or_write_metadata(metadata_path, revised_dir, revised)
        applied_count += len(actions)
        if actions or blocked or review["overall_status"] != "pass":
            round_record["figures"].append(
                {
                    "figure": figure,
                    "status_before": review["overall_status"],
                    "actions": actions,
                    "blocked": blocked,
                }
            )

    return revised_dir, round_record, applied_count


def auto_revise_directory(metadata_dir, output_dir, max_rounds=2):
    metadata_dir = Path(metadata_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    current_dir = metadata_dir
    rounds = []
    applied_total = 0

    for round_number in range(1, max(1, int(max_rounds)) + 1):
        current_dir, round_record, applied_count = run_revision_round(
            current_dir, output_dir, round_number
        )
        rounds.append(round_record)
        applied_total += applied_count
        if applied_count == 0:
            break

    final_review_dir = output_dir / "final_review"
    final_report = REVIEWER.review_directory(current_dir, final_review_dir)
    plan = {
        "summary": {
            "rounds": len(rounds),
            "applied_fixes": applied_total,
            "final_status_counts": final_report["summary"],
        },
        "rounds": rounds,
        "final_review_report": str(final_review_dir / "review_report.json"),
    }
    write_json(output_dir / "revision_plan.json", plan)
    return plan


def main():
    parser = argparse.ArgumentParser(description="Safely revise chart metadata after review.")
    parser.add_argument("--metadata-dir", required=True, help="Directory containing *.metadata.json files.")
    parser.add_argument("--output-dir", required=True, help="Directory for revision outputs.")
    parser.add_argument("--max-rounds", type=int, default=2, help="Maximum safe revision rounds.")
    args = parser.parse_args()
    plan = auto_revise_directory(args.metadata_dir, args.output_dir, args.max_rounds)
    print(json.dumps(plan["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
