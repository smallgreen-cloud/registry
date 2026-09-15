# SmallGreen Registry

> 把開源小型專案整理成自己能運行的服務 | A registry of open-source small projects that people can deploy and run themselves.

**Status: 建置中 — 首批條目整理中**

## 這是什麼

SmallGreen Registry 面向想把開源小型專案變成自己能運行服務的人。它把 Repository 整理成可理解、可比較、可部署的服務卡，並揭露用途、適合對象、部署前提、架構、資料流、限制、驗證等級與最近驗證日期。

Registry 是事實資料層，不是代管平台，也不是替上游專案背書。使用者仍在自己的帳號部署與維護服務。

**收錄 ≠ 驗證。** 驗證等級只有三種，晉級條件全部機械可檢核（見 [spec](https://github.com/smallgreen-cloud/spec)）：

| 等級 | 意義 |
|---|---|
| Discovered | 已發現，未經社群實測 |
| Community Verified | 至少一位社群成員完成真實部署與功能驗收 |
| SmallGreen Ready | 通過完整標準，可由 AI agent 依標準流程安裝與維護 |

## 服務卡要先回答什麼

每張服務卡固定回答：

- 這是什麼專案
- 解決什麼問題
- 適合誰
- 可以做什麼
- 部署前要準備什麼
- 開始前要知道哪些限制
- 怎麼運行，以及證據從哪裡來

技術契約與機器可讀欄位支援這些答案，但不能取代給人的專案說明。

## 統計原則

- 部署統計來自自願提交的 Evidence Pack（conformance 產物），不來自任何遙測
- 彙總資料以 CC 授權公開（SmallGreen Evidence Dataset）
- 服務卡標示驗證當時的 spec 版本，平台規則變動時舊驗證自動可識別為過期

## 提交新專案

完整流程見 [PROJECT_PUBLISHING_STANDARD.md](PROJECT_PUBLISHING_STANDARD.md)：資格檢查 → adapter → conformance → 真實部署與 Evidence Pack → 機械生成服務卡 → Registry／網站 Gate → 人工 review → 發布。

全量案例整理見 [candidates/catalogue-readiness.md](candidates/catalogue-readiness.md)。候選池會先分層與補齊產品內容，不會因列入候選就直接進入正式服務目錄。已完成內容研究的候選放在 [`candidates/research-cases.yaml`](candidates/research-cases.yaml)，由網站以獨立的 Research cases 層呈現。

服務卡不得直接手填推導欄位；`cards/*.yaml` 由 adapter contract、Evidence Pack 與 `tools/gen_cards.py` 的 editorial 欄位決定性生成。

## 自有專案 onboarding

SmallGreen 自有專案可先放在 [`onboarding/first-party.yaml`](onboarding/first-party.yaml)，公開產品用途、適合對象、目前能力與剩餘上架閘門。這些資料會被正式站 render 成獨立的 onboarding 詳頁，但不會混入 `cards/`、驗證服務數或 Evidence 索引。

這個分層是刻意的：有產品形狀不等於已完成 SmallGreen 驗證。專案必須完成契約、conformance、真實部署驗收、teardown 與 Evidence Pack，才能依發布標準生成正式服務卡。

研究案例也遵守同一個邊界：上游 README、授權與 metadata 只能支持內容研究，不是部署證據。研究卡完成契約、實際部署、teardown 與 Evidence Pack 後，才可轉入 `cards/`。

網站英文服務內容由 `translations/en.yaml` 管理。每個服務 ID 必須同時具有英文 `one_liner` 與 `data_flow`，Registry Gate 會拒絕缺漏或孤立翻譯。
