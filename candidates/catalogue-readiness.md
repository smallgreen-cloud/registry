# SmallGreen 全量案例 readiness

> 本檔是把開源小型專案整理成可自己運行服務的內容與案例工作清單，不是服務目錄。候選專案即使列在本檔，也不得視為已收錄、已驗證或可直接部署。

## 目的

全量整理 SmallGreen 的候選池，先讓想使用專案的人看懂用途與適合對象，再進入契約、conformance、真實部署、teardown 與 Evidence Pack。正式站分層 render `cards/` 的 Registry service cards、`onboarding/first-party.yaml` 與 `research-cases.yaml`；研究案例會獨立標示，不會混入正式服務目錄。

服務卡固定回答：

- 這是什麼專案
- 解決什麼問題
- 適合誰
- 可以做什麼
- 部署前要準備什麼
- 開始前要知道哪些限制
- 架構與資料流

## 工作狀態

| 狀態 | 意義 | 可否進正式服務目錄 |
|---|---|---|
| `catalogue-card` | 已存在 Registry card，受 schema、Evidence 與 Registry gate 管理；卡片內另有 Discovered／Community Verified／SmallGreen Ready 等級 | 可以，依驗證等級顯示 |
| `first-party-onboarding` | SmallGreen 自有專案，已公開產品形狀與上架待辦 | 不可以，先獨立公開 |
| `content-research` | 有可追溯上游與授權線索，先補產品摘要、架構與部署研究 | 不可以 |
| `blocked` | 授權、上游身份、平台 Profile 或其他前置條件未解除 | 不可以 |
| `composite-later` | 需要多個單一專案或雙平台編排，保留給未來 showcase | 不可以 |

## 已完成內容層

### Registry service cards：13

目前 `cards/` 已有 13 張服務卡，包含 11 個候選池中的 Cloudflare 專案與 2 個自有 MCP 專案。服務卡的存在不等於每張都已達到相同驗證等級：

`sink`、`uptimeflare`、`counterscale`、`newsnow`、`pastebin-worker`、`hananalytics`、`serverless-dns`、`rin`、`second-brain-cloudflare`、`cloudflare-imgbed`、`microfeed`、`business-card-mcp`、`tapcard-mcp`

這些卡都必須維持 `product_summary` 雙語欄位，並由 `components`／`data_flow` 生成架構圖。

### First-party onboarding：3

目前 `onboarding/first-party.yaml` 已整理：

`homebox-edge`、`kb-vault`、`meeting-capture-kit`

它們可公開產品定位、能力、限制、架構、目前階段與待辦，但在契約、真實部署與 Evidence 完成前，不轉入 `cards/`。

## 全量候選池分層

資料來源：

- [`batch-01-cloudflare-native.md`](batch-01-cloudflare-native.md)：45 項 Cloudflare 原生軸候選，原始快照核對日 2026-07-30
- [`batch-02-github-as-runtime.md`](batch-02-github-as-runtime.md)：12 項 GitHub Actions／Issues／Pages 軸候選，原始快照核對日 2026-07-29

2026-08-27 已用 GitHub GraphQL 重新確認 55 個有明確 full name 的 repository：全部可取得，並更新授權、維護日期、星數、fork 數與封存狀態。這只完成 repository metadata refresh；進入 `content-research` 前，仍必須讀取 README、部署設定與外部服務。

### Batch 01：Cloudflare 原生軸

#### 已有 verified card：11

`Sink`、`CloudFlare-ImgBed`、`microfeed`、`serverless-dns`、`UptimeFlare`、`Rin`、`counterscale`、`second-brain-cloudflare`、`pastebin-worker`、`HanAnalytics`、`newsnow`

#### 已完成 content-research 內容研究卡：21

這些專案有已知 full name 與授權線索，先逐案補產品摘要與架構，不代表已通過 SmallGreen 驗證：

`cloud-mail`、`cloudflare_temp_email`、`ChatGPT-Telegram-Workers`、`agentic-inbox`、`moemail`、`cf-workers-status-page`、`vmail`、`serverless-cloud-notepad`、`zmail`、`roim-picx`、`AuthInbox`、`Webviso`、`imgUU`、`Gins-Blog`、`cf-files-sharing`、`d1-manager`、`ZeroLink`、`Statusflare`、`LLMKit`、`SkyPhusion LLM`、`Beam`

其中 `cf-workers-status-page` 雖有授權，但原始快照標為長期未更新；維護風險必須寫入卡片限制，不可因授權存在就排入優先部署。

`zmail` 目前已可確認為 `takumi913/zmail` 且 GitHub metadata 顯示 MIT，但只有 9 stars；它不再是身份未確認項目，仍須以 README 與部署設定判斷是否值得進入內容草稿。

#### blocked：13

- 授權未確認或沒有 license：`cf-image-hosting`、`Alle`、`mcp-memory`、`img-mom`、`cf-drop`、`rss-worker`、`cf-comment`、`Webhook Debugger`、`PageGuard`
- 上游身份待確認：`gemini-balance-do`、`linklet`
- 授權欄位為自訂／`NOASSERTION`：`CloudPaste`
- 目前 Profile 不相容：`R2-Explorer`；只有在帳號啟用 R2 且重新評估後，才可判斷是否有部署路徑

`blocked` 專案可以保留研究紀錄，但不能建立看似正式的服務卡，也不能用名稱與星數替代授權或部署證據。

### Batch 02：GitHub 當運算層／資料庫軸

#### 已完成 content-research 內容研究卡：10

先以單一專案方式整理：

`Upptime`、`metrics`、`giscus`、`PicX`、`running_page`、`blog-post-workflow`、`shot-scraper`、`gitblog`、`git-history`、`utterances`

這一軸的服務卡必須額外揭露 GitHub Actions、Issues、Discussions 或 repository 在資料流中的角色，不能套用 Cloudflare-only 的架構假設。

#### composite-later：2

`Decap CMS` 與 `osmosfeed` 涉及 GitHub＋Cloudflare 的組合或復活編排，暫不混入單一服務卡。它們未來可以成為 showcase 的組合應用，但要等單一專案案例與共用架構累積後再處理。

## 全量整理順序

1. 重新驗證所有上游與授權；候選快照只作線索。
2. ✅ 已為每個 `content-research` 專案建立雙語 `product_summary`、架構資料與研究待辦；資料存於 [`research-cases.yaml`](research-cases.yaml)。
3. 逐案讀取 README、部署設定與外部服務，將研究假設持續改成可追溯事實。
4. 具備 license、Profile、契約與部署路徑後，才建立 adapter 或 first-party contract。
5. 完成真實部署、驗收、teardown 與 Evidence Pack，才生成正式 `cards/*.yaml`。
6. 全量內容 review、Registry gate、網站 build 與 browser QA 完成後，才形成 release candidate。
7. release candidate 通過後，先部署 `smallgreen-site.pages.dev`；自訂網域另階段處理。showcase 另立專案與路由，不併入本目錄。

## 本階段不做的事

- 不把全部候選直接寫進 `cards/`。
- 不把候選名稱、星數或 README 描述當成部署證據。
- 不因使用 serverless 就直接宣稱 Green Software 成效。
- 不建立 showcase 或組合應用頁面。
- 不把研究中案例誤標成正式服務，也不在未完成部署證據前轉入 `cards/`。
