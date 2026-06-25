"""示例：小提琴图"""
import numpy as np
import pandas as pd
import acadp

np.random.seed(42)
df = pd.DataFrame({
    "组别": (["对照组"] * 50 + ["实验组"] * 50),
    "测量值": np.concatenate([
        np.random.normal(100, 15, 50),
        np.random.normal(110, 12, 50),
    ]),
})

ax = acadp.violinplot(df, x="组别", y="测量值",
                      title="对照组与实验组测量值分布")
print("Done: violinplot_basic")
