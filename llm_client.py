"""
Multi-Provider LLM Client with Seamless Offline Simulation
============================================================
Supports:
- OpenAI API (chat completions & modern responses API)
- Anthropic Claude API (messages API)
- Built-in Simulation Mode (guarantees full app testability even without API keys)
"""

import os
import time
import random
import re
from typing import Dict, Any, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        force_simulation: bool = False
    ):
        self.provider = provider.lower()
        self.force_simulation = force_simulation
        
        # Load API key from parameter or environment
        if self.provider == "anthropic":
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
            self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        else: # default openai
            self.provider = "openai"
            self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
            default_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            # If the user previously had a mock or invalid model like gpt-5.6-luna in .env, default safely
            if "gpt-5.6" in default_model:
                default_model = "gpt-4o-mini"
            self.model = model or default_model

        self.openai_client = None
        self.anthropic_client = None

        if not self.force_simulation and self.api_key:
            self._init_clients()

    def _init_clients(self):
        """Initialize provider clients safely."""
        if self.provider == "openai" and self.api_key:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize OpenAI client: {e}")
                self.openai_client = None

        elif self.provider == "anthropic" and self.api_key:
            try:
                import anthropic
                self.anthropic_client = anthropic.Anthropic(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Anthropic client: {e}")
                self.anthropic_client = None

    def is_live_ready(self) -> bool:
        """Check if an active API client is ready to make live calls."""
        if self.force_simulation:
            return False
        if self.provider == "openai":
            return bool(self.openai_client and self.api_key)
        elif self.provider == "anthropic":
            return bool(self.anthropic_client and self.api_key)
        return False

    def call(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 1500,
        request_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Execute LLM completion with automatic fallback and latency tracking.
        Returns a dict:
        {
            "content": str,
            "provider": str,
            "model": str,
            "is_simulation": bool,
            "latency": float,
            "tokens": int,
            "error": Optional[str]
        }
        """
        start_time = time.time()

        # If live API is ready, attempt real API call
        if self.is_live_ready():
            try:
                if self.provider == "openai" and self.openai_client:
                    messages = []
                    if system_prompt:
                        messages.append({"role": "system", "content": system_prompt})
                    messages.append({"role": "user", "content": prompt})

                    try:
                        # Standard Chat Completions API
                        response = self.openai_client.chat.completions.create(
                            model=self.model,
                            messages=messages,
                            temperature=temperature,
                            top_p=top_p,
                            max_tokens=max_tokens
                        )
                        content = response.choices[0].message.content or ""
                        tokens = response.usage.total_tokens if response.usage else len(content.split())
                        latency = round(time.time() - start_time, 2)
                        return {
                            "content": content,
                            "provider": "OpenAI",
                            "model": self.model,
                            "is_simulation": False,
                            "latency": latency,
                            "tokens": tokens,
                            "error": None
                        }
                    except Exception as chat_err:
                        # Fallback attempt to Responses API if available
                        if hasattr(self.openai_client, "responses"):
                            resp = self.openai_client.responses.create(
                                model=self.model,
                                input=prompt,
                                instructions=system_prompt or "You are an expert AI assistant.",
                                temperature=temperature,
                                top_p=top_p,
                            )
                            content = getattr(resp, "output_text", str(resp))
                            latency = round(time.time() - start_time, 2)
                            return {
                                "content": content,
                                "provider": "OpenAI (Responses API)",
                                "model": self.model,
                                "is_simulation": False,
                                "latency": latency,
                                "tokens": len(content.split()),
                                "error": None
                            }
                        raise chat_err

                elif self.provider == "anthropic" and self.anthropic_client:
                    messages = [{"role": "user", "content": prompt}]
                    kwargs = {
                        "model": self.model,
                        "messages": messages,
                        "max_tokens": max_tokens,
                        "temperature": min(temperature, 1.0),
                        "top_p": min(top_p, 1.0)
                    }
                    if system_prompt:
                        kwargs["system"] = system_prompt

                    response = self.anthropic_client.messages.create(**kwargs)
                    content = "".join([block.text for block in response.content if hasattr(block, "text")])
                    tokens = response.usage.input_tokens + response.usage.output_tokens
                    latency = round(time.time() - start_time, 2)
                    return {
                        "content": content,
                        "provider": "Anthropic",
                        "model": self.model,
                        "is_simulation": False,
                        "latency": latency,
                        "tokens": tokens,
                        "error": None
                    }

            except Exception as api_err:
                # If API call fails (e.g. invalid key, quota, model not found), log and fallback smoothly
                err_msg = str(api_err)
                print(f"API Call Failed ({err_msg}). Falling back to Simulation Engine.")
                simulated_content = self._generate_simulation(prompt, system_prompt, temperature, request_type)
                latency = round(time.time() - start_time, 2)
                return {
                    "content": simulated_content,
                    "provider": "Simulation Engine (Fallback)",
                    "model": f"{self.model} (Simulated)",
                    "is_simulation": True,
                    "latency": latency,
                    "tokens": len(simulated_content.split()),
                    "error": f"Live API Notice: {err_msg[:120]}... Generated using intelligent simulation."
                }

        # Otherwise: Run Simulation Mode directly
        time.sleep(0.4) # realistic micro-delay
        simulated_content = self._generate_simulation(prompt, system_prompt, temperature, request_type)
        latency = round(time.time() - start_time, 2)
        return {
            "content": simulated_content,
            "provider": "Simulation Engine (No API Key Required)",
            "model": "Deterministic Neural Mock",
            "is_simulation": True,
            "latency": latency,
            "tokens": len(simulated_content.split()),
            "error": None
        }

    def _generate_simulation(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        request_type: str = "general"
    ) -> str:
        """Generates rich, context-aware synthetic responses tailored to prompt engineering tasks."""
        full_text = f"{system_prompt or ''}\n{prompt}"
        
        # 1. Content Generation: Story
        if "story" in full_text.lower() or request_type == "story":
            topic_match = re.search(r"topic:?\s*['\"]?([^'\"\n]+)['\"]?", full_text, re.IGNORECASE)
            topic = topic_match.group(1).strip() if topic_match else "The Threshold of Tomorrow"
            
            return f"""Title: Echoes Across The Horizon: A Tale of {topic.title()}

Story:
The salt-scented breeze off the marina always smelled like unfinished equations to Dr. Maya Vance. For seventeen years, she had watched the horizon where the open sea merged into perpetual mist, dreaming of a catalyst that could rewrite what humanity thought possible about {topic}. Today, nestled inside her copper-lined workshop, the prototype finally gave its first steady resonance.

It was not a dramatic explosion or a blinding flash of violet light. Rather, it sounded like a glass harmonica struck in an empty cathedral—a pure, unyielding hum that settled deep in the marrow of her bones. Outside, the gulls ceased their cries as if listening to the quiet pulse of a new epoch. Maya reached out with steady fingers and adjusted the frequency dial, watching the telemetry monitors cascade with luminous green patterns that confirmed her hypothesis. 

In that fleeting second, she realized that true breakthroughs never conquer the universe with brute force; they merely illuminate the subtle harmonies that were always waiting beneath the noise.

Takeaway / Moral:
True innovation rarely arrives with fanfare; it reveals itself when patience and curiosity align with the quiet laws of nature."""

        # 2. Content Generation: Poem
        elif "poem" in full_text.lower() or request_type == "poem":
            topic_match = re.search(r"theme:?\s*['\"]?([^'\"\n]+)['\"]?", full_text, re.IGNORECASE) or \
                          re.search(r"topic:?\s*['\"]?([^'\"\n]+)['\"]?", full_text, re.IGNORECASE)
            topic = topic_match.group(1).strip() if topic_match else "The Silent Architecture"
            
            return f"""Title: Cadence of {topic.title()}

Poem:
Silent beneath the vaulted sky,
A lattice spun of light and dust,
Where mortal questions learn to fly,
Beyond the boundaries of our trust.

We carved our names on stone and reed,
To measure time against the stars,
Yet every dream and urgent need,
Dissolves the cage of antique bars.

The future breathes through open gates,
Not forged in fear, but shaped in grace;
For every soul that watches, waits,
To find its compass in this space.

Poetic Analysis:
This poem utilizes metaphors of celestial architecture and temporal dissolution to highlight how human ambition transforms when confronting {topic.title()}."""

        # 3. Content Generation: Social Media Post
        elif "social" in full_text.lower() or request_type == "social":
            topic_match = re.search(r"about:?\s*['\"]?([^'\"\n]+)['\"]?", full_text, re.IGNORECASE)
            topic = topic_match.group(1).strip() if topic_match else "Innovation in Tech"
            
            return f"""Hook:
Most people completely misunderstand {topic.title()}—and that blind spot will cost them dearly over the next 18 months.

Body:
Here is what the industry consensus is ignoring:

1. Complexity isn't an advantage: The systems winning right now prioritize velocity and clarity over bloated architecture.
2. The human interface is the multiplier: Algorithms optimize inputs, but judgment and strategic taste direct the vector.
3. Speed without directional conviction is just expensive motion.

When you peel back the hype around {topic}, the real leverage belongs to operators who build modular, resilient workflows.

Call to Action:
What is the single biggest misconception you are seeing in your field regarding {topic}? Let's unpack it in the comments below.

Hashtags:
#{topic.replace(' ', '')} #Innovation #FutureOfWork #Leadership #Strategy"""

        # 4. Podcast Planning
        elif "podcast" in full_text.lower() or request_type == "podcast":
            topic_match = re.search(r"centered around:?\s*['\"]?([^'\"\n]+)['\"]?", full_text, re.IGNORECASE) or \
                          re.search(r"topic is\s*['\"]?([^'\"\n]+)['\"]?", full_text, re.IGNORECASE)
            topic = topic_match.group(1).strip() if topic_match else "Next-Gen Intelligence"
            
            return f"""{{
  "podcast_title": "Uncharted Signals: Demystifying {topic.title()}",
  "tagline": "Conversations at the frontier of technology, human agency, and systemic change.",
  "description": "In this deep-dive masterclass episode of Uncharted Signals, we dismantle the myths, breakthroughs, and hidden mechanics driving the revolution in {topic}. Over the past two years, shifts in technology and infrastructure have created an inflection point where previous playbooks no longer apply.\\n\\nJoined by a world-class researcher and practitioner, our host explores the operational blueprints, real-world case studies, and contrarian perspectives that separate tactical noise from generational transformation. Listeners will gain an unfiltered look into the technological hurdles that rarely make headline coverage.\\n\\nWhether you are an architect designing the next wave of tooling or a decision-maker navigating complex trade-offs, this episode equips you with the strategic framework required to anticipate the future rather than simply react to it.",
  "guest_profile": {{
    "role_title": "Chief Research Scientist & Systems Strategist",
    "ideal_background": "Former research lead at top tier AI lab, author of seminal papers on distributed cognition, with 12+ years of field deployment experience across global enterprises.",
    "why_ideal": "Brings the rare combination of peer-reviewed mathematical rigor and hands-on commercial architecture battle scars in {topic}."
  }},
  "interview_questions": [
    {{
      "number": 1,
      "stage": "Icebreaker & Backstory",
      "question": "Can you take us back to the exact moment or breakthrough that made you realize everything we assumed about {topic} was about to change?",
      "rationale": "Establishes personal stakes and humanizes the technical journey."
    }},
    {{
      "number": 2,
      "stage": "Icebreaker & Backstory",
      "question": "What was the most naive assumption you held early in your career that reality forced you to dismantle?",
      "rationale": "Fosters intellectual humility and invites authentic storytelling."
    }},
    {{
      "number": 3,
      "stage": "Core Deep-Dive",
      "question": "When you look under the hood of contemporary implementations of {topic}, where is the fragile bottleneck that everyone tends to sweep under the rug?",
      "rationale": "Pushes past marketing claims directly into architectural realities."
    }},
    {{
      "number": 4,
      "stage": "Core Deep-Dive",
      "question": "How do you navigate the trade-off between deterministic reliability and emergent capability when deploying in high-consequence environments?",
      "rationale": "Deconstructs the core engineering tension in production systems."
    }},
    {{
      "number": 5,
      "stage": "Core Deep-Dive",
      "question": "Could you walk us through a recent post-mortem or stress-test failure that taught your team something completely unexpected?",
      "rationale": "Extracts actionable operational insights from real-world adversity."
    }},
    {{
      "number": 6,
      "stage": "Future Vision & Debates",
      "question": "If you had to take a high-conviction bet on a contrarian trend within {topic} that will become consensus in 3 years, what would it be?",
      "rationale": "Draws out forward-leaning hypotheses and sparks debate."
    }},
    {{
      "number": 7,
      "stage": "Future Vision & Debates",
      "question": "How should regulatory bodies and open-source communities balance safety safeguards without throttling fundamental grassroots innovation?",
      "rationale": "Addresses the broader governance and ethical ecosystem."
    }},
    {{
      "number": 8,
      "stage": "Rapid-Fire Takeaway",
      "question": "What is one counter-intuitive principle every engineer and strategist should immediately adopt when building with {topic}?",
      "rationale": "Delivers an actionable, high-retention mental model for the audience."
    }}
  ]
}}"""

        # 5. Text Analysis: Sentiment & Keywords
        elif "sentiment" in full_text.lower() or "keyword" in full_text.lower() or request_type == "analysis":
            # Extract sample text if present
            sample_text = full_text
            pos_words = ["great", "excellent", "love", "fast", "personalized", "breakthrough", "transform", "good", "amazing", "promising", "benefit"]
            neg_words = ["bad", "terrible", "risk", "harm", "slow", "broken", "danger", "flaw", "fail", "costly", "threat", "worst"]
            
            p_score = sum(1 for w in pos_words if w in sample_text.lower())
            n_score = sum(1 for w in neg_words if w in sample_text.lower())
            
            if p_score > n_score:
                sentiment = "Positive"
                polarity = round(0.55 + min(0.4, p_score * 0.15), 2)
                emotions = ["Optimism", "Enthusiasm", "Confidence"]
                explanation = "The text exhibits distinctly constructive and affirmative language, emphasizing efficiency, empowerment, and forward momentum with minimal critical reservation."
            elif n_score > p_score:
                sentiment = "Negative"
                polarity = round(-0.55 - min(0.4, n_score * 0.15), 2)
                emotions = ["Concern", "Skepticism", "Frustration"]
                explanation = "The prose is characterized by cautionary, adversarial, or critical vocabulary, pointing to vulnerabilities, systemic friction, or negative downstream ramifications."
            else:
                sentiment = "Neutral"
                polarity = 0.08
                emotions = ["Objectivity", "Analytical Focus", "Balance"]
                explanation = "The passage maintains an objective, declarative tone, balancing analytical observations without loaded emotional qualifiers or strong polarity markers."

            words = re.findall(r"\b[A-Za-z]{4,}\b", sample_text)
            filtered = [w.lower() for w in words if w.lower() not in {"this", "that", "with", "from", "your", "have", "will", "what", "role", "task", "context", "constraints"}]
            common = list(dict.fromkeys(filtered))[:6]
            if len(common) < 3:
                common += ["intelligence", "efficiency", "architecture", "adaptation"]

            keywords_json = [
                {"keyword": w, "relevance": round(0.95 - (i * 0.08), 2), "category": "Domain Term" if i % 2 == 0 else "Semantic Concept"}
                for i, w in enumerate(common[:5])
            ]

            import json
            return json.dumps({
                "sentiment": sentiment,
                "polarity_score": polarity,
                "confidence": 94,
                "explanation": explanation,
                "keywords": keywords_json,
                "dominant_emotions": emotions,
                "summary": "Synthesized perspective evaluating structural impacts, technical implications, and operational viability."
            }, indent=2)

        # 6. Parameter Experimentation
        elif "experiment" in full_text.lower() or request_type == "experiment":
            topic_match = re.search(r"Topic:?\s*['\"]?([^'\"\n]+)['\"]?", full_text, re.IGNORECASE) or \
                          re.search(r"concept:?\s*['\"]?([^'\"\n]+)['\"]?", full_text, re.IGNORECASE)
            topic = topic_match.group(1).strip() if topic_match else "Artificial Intelligence"

            if temperature < 0.4:
                # Deterministic, concise, direct vocabulary
                return (
                    f"Artificial intelligence and {topic} represent a structured paradigm shift in computation. "
                    f"By processing vast quantities of historical data through calibrated statistical models, "
                    f"systems identify recurring patterns with high precision. In practical industry deployments, "
                    f"this capability accelerates decision-making cycles, reduces operational error margins, and automates "
                    f"repetitive analytical tasks. As these methodologies mature, their primary value lies in deterministic "
                    f"consistency, scalability, and systematic optimization across standard enterprise workflows."
                )
            else:
                # Highly creative, rich vocabulary, lyrical metaphors
                return (
                    f"Beyond the cold silicon matrices and shimmering phosphors of the data center, {topic} unfurls like "
                    f"an uncharted constellation. It is not merely code executing in the dark, but a kaleidoscopic mirror "
                    f"reflecting human imagination back upon itself. Ideas interlock like clockwork gears of crystal and starlight, "
                    f"weaving unforeseen harmonies out of raw entropy. Here at the wild periphery of invention, algorithms don't "
                    f"just solve equations—they dream in recursive reverberations, dissolving the fragile frontier between creator and creation."
                )

        # General Fallback
        return f"Completed structured analysis and generation for input. All constraints respected and formatted systematically."
