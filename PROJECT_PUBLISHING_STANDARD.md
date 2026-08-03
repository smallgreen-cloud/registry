# SmallGreen Cloud 新專案發布標準 v1.0

> 目的：讓後續 Agent 以一致、可驗證、可重生的方式，把新專案加入 Registry 與官方網站。  
> 核心原則：**網站不是資料輸入介面；Registry YAML 是服務卡真相源，網站只 render。**

## 一、發布狀態機

```text
CANDIDATE
  → ELIGIBILITY_CHECKED
  → ADAPTER_READY
  → EVIDENCE_READY
  → CARD_GENERATED
  → REGISTRY_VALIDATED
  → SITE_RENDERED
  → HUMAN_REVIEWED
  → PUBLISHED
```

任何一步失敗即停在當前狀態並回報，不得跳過 validator、以手填資料偽造下一狀態，或因網站能 render 就宣稱已驗證。

## 二、必要產物

每個新專案至少具備：

```text
adapter-{project}/
├── AGENTS.md
├── UPSTREAM.md
├── .smallgreen/
│   ├── profile.yaml
│   ├── acceptance.yaml
│   └── maintenance.yaml
└── patches/ 或等效的可重現適配資產

registry/
├── evidence/{project}/{date}-{environment}-{run}.json
├── cards/{project}.yaml                 # 由 generator 產生
├── translations/en.yaml                 # 英文網站文案與資料流揭露
└── assets/screenshots/{project}/...     # 有 UI 且 Evidence Pack 引用時才需要
```

無 UI 服務不製造假截圖，網站改用 Deployment Contract 機械生成的架構圖。

## 三、欄位所有權

服務卡欄位分為三類，Agent 必須依來源修改：

| 類型 | 欄位例 | 真相源 | 修改方式 |
|---|---|---|---|
| 契約推導 | `profile`、`repo.upstream`、`license`、`login_method`、`external_services` | adapter `.smallgreen/profile.yaml` | 修改契約後重生卡片 |
| Evidence 推導 | `spec_version`、`last_verified`、`evidence_packs`、`compatible_agents`、`free_tier_grade`、`low_carbon`、截圖引用 | 最新及歷史 Evidence Pack | 新增 append-only Pack 後重生卡片 |
| Editorial | `name`、`one_liner`、`categories`、顯示元件、`maintenance_status` | `tools/gen_cards.py` 的 `EDITORIAL` | 修改 EDITORIAL 後重生卡片 |
| Translation | 英文 `one_liner`、`data_flow` | `translations/en.yaml` | 新增服務時同步新增相同 ID 並通過 I18N Gate |

禁止直接修改 `cards/{project}.yaml` 的推導欄位。檔案頂端已有生成警告；直接修改會在下一次重生時被覆寫。

## 四、Agent 執行流程

### Step 1：資格與公開邊界

Agent 先確認：

- upstream repo 可公開存取且 commit 可鎖定。
- license 已辨識；無 license 只能留 Candidate／Discovered 候選，不得 fork 改作或進入 Community Verified。
- 專案符合 Small App、Pipeline 或兩者組合的 Profile 範圍。
- 資料流、外部服務、secret、資源預算與 teardown 可以明確描述。
- 公開產物不含 token、account／zone／resource ID、私人 URL、使用者資料、私人 log 或未揭露漏洞。

### Step 2：建立 Adapter

Adapter 必須包含：

- `UPSTREAM.md`：上游 repo、鎖定 commit、license、更新策略。
- `AGENTS.md`：非互動部署流程、最多三次必要確認、驗收、失敗停止條件與 teardown。
- `.smallgreen/profile.yaml`：用途、受眾、資料、secret、外部服務、替代部署與 upstream。
- `.smallgreen/acceptance.yaml`：health、smoke、使用者驗收及 uninstall check。
- `.smallgreen/maintenance.yaml`：更新、備份、還原、移除及額度監控。

Agent 是導遊不是裁判；`AGENTS.md` 不得自行宣告通過，通過與否由 conformance 與 Evidence Pack 決定。

### Step 3：Conformance

在任何部署前，執行 adapter 的 schema、profile、secret manifest、上游鎖定與相關 fixture 檢查。所有結果必須通過；不得降低 validator、跳過 hook 或刪除失敗條款以換取綠燈。

### Step 4：真實部署與 Evidence

部署作業依沙盒互斥規則進行，完成：

1. 部署前資源基線。
2. 部署與必要資源建立。
3. health、核心 API／UI 與 acceptance 驗收。
4. 有 UI 時收取真實截圖並清除敏感資訊。
5. 獨立 verifier 或機械裁判複驗。
6. teardown。
7. 所有適用資源類型歸零 diff。
8. 建立 append-only Evidence Pack。

提交 Evidence Pack 前必須依 Spec schema 驗證。既有 Pack 不覆寫；修正或重驗以新 Pack 加 `supersedes` 表達。

### Step 5：註冊 Generator

在 `tools/gen_cards.py`：

1. 將 project ID 加入 `PROJECTS`，指向本地 adapter 目錄與公開 adapter repo slug。
2. 在 `EDITORIAL` 加入名稱、一般人看得懂的 one-liner、taxonomy categories、顯示用 Cloudflare components 與 maintenance status。
3. one-liner 描述使用情境，不堆技術名詞，最長 120 字。
4. category 只能引用 `taxonomy.yaml` 現有 ID；新增 taxonomy 必須獨立說明理由並檢查既有卡片影響。
5. 在 `translations/en.yaml` 新增相同 project ID 的 `one_liner` 與 `data_flow`；網站程式碼不得保存逐服務翻譯。

### Step 6：重生服務卡

```bash
python3 tools/gen_cards.py
```

Agent 必須檢查：

- 只新增或更新預期的卡片。
- 推導欄位與最新 Evidence Pack 一致。
- `images.screenshot` 同時具有存在的站內檔案與 `evidence_pack_ref`。
- 沒有把本機絕對路徑、private repo、secret 或 sandbox resource ID 帶入卡片。

### Step 7：Registry Gate

```bash
python3 tools/check_cards.py --spec ../spec
```

最低必過：

- SVC-1：Schema。
- SVC-2：驗證等級與晉級條件。
- SVC-3：Low-carbon 與最新 Pack 往返一致。
- SVC-4：Free-tier grade 一致。
- SVC-7：Taxonomy 引用完整。
- I18N：每張服務卡都有英文 `one_liner` 與 `data_flow`，且沒有孤立翻譯。
- 所有 Evidence Pack 通過當前 Spec schema。

### Step 8：網站預覽

網站只使用通過 Registry Gate 的資料：

```bash
python3 ../site/tools/build.py --registry . --out <temporary-directory>/dist
```

Agent 檢查：

- 首頁卡數與 Registry 一致。
- 新專案具有服務詳頁、`cards.json`、`llms.txt` 與 sitemap 項目。
- 可見文字、JSON-LD 與 YAML 一致。
- 截圖可載入；無 UI 專案顯示架構圖。
- canonical、語言版本、內部連結及 breadcrumb 正確。
- 375／768／1280 px 無橫向 overflow、孤字行或不可操作控制項。
- 頁面沒有外部 runtime script、style、font 或 image 請求。

### Step 9：人工 Review

機械 Gate 全綠後仍需人工確認：

- one-liner 是否讓非開發者理解。
- 截圖是否真實、無敏感資料且不是 mockup。
- 驗證徽章是否符合 Evidence，而非行銷升級。
- 限制、外連、遙測、費用風險及退場方式是否醒目。
- upstream 名稱、商標、license 與 attribution 是否正確。

人工 review 不得覆蓋機械失敗；兩者都通過才可發布。

## 五、驗證等級與網站語意

| 等級 | 網站可以說 | 網站不可說 |
|---|---|---|
| Discovered | 已發現；若有 Pack，可說特定環境部署與驗收結果 | 社群背書、安全、穩定、適合所有人 |
| Community Verified | 至少一位具名驗證者完成真實使用故事與必要證據 | 無限制、絕對安全、永續效益已證實 |
| SmallGreen Ready | 符合對應 Spec 版本的完整機械條件及 Agent 紀錄 | 永久相容、未來版本自動通過 |

每頁必須顯示 `spec_version`、`last_verified` 與 `verified_commit`／Evidence reference，讓過期驗證可辨識。

## 六、變更類型

### 新增專案

走完整九步流程；不得只新增 YAML 或首頁卡片。

### 更新既有專案

- upstream commit、部署結果或資源條件改變：新 Evidence Pack → 重生卡片。
- 名稱、one-liner、分類或維護狀態改變：更新 `EDITORIAL` → 重生卡片。
- Profile／外連／secret 改變：先更新 adapter contract 與 conformance → 必要時重驗 → 重生卡片。

### 移除或封存

不得直接刪除歷史 Evidence。服務卡標示 `archived` 或移入歷史索引，保留已發布版本、日期與替代方案；真正刪除需另依治理政策決定。

## 七、Agent 完成回報格式

後續 Agent 完成新專案發布工作時，必須回報：

```text
Project:
Upstream + locked commit:
License:
Profile:
Adapter conformance:
Evidence Pack:
Deployment acceptance:
Verifier result:
Teardown + zero diff:
Generated card:
Registry checks:
Site preview checks:
Known limitations:
Files changed:
Not performed (push/deploy/external publication):
```

「完成」只代表上述適用 Gate 已實際通過，不代表僅建立檔案或送出指令。

---

文件版本：v1.0  
定稿日期：2026-08-03  
Owner：SmallGreen Cloud maintainers
