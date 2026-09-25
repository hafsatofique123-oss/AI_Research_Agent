```python
"""
Web search tool for the AI Research Agent.

Uses the current DDGS package to search the web.
"""

from crewai.tools import tool
from ddgs import DDGS


@tool("DuckDuckGo Web Search")
def duckduckgo_search(query: str) -> str:
    """
    Search the web using DDGS and return useful results.

    Args:
        query: A specific web search query.

    Returns:
        A formatted list of search results.
    """

    if not query or not query.strip():
        return "Please provide a search query."

    try:
        results = DDGS().text(
            query.strip(),
            max_results=5,
        )

        if not results:
            return "No search results were found."

        formatted_results = []

        for index, result in enumerate(results, start=1):
            title = result.get("title", "No title")
            url = result.get("href", "")
            body = result.get("body", "")

            formatted_results.append(
                f"{index}. {title}\n"
                f"URL: {url}\n"
                f"Summary: {body}"
            )

        return "\n\n".join(formatted_results)

    except Exception as error:
        return f"Web search failed: {error}"
```
