"""Optional LLM wording layer (W2). Off unless ANTHROPIC_API_KEY is set.

The retrieved passage is the only allowed source. The reply is validated and the
engine falls back to the passage text itself if validation fails, so a bad model
reply can never change a fact or add a second link.
"""
import os
import re

MODEL = os.environ.get("MF_FAQ_MODEL", "claude-sonnet-5-5")

SYSTEM_PROMPT = """You are a facts-only mutual fund FAQ assistant.
Rules:
1. Answer ONLY from the PASSAGE. If the passage does not answer the question, reply exactly: NOT_IN_SOURCES
2. Maximum 3 sentences. Plain, neutral wording. No advice, no opinions, no recommendations.
3. Never compute, compare or mention returns or performance.
4. Copy every number, percentage and date exactly as written in the PASSAGE. Add none.
5. Do not include links, source names or a date; those are added separately."""


def _numbers(text):
    return set(re.findall(r"\d[\d,.]*", text))


def rephrase(question, passage):
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    import anthropic
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=MODEL, max_tokens=200, system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"QUESTION: {question}\n\nPASSAGE: {passage}"}])
    out = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text").strip()
    if not out or "NOT_IN_SOURCES" in out or "http" in out.lower():
        return None
    if len([s for s in re.split(r"(?<=[.!?])\s+", out) if s]) > 3:
        return None
    if not _numbers(out) <= _numbers(passage):   # no invented figures
        return None
    return out
