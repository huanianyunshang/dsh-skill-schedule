#!/usr/bin/env python3
"""碳循环（碳水循环）克数计算器。

方法来源：B 站 BV1Gh411479A「碳水循环上级 - 饮食计划一站式分享」。

规则：
  一周分三段 —— 高碳 2 天 / 中碳 3 天 / 低碳 2 天
  碳水按 50% / 35% / 15% 分配周总量
  脂肪按 15% / 35% / 50% 反向分配
  蛋白每天固定，不随碳档变化

用法：
  python carb_cycle.py --weight 85 --body endo --protein 1.5
  python carb_cycle.py --weight 70 --body ecto --protein 1.2 --json

无第三方依赖，Python 3.9+。
"""

import argparse
import json
import sys

BODY_TYPES = {
    "endo": {"carb": 2.0, "fat": 0.8, "label": "内胚型（容易胖）"},
    "ecto": {"carb": 3.0, "fat": 1.1, "label": "外胚型（不容易胖）"},
}

TIERS = [
    # 名称, 天数, 碳水占比, 脂肪占比
    ("高碳", 2, 0.50, 0.15),
    ("中碳", 3, 0.35, 0.35),
    ("低碳", 2, 0.15, 0.50),
]

KCAL = {"carb": 4, "protein": 4, "fat": 9}


def compute(weight, body, protein_factor):
    cfg = BODY_TYPES[body]
    daily_carb = weight * cfg["carb"]
    daily_fat = weight * cfg["fat"]
    weekly_carb = daily_carb * 7
    weekly_fat = daily_fat * 7
    daily_protein = weight * protein_factor

    rows = []
    for name, days, carb_share, fat_share in TIERS:
        carb = weekly_carb * carb_share / days
        fat = weekly_fat * fat_share / days
        kcal = carb * KCAL["carb"] + daily_protein * KCAL["protein"] + fat * KCAL["fat"]
        rows.append(
            {
                "tier": name,
                "days": days,
                "carb": round(carb, 1),
                "protein": round(daily_protein, 1),
                "fat": round(fat, 1),
                "kcal": round(kcal),
            }
        )

    return {
        "weight": weight,
        "body": body,
        "body_label": cfg["label"],
        "protein_factor": protein_factor,
        "daily": {
            "carb": round(daily_carb, 1),
            "fat": round(daily_fat, 1),
            "protein": round(daily_protein, 1),
        },
        "weekly": {
            "carb": round(weekly_carb, 1),
            "fat": round(weekly_fat, 1),
            "protein": round(daily_protein * 7, 1),
        },
        "tiers": rows,
    }


def render(result):
    out = []
    out.append(
        f"== 碳循环克数（{result['weight']:g}kg / {result['body_label']} / "
        f"蛋白 {result['protein_factor']:g}g/kg）=="
    )
    out.append("")
    out.append(f"{'项':<6}{'每天':>10}{'每周':>10}")
    for key, label in (("carb", "碳水"), ("fat", "脂肪"), ("protein", "蛋白")):
        out.append(
            f"{label:<6}{result['daily'][key]:>8g} g{result['weekly'][key]:>9g} g"
        )
    out.append("")
    out.append(f"{'碳档':<6}{'天':>3}{'碳水/天':>10}{'脂肪/天':>10}{'蛋白/天':>10}{'热量':>11}")
    for r in result["tiers"]:
        out.append(
            f"{r['tier']:<6}{r['days']:>3}{r['carb']:>8g} g{r['fat']:>9g} g"
            f"{r['protein']:>8g} g{r['kcal']:>8} kcal"
        )

    kcals = [r["kcal"] for r in result["tiers"]]
    spread = max(kcals) - min(kcals)
    out.append("")
    if spread >= 300:
        out.append(
            f"[!] 三档热量差 {spread} kcal（最高 {max(kcals)} / 最低 {min(kcals)}）。"
        )
        out.append(
            "  原方法说三档应接近，差额靠加蔬菜补 —— 尤其别让中碳日变成挨饿日。"
        )
    else:
        out.append(f"三档热量差 {spread} kcal，在可接受范围（<300）。")

    out.append("")
    out.append("注：蛋白按 0.8–1.5 g/kg 取，减脂保肌建议 ≥1.2；训练日配高碳，休息日配低碳。")
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(
        description="碳循环克数计算器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--weight", type=float, required=True, help="体重 kg")
    p.add_argument(
        "--body",
        choices=sorted(BODY_TYPES),
        default="endo",
        help="体型：endo=内胚型（容易胖，碳水2g/脂肪0.8g）；ecto=外胚型（碳水3g/脂肪1.1g）",
    )
    p.add_argument(
        "--protein",
        type=float,
        default=1.2,
        help="蛋白系数 g/kg，范围 0.8–1.5（默认 1.2）",
    )
    p.add_argument("--json", action="store_true", help="输出 JSON")
    args = p.parse_args(argv)

    if args.weight <= 0:
        p.error("--weight 必须是正数")
    if not 0.8 <= args.protein <= 1.5:
        print(
            f"警告：蛋白系数 {args.protein} 超出原方法建议的 0.8–1.5 g/kg，仍按输入计算。",
            file=sys.stderr,
        )

    result = compute(args.weight, args.body, args.protein)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
