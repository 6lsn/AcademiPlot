"""示例：直方图"""
import numpy as np
import acadp

np.random.seed(42)
data = np.random.normal(100, 15, 200)

ax = acadp.histogram(data, title="测量值频率分布",
                     xlabel="测量值", ylabel="频数")
print("Done: histogram_basic")
