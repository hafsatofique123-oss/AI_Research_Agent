# 🔎 AI Research Agent (CrewAI + Groq + Streamlit)

A beginner-friendly single-agent research app:

- **CrewAI** runs one agent ("Senior Research Analyst")
- The agent searches the web for free using **DuckDuckGo** (`ddgs` package, no API key)
- The agent thinks/writes using **Groq**'s `openai/gpt-oss-120b` model
- **Streamlit** provides the web UI
- You give it a topic → it researches → it writes you a Markdown report

## Project structure

```
ai-research-agent/
├── app.py                        # Streamlit UI (the entry point)
├── agent.py                      # Defines the CrewAI Agent, Task, Crew
├── search_tool.py                # Free DuckDuckGo search tool for the agent
├── requirements.txt              # Python dependencies
├── .env.example                  # Template for your local API key
├── .streamlit/
│   └── secrets.toml.example      # Template for Streamlit Cloud secrets
├── .gitignore
└── README.md
```

---

## 1. Get a free Groq API key

1. Go to https://console.groq.com/keys
2. Sign up / log in (it's free)
3. Click "Create API Key" and copy it somewhere safe

---

## 2. Run it on your computer first

**Requirements:** Python **3.10, 3.11, or 3.12** (CrewAI does not yet support 3.13/3.14 — check your version with `python --version`).

```bash
# 1. Clone or download this folder, then move into it
cd ai-research-agent

# 2. Create a virtual environment (keeps this project's packages isolated)
python -m venv venv

# 3. Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# 4. Install the dependencies
pip install -r requirements.txt

# 5. Add your Groq API key
cp .env.example .env
# now open .env in a text editor and paste your real key after GROQ_API_KEY=

# 6. Run the app
streamlit run app.py
```

Your browser should open automatically at `http://localhost:8501`. Type a topic and click **Run Research**.

> Tip: if you forget to add the key to `.env`, you can also just paste it into the "Groq API key" box in the app's sidebar — it works either way.

---

## 3. Upload the project to GitHub

1. Create a free account at https://github.com if you don't have one.
2. Click the **+** icon (top right) → **New repository**.
   - Name it something like `ai-research-agent`
   - Keep it **Public** (Streamlit Community Cloud's free tier needs this, unless you connect a paid/private plan)
   - Don't add a README/gitignore from GitHub's UI, since we already have them
3. On your computer, inside the project folder, run:

```bash
git init
git add .
git commit -m "Initial commit: AI research agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-research-agent.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

Because `.env` is listed in `.gitignore`, your real API key will **not** be uploaded — only `.env.example` will. That's exactly what you want.

---

## 4. Deploy on Streamlit Community Cloud

1. Go to https://share.streamlit.io and sign in with your GitHub account.
2. Click **Create app** → **From an existing repo**.
3. Pick your `ai-research-agent` repository, branch `main`, and main file path `app.py`.
4. Click **Advanced settings**:
   - Set the **Python version** to **3.11** (important — CrewAI doesn't support Python 3.13/3.14).
   - Under **Secrets**, paste:
     ```toml
     GROQ_API_KEY = "your_real_groq_api_key_here"
     ```
5. Click **Deploy**.

The first build can take a few minutes since CrewAI pulls in a fair number of dependencies — that's normal. Once it's done, you'll get a public URL you can share.

---

## How it works, in plain terms

- `search_tool.py` wraps the free `ddgs` (DuckDuckGo Search) library as a CrewAI **tool** — basically a function the agent is allowed to call.
- `agent.py` creates:
  - an **Agent** (role, goal, backstory, which tools it can use, which LLM it thinks with)
  - a **Task** (what to do, and what the output should look like)
  - a **Crew** (ties the agent + task together and runs them)
- `app.py` is just a normal Streamlit script: it takes your topic, calls `crew.kickoff(...)`, and displays whatever Markdown report comes back.

## Customizing

- **Change the model**: edit `GROQ_MODEL` in `agent.py`. Any Groq model works as long as you keep the `groq/` prefix, e.g. `groq/llama-3.3-70b-versatile`.
- **Change how deep it searches**: edit `max_results` in `search_tool.py`, or the instructions in the `Task` description in `agent.py`.
- **Change report length/style**: edit the `description` and `expected_output` of the `Task` in `agent.py`.

## Troubleshooting

| Problem | Likely fix |
|---|---|
| `ModuleNotFoundError` locally | Make sure your virtual environment is activated, then re-run `pip install -r requirements.txt`. |
| "Please add your Groq API key" | Add it in `.env` (local) or Streamlit's Secrets box (cloud), or paste it into the sidebar. |
| App works locally but fails to deploy | Double-check you set Python 3.11 in "Advanced settings" when deploying. |
| Search tool returns "No results found" | DuckDuckGo occasionally rate-limits; try again in a moment, or rerun with a shorter topic. |
| Build is slow on Streamlit Cloud | Normal for CrewAI's first install — it has several dependencies. Subsequent redeploys are faster. |
