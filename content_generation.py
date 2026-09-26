"""
Content Generation Module
==========================
Generates creative, structured content (stories, poems, social media posts)
using customized PromptTemplates and parameter tuning.
"""

import re
from typing import Dict, Any, Optional
from prompts import content_prompt, PromptTemplate
from llm_client import LLMClient


def generate_content(
    client: LLMClient,
    topic: str,
    content_type: str = "Story",
    tone: str = "Engaging",
    target_audience: str = "General audience",
    word_count: int = 250,
    temperature: float = 0.7,
    top_p: float = 0.9
) -> Dict[str, Any]:
    """
    Executes content generation using structured prompt engineering.
    Returns:
    {
        "raw_output": str,
        "title": str,
        "body": str,
        "takeaway": str,
        "word_count": int,
        "char_count": int,
        "read_time_mins": float,
        "prompt_template": PromptTemplate,
        "meta": Dict[str, Any]
    }
    """
    template = content_prompt(
        topic=topic,
        content_type=content_type,
        tone=tone,
        target_audience=target_audience,
        word_count=word_count
    )

    system_msg, user_msg = template.as_system_and_user()
    
    # Execute generation via LLM client
    req_type = "story" if "story" in content_type.lower() else ("poem" if "poem" in content_type.lower() else "social")
    response = client.call(
        prompt=user_msg,
        system_prompt=system_msg,
        temperature=temperature,
        top_p=top_p,
        max_tokens=1200,
        request_type=req_type
    )

    raw_text = response.get("content", "").strip()

    # Parse Title and Sections defensively
    title_match = re.search(r"Title:\s*([^\n]+)", raw_text, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else f"{content_type}: {topic}"

    # Extract takeaway or footer if present
    takeaway_match = re.search(r"(?:Takeaway|Moral|Poetic Analysis|Call to Action):\s*([\s\S]+?)$", raw_text, re.IGNORECASE)
    takeaway = takeaway_match.group(1).strip() if takeaway_match else ""

    # Clean body text
    body = raw_text
    if title_match:
        body = body.replace(title_match.group(0), "").strip()

    words = len(raw_text.split())
    chars = len(raw_text)
    read_time = round(max(0.2, words / 200), 1)

    return {
        "raw_output": raw_text,
        "title": title,
        "body": body,
        "takeaway": takeaway,
        "word_count": words,
        "char_count": chars,
        "read_time_mins": read_time,
        "prompt_template": template,
        "meta": response
    }
