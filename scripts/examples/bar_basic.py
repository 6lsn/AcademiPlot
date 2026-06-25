"""示例：基础柱状图"""
import acadp

categories = ["方案A", "方案B", "方案C", "方案D", "方案E"]
values = [85, 72, 91, 68, 78]

ax = acadp.barplot(x=categories, y=values, title="各方案得分对比",
                   xlabel="方案", ylabel="得分", highlight="max")
print("Done: bar_basic")
