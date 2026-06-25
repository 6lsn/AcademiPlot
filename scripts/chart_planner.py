import argparse
import json
import sys
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from utf8_io import configure_utf8_stdio


configure_utf8_stdio()

SKILL_ROOT = Path(__file__).resolve().parents[1]
RECIPE_INDEX = SKILL_ROOT / "references" / "recipe_index.yaml"
ROLE_KEYWORDS = {
    "constraint_compliance": ["达标", "要求阈值", "要求值", "约束", "合规", "是否满足"],
    "threshold_comparison": ["阈值", "标准值", "目标线", "警戒线"],
    "indicator_evaluation": ["绿电直连指标", "评价指标", "指标比例", "指标值"],
    "parameter_optimization": ["优化关系", "寻优", "最优", "最优容量", "最优点", "最优容量轨迹", "等高线"],
    "surface_search": ["等高线", "响应面", "网格", "曲面"],
    "paired_scheme_comparison": ["离散模式", "连续模式", "双方案", "两种方案", "基准方案", "对比方案", "成本节约"],
    "before_after_comparison": ["改造前", "改造后", "前后对比"],
    "two_series_gap": ["节约比例", "节约率", "差距", "差异", "差值"],
    "system_balance": ["供需匹配", "供需差", "净供需差", "净差", "负荷", "出力", "匹配关系"],
    "supply_demand_matching": ["供给", "需求", "用电负荷", "新能源出力"],
    "power_balance": ["电力平衡", "基础电负荷", "总用电负荷", "光伏出力", "风电出力"],
    "multi_factor_sensitivity": ["敏感性", "多因素", "影响幅度", "参数水平"],
    "parameter_sensitivity": ["参数扰动", "参数水平", "储能单位成本", "电价倍率"],
    "scenario_sensitivity": ["场景", "情景"],
    "cost_decomposition": ["成本构成", "成本结构", "构成关系", "购电成本", "运维成本", "设备折旧"],
    "incremental_change": ["增量", "边际", "变化分解"],
    "contribution_breakdown": ["贡献", "拆解", "分解"],
    "composition_comparison": ["天数占比", "结构关系", "达标结构", "占比", "构成比例"],
    "share_structure": ["结构", "份额", "完全满足", "部分满足", "不满足"],
    "annual_status_structure": ["年度", "年化", "年际"],
    "multi_objective_tradeoff": ["日产氨量", "吨氨成本", "成本的对比关系", "运行模式", "多目标", "权衡"],
    "pareto_frontier": ["帕累托", "效率前沿", "非支配"],
    "efficiency_frontier": ["效率前沿", "最优前沿"],
}


def read_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def read_task(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    return json.loads(text)


def load_recipe_index(index_path=RECIPE_INDEX):
    data = read_yaml(index_path)
    if not isinstance(data, dict) or "recipes" not in data:
        raise ValueError(f"Invalid recipe index: {index_path}")
    return data


def load_recipe(recipe_id, root=SKILL_ROOT):
    path = root / "recipes" / f"{recipe_id}.yaml"
    recipe = read_yaml(path)
    if not isinstance(recipe, dict) or recipe.get("id") != recipe_id:
        raise ValueError(f"Invalid recipe file: {path}")
    return recipe


def load_recipe_catalog(root=SKILL_ROOT):
    index = load_recipe_index(root / "references" / "recipe_index.yaml")
    recipes = {}
    for entry in index["recipes"]:
        recipes[entry["id"]] = load_recipe(entry["id"], root=root)
    return index, recipes


def _as_set(value):
    if value is None:
        return set()
    if isinstance(value, dict):
        return set(value.keys())
    if isinstance(value, (list, tuple, set)):
        return set(value)
    return {value}


def _semantic_keys(task):
    semantics = task.get("data_semantics") or {}
    keys = set(semantics)
    for key, value in semantics.items():
        if isinstance(value, dict):
            keys.update(value)
        elif isinstance(value, list) and key == "supply_components":
            keys.add("supply_components")
    return keys


def _flatten_text(value):
    if value is None:
        return ""
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            parts.extend([str(key), _flatten_text(item)])
        return " ".join(parts)
    if isinstance(value, (list, tuple, set)):
        return " ".join(_flatten_text(item) for item in value)
    return str(value)


def infer_role_scores(task):
    explicit_role = task.get("figure_role")
    if explicit_role:
        return {explicit_role: 10}

    # ★ 修复1：也检查 role_keywords 字段（直接映射）
    role_keywords_field = task.get("role_keywords") or []
    if isinstance(role_keywords_field, str):
        role_keywords_field = [role_keywords_field]
    direct_scores = {rk: 10 for rk in role_keywords_field}
    if direct_scores:
        return direct_scores

    # ★ 修复2：扩大检测字段，加入 description / task / context
    text = " ".join(
        _flatten_text(task.get(key))
        for key in [
            "figure_id",
            "purpose",
            "caption",
            "description",
            "task",
            "context",
            "data_semantics",
            "variables",
            "axis_labels",
            "legend_labels",
        ]
    ).lower()
    scores = {}
    for role, keywords in ROLE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword.lower() in text)
        if score:
            scores[role] = score
    return scores


def score_recipe(task, index_entry, recipe):
    score = 0
    reasons = []
    problem_type = task.get("problem_type", "")
    semantic_keys = _semantic_keys(task)
    role_scores = infer_role_scores(task)
    allowed_roles = set(index_entry.get("trigger_roles", []))
    allowed_roles.add(recipe.get("figure_role"))

    explicit_role = task.get("figure_role", "")
    if explicit_role and explicit_role in index_entry.get("trigger_roles", []):
        score += 100
        reasons.append(f"matched figure_role={explicit_role}")
    elif explicit_role and explicit_role == recipe.get("figure_role"):
        score += 90
        reasons.append(f"matched canonical figure_role={explicit_role}")
    elif not explicit_role:
        matched_roles = {
            role: role_scores[role]
            for role in allowed_roles
            if role in role_scores
        }
        if matched_roles:
            role_score = max(matched_roles.values())
            score += min(110, role_score * 35 + (len(matched_roles) - 1) * 10)
            reasons.append(
                "inferred figure_role="
                + ",".join(f"{role}:{weight}" for role, weight in sorted(matched_roles.items()))
            )

    if problem_type in recipe.get("problem_types", []):
        score += 20
        reasons.append(f"matched problem_type={problem_type}")

    required_keys = set((recipe.get("required_semantics") or {}).keys())
    matched_required = required_keys & semantic_keys
    score += len(matched_required) * 4
    if required_keys and matched_required == required_keys:
        score += 20
        reasons.append("all required semantics present")
    elif matched_required:
        reasons.append("partial required semantics present")

    available_templates = _as_set(task.get("available_templates"))
    avoid_templates = set((recipe.get("planner_rules") or {}).get("avoid_templates") or [])
    if available_templates & avoid_templates:
        score += 8
        reasons.append("weak templates detected in available_templates")

    return score, reasons


def choose_recipe(task, root=SKILL_ROOT):
    index, recipes = load_recipe_catalog(root=root)
    scored = []
    for entry in index["recipes"]:
        recipe = recipes[entry["id"]]
        score, reasons = score_recipe(task, entry, recipe)
        scored.append((score, entry, recipe, reasons))
    scored.sort(key=lambda item: item[0], reverse=True)
    best_score, best_entry, best_recipe, reasons = scored[0]
    if best_score <= 0:
        # ★ 修复3：不崩溃，降级返回 None，由上游做兜底
        return None, None, {"score": 0, "reasons": ["未匹配到高级 recipe，建议使用基础模板"]}
    return best_entry, best_recipe, {"score": best_score, "reasons": reasons}


def _axis_labels(recipe, task):
    semantics = task.get("data_semantics") or {}
    defaults = (recipe.get("metadata_defaults") or {}).get("variables") or {}
    labels = {}
    for axis in ["x", "y", "z"]:
        if axis in semantics and isinstance(semantics[axis], str):
            labels[axis] = semantics[axis]
        elif axis in defaults:
            labels[axis] = defaults[axis]
    if not labels:
        labels = {key: value for key, value in defaults.items() if key in {"x", "y", "z"}}
    return labels


def _caption(recipe, task):
    explicit = task.get("caption")
    if explicit:
        return explicit
    return (recipe.get("metadata_defaults") or {}).get("caption_pattern", "")


def _variables(recipe):
    return dict((recipe.get("metadata_defaults") or {}).get("variables") or {})


def _filtered_fallbacks(recipe):
    output = recipe.get("output") or {}
    fallbacks = list(output.get("fallback_templates") or [])
    avoid = set((recipe.get("planner_rules") or {}).get("avoid_templates") or [])
    return [item for item in fallbacks if item not in avoid]


def build_spec(task, index_entry, recipe, trace):
    output = recipe.get("output") or {}
    figure_id = task.get("figure_id", "planned_figure")
    problem_type = task.get("problem_type") or (recipe.get("problem_types") or ["评价类"])[0]
    plot_type = output.get("plot_type")
    usage = output.get("usage", "paper")
    modeling_purpose = task.get("purpose") or f"使用 {recipe['name']} 表达建模结果。"

    metadata = {
        "figure_name": figure_id,
        "plot_type": plot_type,
        "problem_type": problem_type,
        "modeling_purpose": modeling_purpose,
        "variables": _variables(recipe),
        "axis_labels": _axis_labels(recipe, task),
        "legend_labels": [],
        "caption": _caption(recipe, task),
        "usage": usage,
        "annotate": False,
        "annotation_config": None,
    }

    return {
        "figure_id": figure_id,
        "recipe": recipe["id"],
        "recipe_name": recipe["name"],
        "figure_role": task.get("figure_role", recipe["figure_role"]),
        "problem_type": problem_type,
        "plot_type": plot_type,
        "usage": usage,
        "template": output.get("template"),
        "fallback_templates": _filtered_fallbacks(recipe),
        "visual_layers": list(recipe.get("visual_layers") or []),
        "data_semantics": task.get("data_semantics") or {},
        "metadata": metadata,
        "quality_checks": list(recipe.get("quality_checks") or []),
        "data": task.get("data", {}),
        "planner_trace": {
            "selected_from": index_entry.get("path"),
            "score": trace["score"],
            "reasons": trace["reasons"],
        },
    }


def plan_chart(task, root=SKILL_ROOT):
    index_entry, recipe, trace = choose_recipe(task, root=root)
    if index_entry is None:
        # ★ 降级：无高级 recipe 时返回基础模板建议
        return {
            "figure_id": task.get("figure_id", task.get("task", "unnamed")),
            "recipe": None,
            "figure_role": task.get("figure_role", "basic"),
            "problem_type": task.get("problem_type", "general"),
            "plot_type": "basic",
            "data": task.get("data", {}),
            "fallback_templates": ["line", "bar", "grouped_bar", "stacked_area"],
            "planner_trace": trace,
            "note": "未匹配到高级 recipe，建议使用基础模板"
        }
    return build_spec(task, index_entry, recipe, trace)


def render_spec(spec, output_format):
    if output_format == "yaml":
        return yaml.safe_dump(spec, allow_unicode=True, sort_keys=False)
    return json.dumps(spec, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Plan an advanced chart spec from a plotting task.")
    parser.add_argument("task", help="Task JSON/YAML path.")
    parser.add_argument("--format", choices=["json", "yaml"], default="json")
    parser.add_argument("--output", help="Optional output spec path.")
    args = parser.parse_args()

    spec = plan_chart(read_task(args.task))
    rendered = render_spec(spec, args.format)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
