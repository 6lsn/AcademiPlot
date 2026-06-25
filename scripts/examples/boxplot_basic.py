"""示例：箱线图"""
import numpy as np
import pandas as pd
import acadp

np.random.seed(42)
df = pd.DataFrame({
    "方案": (["方案A"] * 30 + ["方案B"] * 30 + ["方案C"] * 30),
    "得分": np.concatenate([
        np.random.normal(80, 5, 30),
        np.random.normal(75, 8, 30),
        np.random.normal(85, 4, 30),
    ]),
})

ax = acadp.boxplot(df, x="方案", y="得分", title="各方案得分分布")
print("Done: boxplot_basic")
