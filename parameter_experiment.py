"""
Parameter Experimentation Module
=================================
Runs identical structured prompts under different hyperparameter settings
(e.g., Temperature 0.2 vs 0.9, Top-P variations) to demonstrate their
mathematical and stylistic impact on LLM output.
"""

import re
from typing import Dict, Any, List
from prompts import experiment_prompt, PromptTemplate
from llm_client import LLMClient


def calculate_lexical_metrics(text: str) -> Dict[str, Any]:
    """
    Computes linguistic diversity metrics:
    - Total words
    - Unique words (vocabulary richness)
    - Type-Token Ratio (TTR: measure of lexical diversity)
    - Average word length
    """
    words = re.findall(r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b", text.lower())
    total_words = len(words)
    if total_words == 0:
        return {
            "total_words": 0,
            "unique_words": 0,
            "lexical_diversity": 0.0,
            "avg_word_length": 0.0
        }

    unique_words = len(set(words))
    ttr = round(unique_words / total_words, 3)
    avg_len = round(sum(len(w) for w in words) / total_words, 1)

    return {
        "total_words": total_words,
        "unique_words": unique_words,
        "lexical_diversity": ttr, # Type-Token Ratio
        "avg_word_length": avg_len
    }


def run_experiment(
    client: LLMClient,
    topic: str,
    temp_low: float = 0.2,
    temp_high: float = 0.9,
    top_p: float = 0.9,
    word_count: int = 100
) -> Dict[str, Any]:
    """
    Runs the same prompt across two temperature extremes.
    Returns:
    {
        "topic": str,
        "prompt_template": PromptTemplate,
        "low_temp": {
            "temperature": float,
            "output": str,
            "metrics": dict,
            "meta": dict
        },
        "high_temp": {
            "temperature": float,
            "output": str,
            "metrics": dict,
            "meta": dict
        },
        "analysis": {
            "ttr_difference": float,
            "vocab_difference": int,
            "summary": str
        }
    }
    """
    template = experiment_prompt(topic, word_count=word_count)
    system_msg, user_msg = template.as_system_and_user()

    # 1. Run Low Temperature
    resp_low = client.call(
        prompt=user_msg,
        system_prompt=system_msg,
        temperature=temp_low,
        top_p=top_p,
        max_tokens=600,
        request_type="experiment"
    )
    text_low = resp_low.get("content", "").strip()
    metrics_low = calculate_lexical_metrics(text_low)

    # 2. Run High Temperature
    resp_high = client.call(
        prompt=user_msg,
        system_prompt=system_msg,
        temperature=temp_high,
        top_p=top_p,
        max_tokens=600,
        request_type="experiment"
    )
    text_high = resp_high.get("content", "").strip()
    metrics_high = calculate_lexical_metrics(text_high)

    ttr_diff = round(metrics_high["lexical_diversity"] - metrics_low["lexical_diversity"], 3)
    vocab_diff = metrics_high["unique_words"] - metrics_low["unique_words"]

    analysis_summary = (
        f"At Temperature {temp_low}, the model sharpens its probability distribution toward "
        "high-frequency, canonical tokens, producing consistent, predictable prose. "
        f"At Temperature {temp_high}, the probability distribution is flattened, allowing "
        f"lower-probability vocabulary to be sampled, yielding a {abs(ttr_diff)*100:.1f}% shift in "
        f"lexical diversity ({metrics_high['unique_words']} unique words vs {metrics_low['unique_words']})."
    )

    return {
        "topic": topic,
        "prompt_template": template,
        "low_temp": {
            "temperature": temp_low,
            "output": text_low,
            "metrics": metrics_low,
            "meta": resp_low
        },
        "high_temp": {
            "temperature": temp_high,
            "output": text_high,
            "metrics": metrics_high,
            "meta": resp_high
        },
        "analysis": {
            "ttr_difference": ttr_diff,
            "vocab_difference": vocab_diff,
            "summary": analysis_summary
        }
    }
