"""Auto-reviser -- applies safe metadata fixes after review."""


def revise_metadata(metadata, review_result):
    """Apply low-risk fixes to metadata based on review feedback.

    Only fixes:
    - Missing caption -> use suggested_caption from review
    - Missing variables -> infer from axis_labels
    - Annotation count too high -> reduce to limit
    - Annotations on caution chart types -> disable

    Does NOT change: data, chart type, variable meanings, causal explanations.

    Returns: (revised_metadata, changes_list)
    """
    changes = []
    meta = dict(metadata)

    # Fix missing caption
    if not meta.get("caption") and review_result.suggested_caption:
        meta["caption"] = review_result.suggested_caption
        changes.append("added missing caption")

    # Fix missing variables from axis labels
    if not meta.get("variables") and meta.get("axis_labels"):
        meta["variables"] = {k: v for k, v in meta["axis_labels"].items() if v}
        if meta["variables"]:
            changes.append("inferred variables from axis_labels")

    # Trim annotation count
    from acadp._style import ANNOTATION_LIMITS, ANNOTATION_CAUTION_CHARTS

    usage = meta.get("usage", "paper")
    limit = ANNOTATION_LIMITS.get(usage, 3)
    config = meta.get("annotation_config") or {}
    count = config.get("count", 0) if isinstance(config, dict) else 0
    if count > limit:
        meta["annotation_config"] = {"count": limit}
        changes.append(f"trimmed annotation count from {count} to {limit}")

    # Disable annotations on caution chart types
    plot_type = meta.get("plot_type", "")
    if any(ct in plot_type for ct in ANNOTATION_CAUTION_CHARTS):
        if meta.get("annotate"):
            meta["annotate"] = False
            meta["annotation_config"] = None
            changes.append(f"disabled annotations on caution chart type: {plot_type}")

    return meta, changes
