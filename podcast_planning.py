"""
Podcast Planning Module
========================
Generates a comprehensive podcast episode plan:
- Engaging episode title & tagline
- 2-3 paragraph episode synopsis
- Target guest profile & qualifications
- Exactly 8 structured interview questions grouped by conversational stage
"""

import re
from typing import Dict, Any, List
from prompts import podcast_prompt, PromptTemplate
from llm_client import LLMClient
from json_utils import safe_json_parse


def generate_podcast_plan(
    client: LLMClient,
    topic: str,
    host_style: str = "Conversational & In-Depth",
    target_audience: str = "Industry professionals and curious learners",
    num_questions: int = 8,
    temperature: float = 0.6,
    top_p: float = 0.9
) -> Dict[str, Any]:
    """
    Generate an episode production plan.
    Returns:
    {
        "podcast_title": str,
        "tagline": str,
        "description": str,
        "guest_profile": dict,
        "interview_questions": list of dicts,
        "prompt_template": PromptTemplate,
        "raw_response": str,
        "meta": dict
    }
    """
    template = podcast_prompt(
        topic=topic,
        host_style=host_style,
        target_audience=target_audience,
        num_questions=num_questions
    )

    system_msg, user_msg = template.as_system_and_user()
    response = client.call(
        prompt=user_msg,
        system_prompt=system_msg,
        temperature=temperature,
        top_p=top_p,
        max_tokens=1800,
        request_type="podcast"
    )

    raw_text = response.get("content", "").strip()
    parsed = safe_json_parse(raw_text, fallback={})

    # Defensive fallback if JSON structure is missing or malformed
    title = parsed.get("podcast_title") or f"Voices of Tomorrow: {topic}"
    tagline = parsed.get("tagline") or f"A deep dive into {topic} and the future of human capability."
    description = parsed.get("description") or (
        f"In this episode, we explore the evolving landscape of {topic}. "
        "Our host dives deep into the technological, social, and practical implications "
        "shaping how practitioners and thinkers navigate this rapid transformation."
    )
    
    guest_profile = parsed.get("guest_profile", {})
    if not isinstance(guest_profile, dict) or not guest_profile.get("role_title"):
        guest_profile = {
            "role_title": f"Senior Domain Specialist & Researcher in {topic}",
            "ideal_background": "10+ years leading cutting-edge research, public speaking, and applied implementations.",
            "why_ideal": "Provides grounded empirical depth and nuanced clarity for listeners."
        }

    raw_questions = parsed.get("interview_questions", [])
    questions: List[Dict[str, Any]] = []

    if isinstance(raw_questions, list) and len(raw_questions) > 0:
        for idx, q in enumerate(raw_questions, 1):
            if isinstance(q, dict):
                stage = q.get("stage", "Core Deep-Dive")
                question_text = q.get("question", str(q))
                rationale = q.get("rationale", "Explores key topic dimensions.")
            else:
                stage = "Discussion Point"
                question_text = str(q)
                rationale = "Provokes detailed narrative response."
            
            questions.append({
                "number": idx,
                "stage": stage,
                "question": question_text,
                "rationale": rationale
            })
    else:
        # Fallback question extraction via regex
        q_lines = re.findall(r"(?:Q?\d+[\.:\)]\s*)([^\n]+)", raw_text)
        if not q_lines:
            q_lines = [
                f"What first sparked your fascination and career journey with {topic}?",
                "What was the most challenging technical roadblock you encountered when starting out?",
                "How has the core paradigm shifted over the past 3 to 5 years?",
                "What is a common misconception the public or industry holds about this space?",
                "Could you walk us through an unexpected failure that yielded your biggest breakthrough?",
                "Where do you see the most exciting convergence between this domain and adjacent technologies?",
                "What ethical or systemic considerations should founders and practitioners keep top of mind?",
                "What is one piece of actionable advice you'd give to someone entering this arena today?"
            ]
        
        stages = [
            "Icebreaker & Backstory",
            "Icebreaker & Backstory",
            "Core Deep-Dive",
            "Core Deep-Dive",
            "Core Deep-Dive",
            "Future Vision & Debates",
            "Future Vision & Debates",
            "Rapid-Fire Takeaway"
        ]
        for i, q_text in enumerate(q_lines[:num_questions], 0):
            stage = stages[i] if i < len(stages) else "Core Deep-Dive"
            questions.append({
                "number": i + 1,
                "stage": stage,
                "question": q_text.strip(),
                "rationale": "Engineered to unpack nuanced insights without superficial yes/no answers."
            })

    return {
        "podcast_title": title,
        "tagline": tagline,
        "description": description,
        "guest_profile": guest_profile,
        "interview_questions": questions,
        "prompt_template": template,
        "raw_response": raw_text,
        "meta": response
    }


def export_as_markdown(plan: Dict[str, Any]) -> str:
    """Format the plan as an industry-standard Podcast Show Notes & Cue Sheet document."""
    lines = [
        f"# 🎙️ Podcast Production Cue Sheet",
        f"## Episode: {plan['podcast_title']}",
        f"*{plan['tagline']}*\n",
        f"---",
        f"### 📋 Episode Synopsis",
        f"{plan['description']}\n",
        f"### 👤 Ideal Guest Profile",
        f"- **Role:** {plan['guest_profile'].get('role_title', 'Expert')}",
        f"- **Pedigree:** {plan['guest_profile'].get('ideal_background', 'N/A')}",
        f"- **Why Chosen:** {plan['guest_profile'].get('why_ideal', 'N/A')}\n",
        f"### ❓ Structured Interview Questions ({len(plan['interview_questions'])} Questions)",
    ]

    for q in plan["interview_questions"]:
        lines.append(f"#### Q{q['number']}. [{q['stage']}]")
        lines.append(f"> \"{q['question']}\"")
        lines.append(f"*Producer Rationale:* {q['rationale']}\n")

    return "\n".join(lines)
