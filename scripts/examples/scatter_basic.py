"""示例：基础散点图"""
import numpy as np
import acadp

np.random.seed(42)
x = np.random.randn(100) * 10
y = 2 * x + np.random.randn(100) * 15 + 50

ax = acadp.scatter(x=x, y=y, title="双变量线性关系散点分布",
                   xlabel="X轴数据", ylabel="Y轴数据")
print("Done: scatter_basic")
