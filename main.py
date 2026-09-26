"""
AI-Powered Content Creation and Analysis System - CLI
======================================================
Command Line Interface for Prompt Engineering, Content Generation,
Podcast Planning, Text Analysis, and Parameter Experimentation.
"""

import sys
import os
import json
from llm_client import LLMClient
from content_generation import generate_content
from podcast_planning import generate_podcast_plan, export_as_markdown
from text_analysis import analyze_text
from parameter_experiment import run_experiment
from prompts import content_prompt, podcast_prompt, text_analysis_prompt, experiment_prompt


# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def print_header(title: str):
    print("\n" + "=" * 65)
    print(f"{BOLD}{CYAN} {title} {RESET}")
    print("=" * 65)


def print_prompt_breakdown(template):
    print(f"\n{BOLD}{YELLOW}--- [Structured Prompt Breakdown: 5 Pillars] ---{RESET}")
    print(f"{BOLD}1. ROLE:{RESET}\n   {template.role}")
    print(f"{BOLD}2. CONTEXT:{RESET}\n   {template.context}")
    print(f"{BOLD}3. TASK:{RESET}\n   {template.task}")
    print(f"{BOLD}4. CONSTRAINTS:{RESET}")
    for c in template.constraints:
        print(f"   • {c}")
    print(f"{BOLD}5. OUTPUT FORMAT:{RESET}\n   {template.output_format[:120]}...\n")


def menu_content(client: LLMClient):
    print_header("✍️ AI Content Generation")
    topic = input(f"{BOLD}Enter topic:{RESET} ").strip()
    if not topic:
        print(f"{YELLOW}Topic cannot be empty.{RESET}")
        return

    print("\nSelect Content Type:")
    print("  1. Short Story")
    print("  2. Lyrical Poem")
    print("  3. Viral Social Media Post")
    choice = input("Enter choice (1-3) [default: 1]: ").strip() or "1"
    
    type_map = {"1": "Story", "2": "Poem", "3": "Social Media Post"}
    content_type = type_map.get(choice, "Story")

    tone = input(f"Enter tone (e.g. Inspiring, Analytical, Dramatic) [default: Engaging]: ").strip() or "Engaging"
    
    print(f"\n{CYAN}Generating {content_type}...{RESET}")
    result = generate_content(client, topic=topic, content_type=content_type, tone=tone)

    print(f"\n{GREEN}{BOLD}=== {result['title']} ==={RESET}\n")
    print(result["body"])
    if result["takeaway"]:
        print(f"\n{BOLD}Key Takeaway / Resonance:{RESET}\n{result['takeaway']}")

    print(f"\n{DIM}Word Count: {result['word_count']} | Est. Read Time: {result['read_time_mins']} min | Source: {result['meta']['provider']}{RESET}")

    view_p = input("\nView structured prompt template? (y/N): ").strip().lower()
    if view_p == "y":
        print_prompt_breakdown(result["prompt_template"])


def menu_podcast(client: LLMClient):
    print_header("🎙️ Podcast Episode Planning")
    topic = input(f"{BOLD}Enter podcast topic:{RESET} ").strip()
    if not topic:
        print(f"{YELLOW}Topic cannot be empty.{RESET}")
        return

    print(f"\n{CYAN}Planning episode and drafting 8 interview questions...{RESET}")
    plan = generate_podcast_plan(client, topic=topic, num_questions=8)

    print(f"\n{GREEN}{BOLD}Episode Title:{RESET} {plan['podcast_title']}")
    print(f"{DIM}Tagline: {plan['tagline']}{RESET}\n")
    print(f"{BOLD}Description:{RESET}\n{plan['description']}\n")

    guest = plan["guest_profile"]
    print(f"{MAGENTA}{BOLD}Ideal Guest Profile:{RESET}")
    print(f"  • Role: {guest.get('role_title', 'Expert')}")
    print(f"  • Background: {guest.get('ideal_background', 'N/A')}")
    print(f"  • Why Ideal: {guest.get('why_ideal', 'N/A')}\n")

    print(f"{CYAN}{BOLD}8 Structured Interview Questions:{RESET}")
    for q in plan["interview_questions"]:
        print(f"\n  {BOLD}Q{q['number']}. [{q['stage']}]{RESET}")
        print(f"     \"{q['question']}\"")
        print(f"     {DIM}↳ Rationale: {q['rationale']}{RESET}")

    save_opt = input("\nSave production cue sheet to markdown file? (y/N): ").strip().lower()
    if save_opt == "y":
        filename = f"podcast_plan_{topic.lower().replace(' ', '_')[:20]}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(export_as_markdown(plan))
        print(f"{GREEN}✓ Saved to {filename}{RESET}")

    view_p = input("\nView structured prompt template? (y/N): ").strip().lower()
    if view_p == "y":
        print_prompt_breakdown(plan["prompt_template"])


def menu_text_analysis(client: LLMClient):
    print_header("📊 Text Analysis (Sentiment & Keywords)")
    print("Enter text to analyze (type or paste text below, press Enter):")
    text = input("> ").strip()
    if not text:
        text = "Artificial intelligence tools make personalized learning significantly faster, but privacy and ethical deployment remain paramount concerns."
        print(f"{DIM}Using sample text: \"{text}\"{RESET}")

    print(f"\n{CYAN}Analyzing emotional tone and extracting salient keywords...{RESET}")
    res = analyze_text(client, text=text)

    sent_color = GREEN if res["sentiment"] == "Positive" else (YELLOW if res["sentiment"] == "Neutral" else "\033[91m")
    print(f"\n{BOLD}Sentiment:{RESET} {sent_color}{BOLD}{res['sentiment']}{RESET} (Polarity: {res['polarity_score']:+.2f}, Confidence: {res['confidence']}%)")
    print(f"{BOLD}Explanation:{RESET} {res['explanation']}\n")

    print(f"{BOLD}Dominant Emotions:{RESET} {', '.join(res['dominant_emotions'])}\n")

    print(f"{CYAN}{BOLD}Top Keywords Extracted:{RESET}")
    for kw in res["keywords"]:
        rel_bar = "█" * int(kw['relevance'] * 10)
        print(f"  • {kw['keyword']:<20} [{kw['category']:<15}] Relevance: {kw['relevance']:.2f} {DIM}{rel_bar}{RESET}")

    stats = res["text_stats"]
    print(f"\n{DIM}Text Stats: {stats['word_count']} words | {stats['char_count']} chars | Est. read time: {stats['read_time_secs']}s{RESET}")

    view_p = input("\nView structured prompt template? (y/N): ").strip().lower()
    if view_p == "y":
        print_prompt_breakdown(res["prompt_template"])


def menu_parameter_experiment(client: LLMClient):
    print_header("🧪 Parameter Experimentation (Temperature 0.2 vs 0.9)")
    topic = input(f"{BOLD}Enter experiment topic:{RESET} ").strip()
    if not topic:
        topic = "The Future of Human-AI Collaboration"
        print(f"{DIM}Using default topic: \"{topic}\"{RESET}")

    print(f"\n{CYAN}Running dual sampling passes on identical prompt...{RESET}")
    exp = run_experiment(client, topic=topic, temp_low=0.2, temp_high=0.9)

    print(f"\n{BOLD}{CYAN}--- [Temperature = 0.2: Deterministic / Focused] ---{RESET}")
    print(exp["low_temp"]["output"])
    m_low = exp["low_temp"]["metrics"]
    print(f"{DIM}Metrics: {m_low['total_words']} words | {m_low['unique_words']} unique words | Lexical Diversity (TTR): {m_low['lexical_diversity']}{RESET}\n")

    print(f"{BOLD}{MAGENTA}--- [Temperature = 0.9: Creative / Divergent] ---{RESET}")
    print(exp["high_temp"]["output"])
    m_high = exp["high_temp"]["metrics"]
    print(f"{DIM}Metrics: {m_high['total_words']} words | {m_high['unique_words']} unique words | Lexical Diversity (TTR): {m_high['lexical_diversity']}{RESET}\n")

    print(f"{BOLD}{YELLOW}Comparative Analysis:{RESET}")
    print(exp["analysis"]["summary"])


def main():
    client = LLMClient()
    
    while True:
        status = f"{GREEN}Live ({client.provider.upper()}){RESET}" if client.is_live_ready() else f"{YELLOW}Demo Simulation Mode{RESET}"
        print_header(f"🤖 AI Content Creation & Analysis System [{status}]")
        print("  1. ✍️ Content Generation (Story, Poem, Social Post)")
        print("  2. 🎙️ Podcast Planning (Title, Guest, 8 Questions)")
        print("  3. 📊 Text Analysis (Sentiment & Keywords)")
        print("  4. 🧪 Parameter Experimentation (Temp 0.2 vs 0.9)")
        print("  5. ⚙️ Toggle Provider / API Key")
        print("  6. ❌ Exit")

        choice = input(f"\n{BOLD}Select an option (1-6):{RESET} ").strip()
        if choice == "1":
            menu_content(client)
        elif choice == "2":
            menu_podcast(client)
        elif choice == "3":
            menu_text_analysis(client)
        elif choice == "4":
            menu_parameter_experiment(client)
        elif choice == "5":
            print("\nProvider options: 1. OpenAI  2. Anthropic  3. Force Simulation Mode")
            p = input("Choose (1-3): ").strip()
            if p == "1":
                key = input("Enter OpenAI API Key: ").strip()
                client = LLMClient(provider="openai", api_key=key, force_simulation=False)
            elif p == "2":
                key = input("Enter Anthropic API Key: ").strip()
                client = LLMClient(provider="anthropic", api_key=key, force_simulation=False)
            elif p == "3":
                client = LLMClient(force_simulation=True)
            print(f"{GREEN}Provider updated.{RESET}")
        elif choice == "6":
            print(f"\n{CYAN}Thank you for using AI Content Creation & Analysis System!{RESET}\n")
            sys.exit(0)
        else:
            print(f"{YELLOW}Invalid choice. Please select 1-6.{RESET}")


if __name__ == "__main__":
    main()
