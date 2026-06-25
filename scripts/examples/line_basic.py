"""示例：基础折线图"""
import numpy as np
import acadp

np.random.seed(42)
x = np.linspace(0, 12, 100)
y = np.sin(x) * 10 + 50 + np.random.randn(100) * 2

ax = acadp.lineplot(x=x, y=y, title="单指标时间变化趋势",
                    xlabel="时间", ylabel="数值")
print("Done: line_basic")
