# 图表速查表

用于按赛题类型或图表名称选择模板脚本。若是论文关键结论图，先用 `SKILL.md` 的高级图优先映射判断是否应改成复合表达。

## 按赛题类型反查

### 评价类问题

| 场景 | 脚本函数 |
|---|---|
| 多方案指标对比 | `plot_grouped_bar` |
| 多维度综合评估（≥4维） | `plot_radar` |
| 整体与部分比例 | `plot_stacked_bar` / `plot_percentage_stacked_bar` |
| 比例展示 | `plot_piechart` / `plot_donut` |
| 数据分布对比 | `plot_boxplot` / `plot_violinplot` |
| 带误差对比 | `plot_line_with_error` / `plot_horizontal_errorbar` |
| 多组多类别对比 | `plot_scatter_grouped` / `plot_grouped_boxplot` |
| 变量相关性 | `plot_corr_heat` / `plot_scatter_basic` |
| 多变量关系 | `plot_matrix_scatter` / `plot9` |
| 多组趋势对比 | `plot_line_multi_series` |
| 类别数据对比 | `plot_bar_basic` / `plot_bar_horizontal` |
| 精确数值对比 | `plot_bar_with_labels` / `plot_dotplot` |
| 不同尺度变量对比 | `plot_double_y_axis` |
| 变化范围分析 | `plot_filled_line_chart` |
| 因素重要性 | `plot7` |
| 多维度对比 | `plot_3d_bar_chart` |
| 特征区分 | `plot3` |
| 多因素关系 | `plot_3d_scatter` |
| 多变量联合分布 | `plot5` / `plot6` |

### 预测类问题

| 场景 | 脚本函数 |
|---|---|
| 时间序列预测 | `plot_time_series` / `plot_line_basic` |
| 趋势走向 | `plot_scatter_with_trend` |
| 周期性数据 | `plot_polar_line` |
| 多因素趋势 | `plot_line_multi_series` |
| 累积趋势 | `plot_area` |
| 趋势对比 | `plot_filled_line_chart` |
| 变量关系探索 | `plot_scatter_basic` / `plot_bubble` |
| 多变量关系 | `plot_3d_scatter` / `plot_matrix_scatter` |
| 含误差预测 | `plot_line_with_error` |
| 复杂关系建模 | `plot_3d_surface` / `plot10` |
| 数据分布预测 | `plot_contour` |
| 三维数据分布 | `plot_3d_contour` |
| 数据特征分析 | `plot_histogram` / `plot_kde` / `plot_histogram_with_kde` |

### 优化类问题

| 场景 | 脚本函数 |
|---|---|
| 方案对比 | `plot_bar_basic` / `plot_grouped_bar` |
| 过程分析 | `plot_line_basic` / `plot_step_line` |
| 资源分配 | `plot_stacked_bar` / `plot_stacked_area` |
| 最优曲面 | `plot_3d_surface` / `plot10` |
| 极值区域 | `plot_contour` / `plot_3d_contour` |
| 过程分析（瀑布） | `plot_waterfall` |
| 关键因素 | `plot7` |
| 资源累积 | `plot_area` |
| 变量规律 | `plot_scatter_with_trend` |

### 聚类/分类问题

| 场景 | 脚本函数 |
|---|---|
| 聚类展示 | `plot_scatter_grouped` / `plot_3d_scatter` |
| 类别对比 | `plot_dotplot` / `plot_bar_basic` |
| 层次结构 | `plot8` |
| 多组对比 | `plot2` |

### 物理/工程/空间问题

| 场景 | 脚本函数 |
|---|---|
| 矢量可视化 | `plot1` |
| 三维结构 | `plot4` |
| 空间分布 | `plot_3d_surface` / `plot_contour` |
| 空间分析 | `plot_3d_contour` |

### 数据处理/统计

| 场景 | 脚本函数 |
|---|---|
| 异常值检测 | `plot_boxplot` / `plot_grouped_boxplot` |
| 数据分布 | `plot_histogram` / `plot_kde` |
| 综合分析 | `plot_histogram_with_kde` / `plot_violinplot` |
| 可靠性评估 | `plot_line_with_error` / `plot_horizontal_errorbar` |

## 按图表名称快查

| 图表名称 | 函数 | 适用赛题 |
|---|---|---|
| 基础散点图 | `plot_scatter_basic` | 评价类、预测类 |
| 带趋势线散点图 | `plot_scatter_with_trend` | 预测类、优化类、拟合 |
| 分组散点图 | `plot_scatter_grouped` | 评价类、聚类 |
| 气泡图 | `plot_bubble` | 评价类、预测类 |
| 基础折线图 | `plot_line_basic` | 预测类、优化类、拟合 |
| 多系列折线图 | `plot_line_multi_series` | 评价类、预测类 |
| 带误差线折线图 | `plot_line_with_error` | 评价类、预测类、拟合 |
| 阶梯折线图 | `plot_step_line` | 优化类、预测类 |
| 基础柱状图 | `plot_bar_basic` | 评价类、优化类 |
| 水平柱状图 | `plot_bar_horizontal` | 评价类 |
| 分组柱状图 | `plot_grouped_bar` | 评价类 |
| 堆叠柱状图 | `plot_stacked_bar` | 评价类、优化类 |
| 百分比堆叠柱状图 | `plot_percentage_stacked_bar` | 评价类 |
| 直方图 | `plot_histogram` | 评价类、预测类 |
| 核密度图 | `plot_kde` | 评价类 |
| 直方图+核密度 | `plot_histogram_with_kde` | 评价类 |
| 箱线图 | `plot_boxplot` | 评价类、预测类、异常值 |
| 小提琴图 | `plot_violinplot` | 评价类 |
| 点图 | `plot_dotplot` | 评价类、聚类 |
| 基础饼图 | `plot_piechart` | 评价类 |
| 环形图 | `plot_donut` | 评价类 |
| 雷达图 | `plot_radar` | 评价类 |
| 热图 | `plot_heat` | 评价类、相关性 |
| 相关性热图 | `plot_corr_heat` | 评价类 |
| 3D散点图 | `plot_3d_scatter` | 预测类、评价类、聚类 |
| 3D曲面图 | `plot_3d_surface` | 预测类、优化类 |
| 等高线图 | `plot_contour` | 预测类、优化类 |
| 瀑布图 | `plot_waterfall` | 优化类、评价类 |
| 面积图 | `plot_area` | 预测类、优化类 |
| 时间序列图 | `plot_time_series` | 预测类 |
| 双Y轴折线图 | `plot_double_y_axis` | 评价类、预测类 |
| 带填充区域折线图 | `plot_filled_line_chart` | 预测类、评价类 |
| 分组箱线图 | `plot_grouped_boxplot` | 评价类、异常值 |
| 3D柱状图 | `plot_3d_bar_chart` | 评价类 |
| 3D等高线图 | `plot_3d_contour` | 预测类、优化类、空间 |
| 误差棒图（横向） | `plot_horizontal_errorbar` | 评价类 |
| 矩阵散点图 | `plot_matrix_scatter` | 评价类、预测类 |
| 堆叠面积图 | `plot_stacked_area` | 评价类、优化类 |
| 带数据标签柱状图 | `plot_bar_with_labels` | 评价类 |
| 极坐标折线图 | `plot_polar_line` | 预测类 |
| 矢量场图 | `plot1` | 物理工程类 |
| 分组点图 | `plot2` | 评价类 |
| 彩色映射折线图 | `plot3` | 评价类 |
| 3D网格图 | `plot4` | 空间分析类 |
| 马赛克图 | `plot5` | 评价类 |
| Andrews曲线 | `plot6` | 评价类 |
| 帕累托图 | `plot7` | 优化类、评价类 |
| 树状图 | `plot8` | 分类分析类 |
| 彩色散点图 | `plot9` | 评价类 |
| 3D曲面(带光照) | `plot10` | 预测类、优化类 |
