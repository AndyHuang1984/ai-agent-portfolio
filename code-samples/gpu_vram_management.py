"""
GPU VRAM Management — 10+ AI Models on Single 32GB GPU

Orchestrates model loading/unloading across ComfyUI and CosyVoice
on a single RTX 5090 32GB. LLM calls route through Hermes Agent
gateway to OpenAI Codex (cloud), freeing GPU entirely for generation.

History: Previously managed ComfyUI ↔ Ollama (Gemma4 31B ~26GB) ↔ CosyVoice
VRAM contention. After Hermes migration (2026-04), local LLM removed —
GPU dedicated to video generation + TTS.
"""

import subprocess
import time
import urllib.request
import json
import logging

logger = logging.getLogger(__name__)

# --- Service VRAM management ---

def comfyui_free():
    """Release all ComfyUI models from VRAM."""
    try:
        req = urllib.request.Request(
            "http://localhost:8188/free",
            data=b'{"unload_models": true, "free_memory": true}',
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=5)
        logger.info("ComfyUI: VRAM freed")
    except Exception:
        pass  # ComfyUI may not be running


# --- High-level mode switches ---

def switch_to_generation():
    """Switch to video generation mode: free VRAM for ComfyUI."""
    logger.info("=== Switching to Generation mode ===")
    # Post-migration: no Ollama to unload. VRAM is free by default.


def switch_to_llm(model=None):
    """Switch to LLM mode: free ComfyUI, stop CosyVoice.

    Note: Ollama/Gemma4 removed (2026-04 Hermes migration).
    Agents now use OpenAI Codex via Hermes gateway, no local LLM needed.
    """
    logger.info("=== Switching to LLM mode (no-op: cloud LLM) ===")
    comfyui_free()
    cosyvoice_stop()
    return True


def ensure_cosyvoice():
    """
    Ensure CosyVoice TTS is running. Frees competing VRAM first.

    Lesson #43: Must call ComfyUI /free before CosyVoice restart.
    SeedVR2/RIFE models in VRAM → CosyVoice startup takes 53s vs 14s.
    """
    comfyui_free()
    time.sleep(5)
    cosyvoice_start()


def cosyvoice_start():
    """Start CosyVoice container and poll health (measured cold start: 40s)."""
    subprocess.run(["docker", "start", "cosyvoice"], capture_output=True, timeout=30)
    for i in range(90):
        try:
            urllib.request.urlopen("http://localhost:5002/health", timeout=3)
            logger.info(f"CosyVoice: ready ({i}s)")
            return True
        except Exception:
            time.sleep(1)
    logger.error("CosyVoice: FAILED to start after 90s")
    return False


def cosyvoice_stop():
    """Stop CosyVoice container to free ~3GB VRAM."""
    subprocess.run(["docker", "stop", "cosyvoice"], capture_output=True, timeout=30)
    logger.info("CosyVoice: stopped")
