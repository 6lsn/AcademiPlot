"""示例：堆积柱状图"""
import acadp

categories = ["Q1", "Q2", "Q3", "Q4"]
components = {
    "产品A": [30, 35, 40, 38],
    "产品B": [20, 25, 22, 28],
    "产品C": [15, 18, 20, 22],
}

ax = acadp.stacked_bar(categories, components, title="季度销售构成",
                       xlabel="季度", ylabel="销售额 (万元)")
print("Done: stacked_bar_basic")
