"""示例：雷达图"""
import acadp

labels = ["准确性", "稳定性", "效率", "可解释性", "泛化能力"]
values = [85, 78, 92, 70, 82]

ax = acadp.radar(labels, values, title="模型综合评估雷达图")
print("Done: radar_basic")
