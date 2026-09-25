```python
"""
AI Research Agent

This file defines:
- One Research Analyst agent
- One research task
- One Crew

The agent uses Groq's GPT-OSS 120B model and
a DuckDuckGo-based web search tool.
"""

import os

from crewai import Agent, Crew, Process, Task
from crewai.llm import LLM

from search_tool import duckduckgo_search


# Current Groq model
GROQ_MODEL = "groq/openai/gpt-oss-120b"


def build_research_crew(topic: str) -> Crew:
    """Build the research crew for the given topic."""

    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. Please add your Groq API key "
            "in Streamlit Secrets."
        )

    llm = LLM(
        model=GROQ_MODEL,
        api_key=api_key,
        temperature=0.4,
    )

    researcher = Agent(
        role="Senior Research Analyst",
        goal=(
            f"Research the topic '{topic}' using web search and produce "
            "an accurate, clearly written and well-organized report."
        ),
        backstory=(
            "You are a careful research analyst who searches the web, "
            "checks information from multiple sources and creates "
            "clear research reports."
        ),
        tools=[duckduckgo_search],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    research_task = Task(
        description=(
            f"Research the following topic: '{topic}'.\n\n"

            "Follow these steps:\n"
            "1. Use the web search tool multiple times with different "
            "specific search queries.\n"
            "2. Gather current and relevant information.\n"
            "3. Cross-check important facts when possible.\n"
            "4. Do not invent information.\n"
            "5. If sources disagree or information is uncertain, "
            "clearly mention the uncertainty.\n\n"

            "Write the final report in Markdown with:\n"
            "- A clear title\n"
            "- A short introduction\n"
            "- 3-5 sections with headings\n"
            "- Important findings\n"
            "- A short conclusion\n"
            "- Sources or URLs used during research"
        ),
        expected_output=(
            "A clear and well-structured Markdown research report "
            "of approximately 400-700 words."
        ),
        agent=researcher,
    )

    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True,
    )

    return crew
```

