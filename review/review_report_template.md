# 绘图审查报告

- 总图数：{{total}}
- 通过：{{pass}}
- 需修改：{{revise}}
- 人工复核：{{manual_review}}
- 建议重画：{{reject}}

## 逐图审查

{{items}}

## 分流规则

- `pass`：可进入 `final_figures/`
- `revise`：进入待返工队列；开启 `--auto-revise` 后仅执行低风险 metadata 修复并复审
- `manual_review`：进入 `manual_review/`
- `reject`：建议换图型或重画

## 自动返工边界

自动返工只处理图注缺失、坐标轴/变量字段补全、annotation 数量超限和慎用图型 annotation 关闭。图型选择、变量含义、数据口径、因果解释和重画建议必须人工确认。
