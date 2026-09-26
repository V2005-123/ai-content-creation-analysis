import os
import streamlit as st
from dotenv import load_dotenv
from llm_client import LLMClient
from content_generation import generate_content
from podcast_planning import generate_podcast_plan, export_as_markdown
from text_analysis import analyze_text
from parameter_experiment import run_experiment
from prompts import (
    content_prompt,
    podcast_prompt,
    text_analysis_prompt,
    experiment_prompt
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Studio | Prompt Engineering & Analysis",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Modern Glassmorphic CSS Styling
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

h1, h2, h3, .brand-title {
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: -0.02em;
}

/* Hero Banner */
.hero-container {
    background: linear-gradient(135deg, rgba(30, 27, 75, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.15);
    backdrop-filter: blur(16px);
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(120deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 1.05rem;
    line-height: 1.5;
}

/* Feature Badge */
.feature-badge {
    display: inline-block;
    padding: 4px 12px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(129, 140, 248, 0.3);
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #c7d2fe;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-right: 6px;
    margin-bottom: 6px;
}

/* Modern Card */
.glass-card {
    background: rgba(17, 24, 39, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(12px);
    transition: border-color 0.2s ease, transform 0.2s ease;
}
.glass-card:hover {
    border-color: rgba(167, 139, 250, 0.3);
}

/* Pillar Container for Prompt Engineering */
.pillar-container {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(79, 70, 229, 0.2);
    border-radius: 12px;
    padding: 16px;
    margin-top: 12px;
}

.pillar-tag {
    font-weight: 700;
    font-size: 0.75rem;
    padding: 3px 8px;
    border-radius: 6px;
    text-transform: uppercase;
    display: inline-block;
    margin-bottom: 6px;
}
.tag-role { background: rgba(59, 130, 246, 0.25); color: #93c5fd; border: 1px solid #3b82f6; }
.tag-context { background: rgba(168, 85, 247, 0.25); color: #d8b4fe; border: 1px solid #a855f7; }
.tag-task { background: rgba(236, 72, 153, 0.25); color: #f472b6; border: 1px solid #ec4899; }
.tag-constraints { background: rgba(245, 158, 11, 0.25); color: #fcd34d; border: 1px solid #f59e0b; }
.tag-format { background: rgba(16, 185, 129, 0.25); color: #6ee7b7; border: 1px solid #10b981; }

/* Question Box */
.question-item {
    background: rgba(30, 41, 59, 0.5);
    border-left: 4px solid #6366f1;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin-bottom: 12px;
}

/* Metric Chip */
.metric-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 255, 255, 0.05);
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.85rem;
    color: #cbd5e1;
    margin-right: 8px;
}

/* Keyword Pill */
.keyword-pill {
    display: inline-block;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2));
    border: 1px solid rgba(139, 92, 246, 0.4);
    color: #e0e7ff;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    margin: 4px;
}

/* Sentiment Badges */
.sentiment-badge-pos {
    background: rgba(16, 185, 129, 0.2);
    border: 1px solid #10b981;
    color: #34d399;
    padding: 6px 16px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 1rem;
    display: inline-block;
}
.sentiment-badge-neu {
    background: rgba(245, 158, 11, 0.2);
    border: 1px solid #f59e0b;
    color: #fbbf24;
    padding: 6px 16px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 1rem;
    display: inline-block;
}
.sentiment-badge-neg {
    background: rgba(239, 68, 68, 0.2);
    border: 1px solid #ef4444;
    color: #f87171;
    padding: 6px 16px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 1rem;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Sidebar Configuration & Provider State
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 12px;'>
            <span style='font-size: 1.8rem;'>⚡</span>
            <div>
                <h3 style='margin: 0; font-size: 1.25rem;'>AI Studio</h3>
                <span style='font-size: 0.75rem; color: #94a3b8;'>Prompt Engineering Suite</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔌 LLM Provider")
    provider_choice = st.selectbox(
        "Service Provider",
        ["OpenAI", "Anthropic Claude", "Simulation Mode (Offline Demo)"],
        index=0
    )

    env_openai_key = os.getenv("OPENAI_API_KEY", "")
    env_anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
    force_sim = (provider_choice == "Simulation Mode (Offline Demo)")

    if provider_choice == "OpenAI":
        api_key_input = st.text_input(
            "OpenAI API Key",
            value=env_openai_key,
            type="password",
            placeholder="sk-proj-...",
            help="Loaded from .env if present. Leave empty to use intelligent simulation."
        )
        model_options = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "o3-mini", "Custom"]
        selected_model = st.selectbox("OpenAI Model", model_options, index=0)
        if selected_model == "Custom":
            active_model = st.text_input("Custom Model Identifier", value="gpt-4o")
        else:
            active_model = selected_model
        provider_name = "openai"

    elif provider_choice == "Anthropic Claude":
        api_key_input = st.text_input(
            "Anthropic API Key",
            value=env_anthropic_key,
            type="password",
            placeholder="sk-ant-...",
            help="Loaded from .env if present. Leave empty to use intelligent simulation."
        )
        model_options = ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"]
        active_model = st.selectbox("Claude Model", model_options, index=0)
        provider_name = "anthropic"

    else:
        api_key_input = ""
        active_model = "Deterministic Neural Mock"
        provider_name = "simulation"

    # Initialize client
    client = LLMClient(
        provider=provider_name,
        api_key=api_key_input,
        model=active_model,
        force_simulation=force_sim
    )

    # Provider Status Banner
    if client.is_live_ready():
        st.success(f"🟢 Connected to {client.provider.upper()} ({active_model})")
    else:
        st.info("🟡 Running in **Simulation Mode** (No API Key Required). All features are fully interactive and demonstrable!")

    st.markdown("---")
    st.markdown("### 🎛️ Default Hyperparameters")
    global_temp = st.slider("Temperature (Creativity)", 0.0, 1.0, 0.7, 0.05,
                           help="Lower values are deterministic; higher values increase variety and surprise.")
    global_top_p = st.slider("Top-P (Nucleus Sampling)", 0.1, 1.0, 0.9, 0.05,
                            help="Limits cumulative token pool probability threshold.")

    st.markdown("---")
    st.caption("Prompt Engineering Assignment • Built with Streamlit & Python")


# ---------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div class="hero-title">⚡ AI Content Creation & Analysis System</div>
    <div class="hero-subtitle">
        An end-to-end prompt engineering workbench demonstrating the <b>5 Pillars of Structured Prompts</b>,
        creative generation, podcast production architecture, NLP text analytics, and hyperparameter sensitivity.
    </div>
    <div style="margin-top: 14px;">
        <span class="feature-badge">Role Architecture</span>
        <span class="feature-badge">Context Framing</span>
        <span class="feature-badge">Constraint Guardrails</span>
        <span class="feature-badge">Podcast Production</span>
        <span class="feature-badge">Sentiment NLP</span>
        <span class="feature-badge">Temperature Sweep</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Main Application Tabs
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "✍️ Content Generation",
    "🎙️ Podcast Planning",
    "📊 Text Analysis",
    "🧪 Parameter Experiment",
    "📐 Prompt Engineering Architecture"
])


# =========================================================
# TAB 1: CONTENT GENERATION
# =========================================================
with tab1:
    st.markdown("### ✍️ Creative AI Content Generation")
    st.caption("Generates structured narrative fiction, lyrical poetry, or viral social copy using tailored prompt templates.")

    col1, col2 = st.columns([2, 1])

    with col1:
        content_topic = st.text_input(
            "Topic or Core Concept",
            value="The First Neural Teleportation Experiment in 2045",
            placeholder="e.g., Renewable Energy Breakthrough, Space Mining, Ancient Library"
        )

    with col2:
        content_type = st.selectbox(
            "Content Type",
            ["Story", "Poem", "Social Media Post"]
        )

    col3, col4, col5 = st.columns(3)
    with col3:
        tone_option = st.selectbox(
            "Tone / Voice",
            ["Engaging & Lyrical", "Suspenseful & Dramatic", "Inspiring & Visionary", "Analytical & Thoughtful", "Witty & Fast-Paced"]
        )
    with col4:
        audience_option = st.selectbox(
            "Target Audience",
            ["General Audience", "Tech Professionals", "Creative Enthusiasts", "Young Adults", "Industry Executives"]
        )
    with col5:
        target_words = st.slider("Target Length (Words)", 100, 500, 250, 50)

    btn_gen = st.button("✨ Generate Structured Content", type="primary", use_container_width=True)

    if btn_gen:
        if not content_topic.strip():
            st.warning("Please specify a topic.")
        else:
            with st.spinner("Synthesizing content with structured prompt..."):
                res = generate_content(
                    client=client,
                    topic=content_topic,
                    content_type=content_type,
                    tone=tone_option,
                    target_audience=audience_option,
                    word_count=target_words,
                    temperature=global_temp,
                    top_p=global_top_p
                )

            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px;">
                    <span style="font-size: 1.3rem; font-weight: 700; color: #a78bfa;">{res['title']}</span>
                    <div>
                        <span class="metric-chip">📝 {res['word_count']} words</span>
                        <span class="metric-chip">⏱️ ~{res['read_time_mins']} min read</span>
                        <span class="metric-chip">⚡ {res['meta']['provider']}</span>
                    </div>
                </div>
                <div style="white-space: pre-wrap; line-height: 1.7; font-size: 1.02rem; color: #f1f5f9;">
{res['body']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if res['takeaway']:
                st.info(f"💡 **Takeaway / Resonance:** {res['takeaway']}")

            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                st.download_button(
                    "📥 Download Markdown",
                    data=f"# {res['title']}\n\n{res['body']}\n\n---\n*Generated by AI Studio*",
                    file_name=f"{content_type.lower()}_{content_topic[:15].strip().replace(' ', '_')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with col_dl2:
                with st.expander("🔍 View Structured Prompt Template"):
                    p_dict = res['prompt_template'].to_dict()
                    st.markdown(f"""
                    <div class="pillar-container">
                        <span class="pillar-tag tag-role">1. Role</span><br>{p_dict['Role']}<br><br>
                        <span class="pillar-tag tag-context">2. Context</span><br>{p_dict['Context']}<br><br>
                        <span class="pillar-tag tag-task">3. Task</span><br>{p_dict['Task']}<br><br>
                        <span class="pillar-tag tag-constraints">4. Constraints</span><br>
                        {''.join(f'• {c}<br>' for c in p_dict['Constraints'])}<br>
                        <span class="pillar-tag tag-format">5. Output Format</span><br>
                        <code>{p_dict['Output Format']}</code>
                    </div>
                    """, unsafe_allow_html=True)


# =========================================================
# TAB 2: PODCAST PLANNING
# =========================================================
with tab2:
    st.markdown("### 🎙️ Podcast Episode Production Planner")
    st.caption("Generates a complete broadcast plan: Episode title, show notes synopsis, ideal guest profile, and 8 structured interview questions.")

    col_p1, col_p2 = st.columns([2, 1])
    with col_p1:
        podcast_topic = st.text_input(
            "Episode Theme / Topic",
            value="The Architecture of Autonomous AI Agents in Production",
            placeholder="e.g., Quantum Computing Reality Check, Future of Clean Meat"
        )
    with col_p2:
        host_style = st.selectbox(
            "Interview Style",
            ["Conversational & In-Depth", "Investigative & Hard-Hitting", "Educational Masterclass", "Founder Story / Origin"]
        )

    col_p3, col_p4 = st.columns([2, 1])
    with col_p3:
        target_listeners = st.text_input(
            "Target Demographic",
            value="Software architects, engineering leaders, and curious technologists"
        )
    with col_p4:
        num_q = st.number_input("Number of Questions", min_value=5, max_value=12, value=8)

    btn_pod = st.button("🎙️ Generate Complete Episode Plan", type="primary", use_container_width=True)

    if btn_pod:
        if not podcast_topic.strip():
            st.warning("Please enter a podcast topic.")
        else:
            with st.spinner("Engineering podcast production cue sheet..."):
                plan = generate_podcast_plan(
                    client=client,
                    topic=podcast_topic,
                    host_style=host_style,
                    target_audience=target_listeners,
                    num_questions=int(num_q),
                    temperature=global_temp,
                    top_p=global_top_p
                )

            # Overview Card
            st.markdown(f"""
            <div class="glass-card">
                <div style="font-size: 1.5rem; font-weight: 700; color: #60a5fa;">{plan['podcast_title']}</div>
                <div style="font-size: 1rem; color: #94a3b8; margin-top: 4px; font-style: italic;">{plan['tagline']}</div>
                <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 16px 0;">
                <div style="font-size: 0.95rem; line-height: 1.65; color: #e2e8f0;">
                    {plan['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Guest Profile Card
            guest = plan['guest_profile']
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #a855f7;">
                <div style="font-weight: 700; font-size: 1.1rem; color: #c084fc; margin-bottom: 8px;">👤 Ideal Guest Persona & Dossier</div>
                <div><b>Target Title:</b> {guest.get('role_title', 'Industry Leader')}</div>
                <div style="margin-top: 4px;"><b>Background & Pedigree:</b> {guest.get('ideal_background', 'N/A')}</div>
                <div style="margin-top: 4px;"><b>Why This Guest:</b> {guest.get('why_ideal', 'N/A')}</div>
            </div>
            """, unsafe_allow_html=True)

            # 8 Structured Questions
            st.markdown(f"#### ❓ Structured Question Progression ({len(plan['interview_questions'])} Questions)")
            for q in plan['interview_questions']:
                stage_color = "#38bdf8" if "Icebreaker" in q['stage'] else ("#ec4899" if "Future" in q['stage'] else ("#10b981" if "Rapid" in q['stage'] else "#818cf8"))
                st.markdown(f"""
                <div class="question-item" style="border-left-color: {stage_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-weight: 700; color: {stage_color}; font-size: 0.9rem;">Question {q['number']}</span>
                        <span style="font-size: 0.75rem; background: rgba(255,255,255,0.08); padding: 2px 8px; border-radius: 4px; color: #cbd5e1;">{q['stage']}</span>
                    </div>
                    <div style="font-size: 1.05rem; font-weight: 500; color: #f8fafc; margin-bottom: 6px;">
                        "{q['question']}"
                    </div>
                    <div style="font-size: 0.85rem; color: #94a3b8; font-style: italic;">
                        ↳ Producer Rationale: {q['rationale']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Export Actions
            md_export = export_as_markdown(plan)
            st.download_button(
                "📋 Download Full Production Cue Sheet (Markdown)",
                data=md_export,
                file_name=f"podcast_cue_sheet_{podcast_topic[:15].strip().replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )


# =========================================================
# TAB 3: TEXT ANALYSIS
# =========================================================
with tab3:
    st.markdown("### 📊 Dual-Layer NLP Text Analysis")
    st.caption("Performs structured sentiment classification, polarity scoring, emotional tone explanation, and ranked keyword extraction.")

    st.markdown("**Quick-load preset examples:**")
    col_pre1, col_pre2, col_pre3 = st.columns(3)
    sample_text = ""
    if col_pre1.button("✨ Positive Tech Review"):
        sample_text = "The new neural compiler dramatically slashes memory footprint by 40% while preserving absolute mathematical accuracy. Our engineering velocity doubled within two weeks, making it easily the most impactful developer tooling upgrade of the year."
    if col_pre2.button("⚖️ Balanced Analysis"):
        sample_text = "Autonomous AI agents offer unprecedented speed for triage and data pipeline automation, yet their non-deterministic nature still introduces fragile edge cases. Teams must balance developer enthusiasm with robust observability and strict human-in-the-loop guardrails."
    if col_pre3.button("⚠️ Critical Incident Postmortem"):
        sample_text = "A severe cascading outage crippled database replicas for four hours due to improper timeout thresholds in the caching layer. The documentation was badly outdated, communication across shifts was chaotic, and customer trust has been seriously damaged."

    analysis_input = st.text_area(
        "Enter text to analyze",
        value=sample_text or "AI tools make personalized learning significantly faster, but privacy and ethical deployment remain paramount concerns.",
        height=140
    )

    btn_analyze = st.button("📊 Run Sentiment & Keyword Extraction", type="primary", use_container_width=True)

    if btn_analyze:
        if not analysis_input.strip():
            st.warning("Please provide text to analyze.")
        else:
            with st.spinner("Performing NLP sentiment and semantic keyword extraction..."):
                analysis_res = analyze_text(
                    client=client,
                    text=analysis_input,
                    temperature=0.2, # Low temperature for analytical consistency
                    top_p=0.9
                )

            sent = analysis_res['sentiment']
            badge_class = "sentiment-badge-pos" if sent == "Positive" else ("sentiment-badge-neu" if sent == "Neutral" else "sentiment-badge-neg")
            stats = analysis_res['text_stats']

            # Results Overview Card
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <div>
                        <span style="font-size: 0.9rem; color: #94a3b8; margin-right: 8px;">Classification:</span>
                        <span class="{badge_class}">{sent}</span>
                    </div>
                    <div>
                        <span class="metric-chip">Polarity: {analysis_res['polarity_score']:+.2f}</span>
                        <span class="metric-chip">Confidence: {analysis_res['confidence']}%</span>
                        <span class="metric-chip">Words: {stats['word_count']}</span>
                    </div>
                </div>
                <div style="font-size: 1rem; color: #f1f5f9; line-height: 1.6; margin-bottom: 14px;">
                    <b>Linguistic Analysis:</b> {analysis_res['explanation']}
                </div>
                <div>
                    <b>Dominant Tone / Emotions:</b> {', '.join(analysis_res['dominant_emotions'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Keywords Section
            st.markdown("#### 🏷️ Salient Keywords & Semantic Tags")
            kw_html = "".join([
                f'<span class="keyword-pill"><b>{kw["keyword"]}</b> <small style="opacity: 0.8;">({kw["category"]} • {kw["relevance"]:.2f})</small></span>'
                for kw in analysis_res['keywords']
            ])
            st.markdown(f'<div style="margin-bottom: 18px;">{kw_html}</div>', unsafe_allow_html=True)

            with st.expander("🔍 View Structured Prompt Sent to Model"):
                st.code(analysis_res['prompt_template'].render(), language="text")


# =========================================================
# TAB 4: PARAMETER EXPERIMENT
# =========================================================
with tab4:
    st.markdown("### 🧪 Hyperparameter Sensitivity Experiment")
    st.caption("Demonstrates the mathematical effect of Temperature (0.2 vs 0.9) on token probability distributions, vocabulary richness, and stylistic divergence.")

    exp_topic = st.text_input(
        "Experiment Topic",
        value="The Awakening of an Orbital Satellite Constellation",
        placeholder="e.g. Deep Ocean Archaeology, Quantum Superposition"
    )

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        t_low = st.slider("Low Temperature (Focused / Deterministic)", 0.0, 0.4, 0.2, 0.05)
    with col_t2:
        t_high = st.slider("High Temperature (Creative / Divergent)", 0.6, 1.2, 0.9, 0.05)

    btn_exp = st.button("🧪 Execute Side-by-Side Experiment", type="primary", use_container_width=True)

    if btn_exp:
        if not exp_topic.strip():
            st.warning("Please enter an experiment topic.")
        else:
            with st.spinner("Running dual sampling passes..."):
                exp_res = run_experiment(
                    client=client,
                    topic=exp_topic,
                    temp_low=t_low,
                    temp_high=t_high,
                    top_p=global_top_p
                )

            col_out1, col_out2 = st.columns(2)

            with col_out1:
                st.markdown(f"""
                <div class="glass-card" style="border-top: 4px solid #38bdf8;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-weight: 700; color: #38bdf8; font-size: 1.1rem;">🌡️ Low Temp = {t_low}</span>
                        <span class="metric-chip">Deterministic</span>
                    </div>
                    <div style="font-size: 0.95rem; line-height: 1.65; color: #f1f5f9; min-height: 140px;">
                        {exp_res['low_temp']['output']}
                    </div>
                    <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 12px 0;">
                    <div style="font-size: 0.85rem; color: #94a3b8;">
                        <b>Total Words:</b> {exp_res['low_temp']['metrics']['total_words']} | 
                        <b>Unique Words:</b> {exp_res['low_temp']['metrics']['unique_words']} | 
                        <b>Lexical Diversity (TTR):</b> {exp_res['low_temp']['metrics']['lexical_diversity']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_out2:
                st.markdown(f"""
                <div class="glass-card" style="border-top: 4px solid #ec4899;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-weight: 700; color: #ec4899; font-size: 1.1rem;">🔥 High Temp = {t_high}</span>
                        <span class="metric-chip">Creative / Divergent</span>
                    </div>
                    <div style="font-size: 0.95rem; line-height: 1.65; color: #f1f5f9; min-height: 140px;">
                        {exp_res['high_temp']['output']}
                    </div>
                    <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 12px 0;">
                    <div style="font-size: 0.85rem; color: #94a3b8;">
                        <b>Total Words:</b> {exp_res['high_temp']['metrics']['total_words']} | 
                        <b>Unique Words:</b> {exp_res['high_temp']['metrics']['unique_words']} | 
                        <b>Lexical Diversity (TTR):</b> {exp_res['high_temp']['metrics']['lexical_diversity']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Analysis Summary
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #f59e0b;">
                <div style="font-weight: 700; color: #f59e0b; margin-bottom: 6px;">📈 Analytical Findings & Softmax Probability Mechanics</div>
                <div style="font-size: 0.95rem; color: #e2e8f0; line-height: 1.6;">
                    {exp_res['analysis']['summary']}
                </div>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
# TAB 5: PROMPT ENGINEERING ARCHITECTURE
# =========================================================
with tab5:
    st.markdown("### 📐 The 5 Pillars of Structured Prompt Engineering")
    st.caption("How prompt templates transform vague user requests into robust, deterministic AI outputs.")

    col_arch1, col_arch2 = st.columns([1, 1])

    with col_arch1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #a78bfa; margin-top: 0;">🏛️ The Five Core Components</h4>
            
            <div style="margin-bottom: 12px;">
                <span class="pillar-tag tag-role">1. ROLE</span>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin: 4px 0 0 0;">
                    Establishes persona, domain identity, vocabulary constraints, and authority (e.g. <i>"Senior Computational Linguist"</i>).
                </p>
            </div>
            
            <div style="margin-bottom: 12px;">
                <span class="pillar-tag tag-context">2. CONTEXT</span>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin: 4px 0 0 0;">
                    Supplies background facts, environment details, user goals, and situational circumstances.
                </p>
            </div>
            
            <div style="margin-bottom: 12px;">
                <span class="pillar-tag tag-task">3. TASK</span>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin: 4px 0 0 0;">
                    Unambiguous, active-verb directive specifying the core deliverable.
                </p>
            </div>
            
            <div style="margin-bottom: 12px;">
                <span class="pillar-tag tag-constraints">4. CONSTRAINTS</span>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin: 4px 0 0 0;">
                    Negative guardrails, length limits, forbidden phrases, tone parameters, and safety requirements.
                </p>
            </div>
            
            <div>
                <span class="pillar-tag tag-format">5. OUTPUT FORMAT</span>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin: 4px 0 0 0;">
                    Exact syntactic contract (JSON schema, Markdown layout, or section tags) enabling reliable downstream parsing.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_arch2:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #60a5fa; margin-top: 0;">⚡ Naive Prompt vs Structured Prompt</h4>
            
            <div style="background: rgba(239, 68, 68, 0.1); border-left: 3px solid #ef4444; padding: 10px 14px; border-radius: 6px; margin-bottom: 14px;">
                <b style="color: #f87171;">❌ Naive / Zero-Shot Prompt:</b>
                <p style="margin: 4px 0 0 0; font-size: 0.9rem; color: #fca5a5; font-family: monospace;">
                    "Write some questions for my podcast about AI."
                </p>
                <small style="color: #cbd5e1;">Flaws: Generic questions, unpredictable format, no guest context, high hallucination risk.</small>
            </div>

            <div style="background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; padding: 10px 14px; border-radius: 6px;">
                <b style="color: #34d399;">✓ Structured 5-Pillar Prompt:</b>
                <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #a7f3d0; font-family: monospace; line-height: 1.4;">
                    ROLE: Executive Producer<br>
                    CONTEXT: 45-min technical episode on production AI agents<br>
                    TASK: Create title, synopsis, guest persona, and 8 progressive questions<br>
                    CONSTRAINTS: 2 backstory, 3 deep dive, 2 vision, 1 takeaway. No yes/no questions<br>
                    OUTPUT FORMAT: Strict JSON schema
                </p>
                <small style="color: #cbd5e1;">Benefits: 100% deterministic parsing, production-ready depth, repeatable automation.</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #64748b;">
    <span>⚡ AI Studio • Prompt Engineering Assignment System</span>
    <span>Python • Streamlit • Multi-Provider Architecture</span>
</div>
""", unsafe_allow_html=True)
