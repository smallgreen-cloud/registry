# SmallGreen 候選：Audio Notes

狀態：Candidate。原碼與 Sites-only Agent Install Contract 已公開；正式部署驗收與 SmallGreen Ready 晉級仍待完成。此頁不是 Ready 徽章。

提交日期：2026-09-15；提交帳號：`ai-cooperation`。

## 公開介紹

**自己的會議自己記！** 用自己的ChatGPT Work整理錄音、校正專業詞彙，留下逐字稿、摘要與待辦。私人資料保存在自己的Sites；語音轉錄使用自己的Groq免費額度。

適用：帳戶實際具備Work／Sites、願意首次在後台設定Groq Key的使用者。SB是選用知識來源；待辦、行事曆與Gmail是可交接的後續工作。

## English listing copy

**Your meetings, your notes.** Use your own ChatGPT Work to turn recordings into transcripts, contextual terminology corrections, meeting summaries and follow-up tasks. Store your data in your private Sites deployment and use your own Groq account for speech recognition.

Requires actual Work/Sites access and initial Groq key setup. Audio is sent to Groq. No verified remote OAuth MCP connection, unattended next-day processing, or zero-configuration deployment is promised.

## 提交位置與資格

- 公開原碼：[ai-cooperation/audio-notes-sites](https://github.com/ai-cooperation/audio-notes-sites)。
- 版本：0.1.0 開源候選；部署來源鎖定 commit：[`b484d674c8572ecfaf8f9649484fa59db98e2250`](https://github.com/ai-cooperation/audio-notes-sites/tree/b484d674c8572ecfaf8f9649484fa59db98e2250)；候選安裝契約 commit：[`9d29844c858c3619dda9d98e1aa5ddc3d42e3e76`](https://github.com/ai-cooperation/audio-notes-sites/tree/9d29844c858c3619dda9d98e1aa5ddc3d42e3e76)。
- 自有程式採 [MIT](https://github.com/ai-cooperation/audio-notes-sites/blob/d25f8a5998418f28cc9d8ade99fe89eb12ee179a/LICENSE)，保留第三方聲明；155 份原碼與文件，全新單一 root 歷史，不含私人營運庫。
- [Work 部署契約](https://github.com/ai-cooperation/audio-notes-sites/blob/d25f8a5998418f28cc9d8ade99fe89eb12ee179a/docs/WORK_DEPLOY.md)與[限制](https://github.com/ai-cooperation/audio-notes-sites/blob/d25f8a5998418f28cc9d8ade99fe89eb12ee179a/docs/LIMITATIONS.md)必須一起閱讀。
- 候選介紹提交 `smallgreen-cloud/registry/candidates/audio-notes-sites.md`。
- 正式網站由 `smallgreen-cloud/site` 的既有生成流程發布，不另建手工頁。
- Sites 是唯一託管環境，Work 是互動執行端；不要求使用者建立外部 Cloudflare 帳號、提供 Cloudflare API Token、部署 GitHub Actions 或其他主機。Groq 是執行期語音辨識 API，Key 只由使用者登入部署後網站自行貼入後台。
- [候選 Agent Install Contract](https://github.com/ai-cooperation/audio-notes-sites/blob/9d29844c858c3619dda9d98e1aa5ddc3d42e3e76/.smallgreen/install.yaml) 已把一句話觸發、Sites 資源、確認、Secret 邊界、部署步驟、分階段驗收及 blockers 機械化。

遵循 [發布標準](https://github.com/smallgreen-cloud/registry/blob/main/PROJECT_PUBLISHING_STANDARD.md)：公開授權來源與鎖定版本→adapter契約→conformance→真實部署/驗收/獨立複驗/teardown→append-only evidence→generator→registry gate→雙語網站→人工review。任何門檻未過，維持候選。

待補：新帳戶傳檔授權、真實E2E、正式資源基線與刪除驗證、相容profile、第三方依賴完整檢視。現行截圖只為未登入預覽，不能充當真實部署Evidence Pack。

## 來源驗證與審查範圍

發布包 SHA-256：`d9136da8ce8a466d2b55ea6948d0009e2a737eb6efa02bc5aaf28c35c6dc7499`。本機核對 155 份 tracked 檔案與發布包逐位元一致；GitHub API 已讀回上述 commit 與 tree `789b5b373fe500697d4a70c798ec4792e8700990`。

原有測試及掃描範圍見 [release](https://github.com/ai-cooperation/audio-notes-sites/tree/d25f8a5998418f28cc9d8ade99fe89eb12ee179a/release)。這些是原碼與隔離測試紀錄，Groq 回應為模擬；不是 SmallGreen Evidence Pack，也不是全新帳戶端對端部署驗收。

此候選請維護者審查 Sites 託管資源與 Work 執行端的 profile 適配方式。正式收錄仍須完成上列門檻。

## 2026 年 9 月 17 日部署交接修正

本次只更新研究卡、複製提示與 `install.json` 的操作規則，不變更應用程式版本，也不宣稱修復安裝腳本或取得真實部署證據。

1. **先檢查再建資源**：目前 agent 必須有 Work／Sites 原生工具。核對環境、文件、乾淨安裝及建置後才建立 Site、D1、R2；前置檢查失敗即停，不以 CLI 名稱或首頁 HTTP 200 判定有部署能力。
2. **分開解析兩個固定版本**：應用程式仍是 `b484d674c8572ecfaf8f9649484fa59db98e2250`，`.smallgreen/` 契約文件從 `9d29844c858c3619dda9d98e1aa5ddc3d42e3e76` 讀取。`agent_install.documents` 提供完整固定網址，禁止默默切換 main 或把應用目錄缺檔誤報為主契約失效。
3. **揭露安裝限制**：macOS 14.6、Bash 3.2、Sites 0.1.65 portable 的文件安裝路徑失敗，不能把此結果外推成所有 Linux 失敗。乾淨安裝因下載逾時未完成；重用既有依賴的建置成功不能替代乾淨安裝。
4. **本人操作與 agent 授權分開**：Groq Key 只由本人在私人網站設定。網站登入不會自動授權 agent 傳檔；授權不可用即停止錄音階段，不改成公開網站、不偽造身分、不在聊天索取憑證。
5. **三階段分別回報**：私人網站部署、本人 Groq 設定、合法傳檔與真實音訊驗收，各自標示 passed／failed／blocked／not_run。模擬 Groq、模型完成審查、schema 通過或首頁 HTTP 200 都不能替代實際部署及使用驗收。

### 本機觀測的證據範圍

這是 2026 年 9 月 17 日原碼與本機檢查摘要，**不是 SmallGreen Evidence Pack**。

| 檢查 | 結果與界線 |
| --- | --- |
| 固定來源 | main／契約為 `9d29844`；應用為 `b484d67`；兩者產品程式及依賴鎖檔一致 |
| macOS helper | Sites 0.1.65 的文件路徑 exit 69，訊息要求 Linux flock、GNU timeout；系統 Bash 3.2 對腳本 coproc 的語法檢查 exit 2 |
| 乾淨安裝補救 | frozen install 首次下載逾時；同 checkout／lockfile 一次 180 秒重試仍未完成，不能算 PASS |
| 重用依賴 | 相同 package／lockfile／workspace 雜湊下，型別、workflow／queue／remote-mcp 測試及正式建置通過；本機首頁 200，未登入 API 與 MCP 401 |
| 模擬音訊 | 本機隔離 Miniflare D1／R2、模擬身分及 mock Groq；合成 1 秒音檔完成四文件保存與讀回。Synthetic for testing only；不能推論真實辨識品質或雲端授權成功 |
| readiness 故障注入 | 主加密金鑰格式錯誤時觀察到 storageReady 為 true、保存 HTTP 400；不是有效 Key 必定失敗。部署應驗證 32-byte 主金鑰及加密操作，不能只看非空設定 |
| 未驗收 | 受管 Linux 乾淨安裝、新學員帳戶發布、真實登入與 Groq、完整備份還原及移除 |

原碼依據：[安裝腳本](https://github.com/ai-cooperation/audio-notes-sites/blob/b484d674c8572ecfaf8f9649484fa59db98e2250/scripts/install-pnpm.sh)、[Work 部署與授權界線](https://github.com/ai-cooperation/audio-notes-sites/blob/b484d674c8572ecfaf8f9649484fa59db98e2250/docs/WORK_DEPLOY.md)、[安裝契約](https://github.com/ai-cooperation/audio-notes-sites/blob/9d29844c858c3619dda9d98e1aa5ddc3d42e3e76/.smallgreen/install.yaml)、[驗收契約](https://github.com/ai-cooperation/audio-notes-sites/blob/9d29844c858c3619dda9d98e1aa5ddc3d42e3e76/.smallgreen/acceptance.yaml)、[維護契約](https://github.com/ai-cooperation/audio-notes-sites/blob/9d29844c858c3619dda9d98e1aa5ddc3d42e3e76/.smallgreen/maintenance.yaml)。
