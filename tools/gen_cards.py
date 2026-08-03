#!/usr/bin/env python3
"""服務卡生成器（P1）：cards/<id>.yaml ← adapter profile.yaml ＋ 最新 Evidence Pack。

原則：機械欄位（repo/license/login_method/grade/low_carbon/verification）一律推導，
禁手填；編輯欄位（one_liner/categories/components/maintenance_status）集中在 EDITORIAL
字典（maintenance_status 依 candidates 表 last_push 機械分級：<6 月 active、6-12 slowing、>12 stalled）。
再生：python3 tools/gen_cards.py（決定性；ADAPTER_ROOT 指向本地 adapter checkouts）。
"""
import json
from datetime import date
from pathlib import Path

import yaml

REG = Path(__file__).resolve().parent.parent
ADAPTER_ROOT = REG.parent  # /Users/user/projects/smallgreen-cloud/

# project_id -> (adapter dir, adapter repo slug)；first-party（Path A）用 FIRST_PARTY
PROJECTS = {
    "sink": ("adapter-sink", "smallgreen-cloud/adapter-sink"),
    "uptimeflare": ("adapter-uptimeflare", "smallgreen-cloud/adapter-uptimeflare"),
    "counterscale": ("adapter-counterscale", "smallgreen-cloud/adapter-counterscale"),
    "newsnow": ("adapter-newsnow", "smallgreen-cloud/adapter-newsnow"),
    "pastebin-worker": ("adapter-pastebin-worker", "smallgreen-cloud/adapter-pastebin-worker"),
    "hananalytics": ("adapter-hananalytics", "smallgreen-cloud/adapter-hananalytics"),
    "serverless-dns": ("adapter-serverless-dns", "smallgreen-cloud/adapter-serverless-dns"),
    "rin": ("adapter-rin", "smallgreen-cloud/adapter-rin"),
    "second-brain-cloudflare": ("adapter-second-brain", "smallgreen-cloud/adapter-second-brain"),
    "cloudflare-imgbed": ("adapter-cloudflare-imgbed", "smallgreen-cloud/adapter-cloudflare-imgbed"),
    "microfeed": ("adapter-microfeed", "smallgreen-cloud/adapter-microfeed"),
}

# first-party（Path A）：契約隨程式碼同 repo，無 adapter 層；profile 自 GitHub raw 取得
FIRST_PARTY = {
    "business-card-mcp": "ai-cooperation/business-card-mcp",
}

# 編輯欄位（維護狀態依 candidates/batch-01 last_push，核對日 2026-07-30）
EDITORIAL = {
    "sink": {
        "name": "Sink", "one_liner": "自架短網址服務，附 Analytics Engine 造訪統計",
        "categories": ["utilities", "analytics"],
        "components": ["workers", "kv", "analytics-engine", "workers-ai(選配)"],
        "maintenance_status": "active",  # last_push 2026-07-19
    },
    "uptimeflare": {
        "name": "UptimeFlare", "one_liner": "自架服務監測與狀態頁（cron 探測＋D1 歷史）",
        "categories": ["utilities"],
        "components": ["workers", "pages", "d1", "kv", "cron"],
        "maintenance_status": "active",  # 2026-06-01
    },
    "counterscale": {
        "name": "Counterscale", "one_liner": "自己帳號裡的網站流量分析（GA 替代）",
        "categories": ["analytics"],
        "components": ["workers", "analytics-engine"],
        "maintenance_status": "slowing",  # 2025-12-15（約 8 個月）
    },
    "newsnow": {
        "name": "NewsNow", "one_liner": "40+ 來源新聞熱榜聚合站，快取存自己的 D1",
        "categories": ["publishing"],
        "components": ["pages", "d1"],
        "maintenance_status": "active",  # 2026-07-07
    },
    "pastebin-worker": {
        "name": "Pastebin Worker", "one_liner": "curl 友善的自架 pastebin／短網址／檔案分享",
        "categories": ["sharing", "utilities"],
        "components": ["workers", "kv"],
        "maintenance_status": "active",  # 2026-07-30
    },
    "hananalytics": {
        "name": "HanAnalytics", "one_liner": "輕量網站流量分析儀表板（Pages Functions＋AE）",
        "categories": ["analytics"],
        "components": ["pages", "analytics-engine"],
        "maintenance_status": "stalled",  # 2025-03-19（約 16 個月）
    },
    "serverless-dns": {
        "name": "serverless-dns", "one_liner": "RethinkDNS 引擎的自架 DoH 解析端點（內建封鎖清單）",
        "categories": ["utilities"],
        "components": ["workers"],
        "maintenance_status": "active",  # 2026-05-06
    },
    "rin": {
        "name": "Rin", "one_liner": "個人部落格系統（文章／評論／RSS／Queue 背景 AI 摘要）",
        "categories": ["publishing"],
        "components": ["workers", "d1", "queues", "workers-ai", "cron"],
        "maintenance_status": "active",  # 2026-06-26
    },
    "second-brain-cloudflare": {
        "name": "Second Brain", "one_liner": "個人知識庫＋MCP server（keyword-only 降級收錄版）",
        "categories": ["sharing"],
        "components": ["workers", "d1", "kv", "workers-ai", "cron"],
        "maintenance_status": "active",  # 2026-07-30
    },
    "cloudflare-imgbed": {
        "name": "CloudFlare-ImgBed", "one_liner": "圖床檔案管理站（External 外鏈降級收錄版，KV 中繼資料）",
        "categories": ["sharing"],
        "components": ["workers", "kv"],
        "maintenance_status": "active",  # 2026-07-29
    },
    "business-card-mcp": {
        "name": "Business Card MCP", "one_liner": "AI 原生的私人名片庫：在 ChatGPT／Claude 辨識名片並寫入自己帳號的 D1／R2",
        "categories": ["sharing"],
        "components": ["workers", "d1", "r2", "kv"],
        "maintenance_status": "active", "license": "MIT",
    },
    "microfeed": {
        "name": "microfeed", "one_liner": "輕量 feed/CMS（JSON/RSS feed＋admin 後台；無 R2 文字模式收錄版）",
        "categories": ["publishing"],
        "components": ["workers", "d1"],
        "maintenance_status": "active",  # 2026-02-13（約 5.6 個月）
    },
}


def latest_pack(pid: str) -> dict:
    packs = sorted((REG / "evidence" / pid).glob("*.json"))
    if not packs:
        raise SystemExit(f"{pid}: 無 Evidence Pack")
    return json.loads(packs[-1].read_text(encoding="utf-8")), packs[-1]


def load_profile(pid: str) -> dict:
    if pid in FIRST_PARTY:
        import urllib.request
        url = f"https://raw.githubusercontent.com/{FIRST_PARTY[pid]}/main/.smallgreen/profile.yaml"
        with urllib.request.urlopen(url, timeout=20) as r:
            return yaml.safe_load(r.read().decode("utf-8"))
    p = ADAPTER_ROOT / PROJECTS[pid][0] / ".smallgreen" / "profile.yaml"
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def build_card(pid: str) -> dict:
    prof = load_profile(pid)
    pack, pack_path = latest_pack(pid)
    ed = EDITORIAL[pid]
    ext = [e["domain"] for e in (prof.get("external_services") or [])]
    all_packs = sorted((REG / "evidence" / pid).glob("*.json"))
    packs_rel = [str(p.relative_to(REG)) for p in all_packs]
    seen = {}
    for pp in all_packs:
        for a in json.loads(pp.read_text(encoding="utf-8")).get("agent_matrix", []):
            if a.get("role", "deployer") != "deployer":
                continue
            key = (a["agent"], a["model"])
            # 同引擎多 run 取最好結果（autonomous > assisted > blocked）
            rank = {"autonomous": 2, "assisted": 1, "blocked": 0}
            if key not in seen or rank[a["result"]] > rank[seen[key]]:
                seen[key] = a["result"]
    agents = [{"agent": k[0], "model": k[1], "result": v}
              for k, v in sorted(seen.items())]
    is_fp = pid in FIRST_PARTY
    repo = {"upstream": FIRST_PARTY[pid] if is_fp else prof["upstream"]["repo"]}
    if not is_fp:
        repo["adapter"] = PROJECTS[pid][1]
        repo["license"] = prof["upstream"]["license"]
    else:
        repo["license"] = ed.get("license", "")
    card = {
        "id": pid,
        "name": ed["name"],
        "one_liner": ed["one_liner"],
        "categories": ed["categories"],
        "profile": prof["profile"],
        "repo": repo,
        "components": {"cloudflare": ed["components"]},
        "login_method": prof.get("login_method", "none"),
        "data_flow": {
            "external_services": ext,
            "disclosure": ((prof.get("data", {}).get("notes") or prof.get("summary", {}).get("purpose") or "")[:200]),
        },
        "verification": {
            "level": "discovered",  # SVC-2：晉級需具名 verifier＋scenario story（blocked-on-real-users）
            "spec_version": pack["spec_version"],
            "last_verified": pack["deploy_event"]["date"],
            "evidence_packs": packs_rel,
            "compatible_agents": agents,
        },
        "free_tier_grade": pack["free_tier"]["grade"],
        "low_carbon": pack["low_carbon"],
        "maintenance_status": ed["maintenance_status"],
    }
    shot = (pack.get("screenshots") or {}).get("app_png")
    if shot:
        card["images"] = {"screenshot": {"path": shot["path"],
                                          "evidence_pack_ref": str(pack_path.relative_to(REG))}}
    if card["free_tier_grade"] in ("C", "D"):
        notes = pack["free_tier"].get("quota_notes") or []
        quota = next((n for n in notes if any(k in n for k in ("額度", "/day", "limit", "Neurons", "writes"))), None)
        if quota:
            card["quota_note"] = quota[:200]
    return card


def main():
    out = REG / "cards"
    out.mkdir(exist_ok=True)
    for pid in list(PROJECTS) + list(FIRST_PARTY):
        card = build_card(pid)
        (out / f"{pid}.yaml").write_text(
            "# 機械生成（tools/gen_cards.py）——editorial 欄位改 EDITORIAL 字典後重生，勿直接手改推導欄位\n"
            + yaml.safe_dump(card, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"generated {len(PROJECTS)} cards")


if __name__ == "__main__":
    main()
