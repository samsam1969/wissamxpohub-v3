# WissamXpoHub V3 — Project Handoff Document
## Date: 2026-04-20 | Continue from this point

---

## PROJECT OVERVIEW
**Platform:** WissamXpoHub V3 — Egyptian Export Intelligence SaaS
**Stack:** Flask (port 4000) + Vanilla HTML/CSS/JS + Supabase Auth + Claude API
**Location:** C:\Users\DELL\Desktop\wissamxpohub-backend\
**Python:** 3.14 in venv | PowerShell workflow

---

## ENVIRONMENT (.env keys)
- ANTHROPIC_API_KEY: configured
- SUPABASE_URL: https://hfvhivxpaqnqaooyqmaw.supabase.co
- SUPABASE_SERVICE_KEY: configured
- TAVILY_API_KEY: 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
- LIGHTPANDA_TOKEN: 5bf6645d003e036f378fb43006e1e9af0f16f84a75c3fb4b7d33b5e3b26db22a
- B2B_EMAIL: wissamxpo@outlook.com
- WHATSAPP: 201116415272

---

## ARCHITECTURE — 5 DATA LAYERS
Layer 0: Knowledge Base (Supabase) — highest priority
Layer 1a: ITC TradeMap (Lightpanda) — 2020-2024
Layer 1b: UN Comtrade API (free) — 2020-2023
Layer 2: Tavily Web Intelligence — 2024-2026
Layer 3: Pricing Engine (calculated)
Layer 4: Claude Sonnet Analysis

---

## SUBSCRIPTION PLANS
- Free:    0 EGP  | 1 report/month
- Starter: 299 EGP | 5 reports/month + Blog + Scanner
- Pro:     599 EGP | 25 reports/month + all features + Buyers
- Agency:  1490 EGP | 100 reports/month + all features

---

## KEY FILES
- main.py — Flask app + blueprints + monthly reset scheduler
- services/claude_service.py — 5-layer analysis
- services/credits_service.py — subscription system
- services/knowledge_service.py — Knowledge Base
- services/tavily_service.py — Tavily integration
- services/trade_data_service.py — Comtrade API
- services/trademap_service.py — TradeMap scraping
- routers/ai.py — AI endpoints
- routers/admin.py — Admin + CRM + check-feature endpoints
- routers/buyers.py — Europages scraping
- WissamXpoHub_V3_Frontend_FIXED.html — Main dashboard
- Blog.html — Blog (locked for free users)
- ExportOpportunityScanner.html — Scanner (Starter+)
- PotentialBuyers.html — Buyers (Pro+)
- admin_knowledge.html — Knowledge Base Admin Panel
- admin_crm.html — Admin CRM page

---

## SUPABASE TABLES
- user_profiles — user data + notes
- user_plans — subscription + credits
- upgrade_requests — upgrade requests
- report_history — report logs
- knowledge_base — internal data
- blog_posts, blog_files — blog content

---

## ADMIN ACCOUNTS
- wissamxpo@outlook.com — Agency (9999 reports) — ADMIN
- aegyptusxpo@gmail.com — Free (1 report/month) — TEST

---

## COMPLETED FEATURES
- 5-layer AI report system with confidence scores
- Subscription system (Free/Starter/Pro/Agency)
- Blog locked for free users (backend verified)
- Scanner locked for Starter+ (backend verified)
- Buyers locked for Pro+ (backend verified)
- WhatsApp upgrade button
- Free trial banner
- Upgrade Modal (3 plans)
- Plan bar (credits display)
- Knowledge Base Admin Panel (with file upload)
- Admin CRM page (user management)
- Monthly reset scheduler (Python thread)
- User registration with full profile
- Language toggle button (partial - UI only)
- PDF export + Copy button

---

## PENDING ISSUES
1. Admin links (CRM + KB) not showing in dashboard
   - Token exists: wissamxpo@outlook.com confirmed in localStorage
   - Fix: adminLinks display:none not switching to inline-flex
   - File: WissamXpoHub_V3_Frontend_FIXED.html
   - Look for: adminLinks + DOMContentLoaded

2. Deployment on Render.com (not done yet)

3. Language system incomplete (toggle exists, full translation pending)

---

## START COMMAND
cd C:\Users\DELL\Desktop\wissamxpohub-backend
.\venv\Scripts\Activate.ps1
python main.py

## KB MANAGER
python kb_manager.py

## ADMIN PAGES
http://localhost:4000/admin/crm
http://localhost:4000/admin/knowledge

---

## MESSAGE TO CONTINUE
"اكمل WissamXpoHub V3 — ارفع ملف الـ handoff وابدأ بإصلاح ظهور روابط Admin في الداشبورد ثم Deployment"
