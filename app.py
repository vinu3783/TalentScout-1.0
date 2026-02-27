"""
app.py — TalentScout Hiring Assistant  v6
──────────────────────────────────────────
ZERO API CALLS. Fully local, no Gemini needed.

• Info gathering  — hardcoded responses
• Resume parsing  — pypdf + local keyword extraction
• Questions       — curated question bank + local templates
• Acknowledgements— rotating local strings

Run:  streamlit run app.py
"""

import streamlit as st

from config import (
    APP_TITLE, BOT_NAME, STAGES, EXIT_KEYWORDS, PLACEHOLDERS,
)
from resume_parser  import parse_resume, generate_resume_questions
from utils.validators import VALIDATORS
from utils.storage    import save_candidate, load_all_candidates
from question_bank    import get_questions_for_stack
from ui_styles        import (
    get_css, get_header_html, get_sidebar_html, get_steps_html,
    get_profile_html, get_qprog_html,
    get_hist_item_html, get_welcome_splash, get_resume_card_html,
)

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TalentScout · AI Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(get_css(), unsafe_allow_html=True)


# ── SESSION STATE ─────────────────────────────────────────────────────────────
def init_session():
    defaults = {
        "stage":           "greeting",
        "messages":        [],
        "candidate":       {},
        "questions":       [],
        "bank_results":    [],
        "q_index":         0,
        "answers":         [],
        "greeted":         False,
        "ended":           False,
        "resume_analysis": {},
        "resume_uploaded": False,
        "resume_skipped":  False,
        "resume_processed": False,   # True after ANY parse attempt - prevents infinite loop
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ── MESSAGE HELPERS ───────────────────────────────────────────────────────────
def bot_say(text: str):
    st.session_state.messages.append({"role": "assistant", "content": text})

def user_said(text: str):
    st.session_state.messages.append({"role": "user", "content": text})

def is_exit(text: str) -> bool:
    return bool(set(text.lower().split()) & EXIT_KEYWORDS)


# ── ROTATING ACKS (zero API) ──────────────────────────────────────────────────
_ACKS = [
    "Got it, thank you! ✅",
    "Great response! 👍",
    "Noted, moving on! 💪",
    "Appreciate the detail! 🎯",
    "Perfect, next one! 🚀",
    "Thanks for sharing! 🙌",
    "Excellent answer! ✨",
]


# ── LOCAL QUESTION FALLBACK ───────────────────────────────────────────────────
# Used when question bank has no match for a tech stack — zero API calls.
_FALLBACK_QUESTIONS = [
    "Describe the most complex technical problem you've solved in your current role and your approach to debugging it.",
    "Walk me through a system you designed from scratch — what trade-offs did you make in the architecture?",
    "Tell me about a time your code caused a production issue. How did you identify and fix it?",
    "How do you approach performance optimisation in a system you're unfamiliar with?",
    "Describe how you've handled technical debt in a project you've worked on.",
]


# ── STAGE HANDLERS ────────────────────────────────────────────────────────────

def handle_greeting():
    bot_say(
        "👋 Welcome to **TalentScout**! I'm **TalentBot**, your AI screening assistant.\n\n"
        "I'll collect a few details, optionally review your **resume**, then ask "
        "**technical questions** tailored to your exact skill set.\n\n"
        "⏱ Takes about **5–10 minutes** · Type `exit` anytime to leave.\n\n"
        "**Let's start — what's your full name?**"
    )
    st.session_state.stage   = "collect_name"
    st.session_state.greeted = True


def handle_collect(stage: str, user_input: str):
    """All collect_* stages — hardcoded responses, zero API."""
    validator = VALIDATORS.get(stage)
    if validator:
        valid, err = validator(user_input)
        if not valid:
            bot_say(f"⚠️ {err} Please try again.")
            return

    field = stage.replace("collect_", "")
    st.session_state.candidate[field] = user_input.strip()
    name = (st.session_state.candidate.get("name") or "there").split()[0]

    current_idx = STAGES.index(stage)
    next_stage  = STAGES[current_idx + 1]
    st.session_state.stage = next_stage

    responses = {
        "collect_email":      f"Nice to meet you, **{name}**! 👋\n\nWhat's your **email address**?",
        "collect_phone":      "Got it! What's your **phone number**? *(include country code, e.g. +91)*",
        "collect_experience": "Perfect! How many **years of professional experience** do you have?",
        "collect_position":   "Great! What **role(s)** are you targeting? *(e.g. Backend Engineer, ML Engineer)*",
        "collect_location":   "Excellent! What's your current **city and country**?",
        "collect_tech_stack": (
            f"Almost there, **{name}**! 🛠️\n\n"
            "List your complete **tech stack** — programming languages, frameworks, "
            "databases, cloud tools, DevOps — everything you'd use on the job.\n\n"
            "*(e.g. Python, FastAPI, React, PostgreSQL, Docker, AWS)*"
        ),
    }

    if next_stage in responses:
        bot_say(responses[next_stage])
    elif next_stage == "collect_resume":
        _prompt_resume_upload()
    elif next_stage == "generate_questions":
        handle_generate_questions()
    else:
        bot_say("Got it! Please continue.")


def _prompt_resume_upload():
    name = st.session_state.candidate.get("name", "there").split()[0]
    bot_say(
        f"Great work so far, **{name}**! 📄\n\n"
        "Would you like to upload your **resume**? I'll scan it and ask questions "
        "specifically about your projects, companies, and experience — no AI, just "
        "smart keyword matching.\n\n"
        "**Accepted:** PDF only · Max 10 MB\n\n"
        "👇 Use the **upload button** below — or type `skip` to continue without one."
    )


def handle_resume_skip():
    st.session_state.resume_skipped   = True
    st.session_state.resume_processed = True
    user_said("skip")
    bot_say("No problem! Loading your technical questions… 🚀")
    st.session_state.stage = "generate_questions"
    handle_generate_questions()


def handle_resume_upload(file_bytes: bytes, mime_type: str, filename: str):
    """Parse résumé locally — zero API calls."""
    user_said(f"📎 Uploaded: *{filename}*")

    # Mark as processed FIRST — prevents re-running on Streamlit reruns regardless of outcome
    st.session_state.resume_processed = True

    with st.spinner("📄 Reading your resume…"):
        result = parse_resume(file_bytes, mime_type)

    if result.get("error"):
        # Always set processed + uploaded to prevent any loop
        st.session_state.resume_uploaded  = True
        err = result["error"]
        if err == "scanned_pdf":
            bot_say(
                "📄 Your PDF appears to be **image-based** (scanned), so I couldn't extract text from it locally.\n\n"
                "No worries — I'll use your **declared tech stack** to generate your technical questions instead! 🚀"
            )
        else:
            bot_say("📄 Couldn't read that file — using your tech stack for questions instead. 🚀")
        st.session_state.stage = "generate_questions"
        handle_generate_questions()
        return

    st.session_state.resume_analysis = result
    st.session_state.resume_uploaded  = True

    name      = st.session_state.candidate.get("name", "there").split()[0]
    skills    = result.get("skills", [])
    projects  = result.get("projects", [])
    companies = result.get("companies", [])
    edu       = result.get("education", "")
    exp       = result.get("experience", "")
    qs        = result.get("questions", [])

    lines = [f"✅ **Resume scanned, {name}!**\n"]
    if companies: lines.append(f"🏢 **Companies:** {', '.join(companies[:3])}")
    if edu:       lines.append(f"🎓 **Education:** {edu}")
    if exp:       lines.append(f"🗓 **Experience:** {exp}")
    if skills:    lines.append(f"⚡ **Skills found:** {', '.join(skills[:8])}")
    if projects:  lines.append(f"🛠 **Projects:** {', '.join(projects[:3])}")
    lines.append(f"\n📝 Ready with **{len(qs)} resume questions** + tech questions. Let's go! 🎯")

    bot_say("\n\n".join(lines))
    st.session_state.stage = "generate_questions"
    handle_generate_questions()


def handle_generate_questions():
    """Build question list — 100% local, zero API calls."""
    tech_stack = st.session_state.candidate.get("tech_stack", "")
    experience = st.session_state.candidate.get("experience", "1")
    name       = st.session_state.candidate.get("name", "there").split()[0]
    analysis   = st.session_state.get("resume_analysis", {})

    all_questions = []
    all_meta      = []

    # ── 1. Resume-based questions (local keyword parser) ─────────────────────
    resume_qs = analysis.get("questions", [])
    for item in resume_qs[:3]:
        q = item["question"] if isinstance(item, dict) else item
        all_questions.append(q)
        all_meta.append({
            "tech":   "resume",
            "level":  "resume",
            "source": item.get("source", "") if isinstance(item, dict) else "",
        })

    # ── 2. Curated question bank (local JSON, zero API) ───────────────────────
    bank = get_questions_for_stack(tech_stack, experience, questions_per_tech=2)
    if bank:
        for item in bank:
            all_questions.append(item["question"])
            all_meta.append(item)
    else:
        # ── 3. Local template fallback — still zero API ───────────────────────
        for q in _FALLBACK_QUESTIONS[:5]:
            all_questions.append(q)
            all_meta.append({"tech": "resume", "level": "resume"})

    # Summary bot message (only when no résumé was uploaded — else already shown)
    if not resume_qs:
        techs = list(dict.fromkeys(
            m["tech"] for m in all_meta if m["tech"] not in ("resume", "General")
        ))
        level = bank[0]["level"] if bank else "general"
        badge = "🟢 Fresher" if level == "fresher" else ("🔵 Experienced" if level == "experienced" else "")
        tech_str = f"on: **{', '.join(techs)}**" if techs else ""
        bot_say(
            f"🎯 Ready, **{name}**!\n\n"
            f"Loaded **{len(all_questions)} technical questions** {tech_str} {badge}\n\n"
            "Take your time — answer as fully as you like. Let's begin! 💪"
        )

    st.session_state.questions    = all_questions
    st.session_state.bank_results = all_meta
    st.session_state.q_index      = 0
    st.session_state.answers      = []
    st.session_state.stage        = "ask_questions"
    _ask_question(0, all_questions)


def _ask_question(index: int, questions: list):
    total = len(questions)
    q     = questions[index]
    meta  = st.session_state.get("bank_results", [])
    m     = meta[index] if meta and index < len(meta) else {}

    level = m.get("level", "")
    tech  = m.get("tech", "")

    if level == "resume":
        src    = m.get("source", "")
        header = f"**📄 Resume Q{index+1} of {total}**" + (f" · *{src}*" if src else "")
    elif level == "fresher":
        header = f"**🟢 Q{index+1} of {total}** · `{tech}`"
    elif level == "experienced":
        header = f"**🔵 Q{index+1} of {total}** · `{tech}`"
    else:
        header = f"**📝 Q{index+1} of {total}**"

    bot_say(f"{header}\n\n{q}")


def handle_answer(user_input: str):
    idx = st.session_state.q_index
    st.session_state.answers.append({
        "question": st.session_state.questions[idx],
        "answer":   user_input,
    })
    bot_say(_ACKS[idx % len(_ACKS)])

    next_idx = idx + 1
    st.session_state.q_index = next_idx
    if next_idx < len(st.session_state.questions):
        _ask_question(next_idx, st.session_state.questions)
    else:
        handle_farewell()


def handle_farewell():
    c       = st.session_state.candidate
    name    = (c.get("name") or "there").split()[0]
    has_res = bool(st.session_state.get("resume_analysis"))
    res_row = "\n| 📄 Resume | ✅ Scanned |" if has_res else ""

    save_candidate(c, st.session_state.answers)
    bot_say(
        f"🎉 **Screening complete, {name}! Well done.**\n\n"
        "---\n**📋 Your Profile**\n\n"
        f"| | |\n|---|---|\n"
        f"| 👤 Name | {c.get('name','—')} |\n"
        f"| 📧 Email | {c.get('email','—')} |\n"
        f"| 📞 Phone | {c.get('phone','—')} |\n"
        f"| 🗓 Experience | {c.get('experience','—')} |\n"
        f"| 💼 Role | {c.get('position','—')} |\n"
        f"| 📍 Location | {c.get('location','—')} |\n"
        f"| 🛠 Stack | {c.get('tech_stack','—')} |"
        f"{res_row}\n\n"
        "---\n✅ Our team will review your responses within **3–5 business days**.\n\n"
        "Thank you and best of luck! 🚀"
    )
    st.session_state.stage = "farewell"
    st.session_state.ended = True


# ── INPUT ROUTER ─────────────────────────────────────────────────────────────
def process_text_input(user_input: str):
    """Route every text message — zero API calls anywhere in this function."""
    if is_exit(user_input):
        user_said(user_input)
        bot_say("Thank you for chatting with **TalentScout**! 🙏 Best of luck! 🌟")
        st.session_state.ended = True
        return

    stage = st.session_state.stage

    if stage == "collect_resume":
        if user_input.lower().strip() in ("skip", "s", "no", "none", "pass"):
            handle_resume_skip()
        else:
            bot_say("👆 Use the **upload button** above to attach your PDF résumé, or type `skip`.")
        return

    user_said(user_input)

    collect_stages = [s for s in STAGES if s.startswith("collect_") and s != "collect_resume"]
    if stage in collect_stages:
        handle_collect(stage, user_input)
    elif stage == "ask_questions":
        handle_answer(user_input)
    else:
        bot_say("Please answer the current question to continue. 👆")


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
def render_sidebar():
    stage    = st.session_state.stage
    cand     = st.session_state.candidate
    analysis = st.session_state.get("resume_analysis", {})

    with st.sidebar:
        st.markdown(get_sidebar_html(), unsafe_allow_html=True)

        st.markdown('<div class="sb-label">Interview Progress</div>', unsafe_allow_html=True)
        st.markdown(get_steps_html(stage), unsafe_allow_html=True)

        st.markdown('<div class="sb-label">Candidate Profile</div>', unsafe_allow_html=True)
        st.markdown(get_profile_html(cand), unsafe_allow_html=True)

        if analysis:
            st.markdown('<div class="sb-label">📄 Resume Insights</div>', unsafe_allow_html=True)
            st.markdown(get_resume_card_html(analysis), unsafe_allow_html=True)

        if stage == "ask_questions":
            st.markdown('<div class="sb-label">Question Progress</div>', unsafe_allow_html=True)
            st.markdown(
                get_qprog_html(st.session_state.q_index, len(st.session_state.questions)),
                unsafe_allow_html=True,
            )

        with st.expander("🗂 Screening History"):
            records = load_all_candidates()
            if records:
                for r in records[:5]:
                    st.markdown(get_hist_item_html(r), unsafe_allow_html=True)
            else:
                st.markdown('<div class="pf-empty">No records yet.</div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="sb-footer">🔒 GDPR-compliant · Data encrypted at rest<br>'
            '100% local processing · No external API calls</div>',
            unsafe_allow_html=True,
        )


# ── RESUME UPLOADER ───────────────────────────────────────────────────────────
def render_resume_uploader():
    if st.session_state.stage != "collect_resume" or st.session_state.ended:
        return

    st.markdown("""
    <div class="resume-upload-zone">
      <div class="ru-icon">📄</div>
      <div class="ru-title">Upload Your Resume</div>
      <div class="ru-sub">PDF only · Max 10 MB · Parsed locally, no data sent externally</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        label="Drop your resume here",
        type=["pdf"],
        key="resume_file_uploader",
        label_visibility="collapsed",
    )

    if uploaded is not None and not st.session_state.resume_processed:
        raw = uploaded.read()
        if len(raw) > 10 * 1024 * 1024:
            st.session_state.resume_processed = True  # stop loop even on size error
            st.error("❌ File too large. Please upload a file under 10 MB.")
            return
        handle_resume_upload(raw, "application/pdf", uploaded.name)
        st.rerun()


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    init_session()

    st.markdown(get_header_html(st.session_state.stage), unsafe_allow_html=True)

    if not st.session_state.greeted:
        handle_greeting()

    render_sidebar()

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown(get_welcome_splash(), unsafe_allow_html=True)

    for msg in st.session_state.messages:
        role = msg["role"]
        with st.chat_message(role, avatar="🤖" if role == "assistant" else "🧑"):
            st.markdown(msg["content"])

    render_resume_uploader()

    st.markdown('</div>', unsafe_allow_html=True)

    # Input area
    if st.session_state.ended:
        st.markdown("<br>", unsafe_allow_html=True)
        _, c2, _ = st.columns([1, 2, 1])
        with c2:
            if st.button("🔄  Start New Session", use_container_width=True):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()
    else:
        stage       = st.session_state.stage
        placeholder = PLACEHOLDERS.get(stage, "Type your message…")
        if inp := st.chat_input(placeholder):
            process_text_input(inp.strip())
            st.rerun()

        st.markdown(
            '<div class="input-footer">'
            '<span>Press <kbd>Enter</kbd> to send · <kbd>Shift+Enter</kbd> for new line</span>'
            '<span>Type <kbd>exit</kbd> to end session</span>'
            '</div>',
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()