# ⚡ AI-Powered Content Creation and Analysis System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![Architecture](https://img.shields.io/badge/Architecture-Modular-green.svg)](#system-architecture)
[![Prompt Engineering](https://img.shields.io/badge/Prompt%20Engineering-5%20Pillars-purple.svg)](#prompt-engineering-framework)

An end-to-end AI application engineered for **Prompt Engineering, Content Generation, Podcast Production Planning, Dual-Layer NLP Text Analysis, and Hyperparameter Sensitivity Experimentation**.

Built with a modular Python backend and a glassmorphic **Streamlit Web UI** paired with an interactive **CLI Terminal Runner**. Supports **OpenAI**, **Anthropic Claude**, and an **Intelligent Offline Simulation Engine** (enabling 100% full application testability with zero API keys required).

---

## 📑 Table of Contents

- [Assignment Requirements Mapping](#assignment-requirements-mapping)
- [Prompt Engineering Framework](#prompt-engineering-framework)
- [Core Features](#core-features)
- [System Architecture](#system-architecture)
- [Quick Start & Installation](#quick-start--installation)
- [Web Application Usage](#web-application-usage)
- [CLI Terminal Usage](#cli-terminal-usage)
- [Parameter Experimentation Insights](#parameter-experimentation-insights)

---

## 🎯 Assignment Requirements Mapping

| Assignment Requirement | Technical Implementation | Module / File |
|---|---|---|
| **1. Prompt Design** | Structured 5-Pillar Template (`ROLE`, `CONTEXT`, `TASK`, `CONSTRAINTS`, `OUTPUT FORMAT`) | [`prompts.py`](file:///Users/vismayjain/Downloads/AI_Content_Creation_Analysis/prompts.py) |
| **2. Content Generation** | Story, Poem, and Social Media Post with dynamic tone, audience, and word count controls | [`content_generation.py`](file:///Users/vismayjain/Downloads/AI_Content_Creation_Analysis/content_generation.py) |
| **3. Podcast Planning** | Episode Title, 2-3 paragraph synopsis, guest dossier, and 8 structured interview questions in 4 stages | [`podcast_planning.py`](file:///Users/vismayjain/Downloads/AI_Content_Creation_Analysis/podcast_planning.py) |
| **4. Text Analysis** | Dual-layer NLP: Sentiment classification + polarity score + explanation & ranked keyword extraction | [`text_analysis.py`](file:///Users/vismayjain/Downloads/AI_Content_Creation_Analysis/text_analysis.py) |
| **5. Parameter Experimentation** | Dual-sampling temperature comparison (0.2 vs 0.9) with lexical diversity (TTR) metrics & analysis | [`parameter_experiment.py`](file:///Users/vismayjain/Downloads/AI_Content_Creation_Analysis/parameter_experiment.py) |

---

## 🏛️ Prompt Engineering Framework

Every prompt in this system follows the **5 Pillars of Prompt Engineering**:

1. **ROLE**: Establishes persona, vocabulary boundaries, and domain authority (e.g., *"Veteran Podcast Executive Producer"* or *"Senior Computational Linguist"*).
2. **CONTEXT**: Supplies the scenario, domain constraints, and listener/reader background.
3. **TASK**: Active-verb, concrete objective without ambiguity.
4. **CONSTRAINTS**: Negative boundaries, length controls, formatting rules, and guardrails against superficial outputs.
5. **OUTPUT FORMAT**: Syntactic contract (Strict JSON Schema or formatted Markdown) ensuring reliable automated parsing.

---

## 🚀 Core Features

### 1. ✍️ Content Generation
- Supports **Short Stories**, **Lyrical Poems**, and **Viral Social Media Posts**.
- Customizable **Tone** (Inspiring, Dramatic, Analytical, Witty), **Target Audience**, and **Word Count**.
- Real-time output metrics: Word count, character count, and estimated reading time.
- Direct export to **Markdown** or structured text.

### 2. 🎙️ Podcast Planning
- Complete production planning package:
  - High-impact **Episode Title** and **Tagline**.
  - Comprehensive 2-3 paragraph **Show Notes / Synopsis**.
  - **Ideal Guest Profile**: Target role, pedigree, and domain rationale.
  - **8 Sequenced Interview Questions**:
    - *Q1-Q2 (Icebreaker & Backstory)*: Origin and personal conviction.
    - *Q3-Q5 (Core Deep-Dive)*: Technical challenges and architectural trade-offs.
    - *Q6-Q7 (Future Vision & Debates)*: Contrarian predictions and industry debates.
    - *Q8 (Rapid-Fire Takeaway)*: Actionable parting insight.
- One-click export to **Podcast Production Cue Sheet (`.md`)**.

### 3. 📊 Text Analysis
- **Sentiment Classification**: Categorizes text as `Positive`, `Negative`, or `Neutral`.
- **Quantitative Polarity**: Computes a continuous score from `-1.0` (critical) to `+1.0` (affirmative).
- **Linguistic Explanation**: Identifies semantic markers and tone qualifiers.
- **Ranked Keywords**: Extracts top keywords with relevance weighting and semantic category tags.
- Quick-load preset samples (Tech Review, Balanced Analysis, Critical Incident).

### 4. 🧪 Parameter Experimentation
- Compares generation under identical prompts at **Temperature 0.2** (Deterministic / Focused) vs **Temperature 0.9** (Creative / Divergent).
- Quantitative metrics calculated:
  - **Total Words** & **Unique Vocabulary Size**.
  - **Type-Token Ratio (TTR)**: Measure of lexical diversity ($TTR = \frac{\text{Unique Words}}{\text{Total Words}}$).
  - Mathematical breakdown explaining softmax distribution flattening and token sampling dynamics.

---

## 🏗️ System Architecture

```text
AI_Content_Creation_Analysis/
├── app.py                   # Premium Streamlit Web Application
├── main.py                  # Interactive Terminal CLI Runner
├── prompts.py               # 5-Pillar Structured Prompt Templates
├── llm_client.py            # Multi-Provider Client (OpenAI, Anthropic, Simulation)
├── content_generation.py    # Story, Poem & Social Post Generator
├── podcast_planning.py      # Podcast Show Planner & Markdown Exporter
├── text_analysis.py         # Sentiment & Keyword Extraction NLP Engine
├── parameter_experiment.py  # Temperature & Lexical Metric Evaluator
├── json_utils.py            # Defensive JSON Parser
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
└── README.md                # Comprehensive Documentation
```

---

## 🛠️ Quick Start & Installation

### 1. Clone & Navigate to Project

```bash
cd /Users/vismayjain/Downloads/AI_Content_Creation_Analysis
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys (Optional)

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Add your keys if desired:
```env
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini

# Optional
ANTHROPIC_API_KEY=sk-ant-...
```

> **Note on Simulation Mode**: If no API key is provided, the system automatically enters **Intelligent Simulation Mode**. All tabs, prompt templates, analytics, and exports work out-of-the-box!

---

## 🌐 Web Application Usage

Launch the Streamlit web app:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

- Select your provider or leave it in **Simulation Mode**.
- Explore the 5 interactive tabs:
  - **Content Generation**
  - **Podcast Planning**
  - **Text Analysis**
  - **Parameter Experiment**
  - **Prompt Engineering Architecture**

---

## 💻 CLI Terminal Usage

To run the full application from the command line:

```bash
python3 main.py
```

Features an interactive menu:
```text
=================================================================
 AI-Powered Content Creation & Analysis System [Demo Simulation Mode]
=================================================================
  1. ✍️ Content Generation (Story, Poem, Social Post)
  2. 🎙️ Podcast Planning (Title, Guest, 8 Questions)
  3. 📊 Text Analysis (Sentiment & Keywords)
  4. 🧪 Parameter Experimentation (Temp 0.2 vs 0.9)
  5. ⚙️ Toggle Provider / API Key
  6. ❌ Exit
```

---

## 🔬 Parameter Experimentation Insights

### Why does Temperature matter?
In Transformer LLMs, the final hidden state produces logits $z_i$ over the vocabulary. The probability of choosing token $i$ is calculated using the temperature-adjusted softmax:

$$P(w_i) = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$$

- **$T = 0.2$ (Low Temperature)**: Divides logits by a fraction, amplifying differences between high and low logits. The model almost exclusively samples the most probable canonical words, resulting in lower lexical diversity ($TTR \approx 0.5 - 0.6$) and high predictability.
- **$T = 0.9$ (High Temperature)**: Flattens the probability curve, giving unusual, expressive, and metaphorical words an opportunity to be sampled. This elevates lexical diversity ($TTR \approx 0.7 - 0.85$), creating more creative and varied text.
