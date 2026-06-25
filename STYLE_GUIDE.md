# 绘图风格与标注使用规范

## 标注使用规范

annotation 是解释性增强，不是装饰，也不是正式图注。它只用于突出关键变化、事件节点、阈值线、极值点和阶段变化；正式图题和图注应放在论文正文或 Word 图片下方。

默认 annotate=False。所有绘图模板默认不自动添加 annotation。

模板可以根据数据返回 suggested_annotations，但不得直接写入图中。只有当用户显式设置 annotate=True，并提供 annotation_config 时，才写入标注。

### 何时使用

只有存在以下情况之一时，才建议使用 annotation：

- 显著极值、异常值或拐点。
- 外部事件节点，例如政策出台、制度调整、试点启动。
- 阈值线、目标线、均值线、警戒线。
- 明显阶段划分或阶段性变化。

### 数量约束

- 论文正文图：正文图标注应克制，建议 0-2 个 annotation，最多不超过 3 个。
- 汇报展示图：建议 2-4 个 annotation。
- 附录探索图：尽量少标注，必要时只保留 1 个关键说明。

一张图只保留 1 个主标注逻辑。不要在同一张图里同时解释极值、阶段、事件、阈值和异常点，除非这些元素共同服务于同一个结论。

### 适用图型

适合使用 annotation 的图型：

- 折线图
- 时间序列图
- 带趋势线的散点图
- 阈值效应图
- 柱状图，且只做少量关键标注

高密度图慎用标注。以下图型应慎用或少用 annotation：

- 热力图
- 散点矩阵
- 聚类树状图
- 雷达图
- 极坐标图
- 3D 图
- 高密度多序列图

### 禁止性约束

annotation 不应用于：

- 重复图例、坐标轴、数据标签已经表达清楚的信息。
- 对每个数据点逐一解释。
- 在高信息密度图中大量堆叠说明框。
- 写缺乏证据支撑的因果性解释。
- 遮挡主要数据、图例或坐标轴标签的位置。

### 保留的通用标注函数

仅保留以下通用 annotation 类型：

- `annotate_point`：关键点标注。
- `annotate_extreme`：最大值/最小值标注。
- `add_event_line`：垂直事件线。
- `add_threshold_line`：水平阈值线。
- `add_phase_span`：阶段背景高亮。

### 模板参数

所有绘图模板应暴露以下参数，并保持默认关闭：

```python
annotate=False
annotation_mode=None
annotation_config=None
auto_annotation=False
```

模板启用 annotation 前，应先通过 `validate_annotation_config()` 校验模式、数量和图型风险。正文图最多 3 个标注，汇报展示图最多 4 个，附录探索图最多 1 个。

### Annotation 自动化边界

所有模板默认 annotate=False，不自动添加 annotation。模板可以根据数据返回 suggested_annotations，但不得直接写入图中。只有当用户显式设置 annotate=True，并提供 annotation_config 时，才写入标注。

如启用 auto_annotation=True，必须先通过 validate_annotation_config() 校验，并遵循：

- paper：最多 3 个；
- presentation：最多 4 个；
- appendix：最多 1 个；
- 3D 图、热力图、散点矩阵、雷达图、极坐标图默认不自动标注。

annotation 只用于解释关键变化，不用于装饰，不用于重复图例、坐标轴或数据标签信息。
