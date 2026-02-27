"""
ui_styles.py — TalentScout Premium UI  v4 (Final Polish)
─────────────────────────────────────────────────────────
All class names verified against app.py:
  chat-container · sb-label · sb-footer · input-footer · pf-empty · sb-top
"""

import re as _re


# ─────────────────────────────────────────────────────────────────────────────
# METADATA
# ─────────────────────────────────────────────────────────────────────────────
_STEPS = [
    ("greeting",           "👋", "Welcome"),
    ("collect_name",       "👤", "Full Name"),
    ("collect_email",      "📧", "Email"),
    ("collect_phone",      "📞", "Phone"),
    ("collect_experience", "🗓", "Experience"),
    ("collect_position",   "💼", "Desired Role"),
    ("collect_location",   "📍", "Location"),
    ("collect_tech_stack", "🛠", "Tech Stack"),
    ("collect_resume",     "📄", "Résumé"),
    ("generate_questions", "⚙️", "Loading…"),
    ("ask_questions",      "📝", "Tech Q&A"),
    ("farewell",           "✅", "Complete"),
]

_STAGE_BADGE = {
    "greeting":           "ACTIVE",
    "collect_name":       "COLLECTING",
    "collect_email":      "COLLECTING",
    "collect_phone":      "COLLECTING",
    "collect_experience": "COLLECTING",
    "collect_position":   "COLLECTING",
    "collect_location":   "COLLECTING",
    "collect_tech_stack": "COLLECTING",
    "collect_resume":     "UPLOAD",
    "generate_questions": "LOADING",
    "ask_questions":      "SCREENING",
    "farewell":           "DONE ✓",
}

_BAR = {
    "very_positive": ("vp", "100%"),
    "positive":      ("p",  "72%"),
    "neutral":       ("n",  "44%"),
    "negative":      ("ng", "26%"),
    "very_negative": ("vn", "12%"),
}


# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
def get_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── TOKENS ──────────────────────────────────────────────────────────────── */
:root{
  --bg:#07080e; --sf0:#0c0d1b; --sf1:#101220; --sf2:#161829;
  --glass:rgba(255,255,255,0.028);
  --gb:rgba(255,255,255,0.068);
  --gh:rgba(255,255,255,0.052);

  --indigo:#6366f1; --il:#818cf8;
  --i-dim:rgba(99,102,241,0.13); --i-glow:rgba(99,102,241,0.28);
  --purple:#a855f7; --p-dim:rgba(168,85,247,0.13);
  --emerald:#10b981; --e-dim:rgba(16,185,129,0.10);
  --amber:#f59e0b; --rose:#f43f5e;

  --t1:#eef0ff; --t2:#8e97bc; --t3:#47506e; --t4:#22273a;

  --r-xl:16px; --r-lg:13px; --r-md:9px; --r-sm:6px; --r-xs:4px;
  --fd:'Syne',sans-serif; --fb:'Outfit',sans-serif; --fm:'JetBrains Mono',monospace;
  --spring:cubic-bezier(.34,1.56,.64,1); --smooth:cubic-bezier(.4,0,.2,1);
}

/* ── BASE ─────────────────────────────────────────────────────────────────── */
*,*::before,*::after{box-sizing:border-box}
html,body,.stApp{font-family:var(--fb)!important;color:var(--t1)!important;background:var(--bg)!important}

.stApp{
  background:
    radial-gradient(ellipse 110% 70% at 0% 0%,   rgba(99,102,241,.10) 0%,transparent 52%),
    radial-gradient(ellipse  75% 85% at 100% 100%,rgba(168,85,247,.07) 0%,transparent 52%),
    radial-gradient(ellipse  55% 65% at 50%  50%, rgba(16,185,129,.04) 0%,transparent 62%),
    var(--bg)!important;
  background-attachment:fixed!important;
}
.stApp::before{
  content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:
    linear-gradient(rgba(99,102,241,.02) 1px,transparent 1px),
    linear-gradient(90deg,rgba(99,102,241,.02) 1px,transparent 1px);
  background-size:72px 72px;
  mask-image:radial-gradient(ellipse 90% 90% at 50% 50%,black 20%,transparent 100%);
  animation:gridDrift 28s ease-in-out infinite;
}
@keyframes gridDrift{0%,100%{transform:translate(0,0);opacity:.65}40%{transform:translate(-10px,7px);opacity:1}70%{transform:translate(7px,-5px);opacity:.8}}

/* ── SCROLLBAR ────────────────────────────────────────────────────────────── */
::-webkit-scrollbar{width:3px;height:3px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,var(--indigo),var(--purple));border-radius:99px}

/* ── LAYOUT RESET ─────────────────────────────────────────────────────────── */
.main .block-container{padding:0!important;max-width:100%!important}
section[data-testid="stMain"]>div{padding:0!important}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stStatusWidget"],.stDeployButton{display:none!important}

/* ── HEADER ───────────────────────────────────────────────────────────────── */
.ts-header{position:relative;overflow:hidden}
.ts-header-bg{
  position:absolute;inset:0;
  background:rgba(9,10,20,.97);
  backdrop-filter:blur(28px) saturate(1.5);
  border-bottom:1px solid var(--gb);
}
.ts-header-bg::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(125deg,rgba(99,102,241,.11) 0%,rgba(168,85,247,.05) 50%,rgba(16,185,129,.06) 100%);
}
.ts-header-bg::after{
  content:'';position:absolute;bottom:0;left:-100%;right:-100%;height:1px;
  background:linear-gradient(90deg,transparent 5%,var(--indigo) 25%,var(--purple) 50%,var(--emerald) 75%,transparent 95%);
  opacity:.55;animation:shimmerLine 5s linear infinite;
}
@keyframes shimmerLine{from{transform:translateX(-40%)}to{transform:translateX(40%)}}

.ts-header-inner{
  position:relative;z-index:1;display:flex;align-items:center;gap:14px;padding:17px 28px;
}

.ts-logo{
  width:46px;height:46px;border-radius:13px;flex-shrink:0;
  background:linear-gradient(135deg,var(--indigo),var(--purple));
  display:flex;align-items:center;justify-content:center;font-size:21px;
  box-shadow:0 0 0 1px rgba(255,255,255,.09) inset,0 6px 24px var(--i-glow),0 0 50px rgba(99,102,241,.16);
  animation:logoBreathe 4.5s ease-in-out infinite;position:relative;
}
.ts-logo::after{
  content:'';position:absolute;inset:0;border-radius:13px;
  background:linear-gradient(140deg,rgba(255,255,255,.18),transparent 60%);pointer-events:none;
}
@keyframes logoBreathe{
  0%,100%{box-shadow:0 0 0 1px rgba(255,255,255,.09) inset,0 6px 24px var(--i-glow),0 0 50px rgba(99,102,241,.16)}
  50%    {box-shadow:0 0 0 1px rgba(255,255,255,.14) inset,0 8px 36px rgba(99,102,241,.55),0 0 70px rgba(168,85,247,.22)}
}

.ts-brand{flex:1;min-width:0}
.ts-wordmark{
  font-family:var(--fd)!important;font-size:1.45rem!important;font-weight:800!important;
  line-height:1.05;letter-spacing:-.01em;
  background:linear-gradient(115deg,#eef0ff 0%,var(--il) 48%,var(--purple) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:0!important;
}
.ts-tagline{font-size:.75rem!important;font-weight:400;color:var(--t3)!important;letter-spacing:.1em;text-transform:uppercase;margin-top:3px!important}

.ts-badges{display:flex;align-items:center;gap:7px;margin-left:auto;flex-shrink:0}
.ts-badge{display:inline-flex;align-items:center;gap:5px;border-radius:var(--r-sm);padding:5px 11px;font-size:.74rem;letter-spacing:.04em}
.ts-badge-model{background:var(--i-dim);border:1px solid rgba(99,102,241,.18);color:var(--il);font-family:var(--fm)}
.ts-badge-live{background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);color:var(--emerald);font-family:var(--fd);font-weight:600;letter-spacing:.08em;text-transform:uppercase}
.ts-live-dot{width:6px;height:6px;border-radius:50%;background:var(--emerald);box-shadow:0 0 7px var(--emerald);animation:liveDot 2s ease-in-out infinite}
@keyframes liveDot{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.3;transform:scale(.6)}}

/* ── SIDEBAR ──────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"]{
  background:linear-gradient(175deg,var(--sf0) 0%,var(--bg) 100%)!important;
  border-right:1px solid var(--gb)!important;
}
[data-testid="stSidebar"]>div:first-child{padding:16px 13px!important}
[data-testid="stSidebarContent"]{background:transparent!important}

.sb-top{display:flex;align-items:center;gap:9px;padding-bottom:13px;margin-bottom:16px;border-bottom:1px solid var(--gb)}
.sb-icon{width:28px;height:28px;border-radius:8px;flex-shrink:0;background:linear-gradient(135deg,var(--indigo),var(--purple));display:flex;align-items:center;justify-content:center;font-size:13px;box-shadow:0 3px 10px rgba(99,102,241,.32)}
.sb-title{font-family:var(--fd);font-size:1rem;font-weight:700;color:var(--t1)}
.sb-sub{font-size:.68rem;color:var(--t3);letter-spacing:.08em;text-transform:uppercase;margin-top:1px}

/* matches app.py usage */
.sb-label{font-family:var(--fd);font-size:.65rem;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:var(--t4);margin:15px 0 8px;display:flex;align-items:center;gap:6px}
.sb-label::after{content:'';flex:1;height:1px;background:var(--gb)}

/* ── STEP TRACKER ─────────────────────────────────────────────────────────── */
.steps{display:flex;flex-direction:column}
.step{display:flex;align-items:flex-start;gap:10px;padding:4px 7px 4px 2px;border-radius:var(--r-sm);transition:background .2s;position:relative}
.step.active{background:var(--i-dim)}

.step-ic{position:relative;flex-shrink:0;width:24px;display:flex;justify-content:center}
.step:not(:last-child) .step-ic::after{
  content:'';position:absolute;top:26px;left:50%;transform:translateX(-50%);
  width:1px;height:calc(100% + 6px);background:var(--gb);
}
.step.done:not(:last-child) .step-ic::after{background:linear-gradient(180deg,var(--emerald),var(--gb));opacity:.4}
.step.active:not(:last-child) .step-ic::after{background:linear-gradient(180deg,var(--indigo),transparent);opacity:.35}

.step-dot{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:1.5px solid var(--t4);background:var(--sf0);color:var(--t3);font-family:var(--fd);font-size:.68rem;font-weight:700;position:relative;z-index:1;transition:all .3s}
.step.done   .step-dot{background:rgba(16,185,129,.14);border-color:var(--emerald);color:var(--emerald)}
.step.active .step-dot{background:var(--i-dim);border-color:var(--indigo);color:var(--il);animation:stepPing 2.2s ease-in-out infinite}
@keyframes stepPing{0%,100%{box-shadow:0 0 0 3px rgba(99,102,241,.11)}50%{box-shadow:0 0 0 5px rgba(99,102,241,.07),0 0 14px rgba(99,102,241,.3)}}
.step-name{font-size:.82rem;color:var(--t2);padding-top:5px;line-height:1}
.step.active .step-name{color:var(--t1);font-weight:500}
.step.done   .step-name{color:var(--t3)}

/* ── PROFILE CARD ─────────────────────────────────────────────────────────── */
.pf-card{background:var(--glass);border:1px solid var(--gb);border-radius:var(--r-lg);overflow:hidden}
.pf-accent{height:2px;background:linear-gradient(90deg,var(--indigo),var(--purple),var(--emerald))}
.pf-body{padding:11px 12px}
.pf-row{margin-bottom:9px}
.pf-row:last-child{margin-bottom:0}
.pf-k{font-family:var(--fd);font-size:.65rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--t3);margin-bottom:3px}
.pf-v{font-size:.9rem;color:var(--t1);font-weight:500;word-break:break-word;line-height:1.4}
.tech-pills{display:flex;flex-wrap:wrap;gap:3px;margin-top:4px}
.tech-pill{background:var(--i-dim);border:1px solid rgba(99,102,241,.18);border-radius:var(--r-xs);padding:3px 8px;font-family:var(--fm);font-size:.72rem;color:var(--il);white-space:nowrap}
/* matches app.py */
.pf-empty{padding:10px 12px;font-size:.82rem;color:var(--t4);font-style:italic;line-height:1.5}

/* ── TONE CARD ────────────────────────────────────────────────────────────── */
.tone-card{background:var(--glass);border:1px solid var(--gb);border-radius:var(--r-lg);padding:11px 12px}
.tone-row{display:flex;align-items:center;gap:9px;margin-bottom:9px}
.tone-emoji{font-size:1.45rem;line-height:1;flex-shrink:0}
.tone-name{font-size:.92rem;font-weight:600;color:var(--t1)}
.tone-sub{font-size:.65rem;color:var(--t3);font-family:var(--fd);letter-spacing:.08em;text-transform:uppercase;margin-top:1px}
.tone-hist-lbl{font-size:.64rem;color:var(--t4);font-family:var(--fd);letter-spacing:.08em;text-transform:uppercase;margin-bottom:5px}
.tone-bars{display:flex;align-items:flex-end;gap:3px;height:26px}
.tone-bar{flex:1;min-height:3px;border-radius:2px 2px 0 0;background:var(--gb);transition:height .4s var(--spring)}
.tone-bar.vp{background:#10b981}
.tone-bar.p {background:var(--il)}
.tone-bar.n {background:var(--t3)}
.tone-bar.ng{background:var(--amber)}
.tone-bar.vn{background:#f43f5e}

/* ── Q PROGRESS ───────────────────────────────────────────────────────────── */
.qp-wrap{padding:2px 0}
.qp-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
.qp-lbl{font-size:.78rem;color:var(--t2);font-family:var(--fd)}
.qp-num{font-size:.84rem;font-weight:700;color:var(--il);font-family:var(--fd)}
.qp-track{height:4px;background:var(--gb);border-radius:99px;overflow:hidden;margin-bottom:6px}
.qp-fill{height:100%;border-radius:99px;background:linear-gradient(90deg,var(--indigo),var(--purple));box-shadow:0 0 8px rgba(99,102,241,.55);transition:width .55s var(--spring)}
.qp-dots{display:flex;gap:4px}
.qp-dot{flex:1;height:3px;border-radius:99px;background:var(--gb);transition:all .4s var(--spring)}
.qp-dot.d{background:var(--emerald)}
.qp-dot.a{background:var(--indigo);box-shadow:0 0 6px rgba(99,102,241,.6)}

/* ── HISTORY ──────────────────────────────────────────────────────────────── */
.hist{background:var(--glass);border:1px solid var(--gb);border-radius:var(--r-sm);padding:8px 10px;margin:4px 0;transition:border-color .2s}
.hist:hover{border-color:rgba(99,102,241,.22)}
.hist-name{font-size:.86rem;font-weight:600;color:var(--t1)}
.hist-meta{font-size:.73rem;color:var(--t3);margin-top:2px}

/* matches app.py "sb-footer" */
.sb-footer{margin-top:18px;padding-top:11px;border-top:1px solid var(--gb);font-size:.6rem;color:var(--t4);text-align:center;line-height:1.75;letter-spacing:.04em}

/* ── CHAT AREA — matches app.py "chat-container" ─────────────────────────── */
.chat-container{max-width:840px;margin:0 auto;padding:10px 24px 8px;min-height:40vh}

.welcome{text-align:center;padding:32px 20px 28px;animation:wUp .5s cubic-bezier(.22,1,.36,1) both}
@keyframes wUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:none}}
.w-icon{width:64px;height:64px;border-radius:18px;margin:0 auto 18px;background:linear-gradient(135deg,var(--indigo),var(--purple));display:flex;align-items:center;justify-content:center;font-size:28px;box-shadow:0 0 0 1px rgba(255,255,255,.07) inset,0 14px 44px var(--i-glow),0 0 70px rgba(99,102,241,.14);animation:logoBreathe 4.5s ease-in-out infinite;position:relative}
.w-icon::after{content:'';position:absolute;inset:0;border-radius:18px;background:linear-gradient(140deg,rgba(255,255,255,.16),transparent 55%)}
.w-h{font-family:var(--fd)!important;font-size:1.65rem!important;font-weight:800!important;background:linear-gradient(115deg,var(--t1) 0%,var(--il) 52%,var(--purple) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:9px!important}
.w-sub{font-size:.95rem!important;color:var(--t2)!important;line-height:1.68;max-width:380px;margin:0 auto!important}
.w-tags{display:flex;justify-content:center;flex-wrap:wrap;gap:6px;margin-top:20px}
.w-tag{background:var(--glass);border:1px solid var(--gb);border-radius:999px;padding:6px 15px;font-size:.78rem;color:var(--t2);letter-spacing:.03em;transition:all .2s}
.w-tag:hover{border-color:rgba(99,102,241,.3);color:var(--il)}

/* ── CHAT MESSAGES ────────────────────────────────────────────────────────── */
[data-testid="stChatMessage"]{background:transparent!important;border:none!important;padding:3px 0!important;animation:msgIn .25s cubic-bezier(.22,1,.36,1) both}
@keyframes msgIn{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}

[data-testid="stChatMessage"] .stMarkdown{padding:13px 17px!important}

/* Bot bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown{
  background:var(--sf1)!important;
  border:1px solid var(--gb)!important;
  border-top-left-radius:3px!important;border-top-right-radius:var(--r-lg)!important;
  border-bottom-right-radius:var(--r-lg)!important;border-bottom-left-radius:var(--r-lg)!important;
  max-width:86%!important;
  box-shadow:0 2px 22px rgba(0,0,0,.42),0 0 0 1px rgba(255,255,255,.025) inset!important;
  position:relative!important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  border-radius:0 var(--r-lg) 0 0;
  background:linear-gradient(90deg,rgba(99,102,241,.55) 0%,rgba(168,85,247,.25) 55%,transparent 100%);
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown{
  background:linear-gradient(135deg,rgba(99,102,241,.13),rgba(168,85,247,.08))!important;
  border:1px solid rgba(99,102,241,.2)!important;
  border-top-right-radius:3px!important;border-top-left-radius:var(--r-lg)!important;
  border-bottom-right-radius:var(--r-lg)!important;border-bottom-left-radius:var(--r-lg)!important;
  max-width:77%!important;margin-left:auto!important;
  box-shadow:0 2px 18px rgba(0,0,0,.28)!important;
}

[data-testid="chatAvatarIcon-assistant"],[data-testid="chatAvatarIcon-user"]{background:transparent!important;border:none!important}

/* ── TYPOGRAPHY ───────────────────────────────────────────────────────────── */
.stMarkdown p{font-size:1rem!important;line-height:1.75!important;color:var(--t1)!important;margin:0 0 10px!important}
.stMarkdown p:last-child{margin-bottom:0!important}
.stMarkdown strong{color:#a5b4fc!important;font-weight:600!important}
.stMarkdown em{color:#86efac!important}
.stMarkdown code{background:rgba(99,102,241,.1)!important;border:1px solid rgba(99,102,241,.2)!important;border-radius:4px!important;padding:2px 8px!important;font-size:.82em!important;color:#c4b5fd!important;font-family:var(--fm)!important;white-space:nowrap}
.stMarkdown hr{border:none!important;border-top:1px solid var(--gb)!important;margin:14px 0!important}

.stMarkdown table{width:100%!important;border-collapse:collapse!important;font-size:.9rem!important;margin:12px 0!important}
.stMarkdown th{background:rgba(99,102,241,.09)!important;color:#a5b4fc!important;padding:9px 14px!important;text-align:left!important;border:1px solid var(--gb)!important;font-family:var(--fd)!important;font-size:.7rem!important;letter-spacing:.1em!important;text-transform:uppercase!important}
.stMarkdown td{padding:9px 14px!important;border:1px solid var(--gb)!important;color:var(--t1)!important;font-size:.9rem!important}
.stMarkdown tr:nth-child(even) td{background:rgba(255,255,255,.014)!important}
.stMarkdown tr:hover td{background:var(--glass)!important}

/* ── INPUT BAR ────────────────────────────────────────────────────────────── */
.stChatInputContainer{background:rgba(8,9,18,.97)!important;border-top:1px solid var(--gb)!important;padding:11px 24px 15px!important;backdrop-filter:blur(22px)!important;position:sticky!important;bottom:0!important}
.stChatInputContainer>div{max-width:840px!important;margin:0 auto!important}

[data-testid="stChatInput"]{background:var(--sf1)!important;border:1px solid var(--gb)!important;border-radius:var(--r-lg)!important;transition:border-color .2s,box-shadow .2s!important}
[data-testid="stChatInput"]:focus-within{border-color:rgba(99,102,241,.42)!important;box-shadow:0 0 0 3px rgba(99,102,241,.09),0 4px 20px rgba(99,102,241,.08)!important}
[data-testid="stChatInput"] textarea{color:var(--t1)!important;font-family:var(--fb)!important;font-size:1rem!important;background:transparent!important;caret-color:var(--il)!important;line-height:1.5!important;padding:11px 4px 11px 14px!important}
[data-testid="stChatInput"] textarea::placeholder{color:var(--t3)!important;font-size:.95rem!important}
[data-testid="stChatInput"] button{background:linear-gradient(135deg,var(--indigo),var(--purple))!important;border-radius:var(--r-sm)!important;border:none!important;box-shadow:0 3px 12px rgba(99,102,241,.38)!important;transition:all .18s var(--smooth)!important;margin:6px 10px 6px 0!important}
[data-testid="stChatInput"] button:hover{transform:scale(1.07)!important;box-shadow:0 5px 18px rgba(99,102,241,.52)!important}
[data-testid="stChatInput"] button:active{transform:scale(.97)!important}

/* matches app.py "input-footer" */
.input-footer{display:flex;justify-content:space-between;align-items:center;max-width:840px;margin:6px auto 0;font-size:.7rem;color:var(--t4);font-family:var(--fd);letter-spacing:.04em}
.input-footer kbd{background:var(--glass);border:1px solid var(--gb);border-radius:3px;padding:1px 6px;font-family:var(--fm);font-size:.67rem;color:var(--t3)}

/* ── BUTTON ───────────────────────────────────────────────────────────────── */
div[data-testid="stButton"] button{background:linear-gradient(135deg,var(--indigo),var(--purple))!important;color:#fff!important;border:none!important;border-radius:var(--r-lg)!important;font-family:var(--fd)!important;font-size:.81rem!important;font-weight:700!important;letter-spacing:.07em!important;text-transform:uppercase!important;padding:12px 28px!important;box-shadow:0 5px 22px rgba(99,102,241,.36),0 0 0 1px rgba(255,255,255,.07) inset!important;transition:all .22s var(--smooth)!important;position:relative!important;overflow:hidden!important}
div[data-testid="stButton"] button::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,.12),transparent);opacity:0;transition:opacity .2s!important}
div[data-testid="stButton"] button:hover{transform:translateY(-2px)!important;box-shadow:0 9px 32px rgba(99,102,241,.5),0 0 0 1px rgba(255,255,255,.1) inset!important}
div[data-testid="stButton"] button:hover::before{opacity:1!important}
div[data-testid="stButton"] button:active{transform:none!important}

/* ── MISC ─────────────────────────────────────────────────────────────────── */
[data-testid="stExpander"]{background:var(--glass)!important;border:1px solid var(--gb)!important;border-radius:var(--r-md)!important}
details summary{color:var(--t2)!important;font-size:.84rem!important;font-family:var(--fb)!important;padding:9px 12px!important}
details summary:hover,details[open] summary{color:var(--t1)!important}
.stCaption{color:var(--t3)!important;font-size:.69rem!important}
hr{border-color:var(--gb)!important}
[data-testid="stNotification"]{border-radius:var(--r-md)!important;font-size:.8rem!important;font-family:var(--fb)!important}

/* ── RESUME UPLOAD ZONE ───────────────────────────────────────────────────── */
.resume-upload-zone{
  background:linear-gradient(135deg,rgba(99,102,241,.07),rgba(168,85,247,.04));
  border:2px dashed rgba(99,102,241,.3);
  border-radius:var(--r-xl);
  padding:28px 24px 16px;
  text-align:center;
  margin:10px 0 4px;
  transition:border-color .25s,background .25s;
  position:relative;overflow:hidden;
}
.resume-upload-zone::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse 60% 60% at 50% 0%,rgba(99,102,241,.08),transparent);
  pointer-events:none;
}
.resume-upload-zone:hover{
  border-color:rgba(99,102,241,.55);
  background:linear-gradient(135deg,rgba(99,102,241,.11),rgba(168,85,247,.07));
}
.ru-icon{font-size:2.4rem;margin-bottom:8px;filter:drop-shadow(0 0 12px rgba(99,102,241,.4))}
.ru-title{font-family:var(--fd);font-size:1rem;font-weight:700;color:var(--t1);margin-bottom:4px}
.ru-sub{font-size:.75rem;color:var(--t3);letter-spacing:.04em}

/* Streamlit file uploader restyled */
[data-testid="stFileUploader"]{
  background:var(--glass)!important;border:1px solid var(--gb)!important;
  border-radius:var(--r-lg)!important;padding:4px!important;margin-top:8px!important;
}
[data-testid="stFileUploader"] section{background:transparent!important;border:none!important;padding:8px!important}
[data-testid="stFileUploaderDropzone"]{
  background:var(--glass)!important;
  border:1.5px dashed rgba(99,102,241,.22)!important;
  border-radius:var(--r-md)!important;padding:14px!important;
  transition:border-color .2s,background .2s!important;
}
[data-testid="stFileUploaderDropzone"]:hover{
  border-color:rgba(99,102,241,.45)!important;background:var(--i-dim)!important;
}
[data-testid="stFileUploaderDropzone"] span{color:var(--t2)!important;font-size:.82rem!important}
[data-testid="stFileUploaderDropzone"] small{color:var(--t3)!important;font-size:.7rem!important}
[data-testid="stFileUploaderDropzone"] button{
  background:linear-gradient(135deg,var(--indigo),var(--purple))!important;
  color:#fff!important;border:none!important;border-radius:var(--r-sm)!important;
  font-family:var(--fd)!important;font-size:.75rem!important;font-weight:700!important;
  padding:7px 16px!important;
  box-shadow:0 3px 12px rgba(99,102,241,.35)!important;transition:all .18s!important;
}
[data-testid="stFileUploaderDropzone"] button:hover{
  transform:translateY(-1px)!important;box-shadow:0 5px 18px rgba(99,102,241,.5)!important;
}
[data-testid="stFileUploaderFile"]{
  background:rgba(99,102,241,.1)!important;
  border:1px solid rgba(99,102,241,.2)!important;
  border-radius:var(--r-sm)!important;padding:6px 10px!important;
}
[data-testid="stFileUploaderFileName"]{color:var(--il)!important;font-size:.8rem!important}

/* ── RÉSUMÉ SIDEBAR CARD ──────────────────────────────────────────────────── */
.res-card{background:var(--glass);border:1px solid var(--gb);border-radius:var(--r-lg);overflow:hidden}
.res-card::before{content:'';display:block;height:2px;background:linear-gradient(90deg,var(--purple),var(--indigo),var(--emerald))}
.res-body{padding:11px 12px}
.res-summary{font-size:.8rem;color:var(--t2);line-height:1.55;margin-bottom:10px}
.res-row{margin-bottom:8px}.res-row:last-child{margin-bottom:0}
.res-k{font-family:var(--fd);font-size:.6rem;font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:var(--t3);margin-bottom:3px}
.res-v{font-size:.8rem;color:var(--t1);font-weight:500;line-height:1.35}
.res-pills{display:flex;flex-wrap:wrap;gap:3px;margin-top:3px}
.res-pill{background:rgba(168,85,247,.12);border:1px solid rgba(168,85,247,.22);border-radius:var(--r-xs);padding:2px 7px;font-size:.65rem;color:#c4b5fd;white-space:nowrap;font-family:var(--fm)}
.res-qs-badge{display:inline-flex;align-items:center;gap:5px;background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.22);border-radius:var(--r-sm);padding:5px 10px;font-size:.72rem;color:var(--emerald);font-family:var(--fd);font-weight:600;margin-top:8px}

@media(max-width:768px){
  .ts-header-inner{padding:13px 14px}
  .ts-badges{display:none}
  .chat-container{padding:14px 12px 6px}
  .stChatInputContainer{padding:9px 12px 13px!important}
}
</style>
"""


# ─────────────────────────────────────────────────────────────────────────────
# HTML GENERATORS
# ─────────────────────────────────────────────────────────────────────────────

def get_header_html(stage: str) -> str:
    badge = _STAGE_BADGE.get(stage, "ACTIVE")
    return (
        '<div class="ts-header">'
          '<div class="ts-header-bg"></div>'
          '<div class="ts-header-inner">'
            '<div class="ts-logo">🤖</div>'
            '<div class="ts-brand">'
              '<div class="ts-wordmark">TalentScout</div>'
              '<div class="ts-tagline">AI · Hiring Assistant · v4</div>'
            '</div>'
            '<div class="ts-badges">'
              '<span class="ts-badge ts-badge-model">✦ gemini-2.0-flash-lite</span>'
              f'<span class="ts-badge ts-badge-live"><span class="ts-live-dot"></span>{badge}</span>'
            '</div>'
          '</div>'
        '</div>'
    )


def get_sidebar_html() -> str:
    return (
        '<div class="sb-top">'
          '<div class="sb-icon">🎯</div>'
          '<div>'
            '<div class="sb-title">TalentScout</div>'
            '<div class="sb-sub">Hiring Assistant</div>'
          '</div>'
        '</div>'
    )


def get_steps_html(current_stage: str) -> str:
    cur = next((i for i, (k, _, _) in enumerate(_STEPS) if k == current_stage), 0)
    rows = []
    for i, (_, icon, name) in enumerate(_STEPS):
        if i < cur:
            cls, dot = "done", "✓"
        elif i == cur:
            cls, dot = "active", icon
        else:
            cls, dot = "", str(i + 1)
        rows.append(
            f'<div class="step {cls}">'
              f'<div class="step-ic"><div class="step-dot">{dot}</div></div>'
              f'<div class="step-name">{name}</div>'
            f'</div>'
        )
    return '<div class="steps">' + "".join(rows) + '</div>'


def get_profile_html(candidate: dict) -> str:
    if not candidate:
        return '<div class="pf-empty">Your profile builds up as we chat →</div>'

    rows = []
    for icon, label, key in [
        ("👤", "Name",       "name"),
        ("📧", "Email",      "email"),
        ("📞", "Phone",      "phone"),
        ("🗓", "Experience", "experience"),
        ("💼", "Role",       "position"),
        ("📍", "Location",   "location"),
    ]:
        val = candidate.get(key, "")
        if val:
            rows.append(
                f'<div class="pf-row">'
                  f'<div class="pf-k">{icon} {label}</div>'
                  f'<div class="pf-v">{val}</div>'
                f'</div>'
            )

    tech = candidate.get("tech_stack", "")
    if tech:
        techs = [t.strip() for t in _re.split(r'[,/;]+', tech) if t.strip()]
        pills = "".join(f'<span class="tech-pill">{t}</span>' for t in techs[:12])
        rows.append(
            '<div class="pf-row">'
              '<div class="pf-k">🛠 Stack</div>'
              f'<div class="pf-v"><div class="tech-pills">{pills}</div></div>'
            '</div>'
        )

    if not rows:
        return '<div class="pf-empty">Your profile builds up as we chat →</div>'

    return (
        '<div class="pf-card">'
          '<div class="pf-accent"></div>'
          f'<div class="pf-body">{"".join(rows)}</div>'
        '</div>'
    )


def get_tone_html(label: str, emoji: str, display: str, history: list) -> str:
    recent = (history or [])[-10:]
    if recent:
        bars = "".join(
            '<div class="tone-bar {cls}" style="height:{h}"></div>'.format(
                cls=_BAR.get(lbl, ("n", "44%"))[0],
                h  =_BAR.get(lbl, ("n", "44%"))[1],
            )
            for _, lbl, _, _ in recent
        )
    else:
        bars = '<div class="tone-bar" style="width:100%;height:10px"></div>'

    return (
        '<div class="tone-card">'
          '<div class="tone-row">'
            f'<div class="tone-emoji">{emoji}</div>'
            '<div>'
              f'<div class="tone-name">{display}</div>'
              '<div class="tone-sub">Candidate Tone</div>'
            '</div>'
          '</div>'
          '<div class="tone-hist-lbl">Last 10 responses</div>'
          f'<div class="tone-bars">{bars}</div>'
        '</div>'
    )


def get_qprog_html(current: int, total: int) -> str:
    if total == 0:
        return ""
    pct  = int(current / total * 100)
    dots = "".join(
        f'<div class="qp-dot {"d" if i < current else "a" if i == current else ""}"></div>'
        for i in range(total)
    )
    return (
        '<div class="qp-wrap">'
          '<div class="qp-header">'
            '<span class="qp-lbl">Questions</span>'
            f'<span class="qp-num">{current} / {total}</span>'
          '</div>'
          f'<div class="qp-track"><div class="qp-fill" style="width:{pct}%"></div></div>'
          f'<div class="qp-dots">{dots}</div>'
        '</div>'
    )


def get_hist_item_html(r: dict) -> str:
    name = r.get("name", "—")
    role = r.get("position", "—")
    date = (r.get("timestamp_utc") or "")[:10]
    tech = (r.get("tech_stack") or "")[:40]
    return (
        '<div class="hist">'
          f'<div class="hist-name">{name}</div>'
          f'<div class="hist-meta">{role} · {date}</div>'
          f'<div class="hist-meta" style="color:var(--t4);font-size:.62rem">{tech}</div>'
        '</div>'
    )


def get_welcome_splash() -> str:
    tags = [
        "⚡ Gemini AI", "📄 Résumé Analysis",
        "🎯 Stack-matched Qs", "🧠 Experience-levelled",
        "📊 420+ question bank", "🔒 GDPR-compliant",
    ]
    tag_html = "".join(f'<span class="w-tag">{t}</span>' for t in tags)
    return (
        '<div class="welcome">'
          '<div class="w-icon">🤖</div>'
          '<div class="w-h">TalentScout AI</div>'
          '<div class="w-sub">'
            'Smart candidate screening — profile collected first, résumé optionally analysed, '
            'then technical questions matched to your exact stack and experience level.'
          '</div>'
          f'<div class="w-tags">{tag_html}</div>'
        '</div>'
    )


def get_resume_card_html(analysis: dict) -> str:
    """Sidebar card showing résumé insights — reads local parser result format."""
    if not analysis:
        return ""

    rows = []

    companies = analysis.get("companies") or []
    if companies:
        rows.append(
            '<div class="res-row">'
              '<div class="res-k">🏢 Companies</div>'
              f'<div class="res-v">{" · ".join(companies[:3])}</div>'
            '</div>'
        )

    education = (analysis.get("education") or "")[:70]
    if education:
        rows.append(
            '<div class="res-row">'
              '<div class="res-k">🎓 Education</div>'
              f'<div class="res-v">{education}</div>'
            '</div>'
        )

    experience = analysis.get("experience") or ""
    if experience:
        rows.append(
            '<div class="res-row">'
              '<div class="res-k">🗓 Experience</div>'
              f'<div class="res-v">{experience}</div>'
            '</div>'
        )

    skills = analysis.get("skills") or []
    if skills:
        pills = "".join(f'<span class="res-pill">{s}</span>' for s in skills[:8])
        rows.append(
            '<div class="res-row">'
              '<div class="res-k">⚡ Skills</div>'
              f'<div class="res-pills">{pills}</div>'
            '</div>'
        )

    projects = analysis.get("projects") or []
    if projects:
        proj_text = " · ".join(p[:30] for p in projects[:3])
        rows.append(
            '<div class="res-row">'
              '<div class="res-k">🛠 Projects</div>'
              f'<div class="res-v">{proj_text}</div>'
            '</div>'
        )

    q_count = len(analysis.get("questions") or [])
    badge = f'<div class="res-qs-badge">📝 {q_count} résumé questions queued</div>' if q_count else ""

    if not rows:
        return '<div class="pf-empty">Résumé parsed — questions ready.</div>'

    return (
        '<div class="res-card">'
          '<div class="res-body">'
            + "".join(rows) + badge +
          '</div>'
        '</div>'
    )