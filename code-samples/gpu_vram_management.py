"""
GPU VRAM Management — 10+ AI Models on Single 32GB GPU

Orchestrates model loading/unloading across ComfyUI, Ollama, and CosyVoice
on a single RTX 5090 32GB. Each service needs exclusive VRAM access
for its heaviest models.

Key challenge: ComfyUI (WAN 2.2 I2V ~20GB) vs Ollama (Gemma4 31B ~26GB)
vs CosyVoice (0.5B ~3GB) cannot coexist simultaneously.
"""

import subprocess
import time
import urllib.request
import json
import logging

logger = logging.getLogger(__name__)

# --- Service health checks ---

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


def ollama_unload(model: str = "gemma4:31b"):
    """Unload Ollama model from VRAM (keep_alive=0)."""
    try:
        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=json.dumps({"model": model, "keep_alive": 0}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=10)
        logger.info(f"Ollama: {model} unloaded")
    except Exception:
        pass


def ollama_load(model: str = "gemma4:31b", num_ctx: int = 8192):
    """Load Ollama model with VRAM verification."""
    # Warmup request to trigger model loading
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps({
            "model": model,
            "prompt": "hi",
            "options": {"num_ctx": num_ctx, "num_predict": 1},
        }).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    urllib.request.urlopen(req, timeout=120)

    # Verify model is actually in GPU VRAM (not CPU offloaded)
    _verify_ollama_vram(model, num_ctx)


def _verify_ollama_vram(model: str, expected_ctx: int):
    """
    Critical: verify model loaded in GPU, not CPU.

    Lesson #46: GGUF native context_length=262144 → KV cache exceeds VRAM
    → entire model offloaded to CPU (size_vram=0) → 67 tok/s → ~2 tok/s.
    3-layer defense: patch GGUF binary + models.json contextWindow + watchdog.
    """
    resp = urllib.request.urlopen("http://localhost:11434/api/ps", timeout=5)
    data = json.loads(resp.read())

    for m in data.get("models", []):
        if model in m.get("name", ""):
            vram = m.get("size_vram", 0)
            ctx = m.get("context_length", 0)

            if vram == 0:
                raise RuntimeError(
                    f"CRITICAL: {model} fully CPU offloaded (size_vram=0, ctx={ctx}). "
                    f"Likely GGUF context too large. Run: patch_gguf_context.py --target {expected_ctx}"
                )

            if ctx > expected_ctx * 2:
                logger.warning(f"{model} context {ctx} >> expected {expected_ctx}")

            logger.info(f"Ollama: {model} healthy (vram={vram/1e9:.1f}GB, ctx={ctx})")
            return

    raise RuntimeError(f"{model} not found in Ollama running models")


# --- High-level mode switches ---

def switch_to_generation():
    """Switch to video generation mode: unload LLM, free VRAM for ComfyUI."""
    logger.info("=== Switching to Generation mode ===")
    ollama_unload()


def switch_to_llm(model: str = "gemma4:31b"):
    """Switch to LLM mode: free ComfyUI, stop CosyVoice, load Ollama."""
    logger.info("=== Switching to LLM mode ===")
    comfyui_free()
    cosyvoice_stop()
    ollama_load(model)


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
