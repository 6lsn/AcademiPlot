---
name: "plotting"
description: |
  数学建模竞赛论文图表策划、绘制与审查 Skill。Use when 需要画图、绘图、可视化、plot、chart、选图、重绘论文图、生成 PNG 图表、审查图表质量，尤其是 CUMCM/MCM 建模论文中的评价、预测、优化、聚类、工程空间和统计图。
---

# 数学建模绘图 Skill

核心原则：先判断图在论文中的论证角色，再选择表达范式；正文主图不要机械套模板换数据。普通附录图可直接用模板，关键结论图优先设计为更能说明模型机制的复合图、对比图或优化图。

## 快速流程

1. 明确图的用途：数据概览、模型过程、结果对比、敏感性、约束达标、优化寻优或论文主结论。
2. 需要选图时读取 `references/chart_lookup.md`，按赛题类型和变量结构选择候选图。
3. 需要论文主图时先考虑高级表达：阈值达标用 bullet，双方案差异用 dumbbell，参数寻优用 contour，成本拆解用 waterfall，敏感性用 small multiples/tornado，供需匹配用供需堆叠加净差。
4. 调用对应模板函数，优先传入 DataFrame 或数组数据；若模板不足以表达论文目的，复制到项目目录写适配脚本。
5. 不要直接修改模板源码；项目定制图应保留同名输出、清晰变量、坐标轴、图例和图注。
6. 保存必须通过 `scripts/style.py` 的 `save_current_figure()` 或等价 metadata 流程，输出 PNG 和 `.metadata.json`。
7. 批量完成后运行 `review/chart_reviewer.py`；审图未通过时先改图型、变量语义、caption 或布局，再复审。

## 按需加载

- `references/chart_lookup.md`：完整图表速查表，含赛题类型到脚本函数、图表名称到适用场景。
- `references/recipe_index.yaml`：高级图 recipe 索引，供 planner 按论文角色选择表达范式。
- `references/style_metadata.md`：论文风格、保存规范、metadata 字段和批量审图命令。
- `references/annotation_rules.md`：标注边界、helper 函数和正文/附录标注数量规则。
- `review/chart_review_rules.md`：AI 审图规则，含图型适配、正文/附录分流和慎用图型。
- `STYLE_GUIDE.md`：更细的模板编码风格和 annotation 约束。
- `scripts/data_profiler.py`：为 CSV、Excel、DataFrame 生成字段摘要和建模语义提示，供 planner 选图使用。
- `scripts/chart_planner.py`：读取任务 JSON/YAML 和 recipe 索引，输出高级图 JSON/YAML spec。
- `scripts/render_from_spec.py`：读取高级图 spec，渲染 PNG，并同步生成 `.metadata.json`。
- `recipes/`：高级图表达范式定义；`scripts/` 里的 `plot_*.py` 是可直接运行或复制改造的绘图模板。

## 高级图优先映射

| 论文意图 | 优先表达 |
|---|---|
| 约束/指标是否达标 | bullet chart、阈值水平线、达标状态色 |
| 两方案成本或效果差异 | dumbbell、lollipop、带节约率标签 |
| 供需、库存、电力平衡 | stacked area + demand line + net balance |
| 参数寻优 | contour/heatmap + optimum path |
| 多因素敏感性 | small multiples、tornado、标准化斜率 |
| 成本构成和边际变化 | stacked bar + total line、waterfall |
| 多目标权衡 | Pareto frontier、效率前沿 |

## 必守规则

- 坐标轴、单位、图例、caption 必须能独立解释图。
- 图内标题只写业务主题，不写“图 1”“柱状图”这类类型名。
- annotation 默认关闭；需要标注时先读 `references/annotation_rules.md`。
- 3D、雷达、饼图、散点矩阵慎用于正文；除非确实比二维表达更有信息价值。
- 审图器只是底线；肉眼还要查遮挡、裁切、图例压字、空白过多和颜色语义冲突。
