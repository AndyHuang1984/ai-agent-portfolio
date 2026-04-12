[🇹🇼 中文版](README.zh-TW.md)

# AI Agent Autonomous Production Platform

> One-person team + Multi-Agent system, fully automated across 2 machines: video production + crypto research + blog publishing

**Andy Huang** — AI Agent System Engineer / Senior Software Developer

[![Resume](https://img.shields.io/badge/Resume-View-blue)](https://andyhuang1984.github.io/ai-agent-portfolio/resume.html)
[![Showcase](https://img.shields.io/badge/Showcase-Portfolio-green)](https://andyhuang1984.github.io/ai-agent-portfolio/showcase.html)
[![YouTube](https://img.shields.io/badge/YouTube-Channel-red)](https://www.youtube.com/@ShrimpCatStudio)

---

## System Architecture

```
Owner (1 person)
  ↓ Telegram Group
  ├── 🖥️ Server (RTX 5090 32GB)             ├── 💻 Mac (Hermes Agent)
  │   Cleo (Captain / GPT-5.4)              │   Independent Agent (GPT-5.4)
  │   Ada (Coder / GPT-5.4-mini)            │   ↓
  │   Amelia (Scout / GPT-5.4-mini)         │   Crypto Research + Blog
  │   ↓ Hermes Agent Framework              │   → Telegram Reports
  │   Nightly Auto Pipeline                 │   → 3-Platform Auto Publish
  │   → YouTube Auto Upload                 │
  │   ↓                                     │
  │   TG Natural Chat (3 agents)            │
  └─────────────────────────────────────────┘
      ↕ Tailscale VPN Cross-Machine Mesh
```

## Products (Fully Automated, Zero Human Intervention)

| Product | Duration | Frequency | Key Tech |
|---------|----------|-----------|----------|
| Short Videos (12 themes) | 15-60s | Daily | FLUX → WAN 2.2 I2V → SeedVR2 1080p |
| Real News | 5-12 min | 2x/week | Auto topic → Self-Refine → Presenter |
| Original Cat Shorts | 60s | Daily | 20 segments, speaker diarization |
| Classic Film Cat Edition | 30-90s | Periodic | SAM2 face swap + original audio |
| Crypto Research | - | 3x daily | Binance Futures testnet |
| Blog Publishing | - | 3x/week | 3 platforms auto-publish |

## Video Production Pipeline

```
LLM Scripting (GPT-5.4)
  → FLUX/HiDream Keyframes
    → WAN 2.2 I2V Dual-Stage (high_noise → low_noise)
      → SeedVR2 1080p Upscale + RIFE 24fps Interpolation
        → CosyVoice3 TTS + BGM Mixing
          → Whisper Hybrid Subtitles (zh/en/ja/ko)
            → YouTube Auto-Upload
```

**10+ AI models** sequenced on a single 32GB GPU with automatic VRAM management.

## Dual-Machine Architecture

### Server (Ubuntu Linux, RTX 5090 32GB)
- **3 AI Agents** via Hermes Agent: captain (GPT-5.4), coder (GPT-5.4-mini), scout (GPT-5.4-mini)
- **Nightly pipeline**: auto-starts at 01:00, serializes 3 production lines, zero human intervention
- **Docker services**: ComfyUI, CosyVoice TTS, ChromaDB, SearXNG
- Migrated from OpenClaw → Hermes Agent (2026-04), replacing 8,900+ lines of custom dispatch/bridge code with native framework features

### Mac (MacBook Air M2 24GB, Hermes Agent)
- **1 AI Agent** (GPT-5.4) — crypto research + blog auto-publishing
- **9 cron jobs**: crypto tracker (10min), daily report (08:00/23:00), blog prep (Sun/Tue/Fri)
- **Crypto research**: Binance Futures Testnet dual-account simulation (100U + 1000U)
- **Blog auto-publish**: 3 platforms (Substack / Medium / vocus), Auto Rewrite Until Pass

### Cross-Machine
- **Tailscale VPN** mesh networking
- **Telegram** unified communication — all agents share one group

## Key Technical Highlights

### Multi-Agent Orchestration
- **4 AI Agents** across 2 machines with distinct roles
- Hermes Agent framework: native multi-profile gateway, built-in cron scheduler, Telegram adapter
- Previously custom-built on OpenClaw (dispatch_task.py, telegram_bridge.py, sync_workspace.sh — 8,900+ lines), migrated to Hermes native features in 2026-04
- Persistent sessions with automatic context compaction
- Telegram multi-bot natural chat — each agent has its own bot identity

### GPU VRAM Management (Single GPU, Multiple Services)
- ComfyUI (WAN 2.2 ~20GB) ↔ CosyVoice TTS (0.5B ~3GB) — serialized on single 32GB GPU
- Automatic VRAM swap: `/free` → unload → load → health verify
- Pipeline LLM calls routed through Hermes API server (OpenAI Codex GPT-5.4)

### Production Reliability
- **47 Lessons Learned** from production incidents (each with root cause + fix + prevention)
- Nightly orchestrator: 3 pipelines serialized, process group kill, CosyVoice recovery
- Quality gates: 11-point Vision LLM check + Self-Refine feedback loop
- TTS 3-tier retry: seed rotation → LLM text rewrite → best-effort with cut repair

### Claude Code — Development Core
- **Claude Code (Opus)** is the primary developer of this entire platform — 50+ scripts, 70+ SOPs, 47 Lessons Learned
- **Claude Daemon** deployed on both machines as pipeline LLM fallback

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
| **Development** | Claude Code (Opus), Claude Daemon (fallback LLM) |
| **LLM** | GPT-5.4 (OpenAI Codex), GPT-5.4-mini, Claude (daemon fallback) |
| **AI Generation** | ComfyUI, FLUX, HiDream, WAN 2.2 I2V/S2V, SeedVR2, RIFE |
| **TTS/STT** | CosyVoice3 0.5B, Whisper turbo |
| **Backend** | FastAPI, Python asyncio, SQLite, EventBus SSE |
| **Frontend** | Phaser.js (virtual office), HTML/CSS/JS |
| **DevOps** | Docker, systemd, Tailscale VPN |
| **Communication** | Telegram Native (Hermes Gateway), WebSocket |

## Experience

14 years in software development. Former Android/iOS/Unity engineer at Gamania, Aspeed Tech, So-net Taiwan. Transitioned to AI Agent systems engineering in mid-2025.

---

*Updated 2026-04-13 — Migrated from OpenClaw to Hermes Agent*
