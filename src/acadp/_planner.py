"""Chart planner — maps data profile + task description to best chart type."""

_TASK_KEYWORDS = {
    "lineplot": ["趋势", "变化", "时间", "增长", "下降", "走势", "trend", "time"],
    "barplot": ["对比", "比较", "各方案", "排名", "得分", "评分", "compare", "ranking"],
    "scatter": ["相关", "关系", "散点", "回归", "关联", "correlation", "scatter"],
    "heatmap": ["相关性", "相关矩阵", "热力", "矩阵", "correlation matrix"],
    "boxplot": ["分布", "箱线", "离散程度", "异常值", "distribution", "boxplot"],
    "violinplot": ["分布", "密度", "小提琴", "violin", "density"],
    "histogram": ["频率", "分布", "直方", "分组统计", "histogram", "frequency"],
    "radar": ["雷达", "综合评估", "多维", "多指标", "radar", "spider"],
    "area": ["面积", "堆积", "累计", "供需", "area", "stacked area"],
    "stacked_bar": ["堆积", "构成", "结构", "占比", "stacked", "composition"],
}


def choose_chart(profile, task):
    """Choose best chart type based on data profile and task description.

    Args:
        profile: dict from profile_data() with columns, semantic_hints, plotting_hints
        task: str describing what the user wants to show

    Returns:
        str: chart function name (e.g., "lineplot", "barplot")
    """
    task_lower = task.lower()
    scores = {}
    for chart, keywords in _TASK_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in task_lower)
        if score:
            scores[chart] = score

    # Boost based on data shape
    hints = profile.get("plotting_hints", {})
    if hints.get("has_categories") and "barplot" in scores:
        scores["barplot"] += 2
    if hints.get("has_time_axis") and "lineplot" in scores:
        scores["lineplot"] += 2
    if hints.get("has_costs") and "barplot" in scores:
        scores["barplot"] += 1

    if not scores:
        # Default fallback based on data shape
        if hints.get("has_categories"):
            return "barplot"
        if hints.get("has_time_axis"):
            return "lineplot"
        cols = profile.get("columns", {})
        numeric_count = sum(
            1 for c in cols.values()
            if c.get("semantic_type") in ("numeric", "cost", "ratio")
        )
        if numeric_count >= 3:
            return "heatmap"
        return "lineplot"

    return max(scores, key=scores.get)
