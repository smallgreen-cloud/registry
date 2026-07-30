# SmallGreen Registry

> 已驗證的小型雲端服務目錄 | Community-verified registry of small, green, self-deployable cloud services.

**Status: 建置中 — 首批條目整理中**

## 這是什麼

收錄可在 **GitHub＋Cloudflare 免費額度**內獨立運作的小型開源服務。每個條目是一張標準化「服務卡」：用途、適合對象、使用的 Cloudflare 元件、是否需要自有網域或外部 API、資料流向、低碳屬性、驗證等級與最近驗證日期。

**收錄 ≠ 驗證。** 驗證等級只有三種，晉級條件全部機械可檢核（見 [spec](https://github.com/smallgreen-cloud/spec)）：

| 等級 | 意義 |
|---|---|
| Discovered | 已發現，未經社群實測 |
| Community Verified | 至少一位社群成員完成真實部署與功能驗收 |
| SmallGreen Ready | 通過完整標準，可由 AI agent 依標準流程安裝與維護 |

## 統計原則

- 部署統計來自自願提交的 Evidence Pack（conformance 產物），不來自任何遙測
- 彙總資料以 CC 授權公開（SmallGreen Evidence Dataset）
- 服務卡標示驗證當時的 spec 版本，平台規則變動時舊驗證自動可識別為過期

## 提交新專案

流程建置中：PR 提交 → conformance CI 初審 → 社群成員實測 → 上架。參考 winget-pkgs 模式。
