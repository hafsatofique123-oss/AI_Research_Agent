"""
Streamlit front-end for our single-agent CrewAI research assistant.

Run locally with:
    streamlit run app.py
"""

import os

import streamlit as st
from dotenv import load_dotenv

from agent import GROQ_MODEL, build_research_crew

# Load GROQ_API_KEY from a local .env file if one exists (for local development).
load_dotenv()

# On Streamlit Community Cloud, secrets are provided through st.secrets instead
# of a .env file. If a key is set there, copy it into the environment so the
# rest of the app (and CrewAI/LiteLLM) can find it the same way either way.
try:
    if st.secrets.get("GROQ_API_KEY"):
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    # No secrets.toml file present (e.g. first run locally) - that's fine.
    pass


st.set_page_config(page_title="AI Research Agent", page_icon="🔎", layout="centered")

st.title("🔎 AI Research Agent")
st.caption(f"CrewAI single agent · Groq ({GROQ_MODEL}) · Free DuckDuckGo search")

# ---------------------------------------------------------------------------
# Sidebar: API key
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Settings")

    key_from_env = os.environ.get("GROQ_API_KEY", "")
    api_key_input = st.text_input(
        "Groq API key",
        type="password",
        value=key_from_env,
        help="Get a free key at console.groq.com/keys",
    )
    if api_key_input:
        os.environ["GROQ_API_KEY"] = api_key_input

    st.markdown("[Get a free Groq API key](https://console.groq.com/keys)")
    st.divider()
    st.markdown(
        "This app uses a single CrewAI agent that:\n"
        "1. Searches the web with DuckDuckGo (free, no key needed)\n"
        "2. Writes up a Markdown report using a Groq-hosted model"
    )

# ---------------------------------------------------------------------------
# Main input
# ---------------------------------------------------------------------------
topic = st.text_input(
    "Research topic",
    placeholder="e.g. The impact of AI on the job market",
)

run_clicked = st.button("Run Research", type="primary")

if run_clicked:
    if not os.environ.get("GROQ_API_KEY"):
        st.error("Please add your Groq API key in the sidebar first.")
    elif not topic.strip():
        st.warning("Please enter a topic to research.")
    else:
        with st.spinner("Researching... this can take a minute or two."):
            try:
                crew = build_research_crew(topic)
                result = crew.kickoff(inputs={"topic": topic})
                st.session_state["report"] = str(result)
                st.session_state["report_topic"] = topic
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ---------------------------------------------------------------------------
# Show the report, if we have one
# ---------------------------------------------------------------------------
if "report" in st.session_state:
    st.divider()
    st.subheader(f"Report: {st.session_state.get('report_topic', '')}")
    st.markdown(st.session_state["report"])
    st.download_button(
        "Download report as Markdown",
        data=st.session_state["report"],
        file_name="research_report.md",
        mime="text/markdown",
    )
