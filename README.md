# AI Agent 自主生產平台

> 一人團隊 + Multi-Agent 系統，跨兩台機器全自動運行：影片生產 + 加密貨幣研究 + 部落格發布

**黃詣超 Andy Huang** — AI Agent System Engineer / Senior Software Developer

[![Resume](https://img.shields.io/badge/Resume-HTML-blue)](resume.html)
[![Showcase](https://img.shields.io/badge/Showcase-Portfolio-green)](showcase.html)
[![YouTube](https://img.shields.io/badge/YouTube-Channel-red)](https://www.youtube.com/@ShrimpCatStudio)

---

## System Architecture

```
老闆（1 人）
  ↓ Telegram 群組
  ├── 🖥️ Server (RTX 5090 32GB)          ├── 💻 Mac (OpenClaw)
  │   克蕾（隊長/GPT-5.4）                │   獨立 Agent（GPT-5.4）
  │   愛達（工程師/Gemma 4 31B 本地）       │   ↓
  │   艾米（素材獵人/Gemma 4 31B 本地）     │   加密貨幣研究 + 部落格
  │   ↓                                   │   → Telegram 報告
  │   夜間全自動 Pipeline                  │   → 三平台自動發布
  │   → YouTube 自動上傳                  │
  │   ↓                                   │
  │   TG 自然閒聊（3 agent 對話）          │
  └───────────────────────────────────────┘
      ↕ Tailscale VPN 跨機器互聯
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
- **Nightly pipeline** 01:00 自動啟動，序列化 3 條生產線，0 人工介入
- **Docker services**: ComfyUI, Ollama, CosyVoice TTS, ChromaDB, SearXNG
- **Claude Code** as development assistant ("蝦師"), remote via `claude.ai/code`
- **Claude Daemon** HTTP server (localhost:5050) for pipeline LLM fallback

### Mac (MacBook Air M2 24GB, OpenClaw)
- **1 AI Agent** (GPT-5.4) — 加密貨幣研究 + 部落格自動發布
- **9 cron jobs**: crypto tracker (10min), daily report (08:00/23:00), blog prep (Sun/Tue/Fri), memory rebuild
- **Crypto research**: Binance Futures Testnet 雙帳戶模擬（100U + 1000U），Research Context 驅動決策
- **Blog auto-publish**: 3 platforms (Substack / Medium / vocus)，Auto Rewrite Until Pass，Chrome 自動操作
- **Claude Daemon** (localhost:5050) + OpenClaw gateway (GPT-5.4)
- **Memory Wiki**: bridge mode, knowledge ingestion + compile cron

### Cross-Machine Integration
- **Tailscale VPN** mesh networking（Server ↔ Mac 互通）
- **SSH remote operations**: Server 端 Claude Code 可直接 SSH 操作 Mac
- **Telegram 統一入口**: 所有 agent 共用 TG 群組，跨機器即時通訊
- **`sync_workspace.sh`**: bootstrap 文件同步到所有 agent workspace（hard copy，非 symlink）

## Key Technical Highlights

### Multi-Agent Orchestration
- **4 AI Agents** across 2 machines with distinct roles
- Cross-process dispatch with `fcntl.flock` semaphore (N=2 concurrent, 10s min interval)
- Persistent sessions with session lock quarantine + automatic fallback
- Heartbeat-driven: every 30 min auto-wake, check 5 health indicators
- Telegram 3-bot natural chat — agents reply without @mention

### GPU VRAM Management (Single GPU, Multiple Services)
- ComfyUI (WAN 2.2 ~20GB) ↔ Ollama (Gemma 4 31B fallback ~26GB) ↔ CosyVoice (0.5B ~3GB)
- Automatic model swap: `/free` → unload → load → health verify
- GGUF binary patching for context window control (262K → 8K)
- 3-layer defense: GGUF patch + models.json + watchdog auto-repair

### Production Reliability
- **47 Lessons Learned** from production incidents (each with root cause + fix + prevention)
- Nightly orchestrator: 3 pipelines serialized, process group kill, CosyVoice recovery
- Quality gates: 11-point Vision LLM check + Self-Refine feedback loop
- TTS 3-tier retry: seed rotation → LLM text rewrite → best-effort with cut repair

### Claude Code — 系統開發核心
- **Claude Code (Opus)** 是整個平台的主要開發者，50+ 腳本、70+ SOP、47 條 Lessons Learned 皆協作完成
- **Claude Daemon** 常駐雙機器，作為 pipeline LLM fallback（Gateway 失敗自動接手）

### Mac Automation
- OpenClaw cron: crypto cycle tracking every 10 min, morning/night reports via Telegram
- Scheduler rescue system: heartbeat fallback if cron misses window
- Daily briefing state machine: day rollover + proactive task discovery
- Chrome desktop automation: `osascript` + `screencapture` for blog publishing

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
  <img src="assets/agents/avatar_cleo.png" width="120" title="克蕾 — Captain (Server)" />
  <img src="assets/agents/avatar_ada.png" width="120" title="愛達 — Coder (Server)" />
  <img src="assets/agents/avatar_amelia.png" width="120" title="艾米 — Scout (Server)" />
  <img src="assets/agents/avatar_mac_agent.jpg" width="120" title="人間清醒 — Mac Agent" />
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
| **Development** | Claude Code (Opus) remote, Claude Daemon (fallback LLM), Deep Plan methodology |
| **LLM** | GPT-5.4 (pipeline + captain), GPT-5.4-mini (coder/scout), Gemma 4 31B (Ollama, local fallback), Claude (daemon fallback) |
| **AI Generation** | ComfyUI, FLUX, HiDream, WAN 2.2 I2V/S2V, SeedVR2, RIFE |
| **TTS/STT** | CosyVoice3 0.5B, Whisper turbo |
| **Backend** | FastAPI, Python asyncio, SQLite, EventBus SSE |
| **Frontend** | Phaser.js (virtual office), HTML/CSS/JS |
| **DevOps** | Docker, systemd, Tailscale VPN |
| **Communication** | Telegram 3-Bot Bridge, WebSocket |

## Experience

14 years in software development. Former Android/iOS/Unity engineer at Gamania (遊戲橘子), Aspeed (信驊科技), So-net Taiwan. Transitioned to AI Agent systems engineering in late 2024.

---

*Updated 2026-04-11*
