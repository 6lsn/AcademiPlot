"""Auto-reviser — applies safe metadata fixes after review.

Only applies low-risk fixes. Returns (revised_metadata, changes, blocked).
Blocked items require human review and are NOT auto-fixed.
"""


UNSAFE_REVIEW_MARKERS = (
    "不匹配",
    "不宜使用饼图",
    "缺乏证据支撑的因果性解释",
)

ANNOTATION_CAUTION_NAMES = {
    "3d", "3d_surface", "3d_scatter", "3d_contour",
    "heat", "heatmap", "corr_heat", "matrix_scatter",
    "scatter_matrix", "radar", "polar",
}

USAGE_ANNOTATION_LIMITS = {
    "paper": 3,
    "presentation": 4,
    "appendix": 1,
}


def _has_unsafe_issue(review_result):
    """Check if review has issues that require human judgment."""
    issues = review_result.major_issues + review_result.minor_issues
    return any(marker in issue for issue in issues for marker in UNSAFE_REVIEW_MARKERS)


def revise_metadata(metadata, review_result):
    """Apply low-risk fixes to metadata based on review feedback.

    Only fixes:
    - Missing caption -> use suggested_caption from review
    - Missing variables -> infer from axis_labels
    - Missing axis_labels -> infer from variables
    - Annotations on caution chart types -> disable
    - Annotation count too high -> reduce to limit

    Does NOT change: data, chart type, variable meanings, causal explanations.

    Returns: (revised_metadata, changes_list, blocked_list)
    """
    changes = []
    blocked = []
    meta = dict(metadata)

    # Safety check — do not auto-fix chart selection or causal issues
    if _has_unsafe_issue(review_result):
        blocked.append("涉及图型选择、建模含义或因果解释，需人工复核")
        return meta, changes, blocked

    # 1. Fix missing caption
    if not meta.get("caption") and review_result.suggested_caption:
        meta["caption"] = review_result.suggested_caption
        changes.append("补全缺失图注")

    # 2. Infer variables from axis_labels
    axis_labels = meta.get("axis_labels") or {}
    if not meta.get("variables") and axis_labels:
        inferred = {k: v for k, v in axis_labels.items() if v}
        if inferred:
            meta["variables"] = inferred
            changes.append("根据坐标轴标签补全变量含义")

    # 3. Infer axis_labels from variables
    variables = meta.get("variables") or {}
    axis_labels = dict(meta.get("axis_labels") or {})
    updated = False
    for key in ("x", "y", "z"):
        if not axis_labels.get(key) and variables.get(key):
            axis_labels[key] = variables[key]
            updated = True
    if updated:
        meta["axis_labels"] = axis_labels
        changes.append("根据变量含义补全坐标轴标签")

    # 4. Disable annotations on caution chart types
    plot_type = str(meta.get("plot_type", "")).lower()
    if any(ct in plot_type for ct in ANNOTATION_CAUTION_NAMES):
        if meta.get("annotate"):
            meta["annotate"] = False
            meta["annotation_config"] = None
            changes.append("关闭慎用图型的 annotation")

    # 5. Trim annotation count
    if meta.get("annotate"):
        usage = meta.get("usage", "paper")
        limit = USAGE_ANNOTATION_LIMITS.get(usage, 3)
        config = meta.get("annotation_config") or {}
        count = config.get("count", 0) if isinstance(config, dict) else 0
        if count > limit:
            new_config = {k: v for k, v in config.items() if k != "count"}
            new_config["count"] = limit
            meta["annotation_config"] = new_config
            changes.append(f"将 annotation 数量从 {count} 限制到 {limit}")

    return meta, changes, blocked
