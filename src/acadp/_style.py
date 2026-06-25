"""AcademiPlot style engine — lazy application with theme switching.

Migrated from scripts/style.py. The style is no longer applied at import
time; instead ``_ensure_style()`` is called on the first chart operation.
Three built-in themes are supported: "nature" (default), "science", and
"ieee".
"""

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


# ============================================================
# Configuration store
# ============================================================

_CONFIG = {
    "style": "nature",
    "dpi": 300,
    "font": None,       # None means "use theme default"
    "context": "paper",
    "_applied": False,
}

_VALID_STYLES = {"nature", "science", "ieee"}


# ============================================================
# Theme definitions
# ============================================================

_THEME_DEFAULTS = {
    "nature": {
        "font.family": ["sans-serif"],
        "font.sans-serif": ["Microsoft YaHei", "SimHei", "DengXian", "Arial", "Helvetica"],
        "font.serif": ["Times New Roman", "Microsoft YaHei", "SimHei"],
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "figure.figsize": (3.5, 2.8),          # Nature single-column
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.labelsize": 9,
        "axes.titlespace": 6,
        "axes.labelspace": 4,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 7.5,
        "lines.linewidth": 1.5,
        "lines.markersize": 4,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "axes.axisbelow": True,
        "axes.edgecolor": "#333333",
        "axes.labelcolor": "#333333",
        "xtick.color": "#555555",
        "ytick.color": "#555555",
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FAFAFA",
        "legend.frameon": False,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
    },
    "science": {
        "font.family": ["serif"],
        "font.serif": ["Times New Roman", "SimSun", "Microsoft YaHei"],
        "font.sans-serif": ["Microsoft YaHei", "SimHei", "DengXian", "Arial"],
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "figure.figsize": (3.5, 2.8),
        "axes.titlesize": 10,
        "axes.titleweight": "bold",
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 7.5,
        "lines.linewidth": 1.2,
        "lines.markersize": 3.5,
        "axes.linewidth": 0.5,
        "axes.grid": False,
        "axes.axisbelow": True,
        "axes.edgecolor": "#000000",
        "axes.labelcolor": "#000000",
        "xtick.color": "#333333",
        "ytick.color": "#333333",
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
    },
    "ieee": {
        "font.family": ["serif"],
        "font.serif": ["Times New Roman", "SimSun", "Microsoft YaHei"],
        "font.sans-serif": ["Microsoft YaHei", "SimHei", "DengXian", "Arial"],
        "figure.dpi": 150,
        "savefig.dpi": 600,
        "figure.figsize": (3.5, 2.6),          # IEEE single-column (narrower)
        "axes.titlesize": 9,
        "axes.titleweight": "bold",
        "axes.labelsize": 8,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "legend.fontsize": 7,
        "lines.linewidth": 1.0,
        "lines.markersize": 3,
        "axes.linewidth": 0.5,
        "axes.grid": False,
        "axes.axisbelow": True,
        "axes.edgecolor": "#000000",
        "axes.labelcolor": "#000000",
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.04,
    },
}


# ============================================================
# Color palette (Nature NMI Pastel + academic)
# ============================================================

COLORS = {
    # ── Nature / top-journal primary palette ──
    "navy":         "#003049",   # Nature navy — primary series
    "coral":        "#E07A5F",   # Coral red — secondary series
    "teal":         "#2A9D8F",   # Teal — tertiary
    "amber":        "#E9C46A",   # Golden amber — highlight
    "slate":        "#264653",   # Dark slate — reference / baseline
    "lavender":     "#81B29A",   # Sage green — 4th series
    "rose":         "#F4845F",   # Warm rose — 5th series
    "sky":          "#457B9D",   # Steel blue — 6th series
    "mauve":        "#B5838D",   # Dusty mauve — 7th series
    "sand":         "#D4A373",   # Warm sand — 8th series

    # ── Legacy aliases (backward compat) ──
    "blue_main":    "#003049",
    "blue_light":   "#457B9D",
    "teal_light":   "#2A9D8F",
    "crimson":      "#E07A5F",
    "crimson_light":"#F4845F",
    "purple":       "#81B29A",
    "purple_light": "#B5838D",

    # ── Neutrals ──
    "grid":         "#E8E8E8",
    "axis":         "#555555",
    "text":         "#333333",
    "muted":        "#999999",
    "background":   "#FFFFFF",

    # ── Sequential ramps ──
    "blue_seq":   ["#003049", "#264653", "#457B9D", "#A8DADC"],
    "green_seq":  ["#2A9D8F", "#40916C", "#76C893", "#B7E4C7"],
    "red_seq":    ["#E07A5F", "#F4845F", "#F4A261", "#F4D35E"],

    # ── Diverging ramp ──
    "diverging_seq": ["#457B9D", "#A8DADC", "#F1FAEE", "#F4A261", "#E07A5F"],
}

# backward-compat aliases
_OLD_MAP = {"blue": "blue_main", "seagreen": "teal"}
for _old, _new in _OLD_MAP.items():
    if _old not in COLORS:
        COLORS[_old] = COLORS[_new]

# Standard cycling palette — high contrast, colorblind-friendly
PALETTE = [
    COLORS["navy"],       # deep navy
    COLORS["coral"],      # warm coral
    COLORS["teal"],       # teal
    COLORS["amber"],      # golden amber
    COLORS["lavender"],   # sage green
    COLORS["sky"],        # steel blue
    COLORS["mauve"],      # dusty mauve
    COLORS["sand"],       # warm sand
    COLORS["rose"],       # warm rose
    COLORS["slate"],      # dark slate
]

# Continuous colormaps
PAPER_CMAP = LinearSegmentedColormap.from_list(
    "acadp_nature",
    ["#003049", "#2A9D8F", "#E9C46A", "#E07A5F"],
)

DIVERGING_CMAP = LinearSegmentedColormap.from_list(
    "acadp_diverging",
    ["#457B9D", "#A8DADC", "#F1FAEE", "#F4A261", "#E07A5F"],
)


def palette(n):
    """Return *n* colours from the cycling palette (wraps around)."""
    return [PALETTE[i % len(PALETTE)] for i in range(n)]


# ============================================================
# Public configuration API
# ============================================================

def set_style(name: str) -> None:
    """Switch theme.  Valid names: 'nature', 'science', 'ieee'."""
    if name not in _VALID_STYLES:
        raise ValueError(f"Unknown style {name!r}. Choose from {_VALID_STYLES}")
    _CONFIG["style"] = name
    _CONFIG["_applied"] = False          # force re-application


def get_style() -> dict:
    """Return a copy of the current configuration dict."""
    return {
        "style":   _CONFIG["style"],
        "dpi":     _CONFIG["dpi"],
        "font":    _CONFIG["font"],
        "context": _CONFIG["context"],
    }


def set_dpi(dpi: int) -> None:
    """Set the default save-DPI."""
    _CONFIG["dpi"] = int(dpi)
    _CONFIG["_applied"] = False


def set_font(font: str) -> None:
    """Override the primary font family (e.g. 'serif', 'sans-serif')."""
    _CONFIG["font"] = font
    _CONFIG["_applied"] = False


def set_context(ctx: str) -> None:
    """Set rendering context (e.g. 'paper', 'presentation')."""
    _CONFIG["context"] = ctx
    _CONFIG["_applied"] = False


# ============================================================
# Style application (lazy)
# ============================================================

def _apply_paper_style() -> dict:
    """Build and apply the full rcParams dict for the active theme."""
    theme = _THEME_DEFAULTS[_CONFIG["style"]]

    rc = {
        "font.sans-serif":      theme.get("font.sans-serif", _THEME_DEFAULTS["nature"]["font.sans-serif"]),
        "font.serif":           theme.get("font.serif", _THEME_DEFAULTS["nature"]["font.serif"]),
        "font.family":          theme["font.family"],
        "axes.unicode_minus":   False,
        "figure.dpi":           theme["figure.dpi"],
        "figure.figsize":       theme.get("figure.figsize", (3.5, 2.8)),
        "savefig.dpi":          _CONFIG["dpi"],
        "savefig.bbox":         theme.get("savefig.bbox", "tight"),
        "savefig.pad_inches":   theme.get("savefig.pad_inches", 0.05),
        "figure.facecolor":     theme.get("figure.facecolor", COLORS["background"]),
        "axes.facecolor":       theme.get("axes.facecolor", COLORS["background"]),
        "axes.edgecolor":       theme.get("axes.edgecolor", COLORS["axis"]),
        "axes.labelcolor":      theme.get("axes.labelcolor", COLORS["text"]),
        "axes.labelsize":       theme["axes.labelsize"],
        "axes.labelpad":        theme.get("axes.labelspace", 4),
        "axes.titlesize":       theme["axes.titlesize"],
        "axes.titleweight":     theme.get("axes.titleweight", "bold"),
        "axes.titlepad":        theme.get("axes.titlespace", 6),
        "axes.linewidth":       theme.get("axes.linewidth", 0.6),
        "axes.grid":            theme.get("axes.grid", False),
        "axes.axisbelow":       True,
        "axes.spines.top":      theme.get("axes.spines.top", False),
        "axes.spines.right":    theme.get("axes.spines.right", False),
        "legend.frameon":       theme.get("legend.frameon", False),
        "legend.fontsize":      theme.get("legend.fontsize", 7.5),
        "legend.handlelength":  1.2,
        "legend.handletextpad": 0.6,
        "xtick.color":          theme.get("xtick.color", "#555555"),
        "ytick.color":          theme.get("ytick.color", "#555555"),
        "xtick.labelsize":      theme.get("xtick.labelsize", 8),
        "ytick.labelsize":      theme.get("ytick.labelsize", 8),
        "xtick.major.width":    theme.get("xtick.major.width", 0.5),
        "ytick.major.width":    theme.get("ytick.major.width", 0.5),
        "xtick.major.size":     theme.get("xtick.major.size", 3),
        "ytick.major.size":     theme.get("ytick.major.size", 3),
        "lines.linewidth":      theme.get("lines.linewidth", 1.5),
        "lines.markersize":     theme.get("lines.markersize", 4),
        "patch.edgecolor":      COLORS["background"],
    }

    # user font override
    if _CONFIG["font"] is not None:
        rc["font.family"] = [_CONFIG["font"]]

    plt.rcParams.update(rc)
    _CONFIG["_applied"] = True
    return rc


def _ensure_style():
    """Apply the style exactly once per configuration change."""
    if not _CONFIG["_applied"]:
        _apply_paper_style()


# ============================================================
# Axis helpers
# ============================================================

def style_axis(ax, grid=False, grid_axis="y", legend_outside=False):
    """Unified axis styling.  Grid is off by default."""
    _ensure_style()
    ax.set_axisbelow(True)

    if grid:
        ax.grid(True, axis=grid_axis, color=COLORS["grid"],
                linestyle="-", linewidth=0.3, alpha=0.5)

    for side in ("top", "right"):
        if side in ax.spines:
            ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        if side in ax.spines:
            ax.spines[side].set_color("#CCCCCC")
            ax.spines[side].set_linewidth(0.5)

    ax.tick_params(colors="#555555", labelsize=8, length=3, width=0.5)

    handles, labels = ax.get_legend_handles_labels()
    labels = [l for l in labels if not l.startswith("_")]
    if labels and ax.get_legend() is None:
        if legend_outside:
            ax.legend(handles, labels, loc="upper center",
                      bbox_to_anchor=(0.5, 1.08), ncol=min(4, len(labels)),
                      borderaxespad=0, frameon=False, fontsize=7.5)
        else:
            ax.legend(handles, labels, loc="upper right", frameon=False, fontsize=7.5)


def set_chart_title(ax, title):
    _ensure_style()
    ax.set_title(title, fontsize=10, fontweight="bold",
                 color="#333333", y=1.04, pad=6)


# ============================================================
# Annotation helpers
# ============================================================

ANNOTATION_ALLOWED_MODES = ("point", "extreme", "event", "threshold", "phase")
ANNOTATION_LIMITS = {"paper": 3, "presentation": 4, "appendix": 1}
ANNOTATION_SUITABLE_CHARTS = {
    "line", "time_series", "scatter_trend", "threshold", "bar",
}
ANNOTATION_CAUTION_CHARTS = {
    "heatmap", "scatter_matrix", "dendrogram", "radar", "polar", "3d",
    "multi_series_dense",
}
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
        raise ValueError(
            f"{figure_context} figures allow at most {max_count} annotation items"
        )
    suggested_annotations = list(suggested_annotations or [])
    if auto_annotation and chart_type in AUTO_ANNOTATION_DISABLED_CHARTS:
        return {
            "enabled": False, "mode": annotation_mode, "config": config,
            "count": count, "chart_type": chart_type,
            "figure_context": figure_context, "caution": True,
            "auto_annotation": True, "suggested_only": True,
            "auto_disabled": True,
            "suggested_annotations": suggested_annotations,
        }
    return {
        "enabled": bool(annotate), "mode": annotation_mode, "config": config,
        "count": count, "chart_type": chart_type,
        "figure_context": figure_context,
        "caution": chart_type in ANNOTATION_CAUTION_CHARTS,
        "auto_annotation": auto_annotation,
        "suggested_only": bool(auto_annotation and not annotate),
        "auto_disabled": False,
        "suggested_annotations": suggested_annotations,
    }


def _annotation_bbox(color, alpha=0.92, pad=0.28, linewidth=0.9):
    return {
        "boxstyle": f"round,pad={pad}",
        "facecolor": COLORS["background"],
        "edgecolor": color, "linewidth": linewidth, "alpha": alpha,
    }


def annotate_point(ax, x, y, text, xytext=(18, 18), color=None, marker_size=58):
    color = color or COLORS["amber"]
    ha = "left" if xytext[0] >= 0 else "right"
    va = "bottom" if xytext[1] >= 0 else "top"
    ax.scatter([x], [y], s=marker_size, color=color,
               edgecolor=COLORS["background"], linewidth=1.2, zorder=5)
    ax.annotate(
        text, xy=(x, y), xytext=xytext, textcoords="offset points",
        ha=ha, va=va, fontsize=9.5, color=COLORS["text"],
        arrowprops={"arrowstyle": "->", "color": color, "lw": 1.2,
                     "shrinkA": 0, "shrinkB": 5},
        bbox=_annotation_bbox(color), zorder=6, clip_on=False,
        annotation_clip=False,
    )
    return ax


def add_event_line(ax, x, label, color=None, linestyle="--", linewidth=1.3):
    color = color or COLORS["amber"]
    ax.axvline(x=x, color=color, linestyle=linestyle,
               linewidth=linewidth, alpha=0.9, zorder=2)
    ax.text(x, 1.01, label, transform=ax.get_xaxis_transform(),
            ha="center", va="bottom", fontsize=9.3, color=color,
            bbox=_annotation_bbox(color, alpha=0.9, pad=0.22, linewidth=0.8),
            zorder=6, clip_on=False)
    return ax


def add_threshold_line(ax, y, label, color=None, linestyle="--", linewidth=1.3):
    color = color or COLORS["crimson"]
    ax.axhline(y=y, color=color, linestyle=linestyle,
               linewidth=linewidth, alpha=0.9, zorder=2)
    ax.annotate(
        label, xy=(0.98, y), xycoords=ax.get_yaxis_transform(),
        xytext=(-4, 6), textcoords="offset points",
        ha="right", va="bottom", fontsize=9.3, color=color,
        bbox=_annotation_bbox(color, alpha=0.9, pad=0.22, linewidth=0.8),
        zorder=6, clip_on=False, annotation_clip=False,
    )
    return ax


def add_phase_span(ax, x_start, x_end, label=None, color=None, alpha=0.08):
    color = color or COLORS["blue_main"]
    ax.axvspan(x_start, x_end, color=color, alpha=alpha, zorder=0)
    if label:
        try:
            cx = x_start + (x_end - x_start) / 2
        except TypeError:
            cx = x_start
        ax.text(cx, 1.06, label, transform=ax.get_xaxis_transform(),
                ha="center", va="bottom", fontsize=9.3, color=color,
                bbox=_annotation_bbox(color, alpha=0.85, pad=0.22, linewidth=0.7),
                zorder=6, clip_on=False)
    return ax


def annotate_extreme(ax, x_values, y_values, mode="max", text=None,
                     color=None, xytext=(18, 18)):
    x_values = np.asarray(x_values)
    y_values = np.asarray(y_values)
    if mode == "max":
        idx = np.nanargmax(y_values)
        default_text = f"最高：{y_values[idx]:.2f}"
        color = color or COLORS["amber"]
    elif mode == "min":
        idx = np.nanargmin(y_values)
        default_text = f"最低：{y_values[idx]:.2f}"
        color = color or COLORS["crimson"]
    else:
        raise ValueError("mode must be 'max' or 'min'")
    annotate_point(ax, x_values[idx], y_values[idx],
                   text or default_text, xytext=xytext, color=color)
    return ax


# ============================================================
# 3-D axis styling
# ============================================================

def style_3d_axis(ax, elev=26, azim=-52):
    _ensure_style()
    ax.view_init(elev=elev, azim=azim)
    ax.set_box_aspect((1.15, 1.0, 0.72))
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1, 1, 1, 0))
        axis.pane.set_edgecolor(COLORS["grid"])
        axis._axinfo["grid"]["color"] = COLORS["grid"]
        axis._axinfo["grid"]["linewidth"] = 0.45
        axis._axinfo["grid"]["linestyle"] = "--"
    ax.tick_params(colors=COLORS["axis"], labelsize=9, pad=2)


# ============================================================
# Finalize / save
# ============================================================

def finalize_plot(fig=None, grid=False, legend_outside=False):
    """Apply axis styles and tight-layout.  Grid defaults to False."""
    _ensure_style()
    fig = fig or plt.gcf()
    axes = fig.get_axes()
    has_3d = any(getattr(ax, "name", "") == "3d" for ax in axes)
    for ax in axes:
        if getattr(ax, "name", "") == "3d":
            style_3d_axis(ax)
        else:
            style_axis(ax, grid=grid, legend_outside=legend_outside)
    if has_3d:
        fig.subplots_adjust(left=0.08, right=0.86, bottom=0.11,
                            top=0.88, wspace=0.32)
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


# ============================================================
# Metadata helpers
# ============================================================

def _json_safe(value):
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, np.ndarray):
        return _json_safe(value.tolist())
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        if math.isnan(float(value)) or math.isinf(float(value)):
            return None
        return float(value)
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    return value


def _numeric_values(data):
    values = []

    def walk(item):
        if item is None:
            values.append(np.nan)
        elif isinstance(item, dict):
            for v in item.values():
                walk(v)
        elif isinstance(item, np.ndarray):
            walk(item.tolist())
        elif isinstance(item, (list, tuple)):
            for v in item:
                walk(v)
        else:
            try:
                values.append(float(item))
            except (TypeError, ValueError):
                pass

    walk(data)
    return values


def _summarize_data(data):
    if not data:
        return {"sample_size": 0, "min": None, "max": None, "missing_values": 0}
    source = data.get("y") if isinstance(data, dict) and "y" in data else data
    values = np.asarray(_numeric_values(source), dtype=float)
    if values.size == 0:
        return {"sample_size": 0, "min": None, "max": None, "missing_values": 0}
    missing = int(np.isnan(values).sum())
    finite = values[np.isfinite(values)]
    return {
        "sample_size": int(values.size),
        "min": float(np.min(finite)) if finite.size else None,
        "max": float(np.max(finite)) if finite.size else None,
        "missing_values": missing,
    }


def _infer_plot_type(stem):
    name = str(stem)
    if name.startswith("plot_"):
        name = name[5:]
    _map = {
        "1": "vector_field", "2": "grouped_scatter", "3": "colored_line",
        "4": "3d_wireframe", "5": "mosaic", "6": "andrews_curve",
        "7": "pareto", "8": "dendrogram", "9": "colored_scatter",
        "10": "3d_surface",
    }
    if name in _map:
        return _map[name]
    return name


def _infer_problem_type(plot_type):
    for key, pt in PROBLEM_TYPE_BY_PLOT.items():
        if key in plot_type:
            return pt
    return "评价类"


def _axis_labels(fig):
    labels = {"x": "", "y": ""}
    axes = fig.get_axes()
    if not axes:
        return labels
    ax = axes[0]
    labels["x"] = ax.get_xlabel()
    labels["y"] = ax.get_ylabel()
    if hasattr(ax, "get_zlabel"):
        labels["z"] = ax.get_zlabel()
    return labels


def _legend_labels(fig):
    labels = []
    for ax in fig.get_axes():
        h, al = ax.get_legend_handles_labels()
        del h
        labels.extend(l for l in al if l and not l.startswith("_"))
    return list(dict.fromkeys(labels))


def build_figure_metadata(stem, fig=None, metadata=None):
    fig = fig or plt.gcf()
    metadata = dict(metadata or {})
    plot_type = metadata.get("plot_type") or _infer_plot_type(stem)
    title = ""
    axes = fig.get_axes()
    if axes:
        title = axes[0].get_title()
    axis_labels = dict(_axis_labels(fig))
    axis_labels.update(metadata.get("axis_labels") or {})
    legend_labels = metadata.get("legend_labels") or _legend_labels(fig)
    caption = metadata.get("caption") or title
    variables = metadata.get("variables") or {k: v for k, v in axis_labels.items() if v}
    modeling_purpose = (
        metadata.get("modeling_purpose")
        or (f"展示{caption}" if caption else "展示建模数据的主要结构和变化特征")
    )
    built = {
        "figure_name": metadata.get("figure_name", str(stem)),
        "plot_type": plot_type,
        "problem_type": metadata.get("problem_type") or _infer_problem_type(plot_type),
        "modeling_purpose": modeling_purpose,
        "variables": variables,
        "axis_labels": axis_labels,
        "legend_labels": legend_labels,
        "caption": caption,
        "usage": metadata.get("usage", "paper"),
        "annotate": bool(metadata.get("annotate", False)),
        "annotation_config": metadata.get("annotation_config"),
        "data_summary": metadata.get("data_summary") or _summarize_data(metadata.get("data")),
    }
    if title:
        built["internal_title"] = title
    if metadata.get("suggested_annotations") is not None:
        built["suggested_annotations"] = metadata["suggested_annotations"]
    return _json_safe(built)


def write_figure_metadata(stem, fig=None, metadata=None):
    output_path = Path(f"{stem}.metadata.json").resolve()
    figure_metadata = build_figure_metadata(stem, fig=fig, metadata=metadata)
    output_path.write_text(
        json.dumps(figure_metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return output_path


def save_current_figure(stem, fig=None, metadata=None, grid=False):
    """Save the current (or given) figure with metadata.  Grid defaults off."""
    _ensure_style()
    fig = fig or plt.gcf()
    finalize_plot(fig, grid=grid)
    output_path = Path(f"{stem}.png").resolve()
    fig.savefig(output_path, dpi=_CONFIG["dpi"], bbox_inches="tight", pad_inches=0.06)
    metadata_path = write_figure_metadata(stem, fig=fig, metadata=metadata)
    plt.close(fig)
    print(f"Saved: {output_path}\nMetadata: {metadata_path}")
    return output_path


def save_figure(fig, path, dpi=None):
    """Simpler save helper for the new API (no metadata sidecar)."""
    _ensure_style()
    dpi = dpi or _CONFIG["dpi"]
    fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=0.06)
