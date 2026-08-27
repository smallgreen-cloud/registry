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
    "tapcard-mcp": "ai-cooperation/tapcard-mcp",
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
        "maintenance_status": "active", "license": "Apache-2.0",
    },
    "tapcard-mcp": {
        "name": "TapCard MCP", "one_liner": "自架 NFC／QR 電子名片＋私人 AI 名片庫：公開頁掃即得，收到的名片存自己帳號",
        "categories": ["sharing"],
        "components": ["workers", "d1", "r2", "kv"],
        "maintenance_status": "active", "license": "Apache-2.0",
    },
    "microfeed": {
        "name": "microfeed", "one_liner": "輕量 feed/CMS（JSON/RSS feed＋admin 後台；無 R2 文字模式收錄版）",
        "categories": ["publishing"],
        "components": ["workers", "d1"],
        "maintenance_status": "active",  # 2026-02-13（約 5.6 個月）
    },
}

# 給人看的服務卡摘要；技術契約仍由 profile／Evidence 提供，這裡只回答
# 「這是什麼專案、解決什麼問題、適合誰、可以做什麼、部署前要知道什麼」。
PRODUCT_SUMMARY = {
    "sink": {
        "project_type": {"zh-tw": "自架短網址與造訪統計服務", "en": "A self-hosted URL shortener with visit analytics"},
        "problem": {"zh-tw": "活動與分享連結依賴第三方短網址，企業無法掌握連結與基本統計", "en": "Campaign and sharing links depend on a third-party shortener, leaving the business without control of links and basic statistics"},
        "audience": {"zh-tw": ["需要品牌短網址的小型企業", "活動與行銷團隊"], "en": ["Small businesses that need branded links", "Event and marketing teams"]},
        "capabilities": {"zh-tw": ["建立短網址與轉址", "在自己的帳號儲存彙總造訪統計", "由部署者維護連結與資料"], "en": ["Create short links and redirects", "Store aggregate visit statistics in your own account", "Maintain links and data under the deployer's control"]},
        "deployment_requirements": {"zh-tw": ["需要自己的 Cloudflare 帳號", "需要 Workers、KV；統計功能需要 Analytics Engine"], "en": ["Your own Cloudflare account", "Workers and KV; Analytics Engine for statistics"]},
        "limitations": {"zh-tw": ["轉址目標由使用者自行提供與負責", "統計受平台保留政策與免費額度限制"], "en": ["The deployer is responsible for destination URLs", "Statistics remain subject to platform retention and free-tier limits"]},
    },
    "uptimeflare": {
        "project_type": {"zh-tw": "自架網站與 API 監測、狀態頁服務", "en": "A self-hosted website and API monitor with a public status page"},
        "problem": {"zh-tw": "小型團隊通常在客戶回報後才知道服務中斷，缺少可查的狀態歷史", "en": "Small teams often learn about outages from customers and lack a simple status history to inspect"},
        "audience": {"zh-tw": ["小型 SaaS 團隊", "接案工作室與需要公開狀態頁的服務商"], "en": ["Small SaaS teams", "Studios and service providers that need a public status page"]},
        "capabilities": {"zh-tw": ["定期探測指定網址", "保存 D1 狀態歷史", "提供公開狀態頁與可選通知"], "en": ["Probe configured URLs on a schedule", "Store status history in D1", "Publish a status page with optional notifications"]},
        "deployment_requirements": {"zh-tw": ["需要 Cloudflare Workers、Pages、D1、KV 與 Cron", "需要自行設定被監測網址與通知方式"], "en": ["Cloudflare Workers, Pages, D1, KV and Cron", "The deployer configures monitored URLs and notification targets"]},
        "limitations": {"zh-tw": ["不是完整的 incident management 或 SLA 平台", "探測頻率受帳號額度與排程限制"], "en": ["It is not a full incident-management or SLA platform", "Probe frequency is limited by account quotas and schedules"]},
    },
    "counterscale": {
        "project_type": {"zh-tw": "自架網站流量分析服務", "en": "A self-hosted website analytics service"},
        "problem": {"zh-tw": "網站需要基本流量洞察，但不想把分析資料交給外部 SaaS", "en": "A website needs basic traffic insight without handing its analytics data to a hosted SaaS"},
        "audience": {"zh-tw": ["公司官網與內容網站", "重視資料掌控的小型團隊"], "en": ["Company and content websites", "Small teams that want control of analytics data"]},
        "capabilities": {"zh-tw": ["收集網站使用統計", "在自己的 Analytics Engine 查詢分析", "以低維運方式提供分析儀表板"], "en": ["Collect website usage metrics", "Query analytics in your own Analytics Engine", "Operate a lightweight analytics dashboard"]},
        "deployment_requirements": {"zh-tw": ["需要 Cloudflare Workers 與 Analytics Engine", "需要在網站加入分析程式碼或事件入口"], "en": ["Cloudflare Workers and Analytics Engine", "A site integration or event endpoint is required"]},
        "limitations": {"zh-tw": ["不等同完整的使用者行為重播或行銷自動化平台", "分析保存與查詢能力受平台政策限制"], "en": ["It is not a full session-replay or marketing-automation platform", "Retention and query capability follow platform policies"]},
    },
    "newsnow": {
        "project_type": {"zh-tw": "自架新聞來源聚合與排行網站", "en": "A self-hosted news-source aggregator and ranking site"},
        "problem": {"zh-tw": "團隊需要持續掌握多個來源，卻沒有簡單且可自有部署的閱讀入口", "en": "A team needs to follow many sources but lacks a simple reading entry point it can deploy and control"},
        "audience": {"zh-tw": ["需要產業情報的小型企業", "研究、內容與社群團隊"], "en": ["Small businesses tracking industry news", "Research, content and community teams"]},
        "capabilities": {"zh-tw": ["聚合多個新聞來源", "把可重建的來源快取存入自己的 D1", "依來源與排行提供閱讀入口"], "en": ["Aggregate multiple news sources", "Cache rebuildable source data in your own D1", "Provide a source and ranking view for reading"]},
        "deployment_requirements": {"zh-tw": ["需要 Cloudflare Pages 與 D1", "需要自行維護來源清單與來源可用性"], "en": ["Cloudflare Pages and D1", "The deployer maintains the source list and accepts source availability risk"]},
        "limitations": {"zh-tw": ["只保存來源快取，不擁有第三方新聞內容", "更新速度受來源 RSS 與排程影響"], "en": ["It caches source data but does not own third-party news content", "Freshness depends on source feeds and schedules"]},
    },
    "pastebin-worker": {
        "project_type": {"zh-tw": "自架文字貼上、短網址與分享服務", "en": "A self-hosted paste, short-link and sharing service"},
        "problem": {"zh-tw": "開發與營運團隊需要暫時分享文字或連結，不想使用不可控的第三方貼上服務", "en": "Development and operations teams need to share text or links temporarily without relying on an uncontrolled third-party paste service"},
        "audience": {"zh-tw": ["開發與維運團隊", "需要簡單分享入口的小型公司"], "en": ["Development and operations teams", "Small companies that need a simple sharing endpoint"]},
        "capabilities": {"zh-tw": ["以 curl 建立與讀取文字內容", "產生短網址與管理連結", "依期限讓內容自動過期"], "en": ["Create and read text with curl", "Generate short links and management links", "Expire content after a configured lifetime"]},
        "deployment_requirements": {"zh-tw": ["需要 Cloudflare Worker 與 KV", "部署者要決定內容可見性與過期政策"], "en": ["A Cloudflare Worker and KV", "The deployer chooses visibility and expiration policies"]},
        "limitations": {"zh-tw": ["目前免費層降級版不支援 R2 multipart 檔案上傳", "知道連結的人可能可以讀取內容，需先確認分享邊界"], "en": ["The free-tier fallback does not support R2 multipart uploads", "Anyone with a readable link may access content, so sharing boundaries must be reviewed"]},
    },
    "hananalytics": {
        "project_type": {"zh-tw": "輕量自架網站分析儀表板", "en": "A lightweight self-hosted website analytics dashboard"},
        "problem": {"zh-tw": "中小企業需要看懂網站流量，但不想導入複雜或過度追蹤的分析平台", "en": "Small businesses need understandable website metrics without adopting a complex or overly tracking-heavy analytics platform"},
        "audience": {"zh-tw": ["中文網站經營者", "需要基本流量報表的中小企業"], "en": ["Chinese-language website operators", "Small businesses that need basic traffic reports"]},
        "capabilities": {"zh-tw": ["收集頁面與地區等基本事件", "用 Analytics Engine 查詢資料", "提供輕量儀表板與可選密碼保護"], "en": ["Collect basic page and geography events", "Query data through Analytics Engine", "Provide a lightweight dashboard with optional password protection"]},
        "deployment_requirements": {"zh-tw": ["需要 Pages Functions 與 Analytics Engine", "要自行決定儀表板是否需要密碼保護"], "en": ["Pages Functions and Analytics Engine", "The deployer must choose whether dashboard protection is required"]},
        "limitations": {"zh-tw": ["不是完整的產品分析或使用者行為重播平台", "未設定保護時，儀表板與回報入口可能是公開的"], "en": ["It is not a full product-analytics or session-replay platform", "Without protection, the dashboard and collection endpoint may be public"]},
    },
    "serverless-dns": {
        "project_type": {"zh-tw": "自架 DNS over HTTPS 解析服務", "en": "A self-hosted DNS-over-HTTPS resolver"},
        "problem": {"zh-tw": "個人或小型團隊需要可自訂的 DNS 解析與封鎖清單入口", "en": "Individuals and small teams need a customizable DNS resolver and blocklist endpoint"},
        "audience": {"zh-tw": ["需要自訂 DNS 的小型團隊", "希望減少第三方解析依賴的技術使用者"], "en": ["Small teams that need custom DNS", "Technical users who want less dependence on third-party resolvers"]},
        "capabilities": {"zh-tw": ["提供 DoH 解析端點", "使用建置時封裝的封鎖清單", "以無狀態方式處理請求"], "en": ["Provide a DoH resolver endpoint", "Use blocklists packaged at build time", "Process requests without storing query history by default"]},
        "deployment_requirements": {"zh-tw": ["需要 Cloudflare Worker", "需要自行維護封鎖清單與解析政策"], "en": ["A Cloudflare Worker", "The deployer maintains blocklists and resolver policies"]},
        "limitations": {"zh-tw": ["不是完整的企業 DNS 管理平台", "封鎖清單更新與錯誤分類需要自行維護"], "en": ["It is not a full enterprise DNS-management platform", "Blocklist updates and false-positive handling remain the deployer's responsibility"]},
    },
    "rin": {
        "project_type": {"zh-tw": "自架個人或小型團隊發布平台", "en": "A self-hosted publishing platform for individuals or small teams"},
        "problem": {"zh-tw": "內容、評論與 RSS 依賴外部平台，團隊想保留自己的發布資料與流程", "en": "Content, comments and RSS depend on an external platform while the team wants to keep its publishing data and workflow"},
        "audience": {"zh-tw": ["個人品牌與內容團隊", "需要簡單發布能力的小型企業"], "en": ["Personal brands and content teams", "Small businesses that need simple publishing"]},
        "capabilities": {"zh-tw": ["管理文章、評論與 RSS", "以 Queue 處理背景摘要工作", "在自己的 Cloudflare 帳號保存內容"], "en": ["Manage posts, comments and RSS", "Process background summaries with a Queue", "Keep content in the deployer's Cloudflare account"]},
        "deployment_requirements": {"zh-tw": ["需要 Workers、D1、Queues 與 Cron", "AI 摘要功能需要另外確認 Workers AI 與額度"], "en": ["Workers, D1, Queues and Cron", "AI summaries require separate review of Workers AI and quotas"]},
        "limitations": {"zh-tw": ["定位是輕量發布平台，不是企業 CMS", "AI 摘要不是必要核心功能，會增加資源與維護範圍"], "en": ["It is a lightweight publishing platform, not an enterprise CMS", "AI summaries are optional and expand resource and maintenance scope"]},
    },
    "second-brain-cloudflare": {
        "project_type": {"zh-tw": "自架個人知識庫與 MCP 服務", "en": "A self-hosted personal knowledge base with an MCP server"},
        "problem": {"zh-tw": "筆記與知識散落在不同工具，AI 無法透過受控介面搜尋自己的內容", "en": "Notes and knowledge are scattered across tools and AI lacks a controlled interface to search them"},
        "audience": {"zh-tw": ["顧問、研究者與創作者", "需要保留工作記憶的小型團隊"], "en": ["Consultants, researchers and creators", "Small teams that need durable working knowledge"]},
        "capabilities": {"zh-tw": ["保存筆記與知識關聯", "提供關鍵字搜尋與 MCP 存取", "以自己的 D1 與 KV 管理資料及授權"], "en": ["Store notes and knowledge relationships", "Provide keyword search and MCP access", "Manage data and authorization in your own D1 and KV"]},
        "deployment_requirements": {"zh-tw": ["需要 Cloudflare Worker、D1 與 KV", "需要自行設定 MCP 授權與備份方式"], "en": ["A Cloudflare Worker, D1 and KV", "The deployer configures MCP authorization and backups"]},
        "limitations": {"zh-tw": ["目前是關鍵字搜尋降級版，不等同向量搜尋", "資料保留與備份責任由部署者承擔"], "en": ["The catalogue profile is keyword-search based, not vector search", "The deployer owns retention and backup responsibilities"]},
    },
    "cloudflare-imgbed": {
        "project_type": {"zh-tw": "自架圖片與檔案管理入口", "en": "A self-hosted image and file management entry point"},
        "problem": {"zh-tw": "網站圖片與檔案管理依賴外部圖床，連結與中繼資料不在自己的帳號", "en": "Website images and files depend on a hosted image service, leaving links and metadata outside the deployer's account"},
        "audience": {"zh-tw": ["小型網站與內容團隊", "需要簡單圖床管理的創作者"], "en": ["Small websites and content teams", "Creators who need a simple image-management tool"]},
        "capabilities": {"zh-tw": ["管理圖片中繼資料與分享連結", "在自己的 KV 保存管理資料", "以降級模式配合外部圖片網址"], "en": ["Manage image metadata and sharing links", "Store management metadata in your own KV", "Operate in a fallback mode using external image URLs"]},
        "deployment_requirements": {"zh-tw": ["需要 Cloudflare Worker 與 KV", "部署者要確認外部圖片來源與連結可用性"], "en": ["A Cloudflare Worker and KV", "The deployer reviews external image origins and link availability"]},
        "limitations": {"zh-tw": ["目前卡片是外鏈降級模式，不等於私有二進位儲存", "外部圖片來源失效時，服務無法保證內容可用"], "en": ["The catalogue card describes an external-link fallback, not private binary storage", "Content availability depends on external image origins"]},
    },
    "microfeed": {
        "project_type": {"zh-tw": "自架輕量內容發布與 RSS 平台", "en": "A self-hosted lightweight publishing and RSS platform"},
        "problem": {"zh-tw": "小型組織需要自己的內容與 feed 入口，不想維護大型 CMS", "en": "A small organization needs its own content and feed entry point without maintaining a large CMS"},
        "audience": {"zh-tw": ["個人品牌、協會與小型團隊", "需要文字發布與 RSS 的網站"], "en": ["Personal brands, associations and small teams", "Websites that need text publishing and RSS"]},
        "capabilities": {"zh-tw": ["管理文字內容與管理後台", "輸出 JSON 與 RSS feed", "將內容與管理資料保存於自己的 D1"], "en": ["Manage text content through an admin interface", "Publish JSON and RSS feeds", "Keep content and administration data in your own D1"]},
        "deployment_requirements": {"zh-tw": ["需要 Cloudflare Workers 與 D1", "目前收錄設定是不使用 R2 的文字模式"], "en": ["Cloudflare Workers and D1", "The catalogue profile uses the no-R2 text-only mode"]},
        "limitations": {"zh-tw": ["目前文字模式停用媒體上傳", "不是高流量新聞或企業內容管理平台"], "en": ["Media upload is disabled in the text-only profile", "It is not a high-traffic news or enterprise content-management platform"]},
    },
    "business-card-mcp": {
        "project_type": {"zh-tw": "自架 AI 聯絡人與名片管理 MCP", "en": "A self-hosted AI contact and business-card MCP"},
        "problem": {"zh-tw": "收到的名片與聯絡資料散落各處，人工整理後仍難以在 AI 對話中查找", "en": "Received business cards and contact details are scattered, and manual entry still leaves them hard to find in AI conversations"},
        "audience": {"zh-tw": ["顧問與業務工作者", "需要自己掌握聯絡資料的小型企業"], "en": ["Consultants and sales professionals", "Small businesses that need control of contact data"]},
        "capabilities": {"zh-tw": ["在 AI 工具中辨識與整理名片", "把聯絡人保存到自己的 D1 與 R2", "提供私人搜尋與名片詳情"], "en": ["Identify and organize cards in AI tools", "Store contacts in your own D1 and R2", "Provide private contact search and details"]},
        "deployment_requirements": {"zh-tw": ["需要自己的 Cloudflare Workers、D1、R2 與 KV", "目前以單人自架與 Remote MCP 連線為主要情境"], "en": ["Your own Cloudflare Workers, D1, R2 and KV", "The current target is single-owner self-hosting with a Remote MCP connection"]},
        "limitations": {"zh-tw": ["目前不是多人 CRM 或完整銷售自動化平台", "名片辨識與 AI 使用仍需部署者確認資料與權限邊界"], "en": ["It is not a multi-user CRM or full sales-automation platform", "The deployer must review data and permission boundaries for card recognition and AI use"]},
    },
    "tapcard-mcp": {
        "project_type": {"zh-tw": "自架 NFC／QR 電子名片與私人名片庫 MCP", "en": "A self-hosted NFC/QR business card and private card-wall MCP"},
        "problem": {"zh-tw": "紙本名片會過時，公開個人資訊與收到的聯絡資料也缺少同一個可控入口", "en": "Paper cards become outdated, while public profile sharing and received contacts lack one controlled entry point"},
        "audience": {"zh-tw": ["顧問、業務與自由工作者", "需要公開名片又要保留私人聯絡資料的小型團隊"], "en": ["Consultants, sales professionals and freelancers", "Small teams that need public profiles and private contact storage"]},
        "capabilities": {"zh-tw": ["發布 NFC／QR 公開電子名片", "下載 vCard 並分享公開個人頁", "預覽、確認、匯入、搜尋與匯出私人名片"], "en": ["Publish an NFC/QR public business card", "Share a public profile and download vCards", "Preview, confirm, import, search and export private cards"]},
        "deployment_requirements": {"zh-tw": ["需要自己的 Workers、D1、R2 與 KV", "需要部署者管理憑證，私人 MCP key 只能由部署者保存"], "en": ["Your own Workers, D1, R2 and KV", "The deployer manages the admin credential and private MCP keys"]},
        "limitations": {"zh-tw": ["目前尚未支援向量搜尋、多人團隊與 NFC 寫卡 App", "URL 匯入只適用於符合規格的公開 TapCard"], "en": ["Vector search, multi-user teams and an NFC-writing app are not in the current scope", "URL import is limited to public TapCards that meet the contract"]},
    },
}


def latest_pack(pid: str) -> dict:
    """卡片的機械欄位取自「最新的一份 Pack」——依事件日期＋提交時刻排序，不用檔名。

    檔名排序會出錯：同日的 `…-shots-01` 排在 `…-sandbox-02` 之後，卡片的 spec_version／
    等級／成熟度就被截圖用 Pack 主導（2026-08-03 second-brain 實際踩到）。
    """
    packs = sorted((REG / "evidence" / pid).glob("*.json"))
    if not packs:
        raise SystemExit(f"{pid}: 無 Evidence Pack")

    def key(p):
        d = json.loads(p.read_text(encoding="utf-8"))
        return ((d.get("deploy_event") or {}).get("date") or "",
                d.get("submitted_at") or "", p.name)

    newest = max(packs, key=key)
    return json.loads(newest.read_text(encoding="utf-8")), newest


def clip(text: str, limit: int = 200) -> str:
    """在句讀邊界截斷並補省略號——直接切會停在半句（「binding 不存在才」），讀者無法判斷是被截還是寫壞。"""
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    head = text[:limit]
    cut = max(head.rfind(c) for c in "。；！？;.")
    return (head[:cut + 1] if cut > limit // 2 else head.rstrip()) + "…"


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
        "product_summary": PRODUCT_SUMMARY[pid],
        "categories": ed["categories"],
        "profile": prof["profile"],
        "repo": repo,
        "components": {"cloudflare": ed["components"]},
        "login_method": prof.get("login_method", "none"),
        "data_flow": {
            "external_services": ext,
            "disclosure": clip(prof.get("data", {}).get("notes") or prof.get("summary", {}).get("purpose") or ""),
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
    # 截圖取自「最新一份**帶截圖**的 Pack」，不是最新的 Pack——驗證輪與截圖輪常是不同 Pack，
    # 只看最新一份會讓卡片在下一次驗證後掉圖（2026-08-03 second-brain 實際踩到）。
    for pp in reversed(all_packs):
        shot = (json.loads(pp.read_text(encoding="utf-8")).get("screenshots") or {}).get("app_png")
        if shot:
            card["images"] = {"screenshot": {"path": shot["path"],
                                             "evidence_pack_ref": str(pp.relative_to(REG))}}
            break
    if card["free_tier_grade"] in ("C", "D"):
        notes = pack["free_tier"].get("quota_notes") or []
        quota = next((n for n in notes if any(k in n for k in ("額度", "/day", "limit", "Neurons", "writes"))), None)
        if quota:
            card["quota_note"] = clip(quota)
    return card


def main():
    out = REG / "cards"
    out.mkdir(exist_ok=True)
    for pid in list(PROJECTS) + list(FIRST_PARTY):
        card = build_card(pid)
        (out / f"{pid}.yaml").write_text(
            "# 機械生成（tools/gen_cards.py）——editorial 欄位改 EDITORIAL 字典後重生，勿直接手改推導欄位\n"
            + yaml.safe_dump(card, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"generated {len(PROJECTS) + len(FIRST_PARTY)} cards（含 {len(FIRST_PARTY)} 張 first-party）")


if __name__ == "__main__":
    main()
