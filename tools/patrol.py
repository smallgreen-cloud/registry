#!/usr/bin/env python3
"""SVC-5 巡邏 detector（生產層）：卡片 spec_version 落後現行 spec minor 版以上 → stale 告警。

設計依 pipeline-invariant-testing 第 5 條：「應該會一直正常」的假設要嘛 CI 測、要嘛生產 detector＋告警。
排程跑（GitHub Actions cron）；發現 stale 或執行失敗都打 Telegram（沉默失敗＝設計缺陷）。
輸出：stdout 報告＋exit code（0 無事、1 有 stale、2 執行錯誤）——告警由 workflow 層依 exit code 觸發。
"""
import json
import sys
import urllib.request
from pathlib import Path

import yaml

REG = Path(__file__).resolve().parent.parent


def current_spec_minor() -> tuple:
    req = urllib.request.Request(
        "https://api.github.com/repos/smallgreen-cloud/spec/tags",
        headers={"User-Agent": "smallgreen-patrol"})
    tags = json.loads(urllib.request.urlopen(req, timeout=20).read())
    versions = []
    for t in tags:
        name = t["name"].lstrip("v")
        parts = name.split(".")
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            versions.append(tuple(int(p) for p in parts))
    if not versions:
        raise RuntimeError("spec repo 無合法版本 tag")
    return max(versions)


def main() -> int:
    try:
        cur = current_spec_minor()
    except Exception as e:
        print(f"ERROR: 取 spec 版本失敗：{e}")
        return 2
    stale = []
    for cp in sorted((REG / "cards").glob("*.yaml")):
        card = yaml.safe_load(cp.read_text(encoding="utf-8"))
        v = card.get("verification", {}).get("spec_version", "0.0.0")
        parts = tuple(int(p) for p in v.split(".") if p.isdigit())
        if len(parts) != 3:
            stale.append((card.get("id", cp.stem), v, "版本格式異常"))
            continue
        # stale 判準：落後現行 minor 版以上（同 minor 的 patch 差不計）
        if (parts[0], parts[1]) < (cur[0], cur[1]):
            stale.append((card.get("id", cp.stem), v, f"落後現行 {'.'.join(map(str, cur))}"))
    if stale:
        print(f"STALE {len(stale)} 張卡（現行 spec {'.'.join(map(str, cur))}）：")
        for cid, v, why in stale:
            print(f" ✗ {cid}: spec_version {v}（{why}）")
        return 1
    print(f"ok: 全部卡片與現行 spec {'.'.join(map(str, cur))} 同 minor 世代")
    return 0


if __name__ == "__main__":
    sys.exit(main())
