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
  ├── 🖥️ Server (RTX 5090 32GB)             ├── 💻 Mac (OpenClaw)
  │   Cleo (Captain / GPT-5.4)              │   Independent Agent (GPT-5.4)
  │   Ada (Coder / GPT-5.4-mini)            │   ↓
  │   Amelia (Scout / GPT-5.4-mini)         │   Crypto Research + Blog
  │   ↓                                     │   → Telegram Reports
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
- **3 AI Agents** via OpenClaw: captain (GPT-5.4), coder (GPT-5.4-mini), scout (GPT-5.4-mini)
- **Nightly pipeline**: auto-starts at 01:00, serializes 3 production lines, zero human intervention
- **Docker services**: ComfyUI, Ollama, CosyVoice TTS, ChromaDB, SearXNG

### Mac (MacBook Air M2 24GB, OpenClaw)
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
- Cross-process dispatch with `fcntl.flock` semaphore (N=2 concurrent, 10s min interval)
- Persistent sessions with session lock quarantine + automatic fallback
- Heartbeat-driven: every 30 min auto-wake, check 5 health indicators
- Telegram 3-bot natural chat — agents reply without @mention

### GPU VRAM Management (Single GPU, Multiple Services)
- ComfyUI (WAN 2.2 ~20GB) ↔ Ollama (Gemma 4 31B ~26GB) ↔ CosyVoice (0.5B ~3GB)
- Automatic model swap: `/free` → unload → load → health verify
- GGUF binary patching for context window control (262K → 8K)
- 3-layer defense: GGUF patch + models.json + watchdog auto-repair

### Production Reliability
- **47 Lessons Learned** from production incidents (each with root cause + fix + prevention)
- Nightly orchestrator: 3 pipelines serialized, process group kill, CosyVoice recovery
- Quality gates: 11-point Vision LLM check + Self-Refine feedback loop
- TTS 3-tier retry: seed rotation → LLM text rewrite → best-effort with cut repair

### Claude Code — Development Core
- **Claude Code (Opus)** is the primary developer of this entire platform — 50+ scripts, 70+ SOPs, 47 Lessons Learned
- **Claude Daemon** deployed on both machines as pipeline LLM fallback

### Mac Automation
- OpenClaw cron: crypto cycle tracking every 10 min, morning/night reports via Telegram
- Scheduler rescue system: heartbeat fallback if cron misses window
- Daily briefing state machine: day rollover + proactive task discovery
- Chrome desktop automation for blog publishing

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
| **AI Agent** | OpenClaw Multi-Agent, Heartbeat, Dispatch Queue |
| **Development** | Claude Code (Opus), Claude Daemon (fallback LLM) |
| **LLM** | GPT-5.4, GPT-5.4-mini, Gemma 4 31B (local fallback), Claude (daemon fallback) |
| **AI Generation** | ComfyUI, FLUX, HiDream, WAN 2.2 I2V/S2V, SeedVR2, RIFE |
| **TTS/STT** | CosyVoice3 0.5B, Whisper turbo |
| **Backend** | FastAPI, Python asyncio, SQLite, EventBus SSE |
| **Frontend** | Phaser.js (virtual office), HTML/CSS/JS |
| **DevOps** | Docker, systemd, Tailscale VPN |
| **Communication** | Telegram 3-Bot Bridge, WebSocket |

## Experience

14 years in software development. Former Android/iOS/Unity engineer at Gamania, Aspeed Tech, So-net Taiwan. Transitioned to AI Agent systems engineering in late 2024.

---

*Updated 2026-04-11*
