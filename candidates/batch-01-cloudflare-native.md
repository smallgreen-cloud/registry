# Candidates Batch 01 — Cloudflare 原生軸（44＋1）

> **本檔只涵蓋「Cloudflare 原生小型服務」單一軸線**。registry 候選池為多軸結構：
> batch-02＝GitHub 當運算層／資料庫軸；watchlist＝雙平台編排與跨平台情報源。
> 狀態：全部 **Discovered**（已發現，未經社群實測）。
> 核對方法：逐一 `gh api repos/<full_name>` 即時驗證（stars／forks／license／archived／last_push），名稱消歧義以「用途描述＋星數量級」雙重比對。
> 核對日期：2026-07-30。原始名單來源：2026-07-26 初步盤點（44 項）。
> 首批 Community Verified 候選（3＋9 執行順序）以「首批」欄標記；`newsnow`（2026-07-29 補列）一併收錄為第 45 項。

## 對照表

| # | 名稱 | full_name | stars | forks | license | last_push | 首批 | 備註 |
|---|------|-----------|------:|------:|---------|-----------|------|------|
| 1 | cloud-mail | maillab/cloud-mail | 12,999 | 18,982 | MIT | 2026-07-03 | | forks>stars 為 API 實測值 |
| 2 | cloudflare_temp_email | dreamhunter2333/cloudflare_temp_email | 11,113 | 7,506 | MIT | 2026-07-29 | | 郵件審慎區 |
| 3 | Sink | miantiao-me/Sink | 6,978 | 5,016 | **AGPL-3.0** | 2026-07-19 | 首批-先行 | 已從 ccbikai/Sink 改名遷移 |
| 4 | CloudFlare-ImgBed | MarSeventh/CloudFlare-ImgBed | 5,982 | 7,487 | MIT | 2026-07-29 | 首批 | |
| 5 | microfeed | microfeed/microfeed | 4,026 | 1,415 | AGPL-3.0 | 2026-02-13 | 首批 | |
| 6 | serverless-dns | serverless-dns/serverless-dns | 3,768 | 2,303 | MPL-2.0 | 2026-05-06 | 首批 | |
| 7 | UptimeFlare | lyc8503/UptimeFlare | 3,701 | 569 | Apache-2.0 | 2026-06-01 | 首批-先行 | |
| 8 | ChatGPT-Telegram-Workers | tbxark/ChatGPT-Telegram-Workers | 3,809 | 897 | MIT | 2026-04-06 | | AI 專區（需自帶模型 key） |
| 9 | agentic-inbox | cloudflare/agentic-inbox | 6,646 | 836 | Apache-2.0 | 2026-04-23 | | 官方專案，快照後成長 1.8x |
| 10 | Rin | openRin/Rin | 2,914 | 2,330 | MIT | 2026-06-26 | 首批 | |
| 11 | moemail | beilunyang/moemail | 2,766 | 2,543 | MIT | 2026-06-16 | | 郵件審慎區 |
| 12 | cf-workers-status-page | eidam/cf-workers-status-page | 2,811 | 1,433 | MIT | 2024-08-21 | | ⚠️ 近 2 年無 push，實質停更 |
| 13 | CloudPaste | ling-drag0n/CloudPaste | 2,567 | 1,701 | 自訂（NOASSERTION） | 2026-01-23 | | 需審閱授權條款 |
| 14 | counterscale | benvinegar/counterscale | 2,109 | 119 | MIT | 2025-12-15 | 首批-先行 | |
| 15 | second-brain-cloudflare | rahilp/second-brain-cloudflare | 684 | 92 | MIT | 2026-07-30 | 首批 | 與自有反思系統同類，對比文素材 |
| 16 | vmail | oiov/vmail | 1,444 | 372 | GPL-3.0 | 2026-07-16 | | owner 已遷移（原 yesmore 404） |
| 17 | pastebin-worker | SharzyL/pastebin-worker | 1,041 | 356 | MIT | 2026-07-30 | 首批 | |
| 18 | cf-image-hosting | ifyour/cf-image-hosting | 655 | 187 | **無 license** | 2024-05-02 | | ⚠️ 停更＋無授權，暫緩 |
| 19 | serverless-cloud-notepad | s0urcelab/serverless-cloud-notepad | 484 | 368 | MIT | 2025-06-06 | | |
| 20 | Alle | bestruirui/Alle | 452 | 151 | **無 license** | 2026-06-05 | | 郵件/AI 區；待作者補授權 |
| 21 | R2-Explorer | G4brym/R2-Explorer | 626 | 538 | MIT | 2026-07-20 | 首批 | |
| 22 | gemini-balance-do | （待人工確認） | — | — | — | — | | 原 335★ repo 疑已刪除/轉私有 |
| 23 | zmail | takumi913/zmail | 7 | — | — | 2026-07-26 | | 原 285★ repo 疑刪除重建，待確認 |
| 24 | roim-picx | roimdev/roim-picx | 289 | 307 | Apache-2.0 | 2026-03-16 | | owner 已遷移 |
| 25 | HanAnalytics | uxiaohan/HanAnalytics | 277 | 163 | MIT | 2025-03-19 | 首批 | |
| 26 | AuthInbox | TooonyChen/AuthInbox | 179 | 74 | MIT | 2026-07-09 | | Deploy Agent 案例候選 |
| 27 | Webviso | yestool/analytics_with_cloudflare | 143 | 40 | MIT | 2024-10-23 | | repo 名與品牌名不同 |
| 28 | mcp-memory | Puliczek/mcp-memory | 148 | 15 | **無 license** | 2025-04-24 | | 待作者補授權 |
| 29 | img-mom | beilunyang/img-mom | 122 | 39 | **無 license** | 2025-04-12 | | 待作者補授權 |
| 30 | cf-drop | lyonbot/cf-drop | 70 | 31 | **無 license** | 2025-02-08 | ⚠️ | 原首批名單，因無授權暫緩；待作者補 license 或替補 |
| 31 | imgUU | yestool/imgUU | 53 | 4 | MIT | 2025-03-13 | | |
| 32 | rss-worker | ProfessorManhattan/rss-worker | 50 | 16 | **無 license** | 2025-04-17 | | 待作者補授權 |
| 33 | linklet | （待人工確認） | — | — | — | — | | 原 44★ repo 疑已刪除/改名 |
| 34 | Gins-Blog | IchimaruGin728/Gins-Blog | 37 | 15 | MIT | 2026-05-17 | | agentic-first 範例 |
| 35 | cf-files-sharing | joyance-professional/cf-files-sharing | 35 | 21 | MIT | 2025-01-01 | | |
| 36 | cf-comment | joyance-professional/cf-comment | 25 | 5 | **無 license** | 2026-03-08 | | 待作者補授權 |
| 37 | d1-manager | JacobLinCool/d1-manager | 634 | 333 | MIT | 2026-07-30 | | 快照 23★ 為筆誤，實為 634★ |
| 38 | Webhook Debugger | brancogao/webhook-debugger | 12 | 2 | **無 license** | 2026-02-17 | | TDD 示範候選；待補授權 |
| 39 | ZeroLink | yclgkd/zerolink | 10 | 0 | AGPL-3.0 | 2026-07-28 | | 安全區，先程式審查 |
| 40 | Statusflare | krzko/statusflare | 9 | 6 | Apache-2.0 | 2025-12-15 | | |
| 41 | PageGuard | toeasy/pageguard | 0 | 1 | **無 license** | 2026-02-26 | | 觀察名單 |
| 42 | LLMKit | smigolsmigol/llmkit | 16 | 4 | MIT | 2026-07-28 | | 已排除同名 prompt 管理工具 |
| 43 | SkyPhusion LLM | skyphusion-labs/prism | 1 | 1 | AGPL-3.0 | 2026-07-29 | | repo 實名 prism |
| 44 | Beam | scobb/beam | 1 | 2 | MIT | 2026-06-16 | | |
| 45 | newsnow | ourongxing/newsnow | 21,309 | 5,876 | MIT | 2026-07-07 | 首批 | 2026-07-29 補列；全池最高星 CF 原生專案 |

## 待人工確認（3 項）

1. **#22 gemini-balance-do**：無 ≥300★ 同名 repo，僅存大量 0-3★ 同名複本——原 repo 疑已刪除或轉私有。需從快照來源（awesome list／部落格）回溯原 owner。
2. **#23 zmail**：`zaunist/zmail` redirect 至 `takumi913/zmail`（7★），與快照 285★ 相差 40 倍——疑原 repo 刪除重建。用途吻合但證據衝突。
3. **#33 linklet**：無 ~44★ 吻合候選（最接近 am-cf-linklet 11★）。疑已刪除或改名。

## 收錄政策影響（本次核對的三個結論）

1. **9 項無 license**（#18/20/28/29/30/32/36/38/41）：無授權＝法律上不可 fork 改作，**不可進入 Community Verified 流程**。處理：向作者開 issue 請求補 license（本身就是社群互動起手式）；cf-drop 因此移出首批，待補授權或替補。
2. **2 項實質停更**（#12、#18：2024 年後無 push）：可收錄為 Discovered，服務卡標示維護狀態；不排入首批。
3. **3 項原始 repo 消失**（#22/23/33）：印證「上游會死」是常態——維護狀態追蹤與復活機制不是理論需求。

---
資料產生：SmallGreen Cloud 計畫，gh api 即時核對。本檔為 registry 原料，非最終服務卡。
