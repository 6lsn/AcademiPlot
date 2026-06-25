# 风格、保存与审图闭环

## 统一论文风格

所有脚本共用 `scripts/style.py`：

- 字体：`Microsoft YaHei` / `SimHei`，衬线备用 `Times New Roman`。
- DPI：`figure.dpi = 120`，`savefig.dpi = 300`。
- 保存：统一调用 `save_current_figure()`，使用 `bbox_inches="tight"`、`pad_inches=0.06`。
- 图内标题：通过 `set_chart_title(ax, "...")` 写具体业务主题名，不写“图1”或单纯图表类型名。
- 坐标轴：保留轴标签、刻度、必要统计标注、浅灰虚线网格，隐藏顶部/右侧 spine。
- 图例：默认无边框，优先放图内右上角；多系列图可放顶部横排，不默认放右侧外部。
- 3D 图：固定视角，降低网格干扰，必要时增加色条和 2D 等高线投影。

## 保存与 metadata

每张图保存时同步生成同名 `.metadata.json`。字段至少包括：

- `figure_name`
- `plot_type`
- `problem_type`
- `modeling_purpose`
- `variables`
- `axis_labels`
- `legend_labels`
- `caption`
- `usage`
- `annotate`
- `annotation_config`
- `data_summary`

如果复制模板到项目目录定制，仍应复用 `style.py` 或写等价的 `save_chart()` 包装函数，显式传入 `plot_type`、`problem_type`、变量含义和图注，避免审图器把路径误判为图型。

## 批量审图

审图模块位于 `review/`：

| 文件 | 用途 |
|---|---|
| `chart_review_rules.md` | 建模主题、图型选择、正文/附录适配和慎用规则 |
| `chart_reviewer.py` | 读取 metadata，输出结构化审图 JSON 和 Markdown 报告 |
| `chart_auto_reviser.py` | 根据审图结果执行安全返工，输出 `revision_plan.json` 并复审 |
| `review_schema.json` | 单图审图结果 schema |
| `review_report_template.md` | 批量审图报告模板 |

常用命令：

```bash
python run_all_examples.py --output-dir example_outputs --review
python run_all_examples.py --output-dir example_outputs --review --auto-revise --max-revision-rounds 2
python review/chart_reviewer.py --metadata-dir path/to/images --output-dir path/to/review_output
```

自动返工只处理低风险 metadata 问题：补图注、补坐标轴/变量字段、裁剪 annotation 数量、关闭慎用图型 annotation。它不会自动改数据、改变量含义、强行换图型或写因果解释。
