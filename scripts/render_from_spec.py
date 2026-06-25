import argparse
import io
import json
import math
import sys
from contextlib import redirect_stdout
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import yaml
from matplotlib.ticker import PercentFormatter

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from utf8_io import configure_utf8_stdio


configure_utf8_stdio()

from style import COLORS, apply_paper_style, save_current_figure, set_chart_title, style_axis


apply_paper_style()


def _array(values):
    return np.asarray(values, dtype=float)


def _labels(values):
    return [str(value) for value in values]


def _metadata(spec):
    metadata = dict(spec.get("metadata") or {})
    metadata.setdefault("figure_name", spec.get("figure_id", "planned_figure"))
    metadata.setdefault("plot_type", spec.get("plot_type", "bar"))
    metadata.setdefault("problem_type", spec.get("problem_type", "评价类"))
    metadata.setdefault("usage", spec.get("usage", "paper"))
    metadata.setdefault("caption", f"{metadata['figure_name']} 图表")
    metadata.setdefault("modeling_purpose", metadata["caption"])
    metadata.setdefault("variables", {"x": "横轴变量", "y": "纵轴变量"})
    metadata.setdefault("axis_labels", {})
    metadata.setdefault("annotate", False)
    metadata.setdefault("annotation_config", None)
    metadata["data"] = spec.get("data") or spec.get("data_semantics") or {}
    return metadata


def _title(spec):
    return spec.get("recipe_name") or spec.get("recipe", "规划图表")


def _save(fig, spec, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_id = spec.get("figure_id", "planned_figure")
    stem = output_dir / figure_id
    metadata = _metadata(spec)
    with redirect_stdout(io.StringIO()):
        image_path = save_current_figure(stem, fig=fig, metadata=metadata)
    metadata_path = Path(f"{stem}.metadata.json").resolve()
    return {
        "figure_id": figure_id,
        "recipe": spec.get("recipe"),
        "image_path": str(Path(image_path).resolve()),
        "metadata_path": str(metadata_path),
    }


def _is_ratio(data):
    unit = str(data.get("unit", "")).lower()
    return unit in {"ratio", "percent", "%", "比例"} or unit == ""


def _format_number(value, as_percent=False):
    if as_percent:
        return f"{value * 100:.1f}%"
    return f"{value:.1f}"


def _pass_check(actual, threshold, direction):
    direction = str(direction).strip()
    if direction.startswith("<"):
        return actual <= threshold
    if direction.startswith(">"):
        return actual >= threshold
    return abs(actual - threshold) <= 1e-9


def render_bullet_threshold(spec, output_dir):
    data = spec["data"]
    categories = _labels(data["category"])
    actual = _array(data["actual"])
    threshold = _array(data["threshold"])
    directions = data.get("direction", [">="] * len(categories))
    y = np.arange(len(categories))
    as_percent = _is_ratio(data) and float(np.nanmax([actual.max(), threshold.max()])) <= 1.5
    max_value = max(float(np.nanmax(actual)), float(np.nanmax(threshold))) * 1.15
    if as_percent:
        max_value = max(max_value, 1.0)

    fig, ax = plt.subplots(figsize=(8.2, 4.9))
    for idx, category in enumerate(categories):
        passed = _pass_check(actual[idx], threshold[idx], directions[idx])
        color = COLORS["seagreen"] if passed else COLORS["crimson"]
        ax.barh(idx, max_value, color="#F3F4F6", height=0.58, edgecolor="none")
        ax.barh(idx, actual[idx], color=color, height=0.42, alpha=0.9)
        ax.vlines(threshold[idx], idx - 0.34, idx + 0.34, color=COLORS["amber"], linewidth=2.5)
        ax.text(actual[idx] + max_value * 0.015, idx, _format_number(actual[idx], as_percent), va="center")
        ax.text(
            threshold[idx],
            idx + 0.42,
            f"{directions[idx]}{_format_number(threshold[idx], as_percent)}",
            ha="center",
            va="bottom",
            fontsize=9,
            color=COLORS["amber"],
        )
    ax.set_yticks(y)
    ax.set_yticklabels(categories)
    ax.set_xlim(0, max_value)
    ax.invert_yaxis()
    if as_percent:
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.set_xlabel("指标值")
    ax.set_ylabel("指标")
    set_chart_title(ax, "指标阈值达标状态")
    style_axis(ax, grid_axis="x")
    handles = [
        mpatches.Patch(color=COLORS["seagreen"], label="达标"),
        mpatches.Patch(color=COLORS["crimson"], label="未达标"),
        mlines.Line2D([], [], color=COLORS["amber"], linewidth=2.5, label="阈值"),
    ]
    ax.legend(handles=handles, loc="lower right", frameon=False)
    return _save(fig, spec, output_dir)


def render_contour_optimization(spec, output_dir):
    data = spec["data"]
    x = _array(data["x"])
    y = _array(data["y"])
    z = np.asarray(data["z"], dtype=float)
    x_grid, y_grid = np.meshgrid(x, y)
    fig, ax = plt.subplots(figsize=(8.8, 5.7))
    contour = ax.contourf(x_grid, y_grid, z, levels=16, cmap="YlGnBu_r", alpha=0.92)
    lines = ax.contour(x_grid, y_grid, z, levels=7, colors="white", linewidths=0.8, alpha=0.82)
    ax.clabel(lines, inline=True, fontsize=8, fmt="%.1f")
    optimum_indices = np.nanargmin(z, axis=1)
    ax.plot(x[optimum_indices], y, color="white", linewidth=2.2, linestyle="--", label="最优轨迹")
    min_idx = np.unravel_index(np.nanargmin(z), z.shape)
    ax.scatter(x[min_idx[1]], y[min_idx[0]], s=95, color=COLORS["crimson"], edgecolor="white", linewidth=1.4, label="最优点")
    baseline = data.get("baseline") or {}
    if {"x", "y"} <= set(baseline):
        ax.scatter(baseline["x"], baseline["y"], s=80, color=COLORS["amber"], edgecolor="white", linewidth=1.2, label="基准点")
    colorbar = fig.colorbar(contour, ax=ax, pad=0.02)
    colorbar.set_label("目标函数值")
    ax.set_xlabel("参数一")
    ax.set_ylabel("参数二")
    set_chart_title(ax, "二维参数寻优等高线")
    style_axis(ax, grid_axis="both")
    ax.legend(loc="upper right", frameon=False)
    return _save(fig, spec, output_dir)


def render_dumbbell_comparison(spec, output_dir):
    data = spec["data"]
    categories = _labels(data["category"])
    baseline = _array(data["baseline"])
    candidate = _array(data["candidate"])
    y = np.arange(len(categories))
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    for idx in range(len(categories)):
        ax.plot([candidate[idx], baseline[idx]], [idx, idx], color=COLORS["grid"], linewidth=5, solid_capstyle="round", zorder=1)
        if baseline[idx]:
            saving = (baseline[idx] - candidate[idx]) / baseline[idx] * 100
            ax.text(max(baseline[idx], candidate[idx]) * 1.01, idx, f"节约 {saving:.1f}%", va="center", color=COLORS["seagreen"], fontweight="bold")
    ax.scatter(baseline, y, s=88, color=COLORS["crimson"], label=data.get("baseline_label", "基准方案"), zorder=3)
    ax.scatter(candidate, y, s=88, color=COLORS["seagreen"], label=data.get("candidate_label", "对比方案"), zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(categories)
    ax.invert_yaxis()
    ax.set_xlabel(f"指标值 ({data.get('unit', '')})".strip())
    ax.set_ylabel("类别")
    set_chart_title(ax, "双方案配对差异")
    style_axis(ax, grid_axis="x")
    ax.legend(loc="lower right", frameon=False)
    return _save(fig, spec, output_dir)


def render_supply_demand_balance(spec, output_dir):
    data = spec["data"]
    time = _array(data["time"])
    supply = {name: _array(values) for name, values in data["supply_components"].items()}
    demand = _array(data["demand"])
    supply_total = np.sum(np.vstack(list(supply.values())), axis=0)
    net = supply_total - demand
    fig = plt.figure(figsize=(10.8, 6.4))
    gs = fig.add_gridspec(2, 1, height_ratios=[3.2, 1.15], hspace=0.1)
    ax_top = fig.add_subplot(gs[0])
    ax_bottom = fig.add_subplot(gs[1], sharex=ax_top)
    ax_top.stackplot(time, list(supply.values()), labels=list(supply.keys()), colors=[COLORS["blue"], COLORS["amber"], COLORS["seagreen"]], alpha=0.72)
    ax_top.plot(time, demand, color=COLORS["crimson"], linewidth=2.4, label="需求")
    for name, values in (data.get("secondary") or {}).items():
        ax_top.plot(time, _array(values), color=COLORS["muted"], linestyle="--", linewidth=1.6, label=name)
    ax_top.set_ylabel("功率/数量")
    set_chart_title(ax_top, "供需匹配与净差")
    style_axis(ax_top, grid_axis="y")
    ax_top.legend(loc="upper left", ncol=4, frameon=False)
    plt.setp(ax_top.get_xticklabels(), visible=False)
    colors = [COLORS["seagreen"] if value >= 0 else COLORS["crimson"] for value in net]
    ax_bottom.bar(time, net, color=colors, alpha=0.85, width=0.72)
    ax_bottom.axhline(0, color=COLORS["axis"], linewidth=0.9)
    ax_bottom.set_xlabel("时间")
    ax_bottom.set_ylabel("净差")
    style_axis(ax_bottom, grid_axis="y")
    return _save(fig, spec, output_dir)


def render_small_multiples_sensitivity(spec, output_dir):
    factors = spec["data"]["factors"]
    cols = 2
    rows = math.ceil(len(factors) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(11.5, 4.0 * rows))
    axes = np.asarray(axes).reshape(-1)
    y_label = spec["data"].get("y_label", "结果指标")
    for idx, factor in enumerate(factors):
        ax = axes[idx]
        x = _array(factor["x"])
        y = _array(factor["y"])
        ax.plot(x, y, marker="o", color=[COLORS["seagreen"], COLORS["amber"], COLORS["crimson"], COLORS["blue"]][idx % 4], linewidth=2.2)
        if len(x) >= 2:
            trend = np.poly1d(np.polyfit(x, y, 1))(x)
            ax.plot(x, trend, linestyle="--", linewidth=1.2, color=COLORS["muted"])
        if "baseline" in factor:
            ax.axvline(factor["baseline"], color=COLORS["muted"], linestyle=":", linewidth=1.2)
        ax.set_xlabel(factor["name"])
        ax.set_ylabel(y_label)
        set_chart_title(ax, factor["name"])
        style_axis(ax, grid_axis="y")
    for ax in axes[len(factors):]:
        ax.set_visible(False)
    return _save(fig, spec, output_dir)


def render_waterfall_cost(spec, output_dir):
    data = spec["data"]
    changes = data["changes"]
    labels = [data.get("start_label", "基准")] + [item["label"] for item in changes] + [data.get("final_label", "最终")]
    start = float(data["start"])
    running = [start]
    for item in changes:
        running.append(running[-1] + float(item["value"]))
    final = running[-1]
    fig, ax = plt.subplots(figsize=(9.2, 5.3))
    ax.bar(0, start, color=COLORS["blue"], alpha=0.86)
    previous = start
    for idx, item in enumerate(changes, start=1):
        value = float(item["value"])
        bottom = previous if value >= 0 else previous + value
        color = COLORS["crimson"] if value >= 0 else COLORS["seagreen"]
        ax.bar(idx, abs(value), bottom=bottom, color=color, alpha=0.86)
        ax.plot([idx - 0.4, idx + 0.4], [previous, previous], color=COLORS["axis"], linewidth=0.8)
        previous += value
    ax.bar(len(labels) - 1, final, color=COLORS["amber"], alpha=0.88)
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_ylabel("累计值")
    set_chart_title(ax, "成本增减瀑布图")
    style_axis(ax, grid_axis="y")
    return _save(fig, spec, output_dir)


def render_pareto_frontier(spec, output_dir):
    data = spec["data"]
    x = _array(data["objective_x"])
    y = _array(data["objective_y"])
    labels = _labels(data.get("labels", range(len(x))))
    efficient = np.asarray(data.get("efficient", [True] * len(x)), dtype=bool)
    fig, ax = plt.subplots(figsize=(7.8, 5.4))
    ax.scatter(x[~efficient], y[~efficient], s=60, color=COLORS["muted"], alpha=0.7, label="被支配解")
    ax.scatter(x[efficient], y[efficient], s=82, color=COLORS["seagreen"], label="有效解")
    order = np.argsort(x[efficient])
    ax.plot(x[efficient][order], y[efficient][order], color=COLORS["seagreen"], linewidth=1.8, linestyle="--", label="Pareto 前沿")
    for xi, yi, label in zip(x, y, labels):
        ax.text(xi, yi, f" {label}", va="center", fontsize=9)
    ax.set_xlabel("目标一")
    ax.set_ylabel("目标二")
    set_chart_title(ax, "多目标 Pareto 前沿")
    style_axis(ax, grid_axis="both")
    ax.legend(loc="best", frameon=False)
    return _save(fig, spec, output_dir)


def render_percentage_structure(spec, output_dir):
    data = spec["data"]
    categories = _labels(data["category"])
    components = {name: _array(values) for name, values in data["components"].items()}
    matrix = np.vstack(list(components.values()))
    totals = matrix.sum(axis=0)
    rates = np.divide(matrix, totals, out=np.zeros_like(matrix), where=totals != 0)
    x = np.arange(len(categories))
    bottom = np.zeros(len(categories))
    colors = [COLORS["seagreen"], COLORS["amber"], COLORS["crimson"], COLORS["blue"]]
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    for idx, (name, rate) in enumerate(zip(components.keys(), rates)):
        bars = ax.bar(x, rate, bottom=bottom, label=name, color=colors[idx % len(colors)], alpha=0.9)
        for col, bar in enumerate(bars):
            if rate[col] >= 0.08:
                ax.text(bar.get_x() + bar.get_width() / 2, bottom[col] + rate[col] / 2, f"{rate[col] * 100:.0f}%", ha="center", va="center", fontsize=9)
        bottom += rate
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 1.0)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.set_xlabel("类别")
    ax.set_ylabel("组成占比")
    set_chart_title(ax, "组成占比结构")
    style_axis(ax, grid_axis="y")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.06), ncol=min(4, len(components)), frameon=False)
    return _save(fig, spec, output_dir)


RENDERERS = {
    "bullet_threshold": render_bullet_threshold,
    "contour_optimization": render_contour_optimization,
    "dumbbell_comparison": render_dumbbell_comparison,
    "supply_demand_balance": render_supply_demand_balance,
    "small_multiples_sensitivity": render_small_multiples_sensitivity,
    "waterfall_cost": render_waterfall_cost,
    "pareto_frontier": render_pareto_frontier,
    "percentage_structure": render_percentage_structure,
}


def read_spec(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    return json.loads(text)


def render_from_spec(spec, output_dir):
    recipe = spec.get("recipe")
    if recipe not in RENDERERS:
        raise ValueError(f"Unsupported recipe: {recipe}")
    if not spec.get("data"):
        raise ValueError("Spec must include a data field for rendering")
    return RENDERERS[recipe](spec, output_dir)


def main():
    parser = argparse.ArgumentParser(description="Render a plotting spec to PNG and metadata.")
    parser.add_argument("spec", help="Spec JSON/YAML path.")
    parser.add_argument("--output-dir", default=".", help="Directory for rendered PNG and metadata.")
    args = parser.parse_args()
    result = render_from_spec(read_spec(args.spec), args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
