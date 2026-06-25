import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


# ============================================================
# 升级配色 — Nature NMI Pastel + 学术色板
# ============================================================
COLORS = {
    # 主色系
    "blue_main":   "#3B6BA5",   # 主蓝 — 风电/售电
    "blue_light":  "#6B93C7",   # 辅助蓝
    "teal":        "#3D8C6A",   # 墨绿 — 制氢/绿电
    "teal_light":  "#6AAF8A",   # 辅助绿
    "amber":       "#D4942B",   # 暖金 — 光伏
    "crimson":     "#C44D4D",   # 暖红 — 电负荷/购电
    "crimson_light": "#D97A6B", # 辅助红
    "purple":      "#7C5E9E",   # 紫 — 强调色
    "purple_light": "#A88FC4",
    
    # 中性色
    "grid":        "#E2E6ED",   # 网格线
    "axis":        "#6B7280",   # 坐标轴
    "text":        "#1F2937",   # 正文
    "muted":       "#9CA3AF",   # 次要文字
    "background":  "#FFFFFF",   # 背景
    
    # 渐变色系
    "blue_seq":    ["#3B6BA5", "#5B8EC9", "#8AB3E0", "#B8D4EF"],
    "green_seq":   ["#3D8C6A", "#6AAF8A", "#9ED1B2", "#C8E6D8"],
    "red_seq":     ["#C44D4D", "#D97A6B", "#ECA89A", "#F5D6D6"],
}



# 标准循环色板（按学术论文常见需求排序）
PALETTE = [
    COLORS["blue_main"],
    COLORS["amber"],
    COLORS["teal"],
    COLORS["crimson"],
    COLORS["purple"],
    COLORS["blue_light"],
    COLORS["teal_light"],
    COLORS["crimson_light"],
]

# ★ 向后兼容：旧名 → 新名
_OLD_MAP = {"blue": "blue_main", "seagreen": "teal"}
for old, new in _OLD_MAP.items():
    if old not in COLORS:
        COLORS[old] = COLORS[new]

# 连续色带
PAPER_CMAP = LinearSegmentedColormap.from_list(
    "paper_main",
    [COLORS["blue_main"], COLORS["teal"], COLORS["amber"], COLORS["crimson"]],
)

DIVERGING_CMAP = LinearSegmentedColormap.from_list(
    "paper_diverging",
    [COLORS["blue_main"], "#F3F4F6", COLORS["crimson"]],
)


def palette(n):
    return [PALETTE[i % len(PALETTE)] for i in range(n)]


# ============================================================
# 修复1: apply_paper_style — 关掉全局网格
# ============================================================
def apply_paper_style():
    plt.rcParams.update(
        {
            "font.sans-serif": ["Microsoft YaHei", "SimHei", "DengXian", "Arial"],
            "font.serif": ["Times New Roman", "Microsoft YaHei", "SimHei"],
            "font.family": ["sans-serif"],
            "axes.unicode_minus": False,
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.06,
            "figure.facecolor": COLORS["background"],
            "axes.facecolor": COLORS["background"],
            "axes.edgecolor": COLORS["axis"],
            "axes.labelcolor": COLORS["text"],
            "axes.labelsize": 11,
            "axes.labelpad": 6,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.titlepad": 10,
            # ★ 修复：关掉默认网格，避免双层重叠
            "axes.grid": False,
            "axes.axisbelow": True,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "legend.frameon": False,
            "legend.fontsize": 9.5,
            "legend.handlelength": 1.2,
            "legend.handletextpad": 0.6,
            "xtick.color": COLORS["axis"],
            "ytick.color": COLORS["axis"],
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "lines.linewidth": 1.8,
            "lines.markersize": 5,
            "patch.edgecolor": COLORS["background"],
        }
    )


# ============================================================
# 修复2: style_axis — 网格默认为关闭
# ============================================================
def style_axis(ax, grid=False, grid_axis="y", legend_outside=False):
    """统一轴样式，grid 默认 False，需要时手动开启"""
    ax.set_axisbelow(True)
    
    # ★ 网格只在主动调用时添加
    if grid:
        ax.grid(True, axis=grid_axis, color=COLORS["grid"], linestyle="-", linewidth=0.4, alpha=0.7)
    
    # 边框
    for side in ("top", "right"):
        if side in ax.spines:
            ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        if side in ax.spines:
            ax.spines[side].set_color("#D1D5DB")
            ax.spines[side].set_linewidth(0.7)
    
    # 刻度
    ax.tick_params(colors=COLORS["axis"], labelsize=9)
    
    # 图例
    handles, labels = ax.get_legend_handles_labels()
    labels = [label for label in labels if not label.startswith("_")]
    if labels and ax.get_legend() is None:
        if legend_outside:
            ax.legend(handles, labels, loc="upper center",
                      bbox_to_anchor=(0.5, 1.08), ncol=min(4, len(labels)),
                      borderaxespad=0, frameon=False)
        else:
            ax.legend(handles, labels, loc="upper right", frameon=False)


def set_chart_title(ax, title):
    ax.set_title(title, fontsize=13, fontweight="bold", color=COLORS["text"], y=1.06, pad=10)


# ============================================================
# 以下为 annotation、save、metadata 等函数（保持不变）
# ============================================================

ANNOTATION_ALLOWED_MODES = ("point", "extreme", "event", "threshold", "phase")
ANNOTATION_LIMITS = {"paper": 3, "presentation": 4, "appendix": 1}
ANNOTATION_SUITABLE_CHARTS = {"line", "time_series", "scatter_trend", "threshold", "bar"}
ANNOTATION_CAUTION_CHARTS = {"heatmap", "scatter_matrix", "dendrogram", "radar", "polar", "3d", "multi_series_dense"}
AUTO_ANNOTATION_DISABLED_CHARTS = {"3d", "heatmap", "scatter_matrix", "radar", "polar"}


def validate_annotation_config(
    annotate=False, annotation_mode=None, annotation_config=None,
    chart_type=None, figure_context="paper", detected=False,
    auto_annotation=False, suggested_annotations=None,
):
    auto_annotation = bool(auto_annotation or detected)
    if not annotate and not auto_annotation:
        return None
    if annotation_mode is None:
        raise ValueError("annotation_mode is required when annotation is enabled")
    if annotate and annotation_config is None:
        raise ValueError("annotation_config is required when annotate=True")
    if annotation_mode not in ANNOTATION_ALLOWED_MODES:
        allowed = ", ".join(ANNOTATION_ALLOWED_MODES)
        raise ValueError(f"annotation_mode must be one of: {allowed}")
    if figure_context not in ANNOTATION_LIMITS:
        contexts = ", ".join(ANNOTATION_LIMITS)
        raise ValueError(f"figure_context must be one of: {contexts}")
    config = dict(annotation_config or {})
    count = int(config.get("count", 1))
    if count < 0:
        raise ValueError("annotation count cannot be negative")
    max_count = ANNOTATION_LIMITS[figure_context]
    if count > max_count:
        raise ValueError(f"{figure_context} figures allow at most {max_count} annotation items")
    suggested_annotations = list(suggested_annotations or [])
    if auto_annotation and chart_type in AUTO_ANNOTATION_DISABLED_CHARTS:
        return {"enabled": False, "mode": annotation_mode, "config": config, "count": count,
                "chart_type": chart_type, "figure_context": figure_context, "caution": True,
                "auto_annotation": True, "suggested_only": True, "auto_disabled": True,
                "suggested_annotations": suggested_annotations}
    return {"enabled": bool(annotate), "mode": annotation_mode, "config": config, "count": count,
            "chart_type": chart_type, "figure_context": figure_context,
            "caution": chart_type in ANNOTATION_CAUTION_CHARTS,
            "auto_annotation": auto_annotation, "suggested_only": bool(auto_annotation and not annotate),
            "auto_disabled": False, "suggested_annotations": suggested_annotations}


def _annotation_bbox(color, alpha=0.92, pad=0.28, linewidth=0.9):
    return {"boxstyle": f"round,pad={pad}", "facecolor": COLORS["background"],
            "edgecolor": color, "linewidth": linewidth, "alpha": alpha}


def annotate_point(ax, x, y, text, xytext=(18, 18), color=None, marker_size=58):
    color = color or COLORS["amber"]
    ha = "left" if xytext[0] >= 0 else "right"
    va = "bottom" if xytext[1] >= 0 else "top"
    ax.scatter([x], [y], s=marker_size, color=color, edgecolor=COLORS["background"],
               linewidth=1.2, zorder=5)
    ax.annotate(text, xy=(x, y), xytext=xytext, textcoords="offset points",
                ha=ha, va=va, fontsize=9.5, color=COLORS["text"],
                arrowprops={"arrowstyle": "->", "color": color, "lw": 1.2, "shrinkA": 0, "shrinkB": 5},
                bbox=_annotation_bbox(color), zorder=6, clip_on=False, annotation_clip=False)
    return ax


def add_event_line(ax, x, label, color=None, linestyle="--", linewidth=1.3):
    color = color or COLORS["amber"]
    ax.axvline(x=x, color=color, linestyle=linestyle, linewidth=linewidth, alpha=0.9, zorder=2)
    ax.text(x, 1.01, label, transform=ax.get_xaxis_transform(), ha="center", va="bottom",
            fontsize=9.3, color=color,
            bbox=_annotation_bbox(color, alpha=0.9, pad=0.22, linewidth=0.8),
            zorder=6, clip_on=False)
    return ax


def add_threshold_line(ax, y, label, color=None, linestyle="--", linewidth=1.3):
    color = color or COLORS["crimson"]
    ax.axhline(y=y, color=color, linestyle=linestyle, linewidth=linewidth, alpha=0.9, zorder=2)
    ax.annotate(label, xy=(0.98, y), xycoords=ax.get_yaxis_transform(),
                xytext=(-4, 6), textcoords="offset points", ha="right", va="bottom",
                fontsize=9.3, color=color,
                bbox=_annotation_bbox(color, alpha=0.9, pad=0.22, linewidth=0.8),
                zorder=6, clip_on=False, annotation_clip=False)
    return ax


def add_phase_span(ax, x_start, x_end, label=None, color=None, alpha=0.08):
    color = color or COLORS["blue_main"]
    ax.axvspan(x_start, x_end, color=color, alpha=alpha, zorder=0)
    if label:
        try:
            cx = x_start + (x_end - x_start) / 2
        except TypeError:
            cx = x_start
        ax.text(cx, 1.06, label, transform=ax.get_xaxis_transform(), ha="center", va="bottom",
                fontsize=9.3, color=color,
                bbox=_annotation_bbox(color, alpha=0.85, pad=0.22, linewidth=0.7),
                zorder=6, clip_on=False)
    return ax


def annotate_extreme(ax, x_values, y_values, mode="max", text=None, color=None, xytext=(18, 18)):
    x_values = np.asarray(x_values); y_values = np.asarray(y_values)
    if mode == "max":
        idx = np.nanargmax(y_values); default_text = f"最高：{y_values[idx]:.2f}"; color = color or COLORS["amber"]
    elif mode == "min":
        idx = np.nanargmin(y_values); default_text = f"最低：{y_values[idx]:.2f}"; color = color or COLORS["crimson"]
    else:
        raise ValueError("mode must be 'max' or 'min'")
    annotate_point(ax, x_values[idx], y_values[idx], text or default_text, xytext=xytext, color=color)
    return ax


def style_3d_axis(ax, elev=26, azim=-52):
    ax.view_init(elev=elev, azim=azim)
    ax.set_box_aspect((1.15, 1.0, 0.72))
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1, 1, 1, 0))
        axis.pane.set_edgecolor(COLORS["grid"])
        axis._axinfo["grid"]["color"] = COLORS["grid"]
        axis._axinfo["grid"]["linewidth"] = 0.45
        axis._axinfo["grid"]["linestyle"] = "--"
    ax.tick_params(colors=COLORS["axis"], labelsize=9, pad=2)


def finalize_plot(fig=None, grid=False, legend_outside=False):
    """★ grid 默认 False"""
    fig = fig or plt.gcf()
    axes = fig.get_axes()
    has_3d = any(getattr(ax, "name", "") == "3d" for ax in axes)
    for ax in axes:
        if getattr(ax, "name", "") == "3d":
            style_3d_axis(ax)
        else:
            style_axis(ax, grid=grid, legend_outside=legend_outside)
    if has_3d:
        fig.subplots_adjust(left=0.08, right=0.86, bottom=0.11, top=0.88, wspace=0.32)
    else:
        fig.tight_layout()


PROBLEM_TYPE_BY_PLOT = {
    "bar": "评价类", "grouped_bar": "评价类", "stacked_bar": "评价类",
    "percentage_stacked_bar": "评价类", "radar": "评价类", "piechart": "评价类",
    "donut": "评价类", "boxplot": "统计处理类", "violinplot": "统计处理类",
    "histogram": "统计处理类", "kde": "统计处理类", "corr_heat": "统计处理类",
    "heat": "统计处理类", "line": "预测类", "time_series": "预测类",
    "scatter_with_trend": "预测类", "area": "预测类", "contour": "优化类",
    "waterfall": "优化类", "3d_surface": "优化类", "3d_contour": "优化类",
    "3d_scatter": "聚类分类类", "matrix_scatter": "统计处理类",
}


def _json_safe(value):
    if isinstance(value, dict): return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [_json_safe(v) for v in value]
    if isinstance(value, np.ndarray): return _json_safe(value.tolist())
    if isinstance(value, (np.integer,)): return int(value)
    if isinstance(value, (np.floating, float)):
        if math.isnan(float(value)) or math.isinf(float(value)): return None
        return float(value)
    if isinstance(value, (np.bool_, bool)): return bool(value)
    return value


def _numeric_values(data):
    values = []
    def walk(item):
        if item is None: values.append(np.nan)
        elif isinstance(item, dict):
            for v in item.values(): walk(v)
        elif isinstance(item, np.ndarray): walk(item.tolist())
        elif isinstance(item, (list, tuple)):
            for v in item: walk(v)
        else:
            try: values.append(float(item))
            except (TypeError, ValueError): pass
    walk(data)
    return values


def _summarize_data(data):
    if not data: return {"sample_size": 0, "min": None, "max": None, "missing_values": 0}
    source = data.get("y") if isinstance(data, dict) and "y" in data else data
    values = np.asarray(_numeric_values(source), dtype=float)
    if values.size == 0: return {"sample_size": 0, "min": None, "max": None, "missing_values": 0}
    missing = int(np.isnan(values).sum())
    finite = values[np.isfinite(values)]
    return {"sample_size": int(values.size), "min": float(np.min(finite)) if finite.size else None,
            "max": float(np.max(finite)) if finite.size else None, "missing_values": missing}


def _infer_plot_type(stem):
    name = str(stem)
    if name.startswith("plot_"): name = name[5:]
    if name in {"1","2","3","4","5","6","7","8","9","10"}:
        return {"1":"vector_field","2":"grouped_scatter","3":"colored_line","4":"3d_wireframe",
                "5":"mosaic","6":"andrews_curve","7":"pareto","8":"dendrogram",
                "9":"colored_scatter","10":"3d_surface"}[name]
    return name


def _infer_problem_type(plot_type):
    for key, pt in PROBLEM_TYPE_BY_PLOT.items():
        if key in plot_type: return pt
    return "评价类"


def _axis_labels(fig):
    labels = {"x": "", "y": ""}
    axes = fig.get_axes()
    if not axes: return labels
    ax = axes[0]; labels["x"] = ax.get_xlabel(); labels["y"] = ax.get_ylabel()
    if hasattr(ax, "get_zlabel"): labels["z"] = ax.get_zlabel()
    return labels


def _legend_labels(fig):
    labels = []
    for ax in fig.get_axes():
        h, al = ax.get_legend_handles_labels(); del h
        labels.extend(l for l in al if l and not l.startswith("_"))
    return list(dict.fromkeys(labels))


def build_figure_metadata(stem, fig=None, metadata=None):
    fig = fig or plt.gcf(); metadata = dict(metadata or {})
    plot_type = metadata.get("plot_type") or _infer_plot_type(stem)
    title = ""
    axes = fig.get_axes()
    if axes: title = axes[0].get_title()
    axis_labels = dict(_axis_labels(fig))
    axis_labels.update(metadata.get("axis_labels") or {})
    legend_labels = metadata.get("legend_labels") or _legend_labels(fig)
    caption = metadata.get("caption") or title
    variables = metadata.get("variables") or {k: v for k, v in axis_labels.items() if v}
    modeling_purpose = metadata.get("modeling_purpose") or f"展示{caption}" if caption else "展示建模数据的主要结构和变化特征"
    built = {"figure_name": metadata.get("figure_name", str(stem)), "plot_type": plot_type,
             "problem_type": metadata.get("problem_type") or _infer_problem_type(plot_type),
             "modeling_purpose": modeling_purpose, "variables": variables,
             "axis_labels": axis_labels, "legend_labels": legend_labels,
             "caption": caption, "usage": metadata.get("usage", "paper"),
             "annotate": bool(metadata.get("annotate", False)),
             "annotation_config": metadata.get("annotation_config"),
             "data_summary": metadata.get("data_summary") or _summarize_data(metadata.get("data"))}
    if title: built["internal_title"] = title
    if metadata.get("suggested_annotations") is not None:
        built["suggested_annotations"] = metadata["suggested_annotations"]
    return _json_safe(built)


def write_figure_metadata(stem, fig=None, metadata=None):
    output_path = Path(f"{stem}.metadata.json").resolve()
    figure_metadata = build_figure_metadata(stem, fig=fig, metadata=metadata)
    output_path.write_text(json.dumps(figure_metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def save_current_figure(stem, fig=None, metadata=None, grid=False):
    """★ grid 默认 False，不添加网格"""
    fig = fig or plt.gcf()
    finalize_plot(fig, grid=grid)
    output_path = Path(f"{stem}.png").resolve()
    fig.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0.06)
    metadata_path = write_figure_metadata(stem, fig=fig, metadata=metadata)
    plt.close(fig)
    print(f"Saved: {output_path}\nMetadata: {metadata_path}")
    return output_path


apply_paper_style()
