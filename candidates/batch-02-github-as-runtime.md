# Candidates Batch 02 — GitHub 當運算層／資料庫軸

> 這條軸線的專案以 **GitHub Actions 當排程運算、Issues/Discussions/repo 當資料庫、Pages 當前端**。
> 44 名單的納入條件只掃了「執行於 Cloudflare」，結構性漏掉本象限——2026-07-29 討論補上。
> 星數以 2026-07-29 `gh api` 即時核對。狀態：全部 **Discovered**。

## 活躍種子（9 項）

| 名稱 | full_name | stars | Pattern | 備註 |
|------|-----------|------:|---------|------|
| Upptime | upptime/upptime | 17,106 | Actions 排程＋Issues 事件庫＋Pages 狀態頁 | 「GitHub as compute」公認代表作 |
| metrics | lowlighter/metrics | 16,985 | Actions 當圖表生成引擎 | |
| Decap CMS | decaporg/decap-cms | 19,267 | Git repo 當 CMS 資料庫 | 雙平台編排橋樑（搭 CF Pages＋Worker OAuth） |
| giscus | giscus/giscus | 11,970 | Discussions 當留言資料庫 | utterances 的活繼承者（繼承者模式案例） |
| PicX | XPoet/picx | 5,075 | repo 當圖床儲存＋CDN | 趨緩（2025-02 後） |
| running_page | yihong0618/running_page | 4,493 | Actions pipeline＋repo 當個人資料庫 | |
| blog-post-workflow | gautamkrishnar/blog-post-workflow | 3,423 | Actions 定時聚合外部內容 | |
| shot-scraper | simonw/shot-scraper | 2,537 | git scraping 家族 | Actions 抓資料、repo 當時序庫 |
| gitblog | yihong0618/gitblog | 1,624 | Issues 當部落格 | |

## 已停更（復活候選池）

| 名稱 | full_name | stars | license | 停更 | 復活評估 |
|------|-----------|------:|---------|------|----------|
| osmosfeed | osmoscraft/osmosfeed | 990 | MIT | 2023-10 | **復活首發**：作者 README 已導流 sister project（明確棄坑）；復活版＝Actions 抓取＋CF Pages/D1＋Workers AI 摘要＋MCP |
| git-history | pomber/git-history | 13,684 | MIT | 2024-10 | 排後：純前端仍可用，復活增量小 |
| utterances | utterance/utterances | 9,692 | MIT | 2024-08 | 不復活：giscus 已是活繼承者，作為「繼承者模式」案例研究 |

復活四規矩：查 license（MIT/Apache 才可自由 fork 復活）；致意原作者（fork 改名＋successor to，先開 issue）；必加當年沒有的能力層（D1／Workers AI／MCP）；每案自帶內容價值。三檔策略：**死掉的才改寫，活著的只串接**。
