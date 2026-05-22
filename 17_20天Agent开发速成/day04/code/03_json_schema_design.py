# -*- coding: utf-8 -*-
"""
Day04 - 03: JSON Schema 设计最佳实践对比
功能：演示烂 Schema 与好 Schema 对模型表现的影响
"""
import json

# ============ ❌ 烂 Schema 反面教材 ============
BAD_SCHEMA = {
    "name": "book_flight",
    "description": "book a flight",  # 太简短，模型不知道边界
    "parameters": {
        "type": "object",
        "properties": {
            "from": {"type": "string"},                       # 关键字冲突
            "to": {"type": "string"},                         # 无 description
            "date": {"type": "string"},                       # 格式没说
            "class": {"type": "string"},                      # 关键字冲突 + 无 enum
            "passengers": {"type": "number"}                  # 没范围约束
        }
        # 没有 required 字段
    }
}


# ============ ✅ 好 Schema 正面示范 ============
GOOD_SCHEMA = {
    "name": "book_flight",
    "description": (
        "预订国内航班机票。"
        "仅支持中国大陆机场，不支持港澳台和国际航班。"
        "下单前会返回价格预估，需用户确认后才真正出票。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "from_city": {
                "type": "string",
                "description": "出发城市的中文名，如 上海、北京。不要使用机场代码（如 PVG）或拼音。"
            },
            "to_city": {
                "type": "string",
                "description": "到达城市的中文名，如 广州、成都。不要使用机场代码或拼音。"
            },
            "date": {
                "type": "string",
                "description": "出发日期，格式必须为 YYYY-MM-DD，例如 2026-05-22。不要写成 2026/05/22 或 5月22日。",
                "pattern": r"^\d{4}-\d{2}-\d{2}$"
            },
            "cabin_class": {
                "type": "string",
                "description": "舱位等级，默认经济舱",
                "enum": ["经济舱", "商务舱", "头等舱"],
                "default": "经济舱"
            },
            "passenger_count": {
                "type": "integer",
                "description": "乘客人数，默认 1 人，最多 9 人",
                "minimum": 1,
                "maximum": 9,
                "default": 1
            }
        },
        "required": ["from_city", "to_city", "date"]
    }
}


# ============ 5 大设计原则验证清单 ============
def audit_schema(schema: dict) -> dict:
    """对 schema 做质量审计"""
    issues = []
    func = schema.get("function", schema)
    desc = func.get("description", "")
    params = func.get("parameters", {})
    props = params.get("properties", {})

    # 原则 1: description 详细度
    if len(desc) < 30:
        issues.append(f"❌ 函数描述太短({len(desc)}字)，建议 30-80 字")

    # 原则 2: 参数 description 检查
    for name, prop in props.items():
        if not prop.get("description"):
            issues.append(f"❌ 参数 {name} 缺少 description")
        elif len(prop.get("description", "")) < 15:
            issues.append(f"⚠️  参数 {name} 描述较短({len(prop['description'])}字)")

    # 原则 3: 字符串字段建议加 enum 或 pattern
    for name, prop in props.items():
        if prop.get("type") == "string" and not (prop.get("enum") or prop.get("pattern")):
            if not any(kw in prop.get("description", "").lower() for kw in ["名", "号", "邮箱", "url"]):
                issues.append(f"💡 参数 {name} 可考虑加 enum 或 pattern 约束")

    # 原则 4: 数字字段建议加范围
    for name, prop in props.items():
        if prop.get("type") in ("number", "integer"):
            if "minimum" not in prop and "maximum" not in prop:
                issues.append(f"⚠️  参数 {name} 缺少 minimum/maximum 范围约束")

    # 原则 5: 必填字段数量
    required = params.get("required", [])
    if not required:
        issues.append("❌ 没有任何 required 字段，模型可能漏填")
    elif len(required) > 3:
        issues.append(f"⚠️  必填字段 {len(required)} 个偏多，建议 ≤3 个")

    return {"score": max(0, 100 - len(issues) * 10), "issues": issues}


if __name__ == "__main__":
    print("=" * 60)
    print("烂 Schema 质量审计：")
    print("=" * 60)
    result = audit_schema(BAD_SCHEMA)
    print(f"得分：{result['score']}/100")
    for issue in result["issues"]:
        print(f"  {issue}")

    print("\n" + "=" * 60)
    print("好 Schema 质量审计：")
    print("=" * 60)
    result = audit_schema(GOOD_SCHEMA)
    print(f"得分：{result['score']}/100")
    for issue in result["issues"]:
        print(f"  {issue}")
    if not result["issues"]:
        print("  ✅ 完美无问题")

    print("\n📋 好 Schema 完整内容：")
    print(json.dumps(GOOD_SCHEMA, indent=2, ensure_ascii=False))
