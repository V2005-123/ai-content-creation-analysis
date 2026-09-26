"""
Structured Prompt Engineering Module
=====================================
Defines the core PromptTemplate dataclass based on the 5 pillars of prompt engineering:
1. ROLE: System persona & domain identity
2. CONTEXT: Background information and situation
3. TASK: Explicit objective and deliverable
4. CONSTRAINTS: Negative boundaries, tone, length, and style limits
5. OUTPUT FORMAT: Precise schema (Markdown or JSON)
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any


@dataclass
class PromptTemplate:
    role: str
    context: str
    task: str
    constraints: List[str] = field(default_factory=list)
    output_format: str = ""

    def render(self) -> str:
        """Render the complete structured prompt as a single formatted string."""
        constraints_str = "\n".join(f"- {c}" for c in self.constraints)
        return (
            f"ROLE:\n{self.role.strip()}\n\n"
            f"CONTEXT:\n{self.context.strip()}\n\n"
            f"TASK:\n{self.task.strip()}\n\n"
            f"CONSTRAINTS:\n{constraints_str.strip()}\n\n"
            f"OUTPUT FORMAT:\n{self.output_format.strip()}"
        )

    def as_system_and_user(self) -> Tuple[str, str]:
        """Split into System Prompt (Role) and User Prompt (Context, Task, Constraints, Format)."""
        system_content = f"You are an AI assistant acting in the following capacity:\n{self.role.strip()}"
        constraints_str = "\n".join(f"- {c}" for c in self.constraints)
        user_content = (
            f"CONTEXT:\n{self.context.strip()}\n\n"
            f"TASK:\n{self.task.strip()}\n\n"
            f"CONSTRAINTS:\n{constraints_str.strip()}\n\n"
            f"OUTPUT FORMAT:\n{self.output_format.strip()}"
        )
        return system_content, user_content

    def to_dict(self) -> Dict[str, Any]:
        """Export as dictionary for UI inspection."""
        return {
            "Role": self.role,
            "Context": self.context,
            "Task": self.task,
            "Constraints": self.constraints,
            "Output Format": self.output_format,
        }


def content_prompt(
    topic: str,
    content_type: str = "Story",
    tone: str = "Engaging",
    target_audience: str = "General audience",
    word_count: int = 250
) -> PromptTemplate:
    """Generate a structured prompt for creative content generation."""
    type_lower = content_type.lower()
    
    if "story" in type_lower:
        role = "You are an award-winning creative fiction writer and master narrative storyteller."
        task = f"Write a captivating short story revolving around the topic: '{topic}'."
        constraints = [
            f"Target length: approximately {word_count} words.",
            f"Tone: {tone.lower()}, with immersive narrative momentum.",
            f"Target audience: {target_audience}.",
            "Introduce a memorable protagonist and a compelling central conflict or revelation.",
            "Use evocative sensory details; avoid clichés or passive narration.",
        ]
        output_format = """Title: <Engaging, Evocative Story Title>

Story:
<The narrative text with smooth paragraph breaks>

Takeaway / Moral:
<One sentence resonance or reflection>"""

    elif "poem" in type_lower:
        role = "You are an accomplished contemporary poet with a keen sense of imagery, rhythm, and lyrical cadence."
        task = f"Compose a poignant, evocative poem exploring the theme: '{topic}'."
        constraints = [
            f"Tone: {tone.lower()}.",
            f"Target audience: {target_audience}.",
            "Structure: 3 to 5 stanzas with deliberate rhythm and resonant imagery.",
            "Use vivid metaphors and sensory language; avoid trite or forced end-rhymes.",
        ]
        output_format = """Title: <Poem Title>

Poem:
<Stanzas separated by line breaks>

Poetic Analysis:
<A brief 2-sentence note on the thematic symbolism>"""

    elif "social" in type_lower:
        role = "You are a top-tier social media strategist and viral copywriter known for high engagement and conversions."
        task = f"Craft an impactful, high-converting social media post about: '{topic}'."
        constraints = [
            f"Tone: {tone.lower()}.",
            f"Target audience: {target_audience}.",
            "Include a magnetic first-line hook that stops scrolling.",
            "Use punchy spacing, bullet points or listicles for readability.",
            "Include a compelling Call-To-Action (CTA) encouraging replies.",
            "Add 3 to 5 highly relevant, non-spammy hashtags.",
        ]
        output_format = """Hook:
<Magnetic opening sentence>

Body:
<Value-packed post content formatted with clean spacing>

Call to Action:
<Engaging closing question or instruction>

Hashtags:
#tag1 #tag2 #tag3 #tag4"""

    else:
        role = "You are a versatile expert content writer and communications specialist."
        task = f"Create a compelling piece of content on '{topic}' formatted as a {content_type}."
        constraints = [
            f"Tone: {tone.lower()}.",
            f"Target audience: {target_audience}.",
            f"Approximate length: {word_count} words.",
            "Maintain exceptional originality and clarity.",
        ]
        output_format = """Title: <Appropriate Title>

Content:
<Structured content>"""

    return PromptTemplate(
        role=role,
        context=f"The content is intended for {target_audience} interested in '{topic}'. The requested format is a {content_type}.",
        task=task,
        constraints=constraints,
        output_format=output_format
    )


def podcast_prompt(
    topic: str,
    host_style: str = "Conversational & In-Depth",
    target_audience: str = "Industry professionals and curious learners",
    num_questions: int = 8
) -> PromptTemplate:
    """Generate a structured prompt for a comprehensive podcast planning session."""
    return PromptTemplate(
        role="You are a veteran podcast executive producer and elite broadcast interviewer with experience producing top-charting talk shows.",
        context=f"The production team is planning a feature episode centered around: '{topic}'. The host style is {host_style} and the target listener demographic is {target_audience}.",
        task=f"Produce a comprehensive podcast episode production plan including title, episode description, ideal guest profile, and exactly {num_questions} structured interview questions.",
        constraints=[
            "Episode description must be 2 to 3 substantive paragraphs suitable for show notes and podcast directory listings.",
            "Guest profile must specify exact domain credentials, background, and why they are the perfect fit.",
            f"Formulate exactly {num_questions} interview questions that progress logically:",
            "  - Q1-Q2: Icebreaker & Backstory (origin journey, personal motivation)",
            "  - Q3-Q5: Technical Deep-Dive & Practical Realities (core breakthroughs, hard challenges)",
            "  - Q6-Q7: Industry Debates & Future Vision (counter-intuitive views, predictions)",
            "  - Q8: Rapid-Fire Key Takeaway (actionable advice for listeners)",
            "Avoid superficial or generic yes/no questions; every question must provoke deep narrative insights.",
            "Return valid JSON matching the exact schema specified below."
        ],
        output_format="""{
  "podcast_title": "Catchy & Professional Episode Title",
  "tagline": "A crisp one-sentence episode subtitle",
  "description": "2-3 comprehensive paragraphs outlining episode themes, stakes, and listener value.",
  "guest_profile": {
    "role_title": "Specific professional title",
    "ideal_background": "Relevant pedigree, accomplishments, and domain authority",
    "why_ideal": "Why this guest provides unique perspectives for this episode"
  },
  "interview_questions": [
    {
      "number": 1,
      "stage": "Icebreaker & Backstory",
      "question": "Engaging opening question...",
      "rationale": "Why this opens the conversation effectively"
    },
    {
      "number": 2,
      "stage": "Icebreaker & Backstory",
      "question": "Follow-up question on motivation or pivotal moment...",
      "rationale": "Explores foundational journey"
    },
    {
      "number": 3,
      "stage": "Core Deep-Dive",
      "question": "Substantive question on the primary topic...",
      "rationale": "Unpacks mechanics or technical reality"
    },
    {
      "number": 4,
      "stage": "Core Deep-Dive",
      "question": "Question on complex challenges or common misconceptions...",
      "rationale": "Dissects common pitfalls"
    },
    {
      "number": 5,
      "stage": "Core Deep-Dive",
      "question": "Question on implementation, methodology, or evidence...",
      "rationale": "Provides tangible takeaways"
    },
    {
      "number": 6,
      "stage": "Future Vision & Debates",
      "question": "Question on upcoming shifts, controversies, or ethical questions...",
      "rationale": "Explores forward-looking landscape"
    },
    {
      "number": 7,
      "stage": "Future Vision & Debates",
      "question": "Question challenging the consensus view...",
      "rationale": "Elicits contrarian wisdom"
    },
    {
      "number": 8,
      "stage": "Rapid-Fire Takeaway",
      "question": "Closing question for an actionable rule of thumb for the audience...",
      "rationale": "Leaves a memorable concluding insight"
    }
  ]
}"""
    )


def text_analysis_prompt(text: str) -> PromptTemplate:
    """Generate a structured prompt for combined sentiment analysis and keyword extraction."""
    return PromptTemplate(
        role="You are a senior computational linguist and Natural Language Processing (NLP) analyst.",
        context=f"Analyze the following user-submitted text for emotional tone, sentiment polarity, and salient semantic keywords:\n\"\"\"\n{text}\n\"\"\"",
        task="Perform an exhaustive sentiment analysis and extract the top keywords/keyphrases from the input text.",
        constraints=[
            "Sentiment classification must be strictly one of: 'Positive', 'Negative', or 'Neutral'.",
            "Provide a polarity score between -1.0 (extremely negative) and +1.0 (extremely positive), with 0.0 being neutral.",
            "Provide a confidence percentage between 0 and 100.",
            "Write a clear, nuanced 2-3 sentence explanation justifying the sentiment classification based on linguistic cues, tone, and qualifiers.",
            "Extract 5 to 8 of the most critical keywords or key phrases, ranked by relevance.",
            "Assign each keyword a relevance weight (0.0 to 1.0) and a category (e.g. Technology, Emotion, Business, Concept).",
            "Do not hallucinate facts not present or implied in the text.",
            "Return valid JSON matching the exact schema specified below."
        ],
        output_format="""{
  "sentiment": "Positive | Negative | Neutral",
  "polarity_score": 0.85,
  "confidence": 95,
  "explanation": "Detailed explanation of linguistic markers, emotional undertones, and semantic balance...",
  "keywords": [
    {"keyword": "sample term", "relevance": 0.95, "category": "Concept"},
    {"keyword": "another term", "relevance": 0.88, "category": "Domain"}
  ],
  "dominant_emotions": ["Optimism", "Determination"],
  "summary": "One sentence summary of the core thesis of the text."
}"""
    )


def experiment_prompt(topic: str, word_count: int = 100) -> PromptTemplate:
    """Generate a structured prompt for temperature and generation parameter experimentation."""
    return PromptTemplate(
        role="You are an imaginative AI author and creative prose stylist.",
        context=f"The user wants an illustrative narrative paragraph exploring the concept: '{topic}'.",
        task="Compose a vivid, compelling paragraph on the specified topic.",
        constraints=[
            f"Length: strictly around {word_count} words (one cohesive paragraph).",
            "Focus on creative imagery, cadence, and thematic clarity.",
            "Do not include bullet points, lists, or headers.",
            "Return ONLY the paragraph itself with no introductory or meta comments."
        ],
        output_format="""<Single vivid paragraph of approximately 100 words>"""
    )
