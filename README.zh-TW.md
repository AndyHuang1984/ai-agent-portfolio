[🇺🇸 English](README.md)

# AI Agent 自主生產平台

> 一人團隊 + Multi-Agent 系統，跨兩台機器全自動運行：影片生產 + 加密貨幣研究 + 部落格發布

**黃詣超 Andy Huang** — AI Agent System Engineer / Senior Software Developer

[![簡歷](https://img.shields.io/badge/簡歷-查看-blue)](https://andyhuang1984.github.io/ai-agent-portfolio/resume.html)
[![作品集](https://img.shields.io/badge/作品集-Portfolio-green)](https://andyhuang1984.github.io/ai-agent-portfolio/showcase.html)
[![YouTube](https://img.shields.io/badge/YouTube-頻道-red)](https://www.youtube.com/@ShrimpCatStudio)

---

## 系統架構

```
老闆（1 人）
  ↓ Telegram 群組
  ├── 🖥️ Server (RTX 5090 32GB)             ├── 💻 Mac (OpenClaw)
  │   克蕾（隊長 / GPT-5.4）                │   獨立 Agent（GPT-5.4）
  │   愛達（工程師 / GPT-5.4-mini）          │   ↓
  │   艾米（素材獵人 / GPT-5.4-mini）        │   加密貨幣研究 + 部落格
  │   ↓                                     │   → Telegram 報告
  │   夜間全自動 Pipeline                    │   → 三平台自動發布
  │   → YouTube 自動上傳                    │
  │   ↓                                     │
  │   TG 自然閒聊（3 agent 對話）            │
  └─────────────────────────────────────────┘
      ↕ Tailscale VPN 跨機器互聯
```

## 產品線（全自動，0 人工介入）

| 產品 | 時長 | 頻率 | 核心技術 |
|------|------|------|----------|
| 短影音（12 主題） | 15-60 秒 | 每日 | FLUX → WAN 2.2 I2V → SeedVR2 1080p |
| Real News 深度報導 | 5-12 分鐘 | 每週 2 支 | 自動選題 → 自我修正 → 虛擬主播 |
| 原創貓咪短片 | 60 秒 | 每日 | 20 段多角色劇情 + 說話人分離 |
| 經典電影貓臉版 | 30-90 秒 | 不定期 | SAM2 臉部替換 + 原始配音 |
| 加密貨幣研究 | - | 每日 3 次 | Binance Futures Testnet |
| 部落格自動發布 | - | 每週 3 次 | 三平台自動發布 |

## 影片生產 Pipeline

```
LLM 編劇 (GPT-5.4)
  → FLUX/HiDream 關鍵幀
    → WAN 2.2 I2V 雙階段（high_noise → low_noise）
      → SeedVR2 1080p 放大 + RIFE 24fps 補幀
        → CosyVoice3 TTS + BGM 混音
          → Whisper 混合字幕（中/英/日/韓）
            → YouTube 自動上傳
```

**10+ AI 模型** 在單張 32GB GPU 上序列化運行，自動 VRAM 管理。

## 雙機器架構

### Server（Ubuntu Linux, RTX 5090 32GB）
- **3 AI Agent**（OpenClaw）：隊長 (GPT-5.4) + 工程師 (GPT-5.4-mini) + 素材獵人 (GPT-5.4-mini)
- **夜間 Pipeline**：01:00 自動啟動，序列化 3 條生產線，0 人工介入
- **Docker 服務**：ComfyUI、Ollama、CosyVoice TTS、ChromaDB、SearXNG

### Mac（MacBook Air M2 24GB, OpenClaw）
- **1 AI Agent** (GPT-5.4) — 加密貨幣研究 + 部落格自動發布
- **9 個 cron 排程**：crypto tracker（10 分鐘）、日報（08:00/23:00）、部落格準備（週日/二/五）
- **加密貨幣研究**：Binance Futures Testnet 雙帳戶模擬（100U + 1000U）
- **部落格自動發布**：三平台（Substack / Medium / vocus），Auto Rewrite Until Pass

### 跨機器整合
- **Tailscale VPN** mesh networking
- **Telegram** 統一通訊入口 — 所有 agent 共用同一群組

## 核心技術亮點

### Multi-Agent 協作
- **4 AI Agent** 跨兩台機器，各有明確角色分工
- 跨進程 dispatch（`fcntl.flock` 信號量，N=2 並發，10 秒最小間隔）
- 持久 session + session lock quarantine + 自動 fallback
- Heartbeat 驅動：每 30 分鐘主動巡檢 5 項健康指標
- Telegram 3-bot 自然對話 — agent 不需 @mention 自動回覆

### GPU VRAM 管理（單 GPU 多服務）
- ComfyUI (WAN 2.2 ~20GB) ↔ Ollama (Gemma 4 31B ~26GB) ↔ CosyVoice (0.5B ~3GB)
- 自動模型切換：`/free` → unload → load → 健康驗證
- GGUF binary patching 控制 context window（262K → 8K）
- 3 層防禦：GGUF patch + models.json + watchdog 自動修復

### 生產可靠性
- **47 條 Lessons Learned**：每條含根因分析 + 修復方案 + 預防措施
- 夜間 orchestrator：3 條 pipeline 序列化、process group kill、CosyVoice 恢復
- 品質閘門：11 項 Vision LLM 檢查 + Self-Refine 回饋迴路
- TTS 3 層重試：seed 輪替 → LLM 改寫文字 → best-effort + cut repair

### Claude Code — 系統開發核心
- **Claude Code (Opus)** 是整個平台的主要開發者，50+ 腳本、70+ SOP、47 條 Lessons Learned 皆協作完成
- **Claude Daemon** 常駐雙機器，作為 pipeline LLM fallback（Gateway 失敗自動接手）

### Mac 自動化
- OpenClaw cron：每 10 分鐘追蹤 crypto cycle，每日晨報/晚報推送 Telegram
- Scheduler rescue 系統：cron 漏跑時 heartbeat 自動補救
- 每日 briefing 狀態機：自動日期翻轉 + 主動探索待辦任務
- Chrome 桌面自動化：blog 自動發布

## 程式碼範例

- [`dispatch_architecture.py`](code-samples/dispatch_architecture.py) — Multi-agent dispatch 跨進程信號量
- [`gpu_vram_management.py`](code-samples/gpu_vram_management.py) — 10+ AI 模型單 GPU VRAM 管理

## 截圖

### 虛擬辦公室（Phaser.js）
<p float="left">
  <img src="assets/screenshots/office_cyberpunk.png" width="45%" />
  <img src="assets/screenshots/office_sakura.png" width="45%" />
</p>

### WebUI 控制台
<img src="assets/screenshots/webui_dashboard.png" width="70%" />

### AI Agent 團隊
<p float="left">
  <img src="assets/agents/avatar_cleo.png" width="120" title="克蕾 — 隊長 (Server)" />
  <img src="assets/agents/avatar_ada.png" width="120" title="愛達 — 工程師 (Server)" />
  <img src="assets/agents/avatar_amelia.png" width="120" title="艾米 — 素材獵人 (Server)" />
  <img src="assets/agents/avatar_mac_agent.jpg" width="120" title="人間清醒 — Mac Agent" />
</p>

### 生成的關鍵幀
<p float="left">
  <img src="assets/keyframes/keyframe_cat_01.png" width="22%" />
  <img src="assets/keyframes/keyframe_cat_05.png" width="22%" />
  <img src="assets/keyframes/keyframe_movie_02.png" width="22%" />
  <img src="assets/keyframes/keyframe_movie_08.png" width="22%" />
</p>

## 技術棧

| 類別 | 技術 |
|------|------|
| **AI Agent** | OpenClaw Multi-Agent, Heartbeat, Dispatch Queue |
| **開發** | Claude Code (Opus), Claude Daemon (fallback LLM) |
| **LLM** | GPT-5.4, GPT-5.4-mini, Gemma 4 31B (本地 fallback), Claude (Daemon fallback) |
| **AI 生成** | ComfyUI, FLUX, HiDream, WAN 2.2 I2V/S2V, SeedVR2, RIFE |
| **TTS/STT** | CosyVoice3 0.5B, Whisper turbo |
| **後端** | FastAPI, Python asyncio, SQLite, EventBus SSE |
| **前端** | Phaser.js（虛擬辦公室）, HTML/CSS/JS |
| **DevOps** | Docker, systemd, Tailscale VPN |
| **通訊** | Telegram 3-Bot Bridge, WebSocket |

## 經歷

14 年軟體開發經驗。先前任職於遊戲橘子、信驊科技、So-net 台灣碩網等，擔任 Android/iOS/Unity 工程師。2025 年中轉型 AI Agent 系統工程。

---

*更新於 2026-04-11*
