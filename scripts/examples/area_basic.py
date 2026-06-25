"""示例：面积图"""
import acadp

x = list(range(1, 13))
y_dict = {
    "风电": [45, 42, 50, 55, 60, 58, 62, 65, 55, 48, 44, 46],
    "光伏": [20, 25, 35, 45, 55, 60, 58, 50, 40, 30, 22, 18],
}

ax = acadp.area(x, y_dict, title="月度发电量变化",
                xlabel="月份", ylabel="发电量 (MWh)")
print("Done: area_basic")
