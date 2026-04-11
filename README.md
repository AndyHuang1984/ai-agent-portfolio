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
  │   愛達（工程師/Gemma4 31B 本地）       │   ↓
  │   艾米（素材獵人/Gemma4 31B 本地）     │   加密貨幣研究 + 部落格
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

## Key Technical Highlights

### Multi-Agent Orchestration
- **3 AI Agents** with distinct roles: captain (planning), coder (execution), scout (research)
- Cross-process dispatch with `fcntl.flock` semaphore (N=2 concurrent, 10s min interval)
- Persistent sessions with session lock quarantine + automatic fallback
- Heartbeat-driven: every 30 min auto-wake, check 5 health indicators

### GPU VRAM Management (Single GPU, Multiple Services)
- ComfyUI (WAN 2.2 ~20GB) ↔ Ollama (Gemma4 31B ~26GB) ↔ CosyVoice (0.5B ~3GB)
- Automatic model swap: `/free` → unload → load → health verify
- GGUF binary patching for context window control (262K → 8K)
- 3-layer defense: GGUF patch + models.json + watchdog auto-repair

### Production Reliability
- **47 Lessons Learned** from production incidents (each with root cause + fix + prevention)
- Nightly orchestrator: 3 pipelines serialized, process group kill, CosyVoice recovery
- Quality gates: 11-point Vision LLM check + Self-Refine feedback loop
- TTS 3-tier retry: seed rotation → LLM text rewrite → best-effort with cut repair

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
  <img src="assets/agents/avatar_cleo.png" width="120" title="克蕾 — Captain" />
  <img src="assets/agents/avatar_ada.png" width="120" title="愛達 — Coder" />
  <img src="assets/agents/avatar_amelia.png" width="120" title="艾米 — Scout" />
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
| **AI Agent** | OpenClaw Multi-Agent, Heartbeat, Dispatch Queue, Claude Code |
| **LLM** | GPT-5.4, Gemma4 31B (Ollama), Claude, 3-layer fallback |
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
