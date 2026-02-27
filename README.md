# 🤖 TalentScout — AI-Powered Hiring Assistant Chatbot

> AI/ML Intern Assignment · PG-AGI  
> Built with Python · Streamlit · Local NLP · Google Gemini (optional)

---

## 📌 Project Overview

**TalentScout** is an intelligent hiring assistant chatbot that automates the initial screening of technology candidates. It conducts a structured, conversational interview — collecting candidate details, optionally analysing their resume, and generating targeted technical questions based on their declared tech stack and experience level.

### Key Capabilities

| Feature | Description |
|---|---|
| 🗣 Structured Interview Flow | 11-stage pipeline from greeting to farewell |
| 📋 Info Collection | Name, email, phone, experience, role, location, tech stack |
| 📄 Resume Parsing | Local PDF extraction — extracts companies, projects, skills, generates personalised questions |
| 🛠 Technical Questions | 420+ curated questions across 21 tech stacks, levelled by experience |
| 🎨 Premium UI | Custom dark-theme Streamlit interface with glassmorphism design |
| 🔒 GDPR-Compliant | Local data storage, no external data transmission |
| ⚡ Zero API Dependency | Core flow runs 100% locally — no API key required for basic use |

---

## 🗂 Project Structure

```
talentscout/
│
├── app.py                  # Main Streamlit app — all stage handlers & routing
├── config.py               # Central config — stages, prompts, constants
├── question_bank.py        # 420+ curated tech interview questions (local)
├── resume_parser.py        # Local PDF parser — keyword extraction & question gen
├── ui_styles.py            # All CSS, HTML components, sidebar widgets
├── requirements.txt        # Python dependencies
│
├── utils/
│   ├── llm.py              # Google Gemini client (optional fallback only)
│   ├── validators.py       # Email, phone, name input validators
│   └── storage.py          # Local JSON candidate data storage
│
└── .streamlit/
    └── secrets.toml        # API key config (optional)
```

---

## ⚙️ Installation Instructions

### Prerequisites

- Python 3.10 or higher
- pip

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/talentscout.git
cd talentscout
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
pip install pdfplumber pypdf
```

Full dependency list:

```
streamlit>=1.35.0
pdfplumber
pypdf
google-genai>=1.0.0    # optional — only for Gemini fallback question generation
```

### Step 4 — API Key Setup (Optional)

The chatbot runs fully without an API key. Gemini is only used as a fallback when the local question bank has no match for a niche tech stack.

To enable Gemini (optional):

```bash
mkdir -p .streamlit
```

Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "AIza-your-key-here"
```

Get a free key at: https://aistudio.google.com/app/apikey

### Step 5 — Run the Application

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🚀 Usage Guide

### Candidate Flow

1. **Greeting** — TalentBot introduces itself and the screening process
2. **Info Collection** — Bot asks for full name, email, phone, years of experience, desired role, current location, and tech stack — one field at a time
3. **Resume Upload** *(optional)* — Candidate uploads a PDF resume. The bot extracts text locally using `pdfplumber`, finds companies, projects, and skills, then generates 3 personalised questions referencing actual experience
4. **Technical Questions** — 3–8 curated questions matched to the declared tech stack and levelled by experience (fresher vs experienced)
5. **Farewell** — Bot summarises the candidate's full profile and explains next steps

### Exit Keywords

Type any of these at any point to end the session:

`exit` · `quit` · `bye` · `goodbye` · `end` · `stop` · `done`

### Resume Upload Notes

- **PDF only** — Max 10 MB
- Works best with text-based PDFs (not scanned/image PDFs)
- If text cannot be extracted, bot automatically continues with tech stack questions — no disruption to the flow

---

## 🔧 Technical Details

### Architecture

The app uses a **linear stage pipeline** managed through `st.session_state`. Each stage maps to a dedicated handler function in `app.py`. No LLM memory is needed between stages — all context is held in Streamlit's session state dictionary.

```
greeting → collect_name → collect_email → collect_phone →
collect_experience → collect_position → collect_location →
collect_tech_stack → collect_resume → generate_questions →
ask_questions → farewell
```

### Libraries Used

| Library | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `pdfplumber` | Primary PDF text extraction (handles complex layouts and tables) |
| `pypdf` | Fallback PDF text extraction |
| `re` (stdlib) | Regex-based keyword and pattern matching in resume parser |
| `json` (stdlib) | Local candidate data storage |
| `google-genai` | Optional Gemini API for fallback question generation |

### Question Bank (`question_bank.py`)

- 420+ hand-curated technical interview questions
- Covers 21 tech stacks: Python, JavaScript, React, Java, Go, SQL, MongoDB, Docker, Kubernetes, AWS, GCP, Machine Learning, Deep Learning, NLP, Kafka, Microservices, CI/CD, and more
- Two difficulty levels per technology: **Fresher** (0–2 years) and **Experienced** (3+ years)
- Selection logic: parses the candidate's tech stack string, matches tokens against the `TECH_GROUPS` dictionary, picks 2 questions per matched technology

### Resume Parser (`resume_parser.py`)

Fully local — zero API calls. Pipeline:

1. **Text extraction** — `pdfplumber` first, `pypdf` as fallback
2. **Skill detection** — scans text for 40+ tech group keywords (e.g. `"fastapi"` → `"Python"` group)
3. **Company extraction** — regex matching `"at CompanyName |"` and pipe-separated lines with year ranges
4. **Project extraction** — scans lines under the `PROJECTS` section header, filters to short title-length lines (10–60 chars)
5. **Education extraction** — matches degree keywords (B.Tech, M.S., MBA, etc.)
6. **Experience estimation** — extracts explicit year mentions, or calculates span from date ranges
7. **Question generation** — template-based questions referencing actual project names and company names extracted above

### Data Storage (`utils/storage.py`)

- Candidate profiles saved as JSON in a local `candidates/` directory
- Each record includes all collected fields plus the list of questions and answers
- No cloud storage, no external data transmission
- GDPR-compliant: data can be deleted at any time by removing the `candidates/` folder

### UI Design (`ui_styles.py`)

- **Dark theme** — obsidian background (`#080912`)
- **Glassmorphism** — translucent card borders with blur effects
- **Typography** — Syne (headings), Outfit (body), JetBrains Mono (code/tags)
- **Colour palette** — Electric Indigo · Purple · Emerald accent
- **Sidebar** — Live progress tracker, candidate profile card, resume insights card, question progress indicator
- **Chat bubbles** — iMessage-style with sharp speaker corner and gradient top accent

---

## 🎯 Prompt Design

### Information Gathering

All info-gathering responses are **hardcoded strings** — no LLM calls. This was a deliberate architectural decision for three reasons:

1. Eliminates rate limit errors on free-tier APIs
2. Responses are instant (no network latency)
3. Guarantees 100% on-topic, predictable behaviour

Each stage transition has a specific, warm, contextual response. After collecting the name, the bot addresses the candidate by first name for the remainder of the session.

### Technical Question Generation

**Primary — Curated question bank (local, zero API):**

```
Parse tech_stack string
  → split on commas/spaces
  → match each token against TECH_GROUPS dictionary
  → fetch 2 questions per matched group
  → select fresher or experienced tier based on years_of_experience
```

**Fallback — Gemini API (only for unknown stacks):**

When a candidate declares a niche tech stack not present in the bank, the app calls Gemini with this system prompt:

```
You are a principal engineer at a top tech company conducting technical interviews.
Ask deep, specific, scenario-based questions that reveal real hands-on experience.
Never ask generic questions like "what is X" or "explain Y".
Every question must name a specific technology and probe internals, trade-offs,
or real production scenarios.
Return ONLY a valid JSON array of strings.
```

### Resume-Based Questions

Questions are generated from templates that embed actual resume content:

| Type | Template |
|---|---|
| Project | `"Your resume mentions {project} — walk me through the most challenging part of building it and what you'd do differently now."` |
| Company | `"At {company}, what was the most technically complex problem you solved and what was your approach?"` |
| Two companies | `"You've worked at both {co1} and {co2} — what was the biggest technical or architectural difference between the two environments?"` |
| Skill depth | Technology-specific questions from the `TECH_QUESTIONS` dictionary in `resume_parser.py` |

### Fallback Mechanism

Unexpected inputs are handled per-stage:

- **Info fields** — Input is validated (email format, phone digits, etc.). Invalid input shows a specific error and re-asks the same question without advancing
- **Resume stage** — Only `skip` keyword or file upload accepted; any other text shows a redirect message
- **Q&A stage** — Any text is accepted as an answer (no format restriction imposed on candidates)
- **General** — Bot responds with "Please answer the current question to continue" and does not deviate from the interview flow

---

## 🧩 Challenges & Solutions

### Challenge 1 — Gemini API Rate Limits

**Problem:** The free tier allows only 30 requests/minute. Early versions called the API for every single field collection, answer acknowledgement, and sentiment check — easily 20+ calls per session, causing constant rate limit errors.

**Solution:** Eliminated all non-essential API calls. Info gathering uses hardcoded strings. Answer acknowledgements use a list of 7 rotating local phrases. Sentiment analysis was removed from the core flow. Result: 0 API calls per session for most users; maximum 1 call (question generation fallback) for unusual tech stacks.

### Challenge 2 — Infinite Upload Loop on Scanned PDFs

**Problem:** When a scanned (image-based) PDF was uploaded, `pypdf` returned empty text. The error handler showed a warning but did not advance the stage or set any processed flag. Streamlit's rerun mechanism re-triggered the upload widget on every render cycle → re-read the file → same error → infinite loop of error messages in the chat.

**Solution:** Added a `resume_processed` boolean flag in session state, set to `True` as the very first line of `handle_resume_upload()` — before any parsing begins. The upload widget checks `resume_processed`, not `resume_uploaded`. Even on failure, the bot now automatically advances to the question stage so the candidate is never blocked.

### Challenge 3 — Complex PDF Layouts

**Problem:** `pypdf` failed on resumes with tables, multi-column layouts, or custom fonts — a common format for professionally designed resumes.

**Solution:** Added `pdfplumber` as the primary extractor (handles layout-aware extraction including tables and columns), with `pypdf` as a silent fallback. If both fail, the app auto-continues with tech stack questions — no user action required.

### Challenge 4 — Streamlit Rerun Recursion

**Problem:** Streamlit reruns the full script on every widget interaction. Functions that triggered side-effects and then called `st.rerun()` could enter recursive loops.

**Solution:** All session state mutations are completed before `st.rerun()` is called. The `resume_processed` flag pattern ensures each upload handler executes exactly once per file, regardless of how many reruns Streamlit performs.

---

## 📦 Deliverables Checklist

- [x] Source code — well-structured, modular Python
- [x] Custom Streamlit UI with premium dark theme
- [x] All 7 candidate info fields collected and validated
- [x] Tech stack → 3–5 targeted technical questions (local question bank)
- [x] Resume upload → personalised questions (local parser)
- [x] Exit keyword handling at every stage
- [x] Fallback for unexpected or invalid inputs
- [x] Graceful farewell with full profile summary and next steps
- [x] Local candidate data storage (GDPR-compliant)
- [x] README documentation
- [x] Demo video (Loom)
- [x] Public GitHub repository

---

## 🏆 Bonus Enhancements Implemented

**UI Enhancements ✅**
- Premium dark glassmorphism design language
- Animated step-by-step progress tracker in sidebar
- Live candidate profile card updated in real time
- Resume insights card showing companies, skills, and project count
- Question progress bar with dot indicators
- iMessage-style chat bubbles with gradient accents
- Custom styled file uploader

**Performance Optimization ✅**
- Zero API calls during info gathering → instant responses
- Local question bank lookup → < 1ms per question
- Local PDF parsing → no network round-trip
- `resume_processed` flag prevents any redundant computation on reruns

---

## 👤 Author

**Vinayaka G C**  
AI/ML Intern Candidate  
Assignment submitted to PG-AGI via Career Portal
