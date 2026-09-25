"""
This file defines our single-agent research crew:
- one Agent (a "Research Analyst")
- one Task (write a report on a topic)
- one Crew that runs that task

The agent "thinks" using a Groq-hosted model, and can search the web
with the DuckDuckGo tool defined in search_tool.py.
"""

import os

from crewai import Agent, Crew, Process, Task
from crewai.llm import LLM

from search_tool import duckduckgo_search

# The Groq model requested for this project.
# CrewAI routes non-OpenAI models through LiteLLM, so Groq models
# need the "groq/" prefix in front of the model name.
GROQ_MODEL = "groq/openai/gpt-oss-120b"


def build_research_crew(topic: str) -> Crew:
    """Builds (but does not run) a single-agent Crew that researches `topic`."""

    llm = LLM(
        model=GROQ_MODEL,
        api_key=os.environ.get("GROQ_API_KEY"),
        temperature=0.4,
    )

    researcher = Agent(
        role="Senior Research Analyst",
        goal=(
            f"Research the topic '{topic}' using web search, and produce an accurate, "
            "clearly written, well-organized report."
        ),
        backstory=(
            "You are a meticulous research analyst. You are excellent at using web "
            "search to gather current, factual information, cross-checking claims "
            "across multiple sources, and turning your findings into a report that "
            "a busy reader can quickly understand."
        ),
        tools=[duckduckgo_search],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    research_task = Task(
        description=(
            f"Research the topic: '{topic}'.\n\n"
            "Steps to follow:\n"
            "1. Use the DuckDuckGo Search tool at least 2-3 times with different, "
            "specific search queries to gather current and relevant information.\n"
            "2. Cross-check important facts against more than one search result "
            "where possible.\n"
            "3. Write a clear, well-structured report in Markdown containing:\n"
            "   - A short introduction to the topic\n"
            "   - 3-5 sections with headings covering the key findings\n"
            "   - A brief conclusion / summary\n\n"
            "Only include information you found through search. If something is "
            "uncertain or sources disagree, say so plainly instead of guessing."
        ),
        expected_output=(
            "A well-structured Markdown report, roughly 400-700 words, with a title, "
            "an introduction, a few clearly headed sections, and a short conclusion."
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
