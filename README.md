[🇹🇼 中文版](README.zh-TW.md)

# AI Agent Autonomous Production Platform

> One-person team + Multi-Agent system, fully automated across 3 realms: **video production + crypto research + blog publishing + B2C legal SaaS**

**Andy Huang** — AI Agent System Engineer / Senior Software Developer

[![Resume](https://img.shields.io/badge/Resume-View-blue)](https://andyhuang1984.github.io/ai-agent-portfolio/resume.html)
[![Showcase](https://img.shields.io/badge/Showcase-Portfolio-green)](https://andyhuang1984.github.io/ai-agent-portfolio/showcase.html)
[![YouTube](https://img.shields.io/badge/YouTube-Channel-red)](https://www.youtube.com/@ShrimpCatStudio)

---

## System Architecture (3 realms)

```
Owner (1 person)
  ↓ Telegram Group / Browser
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                                                                          │
  │  🖥️ Server (RTX 5090 32GB)        💻 Mac (M2 24GB)        ☁️ Cloudflare │
  │  Cleo  — Captain / GPT-5.4       Independent Agent        Lex Legal SaaS │
  │  Ada   — Coder   / GPT-5.4-mini   GPT-5.4                  Workers + D1   │
  │  Amelia— Scout   / GPT-5.4-mini   ↓                        Vectorize Index│
  │  ↓ Hermes Agent Framework         Crypto Research          (3,245 TW laws)│
  │  Nightly Auto Pipeline (01:00)    + Blog Publishing        Workers AI     │
  │  → YouTube Auto Upload            (Substack/Medium/vocus)  10 AI agents   │
  │  ↓                                + 9 cron jobs            (zero ops)     │
  │  TG natural chat (3 agents)                                                │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘
                            ↕ Tailscale VPN mesh
```

## Products (Fully Automated, Zero Human Intervention)

| Product | Duration | Frequency | Key Tech |
|---------|----------|-----------|----------|
| Short Videos (12 themes) | 15-60s | Daily | FLUX → WAN 2.2 I2V → SeedVR2 1080p |
| Real News | 5-12 min | 2x/week | Auto topic → Self-Refine → Presenter |
| Original Cat Shorts | 60s | Daily | 20 segments, speaker diarization |
| Classic Film Cat Edition | 30-90s | Periodic | SAM2 face swap + original audio |
| **Urban Fatso Drama Series (都市肥仔的人生)** | **5-10 min** | **Episodic (EP01-04 live)** | **South Park-style cels + lip-flap + multi-character composition** |
| **🐙 Zhangyu Novel Platform** (`aigcmore.app`) | **N/A (read-anytime)** | **continuous** | **Cloudflare Workers + D1 + R2 + Next.js 15 + AdSense + 230 books / 7566 chapters** |
| **Lex Legal SaaS** (`lex.aigcmore.app`) | **per task** | **continuous** | **Cloudflare Workers + D1 + Vectorize RAG (3,245 TW laws) + Workers AI** |
| Crypto Research | - | 3x daily | Binance Futures testnet |
| Blog Publishing | - | 3x/week | 3 platforms auto-publish |
| **Services-as-Software intel** | **daily 09:00** | **daily** | **Hermes captain cron + blogwatcher skill, 48 products tracked across 13 verticals over 13 days** |

## Video Production Pipeline

```
LLM Scripting (GPT-5.4)
  → FLUX/HiDream Keyframes
    → WAN 2.2 I2V Dual-Stage (high_noise → low_noise)
      → SeedVR2 1080p Upscale + RIFE 24fps Interpolation
        → Edge TTS HsiaoYu (zh-TW) + BGM Sidechain Mixing
          → Whisper Hybrid Subtitles (zh/en/ja/ko)
            → YouTube Auto-Upload
```

**10+ AI models** sequenced on a single 32GB GPU with automatic VRAM management.

## 3-Realm Architecture

### Server (Ubuntu Linux, RTX 5090 32GB)
- **3 AI Agents** via Hermes Agent: captain (GPT-5.4), coder (GPT-5.4-mini), scout (GPT-5.4-mini)
- **Nightly pipeline**: auto-starts at 01:00, serializes 3 production lines, zero human intervention
- **Docker services**: ComfyUI, ChromaDB, SearXNG (CosyVoice retired 2026-04-26 → Edge TTS HsiaoYu)
- Migrated from OpenClaw → Hermes Agent (2026-04), removing 8,900+ lines of custom dispatch/bridge code in favor of native framework features

### Mac (MacBook Air M2 24GB, Hermes Agent)
- **1 AI Agent** (GPT-5.4) — crypto research + blog auto-publishing
- **9 cron jobs**: crypto tracker (10min), daily report (08:00/23:00), blog prep (Sun/Tue/Fri)
- **Crypto research**: Binance Futures Testnet dual-account simulation (100U + 1000U)
- **Blog auto-publish**: 3 platforms (Substack / Medium / vocus), Auto Rewrite Until Pass

### Cloudflare Cloud (Zhangyu Novel Platform + Lex Legal SaaS)
- **Zhangyu (`aigcmore.app`)** — Chinese serialized novel platform, **rebranded 2026-05-03**
  - Firebase RTDB → Cloudflare D1/R2/Workers full migration in 1 day (M1-M9, 2026-05-02)
  - **230 published books / 7566 chapters / 23 categories / 21 unique pen names** with AI co-pilot byline
  - Next.js 15 App Router + OpenNext + Tailwind 4, SSG (266 pages) + ISR (7566 chapters) hybrid
  - Firebase Auth (Web SDK) + KV opaque token + httpOnly cookie + 6 admin pages with CSRF
  - **Google AdSense ca-pub-...** integrated with 8 ad slots (home/category/search/book/chapter)
  - Cloudflare Web Analytics (cookieless) + sitemap 7824 URLs (full-chapter SEO)

### Cloudflare Cloud (Lex 法律鋪)
- **B2C Legal SaaS** at `lex.aigcmore.app` (Preview)
- **Stack**: Next.js 15 App Router on OpenNext + Cloudflare Workers + D1 + R2 + Vectorize Index + Workers AI
- **RAG**: 3,245 Taiwan law articles indexed; weekly auto-refresh via cron
- **10 AI agents** for contract drafting / review / compliance audit / privacy policy / FOIA-style redaction
- **Compliance-aware design**: PDPA §8 disclosure aligned with actual implementation; cookieless analytics (Cloudflare Web Analytics)

### Cross-Realm
- **Tailscale VPN** mesh networking (Server ↔ Mac)
- **Telegram** unified communication — all agents share one group
- **Cloudflare** as production stack for public-facing SaaS (Lex)

## Key Technical Highlights

### Multi-Agent Orchestration
- **5 AI Agents** across 3 realms with distinct roles
- Hermes Agent framework: native multi-profile gateway, built-in cron scheduler, Telegram adapter
- Previously custom-built on OpenClaw (dispatch_task.py, telegram_bridge.py, sync_workspace.sh — 8,900+ lines), migrated to Hermes native features in 2026-04
- Persistent sessions with automatic context compaction
- Telegram multi-bot natural chat — each agent has its own bot identity

### Vertical AI / RAG (Lex)
- **3,245 Taiwan law articles** indexed in Cloudflare Vectorize for retrieval
- **Domain models**: contract type classification, clause extraction, risk flagging, redline suggestions
- **D1 batch transactions** for cross-table consistency (lesson learned: avoid sequential INSERT race)
- **Compliance-first**: outputs include `verify_token` + `audit_log` + sanitization layer for LLM tool_use
- Lex `agent_outputs` table tracks every agent invocation with type/lang/contract_type for analytics

### GPU VRAM Management (Single GPU, Multiple Services)
- ComfyUI (WAN 2.2 ~20GB) + image generation pipeline serialized on single 32GB GPU
- Automatic VRAM swap: `/free` → unload → load → health verify
- Pipeline LLM calls routed through Hermes API server (OpenAI Codex GPT-5.4)

### Production Reliability
- **105 Lessons Learned** from production incidents (each with root cause + fix + prevention rule)
- Nightly orchestrator: 3 pipelines serialized, process group kill, sequential failure recovery
- Quality gates: 11-point Vision LLM check + Self-Refine feedback loop
- TTS 3-tier retry: seed rotation → LLM text rewrite → best-effort with cut repair
- Automated weekly health audits across 5 scheduler systems (Linux crontab + systemd timers + Hermes per-profile cron + Claude RemoteTrigger)
- Daily Services-as-Software intelligence cron (Hermes captain) — 48 products tracked across 13 verticals over 13 days

### Claude Code — Development Core
- **Claude Code (Opus)** is the primary developer of this entire platform — 70+ scripts, 100+ SOPs, 105 Lessons Learned
- **Claude Daemon** deployed on both machines as pipeline LLM fallback
- Heavy use of `/deep-plan` 16-Lens Reflection methodology for complex refactors

### Mac Automation
- Hermes Agent cron: crypto cycle tracking every 10 min, morning/night reports via Telegram
- Blog pipeline: topic prep → draft → 3-platform rewrite (Sun/Tue/Fri schedule)
- Daily briefing state machine: day rollover + proactive task discovery
- Chrome desktop automation (CDP) for Substack/Medium/vocus publishing

## Code Samples

- [`dispatch_architecture.py`](code-samples/dispatch_architecture.py) — Multi-agent dispatch with cross-process semaphore
- [`gpu_vram_management.py`](code-samples/gpu_vram_management.py) — 10+ AI models on single 32GB GPU

## Screenshots

### Virtual Office (Phaser.js)
<p float="left">
  <img src="assets/screenshots/office_cyberpunk.png" width="45%" />
  <img src="assets/screenshots/office_sakura.png" width="45%" />
</p>

### WebUI Dashboard
<img src="assets/screenshots/webui_dashboard.png" width="70%" />

### AI Agent Team
<p float="left">
  <img src="assets/agents/avatar_cleo.png" width="120" title="Cleo — Captain (Server)" />
  <img src="assets/agents/avatar_ada.png" width="120" title="Ada — Coder (Server)" />
  <img src="assets/agents/avatar_amelia.png" width="120" title="Amelia — Scout (Server)" />
  <img src="assets/agents/avatar_mac_agent.jpg" width="120" title="Lucid — Mac Agent" />
</p>

### Generated Keyframes
<p float="left">
  <img src="assets/keyframes/keyframe_cat_01.png" width="22%" />
  <img src="assets/keyframes/keyframe_cat_05.png" width="22%" />
  <img src="assets/keyframes/keyframe_movie_02.png" width="22%" />
  <img src="assets/keyframes/keyframe_movie_08.png" width="22%" />
</p>

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **AI Agent** | Hermes Agent (migrated from OpenClaw 2026-04), Multi-Profile Gateway, Built-in Cron |
| **Development** | Claude Code (Opus), Claude Daemon (fallback LLM), `/deep-plan` 16-Lens Reflection methodology |
| **LLM** | GPT-5.4 (OpenAI Codex), GPT-5.4-mini, Anthropic Claude (daemon fallback), Workers AI |
| **AI Generation** | ComfyUI, FLUX, HiDream, WAN 2.2 I2V/S2V, SeedVR2, RIFE |
| **TTS / STT** | Edge TTS HsiaoYu (zh-TW, replaced CosyVoice 2026-04-26), Whisper turbo |
| **Vertical AI / RAG** | Cloudflare Vectorize Index (3,245 TW laws), ChromaDB |
| **Cloud SaaS Stack** (Lex) | Next.js 15 App Router, OpenNext, Cloudflare Workers / D1 / R2 / KV / Workers AI / Web Analytics |
| **Backend** | FastAPI, Python asyncio, SQLite, EventBus SSE, Cloudflare Workers |
| **Frontend** | Next.js, React, Phaser.js (virtual office), HTML/CSS/JS |
| **DevOps** | Docker, systemd timers, Linux crontab, Hermes per-profile cron, Tailscale VPN |
| **Communication** | Telegram Native (Hermes Gateway), WebSocket |

## Experience

14 years in software development. Former Android/iOS/Unity engineer at Gamania, Aspeed Tech, So-net Taiwan. Transitioned to AI Agent systems engineering in mid-2025. Currently operating a 3-realm autonomous platform spanning self-hosted GPU infrastructure, Mac-based agent automation, and Cloudflare-hosted B2C SaaS.

---

*Updated 2026-05-01 — Added Cloudflare realm (Lex Legal SaaS), Urban Fatso Drama Series, Services-as-Software intelligence cron; CosyVoice retirement; Lessons Learned 47 → 105*
