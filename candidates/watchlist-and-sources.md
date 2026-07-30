# Watchlist — 雙平台編排、跨平台情報源與巡邏關鍵字

> 部署支援範圍維持 GitHub＋Cloudflare 不動；本檔的其他平台定位為**情報源＋遷移流量源**，不是支援目標。
> 數據核對日期標於各節。

## 一、雙平台編排軸（CF＋GH 同時編排——幾乎無人標準化的象限）

> 2026-07-30 更新：本軸已非純觀察——三個項目排進首波（見 batch-02 首波標記與下表）。**雙平台整合是社群吸引力核心，首波必須有真整合 G+C 的高價值工具。**

| 專案/pattern | 首波 | 說明 |
|---|---|---|
| Decap CMS G+C 組合包 | **首波-S3（適配 repo）** | GitHub repo 當內容資料庫＋CF Pages 出站＋CF Worker OAuth 代理（decaporg/decap-cms 19,267★）；市場缺的只是標準化一鍵組合 |
| osmosfeed 復活版 | **首波-S3（自建）** | GH Actions 抓 RSS＋repo 時序庫＋CF Pages＋Workers AI 摘要——G+C 整合旗艦示範＋復活敘事（詳 batch-02） |
| meeting-capture pattern（自有原型） | 架構揭露文 | LINE 入口＋CF Worker 閘道（KV lock）＋GH Actions 批次運算＋repo 歸檔——Pipeline Profile 的定義原型 |
| Upptime 類 | **首波-S2（驗證）** | 純 GH 三元件編排，Pipeline Profile 第一個驗證對象；可延伸接 CF 前端 |

## 二、活的巨型專案（只串接不改寫）

| 專案 | stars | license | 策略 |
|------|------:|---------|------|
| RSSHub（DIYgod/RSSHub） | 45,457 | AGPL-3.0 | 日日有 commit；不碰本體，子集移植（挑熱門路由做 Workers 版）或當上游資料源 |

（2026-07-29 核對）

## 三、跨平台情報源（需求挖掘用）

| 來源 | 挖什麼 |
|---|---|
| **Val Town 歷期 Talk of the Town 存檔** | **已驗證需求金礦**：每個被精選的 val＝被驗證有人要的小服務需求（記帳 email handler、每日數據推播、個人財務工具……），逐個評估做 CF+GH 開源版＝免費產品市調 |
| HF Spaces（Gradio MCP） | 官方支援 Spaces as MCP servers；高流量 MCP Space＝雙棲候選與需求訊號 |
| Glitch 遷移討論串 | 2025-07 關站後「找不到新家的熱門專案」＝復活/收錄候選＋受眾所在 |
| Vercel 軸旗艦 | 需求規模佐證（2026-07-29 核對）：NextChat 88,564★／umami 37,949★／dub 24,184★——「一鍵部署到免費平台」的需求量級證明 |

## 四、平台風險論述素材（對外敘事）

- Glitch 2025-07-08 關停應用託管；Heroku 2022 砍免費層
- 對照：Cloudflare 與 GitHub 免費層＝商業模式核心（開發者生態獲客），非燒錢補貼
- 敘事鉤子：「你的小服務該搬到不會死的免費層」

## 五、季度巡邏關鍵字（併入月選節奏）

- GitHub topics：`deploy-to-cloudflare`、`cloudflare-workers`、`github-actions-automation`
- `gradio mcp-server`（HF Spaces）
- Val Town 官方部落格月報
- `deno-deploy` template repos
- 競品六面：MCP 託管（Smithery/Alpic）、平台市場（Railway/Vercel templates）、平台 agent 化（cloudflare/skills）、自架目錄、`.agent` 打包標準動態、小服務社群（Val Town）
