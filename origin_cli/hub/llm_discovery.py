"""
LLM-powered deep project discovery for `origin hub discover --deep`.
Reads source files and uses an available LLM API to infer precise tech tags.
"""
import json
import os
from pathlib import Path
from typing import List

SOURCE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".java", ".go", ".rs",
    ".cs", ".cpp", ".c", ".rb", ".php", ".swift", ".kt",
}
IGNORE_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    "dist", "build", ".next", "target", ".idea", ".vscode",
}
MAX_FILES = 10
MAX_CHARS_PER_FILE = 2000

SYSTEM_PROMPT = """You are a senior software architect. Analyze the provided source code samples and respond with ONLY a valid JSON object. No markdown, no explanation. The JSON object must have two keys:
- "tags": a list of lowercase technology/framework tags inferred from the code (e.g. "react", "fastapi", "spring-boot", "postgresql", "redis", "graphql").
- "summary": a one-sentence description of what the project does.

Be specific. Prefer framework names over language names (e.g., prefer "fastapi" over just "python").
"""


def _sample_source_files(project_dir: Path) -> str:
    """Collect and sample source files from the project directory."""
    collected = []
    for file in sorted(project_dir.rglob("*")):
        if len(collected) >= MAX_FILES:
            break
        if any(part in IGNORE_DIRS for part in file.parts):
            continue
        if file.suffix not in SOURCE_EXTENSIONS:
            continue
        if not file.is_file():
            continue
        try:
            content = file.read_text(encoding="utf-8", errors="ignore")[:MAX_CHARS_PER_FILE]
            collected.append(f"### {file.relative_to(project_dir)}\n```\n{content}\n```")
        except Exception:
            continue
    return "\n\n".join(collected)


def _call_openai(prompt: str) -> dict:
    import httpx
    api_key = os.environ["OPENAI_API_KEY"]
    resp = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    resp.raise_for_status()
    text = resp.json()["choices"][0]["message"]["content"]
    return json.loads(text)


def _call_anthropic(prompt: str) -> dict:
    import httpx
    api_key = os.environ["ANTHROPIC_API_KEY"]
    resp = httpx.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        json={
            "model": "claude-3-haiku-20240307",
            "max_tokens": 512,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=30,
    )
    resp.raise_for_status()
    text = resp.json()["content"][0]["text"]
    return json.loads(text)


def _call_gemini(prompt: str) -> dict:
    import httpx
    api_key = os.environ["GEMINI_API_KEY"]
    resp = httpx.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
        headers={"Content-Type": "application/json"},
        json={
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0},
        },
        timeout=30,
    )
    resp.raise_for_status()
    text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    return json.loads(text)


def discover_with_llm(project_dir: Path) -> dict:
    """
    Sample source files, call an LLM, and return a dict with 'tags' and 'summary'.
    Tries OPENAI_API_KEY, then ANTHROPIC_API_KEY, then GEMINI_API_KEY.
    Raises RuntimeError if no API key is configured.
    """
    code_sample = _sample_source_files(project_dir)
    if not code_sample:
        raise RuntimeError("No source files found to analyze.")

    prompt = f"Analyze this project's source code:\n\n{code_sample}"

    if os.environ.get("OPENAI_API_KEY"):
        return _call_openai(prompt)
    elif os.environ.get("ANTHROPIC_API_KEY"):
        return _call_anthropic(prompt)
    elif os.environ.get("GEMINI_API_KEY"):
        return _call_gemini(prompt)
    else:
        raise RuntimeError(
            "No LLM API key found. Set one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY."
        )
