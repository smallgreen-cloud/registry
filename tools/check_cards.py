#!/usr/bin/env python3
"""服務卡檢核（registry CI）：SVC-1 schema／SVC-2 晉級條件式／SVC-3 low_carbon 往返／
SVC-4 grade 一致性／SVC-7 taxonomy 引用完整性。

用法：check_cards.py --spec <spec repo 路徑>（cards/ 與 evidence/ 取相對本檔的 registry 根）
SVC-3/4 的真值源＝該專案最新 Evidence Pack（Pack 值為驗證期機械推導紀錄）；
SVC-4 另加規則檢查：components 含非選配 workers-ai 的卡，grade 不得為 A/B（SVC-4 判定表 D 列與 v0.2 C 例外）。
"""
import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

REG = Path(__file__).resolve().parent.parent


def latest_pack(pid: str):
    packs = sorted((REG / "evidence" / pid).glob("*.json"))
    return json.loads(packs[-1].read_text(encoding="utf-8")) if packs else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, type=Path)
    args = ap.parse_args()

    schema = json.loads((args.spec / "schemas" / "service-card.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    taxonomy = yaml.safe_load((REG / "taxonomy.yaml").read_text(encoding="utf-8"))
    cat_ids = {c["id"] for c in taxonomy["categories"]}
    fails = []
    cards = sorted((REG / "cards").glob("*.yaml"))
    if not cards:
        print("no cards found", file=sys.stderr)
        return 1

    for cp in cards:
        card = yaml.safe_load(cp.read_text(encoding="utf-8"))
        cid = card.get("id", cp.stem)

        # SVC-1 schema
        errs = list(validator.iter_errors(card))
        for e in errs:
            fails.append(f"{cid} SVC-1: {e.json_path} {e.message[:100]}")

        # SVC-7 taxonomy
        for c in card.get("categories", []):
            if c not in cat_ids:
                fails.append(f"{cid} SVC-7: 分類 '{c}' 不在 taxonomy.yaml")

        # SVC-2 晉級條件式
        lvl = card.get("verification", {}).get("level")
        v = card.get("verification", {})
        if lvl in ("community-verified", "smallgreen-ready"):
            stories = [s for s in card.get("scenario_stories", []) if s.get("reviewed")]
            if not (v.get("evidence_packs") and v.get("verifiers") and stories):
                fails.append(f"{cid} SVC-2: {lvl} 需 evidence_packs＋具名 verifiers＋reviewed story")
        if lvl == "smallgreen-ready" and not v.get("compatible_agents"):
            fails.append(f"{cid} SVC-2: smallgreen-ready 需 agent 全自主紀錄")

        # SVC-3 / SVC-4 對最新 Pack 往返
        pack = latest_pack(cid)
        if pack is None:
            if lvl != "discovered":
                fails.append(f"{cid} SVC-2: 無 Evidence Pack 但等級非 discovered")
        else:
            if card.get("low_carbon") != pack.get("low_carbon"):
                fails.append(f"{cid} SVC-3: low_carbon 與最新 Pack 不一致（卡 {card.get('low_carbon')} vs Pack {pack.get('low_carbon')}）")
            if card.get("free_tier_grade") != pack.get("free_tier", {}).get("grade"):
                fails.append(f"{cid} SVC-4: grade 與最新 Pack 不一致")
        comps = card.get("components", {}).get("cloudflare", [])
        if any(c == "workers-ai" for c in comps) and card.get("free_tier_grade") in ("A", "B"):
            fails.append(f"{cid} SVC-4: 非選配 workers-ai 但 grade {card['free_tier_grade']}（判定表：至多 C）")

    if fails:
        print(f"FAIL {len(fails)} 項：")
        for f in fails:
            print(" ✗", f)
        return 1
    print(f"all checks passed（{len(cards)} cards：SVC-1/2/3/4/7）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
