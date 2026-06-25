# 标注规则

annotation 是解释性增强，不是装饰，也不是正式图注。正文图标注应克制，高密度图慎用标注，一张图只保留 1 个主标注逻辑。

## 启用边界

- 默认 annotate=False。
- 模板可以根据数据返回 suggested_annotations，但不得直接写入图中。
- 只有当用户显式设置 annotate=True，并提供 annotation_config 时，才写入标注。
- 如启用 auto_annotation=True，只能作为建议生成流程，必须先通过 `validate_annotation_config()` 校验。
- 3D 图、热力图、散点矩阵、雷达图、极坐标图默认不自动标注。

## 数量限制

- 正文图建议 0-2 个 annotation，最多不超过 3 个。
- 汇报展示图建议 2-4 个。
- 附录探索图尽量少标注，必要时只保留 1 个关键说明。
- 一张图建议只添加 1-3 个关键标注，避免遮挡主体数据或造成论文图过度解释。

## 适用与慎用

适合折线图、时间序列图、带趋势线散点图、阈值效应图和少量柱状图。热力图、散点矩阵、聚类树状图、雷达图、极坐标图、3D 图和高密度多序列图慎用。

不得逐点解释，不得重复图例、坐标轴或数据标签已经表达的信息，不得写缺乏证据支撑的因果性解释。

## 共享 helper

| 函数 | 用途 |
|---|---|
| `annotate_point(ax, x, y, text, xytext=(18, 18), color=None)` | 标注关键点、拐点、异常点、最高点、最低点 |
| `add_event_line(ax, x, label, color=None)` | 添加垂直事件线，例如政策出台、试点启动、阶段分界 |
| `add_threshold_line(ax, y, label, color=None)` | 添加水平阈值线、目标线、均值线、警戒线 |
| `add_phase_span(ax, x_start, x_end, label=None, color=None, alpha=0.08)` | 添加阶段背景高亮，例如快速增长期、调整期、政策强化期 |
| `annotate_extreme(ax, x_values, y_values, mode="max", text=None)` | 自动标注最大值或最小值 |

标注颜色必须来自 `COLORS`，文字框使用白色半透明圆角框，箭头颜色与标注颜色一致。
