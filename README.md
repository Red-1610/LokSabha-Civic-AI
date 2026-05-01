# 🗳️ DemocracyOS — Civic Intelligence Platform

**DemocracyOS** is an AI-powered civic education app built with Streamlit that helps every Indian citizen understand the election process, check their voter eligibility, explore historical data, and ask election questions in plain language.

---

## 🚀 Features

| Module | Description |
|---|---|
| 🏠 Live Election Feed | Real-time news timeline: winners, reactions, and incidents |
| 🗺️ Election Journey | Interactive 6-phase walkthrough of India's election lifecycle |
| 🤖 AI Analyst | Gemini-powered Q&A with constitutional citations |
| ✅ Voter Eligibility | Logic-driven checker with official ID document list |
| 🎓 Democracy Quiz | 6-question civic knowledge test with explanations |

### Google Services Integration
- **Google Translate Widget** — Translate the entire app into 10 Indian languages (Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi)
- **Google Fonts** — Sora + JetBrains Mono for premium typography

### AI Integration
- **Google Gemini** (`gemini-1.5-flash`) — Real conversational AI for election Q&A
- Conversation history maintained across turns
- Sanitised inputs; constitutional citations in responses

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Custom CSS, glassmorphism dark theme)
- **AI**: Google Gemini API (`gemini-2.5-flash`)
- **Translation**: Google Translate Widget
- **News**: NewsAPI (Live timeline of winners, reactions, and incidents)

---

## 📦 Installation

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd election_ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API keys (optional but recommended)
export ANTHROPIC_API_KEY="your_key_here"
export NEWS_API_KEY="your_key_here"

# 4. Run
streamlit run app.py
```

### Streamlit Cloud Deployment
Add secrets in the Streamlit Cloud dashboard:
```toml
# .streamlit/secrets.toml
GOOGLE_API_KEY = "AIza..."
NEWS_API_KEY = "your_newsapi_key"
```

---

## 🔒 Security

- All user inputs are sanitised via regex (strips special characters, limits length)
- API keys read exclusively from environment variables / Streamlit secrets — never hardcoded
- No PII collected or stored
- External requests use `timeout` parameters and `try/except` error handling
- Logging via Python `logging` module (not `print`)

---

## ♿ Accessibility

- ARIA roles and `aria-label` attributes on all interactive regions
- Skip-to-content link (`<a class="skip-link">`)
- `aria-live` regions for dynamic eligibility results
- Colour contrast ≥ 4.5:1 for all text
- All images have `aria-hidden="true"` (decorative icons)
- Keyboard-navigable sidebar and forms

---

## 🧪 Testing

Run manual smoke tests:
```bash
# Syntax check
python -m py_compile app.py && echo "✅ Syntax OK"

# Import check
python -c "import streamlit, requests; print('✅ All imports OK')"
```

---

## 📁 Repository Size

| File | Size |
|---|---|
| `app.py` | ~45 KB |
| `requirements.txt` | < 1 KB |
| `README.md` | ~4 KB |
| **Total (excl. `.git`)** | **~50 KB** |

Well within the 8–9 MB GitHub constraint.

---

## 📜 Legal & Data

- Historical election data is synthetic and for educational purposes only.
- Official data: [eci.gov.in](https://eci.gov.in) · [voters.eci.gov.in](https://voters.eci.gov.in)
- Voter Helpline: **1950** (toll-free)

---

*Built for the Promptwars competition. Optimised for Code Quality, Security, Accessibility, Efficiency, and Google Services criteria.*
