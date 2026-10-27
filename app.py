"""
DemocracyOS — Civic Intelligence Platform
AI-powered election guide with Google services, accessibility, and rich analytics.
"""

import os
import re
import time
import json
import hashlib
import logging
import requests
import streamlit as st
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("DemocracyOS")

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DemocracyOS | Civic Intelligence",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://eci.gov.in",
        "Report a bug": None,
        "About": "DemocracyOS — AI-powered civic education for India's elections.",
    },
)

# ── CSS / Design System ───────────────────────────────────────────────────────
STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg-deep:       #050d1a;
    --bg-card:       rgba(10, 25, 47, 0.85);
    --bg-glass:      rgba(255,255,255,0.04);
    --accent:        #f97316;
    --accent-soft:   rgba(249,115,22,0.15);
    --accent2:       #0ea5e9;
    --accent2-soft:  rgba(14,165,233,0.15);
    --green:         #22c55e;
    --green-soft:    rgba(34,197,94,0.15);
    --red:           #ef4444;
    --gold:          #fbbf24;
    --text-primary:  #f0f4ff;
    --text-muted:    #8899aa;
    --border:        rgba(255,255,255,0.07);
    --border-accent: rgba(249,115,22,0.4);
    --radius:        16px;
    --radius-sm:     10px;
    --shadow:        0 8px 32px rgba(0,0,0,0.4);
    --font:          'Sora', sans-serif;
    --mono:          'JetBrains Mono', monospace;
}

/* ── Base ── */
html, body, [class*="css"] { font-family: var(--font) !important; }

.stApp {
    background: var(--bg-deep) !important;
    color: var(--text-primary) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 4px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060e1e 0%, #0a1629 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg,
        rgba(249,115,22,0.12) 0%,
        rgba(14,165,233,0.08) 50%,
        rgba(249,115,22,0.05) 100%);
    border: 1px solid var(--border-accent);
    border-radius: 24px;
    padding: 48px 40px 40px;
    text-align: center;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(circle at 70% 30%, rgba(249,115,22,0.07), transparent 60%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: var(--accent-soft);
    border: 1px solid var(--border-accent);
    color: var(--accent);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 99px;
    margin-bottom: 18px;
}
.hero-title {
    font-size: clamp(2rem, 5vw, 3.6rem);
    font-weight: 800;
    background: linear-gradient(135deg, #f97316 0%, #fb923c 40%, #0ea5e9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.15;
    margin-bottom: 12px;
}
.hero-sub {
    font-size: 1.1rem;
    color: var(--text-muted);
    max-width: 560px;
    margin: 0 auto;
}

/* ── Cards ── */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.card:hover {
    border-color: var(--border-accent);
    box-shadow: 0 0 0 1px rgba(249,115,22,0.15), var(--shadow);
}
.card-icon { font-size: 1.6rem; margin-bottom: 10px; }
.card-title { font-size: 1rem; font-weight: 700; margin-bottom: 6px; }
.card-body { font-size: 0.88rem; color: var(--text-muted); line-height: 1.6; }

/* ── Stat boxes ── */
.stat-box {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 20px 16px;
    text-align: center;
}
.stat-value {
    font-size: 2rem;
    font-weight: 800;
    color: var(--accent);
    font-family: var(--mono);
}
.stat-label { font-size: 0.78rem; color: var(--text-muted); margin-top: 4px; }

/* ── Timeline ── */
.phase-wrap {
    background: linear-gradient(135deg, rgba(249,115,22,0.1), rgba(14,165,233,0.06));
    border: 1px solid var(--border-accent);
    border-radius: var(--radius);
    padding: 32px 36px;
    margin-top: 20px;
}
.phase-num {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 6px;
    font-family: var(--mono);
}
.phase-name { font-size: 1.8rem; font-weight: 700; margin-bottom: 10px; }
.phase-desc { font-size: 1.05rem; color: var(--text-primary); margin-bottom: 14px; }
.phase-detail { font-size: 0.9rem; color: var(--text-muted); line-height: 1.7; }

/* ── Quiz ── */
.quiz-q {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 20px 24px;
    margin-bottom: 18px;
}
.quiz-q-num { font-family: var(--mono); color: var(--accent); font-size: 0.8rem; }
.quiz-q-text { font-size: 1rem; font-weight: 600; margin: 6px 0 0; }

/* ── Eligibility ── */
.check-result {
    border-radius: var(--radius);
    padding: 28px;
    text-align: center;
    font-weight: 700;
    font-size: 1.15rem;
    margin-top: 20px;
}
.check-pass { background: var(--green-soft); border: 1px solid rgba(34,197,94,0.4); color: var(--green); }
.check-fail { background: rgba(239,68,68,0.12); border: 1px solid rgba(239,68,68,0.4); color: var(--red); }

/* ── Chat ── */
.chat-bubble-user {
    background: var(--accent-soft);
    border: 1px solid var(--border-accent);
    border-radius: 14px 14px 4px 14px;
    padding: 12px 18px;
    margin: 8px 0 8px 60px;
    font-size: 0.94rem;
    line-height: 1.6;
}
.chat-bubble-ai {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 4px 14px 14px 14px;
    padding: 12px 18px;
    margin: 8px 60px 8px 0;
    font-size: 0.94rem;
    line-height: 1.6;
}

/* ── Status chips ── */
.chip {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.chip-green { background: var(--green-soft); color: var(--green); border: 1px solid rgba(34,197,94,0.3); }
.chip-orange { background: var(--accent-soft); color: var(--accent); border: 1px solid var(--border-accent); }
.chip-blue { background: var(--accent2-soft); color: var(--accent2); border: 1px solid rgba(14,165,233,0.3); }

/* ── Accessibility skip link ── */
.skip-link {
    position: absolute;
    top: -100px;
    left: 16px;
    background: var(--accent);
    color: white;
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: 700;
    z-index: 9999;
    text-decoration: none;
}
.skip-link:focus { top: 16px; }

/* ── Dividers ── */
hr { border-color: var(--border) !important; }

/* ── Plotly chart backgrounds ── */
.js-plotly-plot { border-radius: var(--radius-sm); }

/* ── Streamlit overrides ── */
.stSelectbox > div, .stMultiSelect > div,
.stTextInput > div, .stNumberInput > div,
.stTextArea > div {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #f97316, #ea580c) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* ── ARIA / screen-reader utilities ── */
.sr-only {
    position: absolute; width: 1px; height: 1px;
    padding: 0; margin: -1px; overflow: hidden;
    clip: rect(0,0,0,0); white-space: nowrap; border: 0;
}

/* ── Google Translate widget alignment ── */
#google_translate_element { margin-top: 6px; }

/* ── News card ── */
.news-card {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 12px 14px;
    margin-bottom: 10px;
    font-size: 0.82rem;
}
.news-date { color: var(--accent); font-family: var(--mono); font-size: 0.72rem; }
.news-title { color: var(--text-primary); font-weight: 600; margin-top: 4px; }
.news-src { color: var(--text-muted); font-size: 0.7rem; margin-top: 3px; }
</style>

<!-- ── Skip navigation for accessibility ── -->
<a class="skip-link" href="#main-content" aria-label="Skip to main content">Skip to content</a>

<!-- ── Google Translate Widget ── -->
<div id="google_translate_element" aria-label="Language Selector"></div>
<script type="text/javascript">
function googleTranslateElementInit() {
    new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'en,hi,bn,ta,te,mr,gu,kn,ml,pa',
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
        autoDisplay: false
    }, 'google_translate_element');
}
</script>
<script type="text/javascript"
    src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit">
</script>
"""

st.markdown(STYLE, unsafe_allow_html=True)


# ── Security: Input sanitisation ─────────────────────────────────────────────
_ALLOWED = re.compile(r"[^a-zA-Z0-9\s\-_.,?!'()+\u0900-\u097F\u0A00-\u0A7F\u0B00-\u0B7F]")

def sanitise(text: str, max_len: int = 500) -> str:
    """Strip potentially dangerous characters and trim length."""
    if not isinstance(text, str):
        return ""
    cleaned = _ALLOWED.sub("", text).strip()
    return cleaned[:max_len]


def redact_key(value: str) -> str:
    """Return a safe display version of a secret (last 4 chars)."""
    return "•" * (len(value) - 4) + value[-4:] if len(value) > 4 else "•" * len(value)


# ── External APIs ─────────────────────────────────────────────────────────────
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


@st.cache_data(ttl=600, show_spinner=False)
def fetch_news(query: str = "India election") -> list[dict]:
    """Fetch headlines from NewsAPI (rate-limited, cached 10 min)."""
    if not NEWS_API_KEY:
        return []
    safe_q = sanitise(query, 80)
    url = (
        f"https://newsapi.org/v2/everything"
        f"?q={safe_q}&apiKey={NEWS_API_KEY}&pageSize=6&sortBy=publishedAt&language=en"
    )
    try:
        resp = requests.get(url, timeout=8)
        resp.raise_for_status()
        return resp.json().get("articles", [])
    except requests.RequestException as exc:
        logger.warning("NewsAPI request failed: %s", exc)
        return []


def call_ai(messages: list[dict], system: str = "") -> str:
    """
    Call Google Gemini with conversation history.
    Returns response text or an error string.
    """
    if not GOOGLE_API_KEY:
        return (
            "⚠️ No Google API key found. Set the `GOOGLE_API_KEY` environment variable "
            "to enable the AI assistant."
        )
    try:
        model = genai.GenerativeModel("gemini-3.8-flash", system_instruction=system)
        formatted_messages = []
        for m in messages:
            formatted_messages.append({"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]})
        
        chat = model.start_chat(history=formatted_messages[:-1])
        response = chat.send_message(formatted_messages[-1]["parts"][0])
        return response.text.strip() if response.text else "❌ AI service returned an empty response."
    except Exception as exc:
        logger.error("Gemini API error: %s", exc)
        return "❌ AI service temporarily unavailable. Please try again shortly."


# ── Static Content ────────────────────────────────────────────────────────────
ELECTION_PHASES = [
    {
        "name": "Announcement & MCC",
        "emoji": "📢",
        "desc": "The Election Commission issues the official poll schedule and triggers the Model Code of Conduct.",
        "details": (
            "Once announced, all government expenditure is frozen and no new welfare schemes may be launched. "
            "Political parties must follow strict neutrality rules regarding the use of public resources. "
            "The MCC is binding on all political parties, candidates, and government machinery from this date."
        ),
        "duration": "~3 weeks before polling",
        "key_body": "Election Commission of India",
        "legal_ref": "Article 324, Constitution of India",
    },
    {
        "name": "Voter Registration",
        "emoji": "📝",
        "desc": "Electoral rolls are updated and new voters register using Form 6.",
        "details": (
            "Eligible citizens can enrol via the Voter Helpline App, the NVSP portal, or Booth Level Officers. "
            "EPIC (Elector's Photo Identity Card) cards are issued. "
            "The final electoral roll is published at least 30 days before the date of poll."
        ),
        "duration": "Continuous; finalised 30 days before poll",
        "key_body": "State Chief Electoral Officers",
        "legal_ref": "Representation of the People Act, 1950 – Section 22",
    },
    {
        "name": "Nominations",
        "emoji": "📋",
        "desc": "Candidates file nomination papers with affidavits disclosing assets and criminal records.",
        "details": (
            "Candidates must be Indian citizens, at least 25 years old for the Lok Sabha, "
            "and enrolled as a voter. Detailed affidavits (Form 26) disclosing assets, liabilities, "
            "educational qualifications, and pending criminal cases are mandatory and publicly available."
        ),
        "duration": "~2 weeks before polling",
        "key_body": "Returning Officer",
        "legal_ref": "RPA 1951 – Sections 33–36",
    },
    {
        "name": "Campaigning",
        "emoji": "🎙️",
        "desc": "Political parties hold rallies and present manifestos to voters.",
        "details": (
            "A strict 48-hour 'campaign silence' period begins before the first vote is cast. "
            "Campaign expenditure limits are enforced by Election Observers. Exit polls are prohibited "
            "until the last phase of polling concludes. Social media content is also subject to MCC."
        ),
        "duration": "2–4 weeks",
        "key_body": "Election Commission Observers",
        "legal_ref": "RPA 1951 – Section 126 (silence period)",
    },
    {
        "name": "Polling Day",
        "emoji": "🗳️",
        "desc": "Voters cast ballots at designated booths using Electronic Voting Machines.",
        "details": (
            "EVMs with VVPAT (Voter Verifiable Paper Audit Trail) units are used. "
            "Each voter can verify their paper slip before it drops into the sealed box. "
            "Central Armed Police Forces are deployed. Voter ID or one of 12 alternate documents is required."
        ),
        "duration": "7 AM – 6 PM",
        "key_body": "Presiding Officers & Micro-Observers",
        "legal_ref": "The Conduct of Elections Rules, 1961",
    },
    {
        "name": "Counting & Results",
        "emoji": "🏆",
        "desc": "Votes are counted under tight security; results declared constituency-wise.",
        "details": (
            "Counting begins with postal ballots, followed by EVM rounds. "
            "VVPAT slips are randomly verified for at least 5 booths per constituency. "
            "The candidate with the most votes (FPTP system) wins. Coalition talks follow for government formation."
        ),
        "duration": "Usually 1 day (counting day)",
        "key_body": "Returning Officer & EC Counting Teams",
        "legal_ref": "RPA 1951 – Section 66",
    },
]

QUIZ_QUESTIONS = [
    {
        "q": "What is the minimum voting age in India?",
        "options": ["16 years", "18 years", "21 years", "25 years"],
        "answer": "18 years",
        "explanation": "The 61st Constitutional Amendment (1989) lowered the voting age from 21 to 18.",
    },
    {
        "q": "What does VVPAT stand for?",
        "options": [
            "Voter Verified Paper Audit Trail",
            "Voter Visual Paper Account Tool",
            "Video Verified Paper Audit Tech",
            "Validated Voter Printed Audit Track",
        ],
        "answer": "Voter Verified Paper Audit Trail",
        "explanation": "VVPAT was introduced to provide a paper trail so voters can verify their vote was cast correctly.",
    },
    {
        "q": "Which body is constitutionally empowered to conduct elections in India?",
        "options": [
            "Parliament of India",
            "Supreme Court",
            "Election Commission of India",
            "Ministry of Home Affairs",
        ],
        "answer": "Election Commission of India",
        "explanation": "Article 324 vests election supervision, direction, and control in the Election Commission of India.",
    },
    {
        "q": "What is the Model Code of Conduct (MCC)?",
        "options": [
            "A law passed by Parliament",
            "A set of guidelines issued by the ECI for elections",
            "A Supreme Court directive",
            "A treaty between political parties",
        ],
        "answer": "A set of guidelines issued by the ECI for elections",
        "explanation": "The MCC is not a statute; it is a set of guidelines voluntarily accepted by political parties and enforced by the ECI.",
    },
    {
        "q": "How many hours before voting must election campaigning stop?",
        "options": ["24 hours", "36 hours", "48 hours", "72 hours"],
        "answer": "48 hours",
        "explanation": "Section 126 of the Representation of the People Act, 1951, mandates a 48-hour silence period before polling.",
    },
    {
        "q": "What electoral system is used for Lok Sabha elections?",
        "options": [
            "Proportional Representation",
            "First-Past-The-Post (FPTP)",
            "Single Transferable Vote",
            "Two-Round System",
        ],
        "answer": "First-Past-The-Post (FPTP)",
        "explanation": "India uses the FPTP system where the candidate with the most votes in a constituency wins, regardless of majority.",
    },
]

AI_SYSTEM_PROMPT = """You are DemocracyOS, an expert civic education assistant specialising in Indian elections. 
Your role is to help citizens understand the election process, voter rights, constitutional provisions, and democratic participation.

Guidelines:
- Always be accurate, factual, and cite relevant Articles or Acts when possible.
- Use clear, accessible language suitable for all literacy levels.
- Encourage civic participation and voting.
- If asked about specific current election results or very recent events, acknowledge your knowledge may be limited.
- Never provide partisan political opinions or endorse any candidate or party.
- For eligibility questions, refer users to official sources: voters.eci.gov.in or the Voter Helpline (1950).
- Keep respo
