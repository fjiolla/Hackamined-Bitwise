# 🎬 EpisodeIQ — AI-Powered Short-Form Series Generator

<div align="center">

![EpisodeIQ](https://img.shields.io/badge/EpisodeIQ-Live-00ff88?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18.x-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Local_NLP-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

**Turn any story idea into a complete, analysed, and optimised short-form episodic series — in seconds.**

Team: Bitwise · Code: 1605 · Track: Quantloop · Leader: Krisha Shastri

</div>

---

## 📸 Preview

[▶ Watch Demo](https://github.com/user-attachments/assets/be0f4196-fd23-4553-adc4-d45aad70433e)

---

## ✨ Features

- 🧠 **AI Series Bible** — Extracts archetype, protagonist, supporting characters, and central conflict from any idea
- 🎬 **Structured Episode Generation** — Each episode follows a strict 5-beat format: Hook → Conflict → Escalation → Twist → Cliffhanger (mapped to 90 seconds)
- 📜 **Screenplay Hydration** — Generates format-compliant screenplays per episode with proper FADE IN / SMASH CUT TO BLACK endings
- 📊 **Emotional Arc Analyser** — Scores each beat −1.0 to +1.0 using RoBERTa sentiment, flags flat engagement zones where Δ < 0.15
- 🎯 **Cliffhanger Strength Scorer** — Cosine similarity against 5 narrative archetypes, scored 0–10
- 📉 **Retention Risk Predictor** — Semantic engagement delta cross-referenced with emotional intensity, mapped to LOW / MEDIUM / HIGH per time block
- 🔍 **Narrative Stress Tester** — Runs 5 structural checks: hook strength, emotional flatness, cliffhanger impact, retention risk, narrative flow
- ⚡ **One-Click Episode Repair** — Detects weaknesses, compiles suggestions, and regenerates only the broken episode with full continuity context
- 📚 **Continuity Ledger** — Tracks characters (via spaCy NER), revealed secrets, unresolved threads, and timeline events across all episodes
- 🏆 **Series Arc Score** — Grades the full series 0–100 across cliffhanger strength, emotional variance, and retention health

---

## 🚀 Tech Stack

### Backend
- **FastAPI** — Async API framework
- **LLaMA 3.3-70B via Groq API** — Series bible generation, episode beat generation, screenplay writing
- **`cardiffnlp/twitter-roberta-base-sentiment`** — Emotional arc analysis per beat
- **`sentence-transformers/all-MiniLM-L6-v2`** — Cliffhanger scoring, engagement scoring, narrative flow analysis
- **spaCy (`en_core_web_sm`)** — Named entity recognition for character extraction in the continuity ledger
- **Pydantic v2** — Data validation and model definitions
- **Python asyncio** — Fully async pipeline execution

### Frontend
- **React 18** — Component-based UI
- **Recharts** — Emotional arc line chart and retention risk bar chart
- **CSS Variables** — Dark theme design system

---

## 📂 Project Structure

```
.
├── backend
│   └── app
│       ├── analysis
│       │   ├── cliffhanger_score.py     # CliffhangerScorer — semantic archetype similarity
│       │   ├── emotional_arc.py         # EmotionalArcAnalyzer — RoBERTa sentiment per beat
│       │   ├── retention_predictor.py   # RetentionRiskPredictor — LOW/MEDIUM/HIGH per beat
│       │   └── semantic_scorer.py       # Core MiniLM embedding functions
│       ├── api
│       │   ├── analyse.py               # /emotional-arc, /cliffhanger, /retention, /full
│       │   └── generate.py              # /generate-series, /regenerate-episode, /suggest-episodes
│       ├── engines
│       │   ├── bible_engine.py          # SeriesBibleGenerator — StoryIdea → SeriesBible
│       │   ├── continuity_ledger.py     # ContinuityLedger — cross-episode story state tracking
│       │   ├── episode_generator.py     # EpisodeGenerator — SeriesBible → EpisodeStructure
│       │   ├── pipeline_engine.py       # PipelineEngine — full end-to-end orchestration
│       │   └── script_generator.py      # ScriptGenerator — EpisodeStructure → Screenplay
│       ├── models
│       │   └── story_models.py          # Pydantic models: StoryIdea, SeriesBible, EpisodeStructure
│       ├── optimisation
│       │   ├── stress_test.py           # NarrativeStressTest — 5 structural checks
│       │   └── suggestion_engine.py     # SuggestionEngine — issue → human-readable fix
│       ├── utils
│       │   ├── gemini_client.py         # Async Gemini API wrapper (episode & script generation)
│       │   └── groq_client.py           # Async Groq API wrapper (series bible generation)
│       ├── config.py                    # App settings and environment config
│       └── main.py                      # FastAPI app entry point
│
├── EPISODEIQ_DOCUMENTATION.md
│
└── frontend
    ├── src
    │   ├── components
    │   │   ├── ContinuityLedgerModal.jsx  # Floating ledger modal
    │   │   ├── EmotionalChart.jsx         # Recharts line chart for emotional arc
    │   │   ├── EpisodeViewer.jsx          # Screenplay / Analysis / Suggestions tabs
    │   │   ├── RetentionChart.jsx         # Recharts bar chart for retention risk
    │   │   ├── StoryInput.jsx             # Landing page form + loading state
    │   │   └── SuggestionsPanel.jsx       # Issue cards + regenerate button
    │   ├── api.js                         # API calls to backend
    │   ├── App.jsx                        # Dashboard layout, sidebar, episode navigation
    │   ├── App.css                        # Layout, tab navigation, animations
    │   ├── index.css                      # Design tokens, global dark theme
    │   └── main.jsx                       # React entry point
    ├── index.html
    ├── vite.config.js
    └── package.json
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- A [Groq API key](https://console.groq.com)

### Backend

```bash
# Clone the repository
git clone https://github.com/fjiolla/Hackamined-Bitwise.git
cd Hackamined-Bitwise/backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Set your Groq API key in .env or config
GROQ_API_KEY=your_key_here

# Start the server
uvicorn app.main:app --reload
```

### Frontend

```bash
cd Hackamined-Bitwise/frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend runs on `http://localhost:5173` and expects the backend at `http://localhost:8000`.

---

## 🔁 How the Pipeline Works

```
Creator Input (Title · Genre · Description · Episode Count)
        │
        ▼
Series Bible Generator  ──  LLaMA 3.3-70B / Groq
(Archetype · Protagonist · Supporting Cast · Central Conflict)
        │
        ▼
Episode Generator  ──  Sequential loop with continuity context
(5–8 episodes × 5 beats: Hook → Conflict → Escalation → Twist → Cliffhanger)
        │
        ├─── For each episode:
        │         │
        │         ├── Emotional Arc Analyser    (RoBERTa — local)
        │         ├── Cliffhanger Scorer        (MiniLM — local)
        │         ├── Retention Risk Predictor  (MiniLM + RoBERTa — local)
        │         ├── Narrative Stress Test     (heuristic rules)
        │         └── Suggestion Engine         (rule-mapped output)
        │
        ▼
Script Hydration Engine  ──  LLaMA 3.3-70B / Groq
(90-second screenplays · last 20 lines of prior script injected as context)
        │
        ▼
Final Output: Series Bible · Beat Maps · Emotional Arc · Cliffhanger Scorecard
             Retention Timeline · Exportable Screenplay · Series Arc Score /100
```

---

## 📡 API Endpoints

### Generation
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/generate/generate-series` | Full end-to-end pipeline |
| `POST` | `/api/generate/regenerate-episode` | Regenerate one episode with continuity |
| `POST` | `/api/generate/suggest-episodes` | Suggest optimal episode count |

### Analysis
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/analyse/emotional-arc` | Emotional arc per beat |
| `POST` | `/api/analyse/cliffhanger` | Cliffhanger strength score |
| `POST` | `/api/analyse/retention` | Retention risk per beat |
| `POST` | `/api/analyse/full` | Full analysis + suggestions |

---

## 📊 Scoring Explained

### Series Arc Score (0–100)
| Component | Weight | Metric |
|-----------|--------|--------|
| Cliffhanger Strength | 40 pts | Avg cosine similarity vs 5 archetypes |
| Emotional Variance | 35 pts | Max − Min emotion score across all beats |
| Retention Health | 25 pts | Proportion of beats without HIGH risk |

### Cliffhanger Score (0–10)
Each of 5 archetypes contributes up to 2 points (≥ 0.4 similarity → 2pts, ≥ 0.25 → 1pt, else 0):
- Unresolved Tension · Revelation Hook · Stakes Escalation · Character Jeopardy · Time Pressure

### Retention Risk (per beat)
Semantic engagement delta (engaging vs boring archetypes) combined with emotional intensity → **LOW / MEDIUM / HIGH**

---

## 🔗 Connect With Team Bitwise

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Team_Bitwise-181717?style=for-the-badge&logo=github)](https://github.com/fjiolla/Hackamined-Bitwise)
[![Track](https://img.shields.io/badge/Track-Quantloop-00ff88?style=for-the-badge)]()
[![Code](https://img.shields.io/badge/Team_Code-1605-F55036?style=for-the-badge)]()

</div>

---

## 📝 License

This project was built for hackathon purposes and is open source under the [MIT License](LICENSE).

---

<div align="center">

**⭐ If EpisodeIQ impressed you, give it a star!**

Built with ❤️ by Team Bitwise

</div>
