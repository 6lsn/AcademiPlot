"""示例：相关性热力图"""
import numpy as np
import pandas as pd
import acadp

np.random.seed(42)
df = pd.DataFrame(np.random.randn(100, 5),
                  columns=["指标A", "指标B", "指标C", "指标D", "指标E"])

ax = acadp.heatmap(df.corr(), labels=list(df.columns), title="指标相关性矩阵")
print("Done: heatmap_corr")
