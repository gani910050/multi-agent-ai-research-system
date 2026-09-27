# 🔎 Multi-Agent Research System

A multi-agent research pipeline built with **LangChain**, **Google Gemini**, and **Tavily**, wrapped in a **Streamlit** UI. Given a topic, it searches the web, scrapes the most relevant source, writes a structured report, and critiques its own output.

## How It Works

The pipeline runs four stages in sequence (`pipeline.py`):

1. **Search Agent** — uses the `web_search` tool (Tavily) to find recent, reliable information on the topic.
2. **Reader Agent** — uses the `scrape_url` tool to pick the most relevant URL from the search results and scrape its content.
3. **Writer Chain** — a Gemini-powered prompt chain that drafts a structured report (Introduction, Key Findings, Conclusion, Sources).
4. **Critic Chain** — a second Gemini-powered prompt chain that scores the report out of 10 and lists strengths and areas to improve.

All agents run on `ChatGoogleGenerativeAI` (Gemini) via `langchain-google-genai`, and the search/reader agents are built with LangChain's `create_agent`.

## Project Structure

```
.
├── app.py              # Streamlit UI
├── pipeline.py          # Orchestrates the 4-step research pipeline
├── agents.py            # LLM setup, agent builders, writer/critic chains
├── tools.py             # web_search (Tavily) and scrape_url (BeautifulSoup) tools
└── requirements.txt      # Python dependencies
```

## Setup

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd <your-repo-folder>
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file with your API keys:

```
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

> **Note:** `agents.py` currently loads the `.env` file from a `.venv/.env` path. Either place your `.env` there, or update the `env_path` in `agents.py` to point to your project root (recommended for portability).

### 3. Run the app

```bash
streamlit run app.py
```

Open the local URL Streamlit prints (usually `http://localhost:8501`), enter a research topic, and click **Start Research**.

## Requirements

- Python 3.10+
- A [Google AI Studio](https://aistudio.google.com/) API key (Gemini)
- A [Tavily](https://tavily.com/) API key (web search)

See `requirements.txt` for the full dependency list.

## Notes & Known Limitations

- **Rate limits:** the pipeline catches Gemini `429 / RESOURCE_EXHAUSTED` errors from the free tier and returns gracefully instead of crashing.
- **Scraping:** `scrape_url` truncates page content to 3,000 characters and strips scripts/styles/nav/footer before returning text.
- **`.env` path:** `tools.py` loads `.env` from the current working directory, while `agents.py` loads it from `.venv/.env` — keep these consistent to avoid missing API keys.
- `tools.py` includes top-level test calls (`web_search.invoke(...)`, `scrape_url.invoke(...)`) that run on import — consider removing or guarding these with `if __name__ == "__main__":` before deploying.
