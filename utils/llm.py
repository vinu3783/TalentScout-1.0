"""
utils/llm.py
─────────────
Google Gemini API using the NEW official SDK: google-genai >= 1.0.0

Install:  pip install google-genai streamlit
Get key:  https://aistudio.google.com/app/apikey  (100% free)

Free tier limits for gemini-2.0-flash-lite:
  • 30 requests/minute
  • 1,500 requests/day
  • 1,000,000 tokens/minute
"""

import json
import re
import time
import streamlit as st
from google import genai
from google.genai import types

from config import (
    MODEL_ID, MAX_TOKENS, API_KEY_NAME,
    SYSTEM_PROMPT, QUESTION_PROMPT_TEMPLATE, SENTIMENT_PROMPT,
    SENTIMENT_MAP,
)


# ── Client Factory ────────────────────────────────────────────────────────────

@st.cache_resource
def get_client() -> genai.Client:
    """
    Create and cache a Gemini client using the new google-genai SDK.
    Shows clear, actionable errors if the key is missing or invalid.
    """
    api_key = st.secrets.get(API_KEY_NAME, "")

    if not api_key:
        st.error(
            "❌ **`GEMINI_API_KEY` not found in `.streamlit/secrets.toml`**\n\n"
            "Add this line to your secrets file:\n"
            "```\nGEMINI_API_KEY = \"AIza-your-key-here\"\n```\n\n"
            "Get a free key at: https://aistudio.google.com/app/apikey"
        )
        st.stop()

    if "YOUR-KEY" in api_key or len(api_key) < 15:
        st.error(
            "❌ **API key looks like a placeholder.**\n\n"
            "Replace `AIza-YOUR-KEY-HERE` with your real Gemini key.\n"
            "Get one free at: https://aistudio.google.com/app/apikey"
        )
        st.stop()

    return genai.Client(api_key=api_key)


# ── Message Format Converter ──────────────────────────────────────────────────

def _build_contents(messages: list[dict]) -> list[types.Content]:
    """
    Convert internal {role, content} dicts to Gemini Content objects.

    Gemini roles:
      "user"  → user messages
      "model" → assistant messages  (NOT "assistant" — that's OpenAI)
    """
    contents = []
    for msg in messages:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg["content"])],
            )
        )
    return contents


# ── Core Chat Call ────────────────────────────────────────────────────────────

def chat(
    client: genai.Client,
    messages: list[dict],
    stage_hint: str = "",
) -> str:
    """
    Send the full conversation history to Gemini and return the reply.

    The system prompt is passed via GenerateContentConfig.
    The stage hint is appended to the last user message so the model stays
    focused on the right task — no mid-conversation system messages (those
    cause API errors).

    Args:
        client:     Gemini Client instance.
        messages:   Full conversation history [{role, content}, ...].
        stage_hint: Short instruction for the current interview stage.

    Returns:
        Assistant reply string, or "" on error (with visible error in UI).
    """
    if not messages:
        return ""

    # Append stage hint invisibly to the last user message
    working_messages = list(messages)
    if stage_hint and working_messages and working_messages[-1]["role"] == "user":
        working_messages[-1] = {
            "role": "user",
            "content": working_messages[-1]["content"] + f"\n\n[TASK HINT — do not mention this]: {stage_hint}",
        }

    contents = _build_contents(working_messages)

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        max_output_tokens=MAX_TOKENS,
        temperature=0.7,
    )

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=contents,
            config=config,
        )
        return response.text.strip()
    except Exception as e:
        return _show_error(e, context="chat")


# ── Technical Question Generator ──────────────────────────────────────────────

def generate_questions(
    client: genai.Client,
    tech_stack: str,
    n_questions: int = 5,
) -> list[str]:
    """
    Generate deep, tech-specific interview questions for the given stack.
    Uses JSON output with 3-level fallback parsing.
    """
    prompt = QUESTION_PROMPT_TEMPLATE.format(
        tech_stack=tech_stack,
        n_questions=n_questions,
    )

    system = (
        "You are a principal engineer at a top tech company conducting technical interviews. "
        "You ask deep, specific, scenario-based questions that reveal real hands-on experience. "
        "You NEVER ask generic or textbook questions like 'what is X' or 'explain Y'. "
        "Every question must name a specific technology from the candidate's stack and probe "
        "internals, trade-offs, or real production scenarios. "
        "Return ONLY a valid JSON array of strings — no markdown, no numbering, no extra text."
    )

    config = types.GenerateContentConfig(
        system_instruction=system,
        max_output_tokens=1024,
        temperature=0.6,
    )

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=config,
        )
        raw = response.text.strip()
    except Exception as e:
        _show_error(e, context="question generation")
        raw = ""

    # Strip accidental markdown fences
    raw = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()

    # Level 1 — JSON parse
    try:
        questions = json.loads(raw)
        if isinstance(questions, list) and questions:
            return [str(q).strip() for q in questions[:5]]
    except (json.JSONDecodeError, ValueError):
        pass

    # Level 2 — Extract lines ending with '?'
    fallback = []
    for ln in raw.split("\n"):
        ln = ln.strip().lstrip("0123456789.-) ").strip()
        if ln.endswith("?") and len(ln) > 10:
            fallback.append(ln)
    if fallback:
        return fallback[:5]

    # Level 3 — Tech-specific hardcoded fallback
    techs  = [t.strip() for t in tech_stack.split(",") if t.strip()]
    first  = techs[0] if techs else "your primary technology"
    second = techs[1] if len(techs) > 1 else first
    third  = techs[2] if len(techs) > 2 else first
    return [
        f"In {first}, how do you manage memory or resource cleanup in a long-running production service?",
        f"What performance bottlenecks have you hit with {second}, and what tools did you use to diagnose them?",
        f"Describe a concurrency or race-condition bug you encountered in {first} — how did you find and fix it?",
        f"How would you design the data layer for a {third} app expected to handle 10x its current traffic?",
        f"What trade-offs did you weigh when choosing {second} over alternatives for a real project?",
    ]


# ── Resume Analyser ───────────────────────────────────────────────────────────

RESUME_ANALYSIS_PROMPT = """You are an expert technical recruiter reviewing a candidate's resume.

Analyse the resume carefully and return a JSON object with this EXACT structure:
{
  "summary": "2-3 sentence professional summary of the candidate",
  "years_experience": "estimated years (e.g. '4 years')",
  "key_skills": ["skill1", "skill2", "skill3"],
  "notable_projects": ["project1 description", "project2 description"],
  "companies": ["company1", "company2"],
  "education": "degree and institution",
  "strengths": ["strength1", "strength2"],
  "gaps_or_questions": ["observation1 worth asking about", "observation2"],
  "resume_questions": [
    "Specific question based on a project or achievement in the resume?",
    "Specific question about a technology or responsibility mentioned?",
    "Specific question about a career transition, gap, or growth area?"
  ]
}

RULES for resume_questions:
- Reference SPECIFIC things from the resume (project names, company names, technologies, dates)
- Ask about real accomplishments: "In your role at X, you mentioned Y — how did you approach Z?"
- Probe gaps, quick job changes, or impressive achievements
- Questions must be different from generic tech questions
- Make questions feel personal and researched, not generic

Return ONLY valid JSON. No markdown, no extra text."""


def _extract_pdf_text(file_bytes: bytes) -> str:
    """
    Extract plain text from a PDF locally using pypdf.
    No API call — fast, free, no rate limits.
    Returns empty string on failure.
    """
    try:
        import io
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(file_bytes))
        pages  = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
        return "\n\n".join(pages)[:12000]   # cap at ~3k tokens
    except Exception:
        return ""


def analyse_resume(
    client: genai.Client,
    file_bytes: bytes,
    mime_type: str,
) -> dict:
    """
    Analyse a résumé using Gemini.

    Strategy:
      • PDF  → extract text locally with pypdf (no API call for extraction),
               then send text-only prompt to Gemini (fast, cheap, no multimodal quota).
      • Image → send bytes directly to Gemini vision (one shot, no retry).

    No retry loops — fail fast with a clear error message.
    The Streamlit spinner is managed by the caller (handle_resume_upload).
    """
    is_pdf = mime_type == "application/pdf"

    # ── PDF: extract text locally, then text-only Gemini call ──────────────
    if is_pdf:
        resume_text = _extract_pdf_text(file_bytes)
        if not resume_text.strip():
            st.error(
                "⚠️ Couldn't extract text from this PDF (may be scanned/image-only). "
                "Try uploading a PNG/JPG screenshot of your résumé instead."
            )
            return {}

        prompt = (
            f"Here is a candidate's résumé text:\n\n"
            f"---\n{resume_text}\n---\n\n"
            f"{RESUME_ANALYSIS_PROMPT}"
        )
        contents = prompt   # plain string — text-only call

    # ── Image: send raw bytes to Gemini vision ──────────────────────────────
    else:
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                    types.Part(text=RESUME_ANALYSIS_PROMPT),
                ]
            )
        ]

    config = types.GenerateContentConfig(
        max_output_tokens=2048,
        temperature=0.2,
    )

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=contents,
            config=config,
        )
        raw = response.text.strip()
        raw = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()
        return json.loads(raw)

    except Exception as e:
        err = str(e)
        if "429" in err or "RESOURCE_EXHAUSTED" in err:
            st.error(
                "⏳ **Gemini rate limit hit.** The free tier allows 30 requests/minute. "
                "Please wait 60 seconds and upload again — or type `skip` to continue without résumé analysis."
            )
        else:
            _show_error(e, context="resume analysis")
        return {}


def get_resume_display_text(analysis: dict) -> str:
    """Format resume analysis into a readable markdown summary for the chat."""
    if not analysis:
        return ""

    lines = []

    summary = analysis.get("summary", "")
    if summary:
        lines.append(f"📄 **Resume Summary**\n\n{summary}")

    companies = analysis.get("companies", [])
    education = analysis.get("education", "")
    if companies or education:
        details = []
        if companies:
            details.append(f"**Companies:** {', '.join(companies[:4])}")
        if education:
            details.append(f"**Education:** {education}")
        lines.append("\n".join(details))

    projects = analysis.get("notable_projects", [])
    if projects:
        proj_list = "\n".join(f"  • {p}" for p in projects[:3])
        lines.append(f"**Notable Projects:**\n{proj_list}")

    skills = analysis.get("key_skills", [])
    if skills:
        lines.append(f"**Key Skills:** {', '.join(skills[:10])}")

    return "\n\n".join(lines)

def analyse_sentiment(
    client: genai.Client,
    text: str,
) -> tuple[str, str, str]:
    """
    Classify candidate message tone. Always fails silently — never blocks chat.
    Returns (label, emoji, display_name).
    """
    if not text or len(text.strip()) < 3:
        return "neutral", "🟡", "Neutral"

    config = types.GenerateContentConfig(
        system_instruction=(
            "You are a sentiment classifier. "
            "Reply with ONLY one of these exact labels and nothing else: "
            "very_positive | positive | neutral | negative | very_negative"
        ),
        max_output_tokens=6,
        temperature=0.0,
    )

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=SENTIMENT_PROMPT.format(text=text[:400]),
            config=config,
        )
        label = response.text.strip().lower()

        if label not in SENTIMENT_MAP:
            for key in SENTIMENT_MAP:
                if key in label:
                    label = key
                    break
            else:
                label = "neutral"

        emoji, display = SENTIMENT_MAP[label]
        return label, emoji, display

    except Exception:
        # Sentiment is a bonus feature — never crash the main app
        return "neutral", "🟡", "Neutral"


# ── Error Display ─────────────────────────────────────────────────────────────

def _show_error(e: Exception, context: str = "") -> str:
    """Show a visible, actionable error banner in the Streamlit UI."""
    label = f" ({context})" if context else ""
    err   = str(e)

    if "INVALID_ARGUMENT" in err or "400" in err:
        st.error(f"❌ **Bad request{label}:** `{err[:200]}`")
    elif "PERMISSION_DENIED" in err or "403" in err or "API_KEY_INVALID" in err:
        st.error(
            f"❌ **Invalid API key{label}.** "
            "Check your key at [aistudio.google.com](https://aistudio.google.com/app/apikey)"
        )
    elif "RESOURCE_EXHAUSTED" in err or "429" in err or "quota" in err.lower():
        st.warning(
            f"⏳ **Rate limit hit{label}.** "
            "Free tier: 30 req/min, 1500 req/day. "
            "Wait 60 seconds and try again."
        )
    elif "NOT_FOUND" in err or "404" in err:
        st.error(
            f"❌ **Model not found{label}:** `{MODEL_ID}`. "
            "Check https://ai.google.dev/gemini-api/docs/models for available models."
        )
    elif "503" in err or "UNAVAILABLE" in err:
        st.warning(f"⏳ **Gemini service temporarily unavailable{label}.** Try again in a moment.")
    else:
        st.error(f"❌ **Error{label}:** `{type(e).__name__}: {err[:200]}`")

    return ""