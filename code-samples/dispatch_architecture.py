"""
Multi-Agent Dispatch Architecture (Simplified)

Cross-process semaphore + session management for 3 AI agents.
Originally built for OpenClaw, migrated to Hermes Agent (2026-04).

Real system handles: fcntl.flock N=2 concurrency, min 10s interval,
session lock quarantine, persistent vs isolated sessions, and
automatic fallback on timeout.
"""

import fcntl
import time
import subprocess
import json
from pathlib import Path

# --- Cross-process concurrency control ---

SEMAPHORE_PATH = Path("/tmp/dispatch_slots.lock")
MAX_CONCURRENT = 2       # Max 2 simultaneous LLM requests (rate limit protection)
MIN_INTERVAL_SEC = 10    # Minimum gap between dispatches
DISPATCH_TIMEOUT = 900   # 15 min default

_last_dispatch_time = 0.0


def _acquire_dispatch_slot(timeout: int = 300) -> 'DispatchSlot':
    """Acquire a cross-process dispatch slot (fcntl.flock, max N=2)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        for slot_id in range(MAX_CONCURRENT):
            lock_path = SEMAPHORE_PATH.parent / f".dispatch_slot_{slot_id}.lock"
            fd = open(lock_path, "w")
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                fd.write(f"{os.getpid()}")
                fd.flush()
                return DispatchSlot(fd, slot_id)
            except OSError:
                fd.close()
        time.sleep(1)
    raise TimeoutError(f"No dispatch slot available after {timeout}s")


def _enforce_min_interval():
    """Prevent burst dispatches that trigger rate limit → cooldown cascade."""
    global _last_dispatch_time
    elapsed = time.time() - _last_dispatch_time
    if elapsed < MIN_INTERVAL_SEC:
        time.sleep(MIN_INTERVAL_SEC - elapsed)
    _last_dispatch_time = time.time()


# --- Agent dispatch ---

def dispatch(message: str, role: str, timeout: int = DISPATCH_TIMEOUT) -> dict:
    """
    Dispatch a task to an AI agent.

    Flow: acquire slot → enforce interval → build preamble → agent CLI
    → parse result → emit events (originally OpenClaw, now Hermes Agent)
    """
    slot = _acquire_dispatch_slot()
    try:
        _enforce_min_interval()

        preamble = _build_slim_preamble(role, message)
        full_message = f"{preamble}\n\n---\n\n{message}"

        cmd = [
            "hermes", "chat", "-q",  # was: "openclaw", "agent"
            "--role", role,
            "--message", full_message,
            "--timeout", str(timeout * 1000),  # ms
        ]

        result = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=timeout + 30,  # grace period
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout[-2000:],  # Last 2KB
            "role": role,
            "elapsed": timeout,
        }
    finally:
        slot.release()


def _build_slim_preamble(role: str, task: str) -> str:
    """
    Build a minimal context preamble (93% smaller than v1).

    4-layer architecture:
    1. Identity (who you are)
    2. Tools (what you can use)
    3. Context (current state)
    4. Task (what to do)
    """
    agent = _load_agent_registry(role)

    return f"""[Identity] {agent['name']} — {agent['personality']}
[Tools] {', '.join(agent['tools'])}
[Context] GPU: {_gpu_status()} | CosyVoice: {_cosyvoice_status()}
[Task] {task[:200]}"""
