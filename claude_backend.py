"""Two ways to reach Claude with the same system prompt and messages.

    backend="api"   Anthropic API; needs ANTHROPIC_API_KEY (default)
    backend="cli"   `claude -p`; runs on a logged-in Claude Code subscription

Both take a list of {"role", "content"} messages and return the reply text, so
the agent code never has to know which one it is talking to.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

MODEL = "claude-opus-5"
EFFORTS = ["low", "medium", "high", "xhigh", "max"]

# Models that accept the server-side refusal fallback.
FALLBACK_MODELS = {"claude-opus-5"}


def call_api(messages: list[dict], system: str, model: str = MODEL, effort: str = "low") -> str:
    """One turn through the Anthropic API. Bills API credits."""
    import anthropic

    kwargs: dict = {}
    if model in FALLBACK_MODELS:
        # On a policy decline, re-run the request on Anthropic's recommended model.
        kwargs = {"betas": ["server-side-fallback-2026-07-01"],
                  "extra_body": {"fallbacks": "default"}}

    response = anthropic.Anthropic().beta.messages.create(
        model=model,
        max_tokens=16000,
        system=system,
        messages=messages,
        thinking={"type": "adaptive"},
        output_config={"effort": effort},
        **kwargs,
    )
    if response.stop_reason == "refusal":
        raise RuntimeError("the model declined to answer this request")
    return "".join(b.text for b in response.content if b.type == "text")


def find_claude() -> str:
    """Locate the Claude Code executable, which the installer may leave off PATH."""
    found = shutil.which("claude")
    if found:
        return found
    fallback = Path.home() / ".local" / "bin" / ("claude.exe" if os.name == "nt" else "claude")
    if fallback.exists():
        return str(fallback)
    raise RuntimeError("Claude Code not found; install it or use --backend api")


def call_cli(messages: list[dict], system: str, model: str = MODEL, effort: str = "low") -> str:
    """One turn through `claude -p`. Runs on the Claude Code subscription.

    Each `claude -p` call starts fresh, so a multi-turn exchange is replayed as a
    single prompt. `--tools ""` leaves the model no tools at all: it can only
    reply with text, never touch files.
    """
    if len(messages) == 1:
        prompt = messages[0]["content"]
    else:
        prompt = "\n\n".join(f"[{m['role']}]\n{m['content']}" for m in messages)

    # A key in the environment would make Claude Code bill the API instead.
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    proc = subprocess.run(
        [
            find_claude(), "-p",
            "--system-prompt", system,
            "--model", model,
            "--effort", effort,
            "--tools", "",
            "--no-session-persistence",
        ],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        timeout=300,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"claude -p exited {proc.returncode}: {proc.stderr.strip()[-300:]}")
    return proc.stdout


BACKENDS = {"api": call_api, "cli": call_cli}


def add_backend_args(parser) -> None:
    """The shared --backend / --model / --effort flags for any entry point."""
    parser.add_argument("--backend", default="api", choices=list(BACKENDS),
                        help="api: API credits (default); cli: Claude Code subscription")
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--effort", default="low", choices=EFFORTS,
                        help="how hard the model thinks (default: low)")
