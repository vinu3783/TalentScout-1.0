"""
config.py
─────────
Central configuration for TalentScout Hiring Assistant.
Edit this file to customise prompts, stages, and app behaviour.
"""

# ── App Identity ────────────────────────────────────────────────────────────
APP_TITLE       = "TalentScout"
APP_SUBTITLE    = "AI-Powered Hiring Assistant"
BOT_NAME        = "TalentBot"
COMPANY_NAME    = "TalentScout"
MODEL_ID        = "gemini-2.0-flash-lite"  # best free-tier quota (30 RPM, 1500 RPD)
MAX_TOKENS      = 1024
API_KEY_NAME    = "GEMINI_API_KEY"       # key in .streamlit/secrets.toml

# ── Conversation Stages (ordered pipeline) ──────────────────────────────────
STAGES = [
    "greeting",
    "collect_name",
    "collect_email",
    "collect_phone",
    "collect_experience",
    "collect_position",
    "collect_location",
    "collect_tech_stack",
    "collect_resume",          # ← NEW: optional resume upload
    "generate_questions",
    "ask_questions",
    "farewell",
]

# ── Exit Keywords ────────────────────────────────────────────────────────────
EXIT_KEYWORDS = {"exit", "quit", "bye", "goodbye", "end", "stop", "done", "q"}

# ── Sentiment Labels & Emoji ─────────────────────────────────────────────────
SENTIMENT_MAP = {
    "very_positive": ("🟢", "Very Positive"),
    "positive":      ("🟩", "Positive"),
    "neutral":       ("🟡", "Neutral"),
    "negative":      ("🟧", "Negative"),
    "very_negative": ("🔴", "Very Negative"),
}

# ── Field Metadata ───────────────────────────────────────────────────────────
FIELDS = {
    "name":       {"label": "👤 Full Name",        "icon": "👤"},
    "email":      {"label": "📧 Email",             "icon": "📧"},
    "phone":      {"label": "📞 Phone",             "icon": "📞"},
    "experience": {"label": "🗓️ Experience",        "icon": "🗓️"},
    "position":   {"label": "💼 Desired Role",      "icon": "💼"},
    "location":   {"label": "📍 Location",          "icon": "📍"},
    "tech_stack": {"label": "🛠️ Tech Stack",        "icon": "🛠️"},
}

# ── Placeholders per stage ───────────────────────────────────────────────────
PLACEHOLDERS = {
    "collect_name":       "e.g.  Aarav Sharma",
    "collect_email":      "e.g.  aarav@example.com",
    "collect_phone":      "e.g.  +91 98765 43210",
    "collect_experience": "e.g.  3 years  or  5+",
    "collect_position":   "e.g.  Backend Engineer, ML Engineer",
    "collect_location":   "e.g.  Bengaluru, India",
    "collect_tech_stack": "e.g.  Python, FastAPI, React, PostgreSQL, Docker",
    "collect_resume":     "Type 'skip' to proceed without uploading…",
    "ask_questions":      "Type your answer here…",
    "default":            "Type your message…",
}

# ── Stage hints sent to LLM on every call ────────────────────────────────────
STAGE_HINTS = {
    "collect_name":       "Ask warmly for the candidate's full name.",
    "collect_email":      "Email collected. Ask for their email address.",
    "collect_phone":      "Ask for their phone number with country code.",
    "collect_experience": "Ask how many years of professional experience they have.",
    "collect_position":   "Ask which tech role(s) they are interested in.",
    "collect_location":   "Ask their current city and country.",
    "collect_tech_stack": (
        "Ask the candidate to list their FULL tech stack: programming languages, "
        "frameworks, databases, cloud tools, DevOps tools, etc. Be encouraging."
    ),
    "ask_questions": "Ask the next technical question clearly and professionally.",
    "farewell":      "Thank the candidate, summarise next steps, end the conversation.",
}

# ── Master System Prompt ─────────────────────────────────────────────────────
SYSTEM_PROMPT = f"""You are {BOT_NAME}, a warm, professional, and highly competent hiring assistant \
for {COMPANY_NAME} — a recruitment agency specialising in technology placements.

═══ YOUR SOLE PURPOSE ═══
1. Greet the candidate and explain the screening process.
2. Collect: full name, email, phone, years of experience, desired role(s), current location, tech stack.
3. After the tech stack is declared, generate 3-5 focused technical questions tailored to each technology.
4. Ask those questions one at a time, acknowledge each answer, then move on.
5. Conclude graciously and tell the candidate what happens next.

═══ STRICT RULES ═══
• Stay 100 % on-topic. If the user goes off-topic, politely redirect them.
• Never request financial, health, or password information.
• Be concise — responses ≤ 120 words unless answering a complex topic.
• If input is ambiguous, ask for clarification instead of guessing.
• Never evaluate or score answers — only acknowledge them encouragingly.
• Use the candidate's first name once you know it.
"""

# ── Question Generation Prompt ────────────────────────────────────────────────
QUESTION_PROMPT_TEMPLATE = """You are conducting a technical interview. The candidate listed this tech stack: {tech_stack}

Generate exactly {n_questions} technical interview questions following ALL these rules:

RULES:
1. Each question MUST name a specific technology from the stack above — no generic questions.
2. Questions must probe DEEP understanding: internals, trade-offs, edge cases, real scenarios.
3. NEVER ask "what is X" or "explain X" — ask HOW, WHY, or WHEN to use specific features.
4. Each question must be about a DIFFERENT technology from the stack.
5. Questions should reveal whether the candidate has actually used the technology in production.
6. Difficulty: senior/intermediate level — not beginner.

BAD examples (too generic — never generate these):
- "What are the key features of Python?"
- "Explain object-oriented programming."
- "What is a REST API?"

GOOD examples (specific, deep, scenario-based):
- "In Python, how does the GIL affect CPU-bound vs I/O-bound multithreading, and when would you choose multiprocessing instead?"
- "When using PostgreSQL, how would you diagnose and fix a slow query that only becomes slow under high concurrency?"
- "In React, what is the difference between useCallback and useMemo, and give a scenario where using one instead of the other would cause a bug?"
- "How does Docker layer caching work, and what ordering of Dockerfile instructions would you use to optimise build times for a Python app?"

Now generate {n_questions} questions for the stack: {tech_stack}

Return ONLY a valid JSON array of strings. No markdown, no numbering, no extra text.
Example format: ["Question 1?", "Question 2?", "Question 3?"]
"""

# ── Sentiment Prompt ──────────────────────────────────────────────────────────
SENTIMENT_PROMPT = """Analyse the emotional tone of the following candidate message.
Reply with EXACTLY one of these labels (no other text):
very_positive | positive | neutral | negative | very_negative

Message: \"\"\"{text}\"\"\""""