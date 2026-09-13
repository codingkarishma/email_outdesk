# Outreach Desk

**Write a personalized B2B cold email in under a minute.**

Outreach Desk is a small AI agent that turns a handful of facts about a
prospect — their name, role, company, and a personalization hook — into a
polished, ready-to-send cold outreach email. It runs as a web app with a
clean writing-desk interface, or as a CLI for scripting into a larger
workflow.

Built with [LangChain](https://www.langchain.com/) and served by
[Groq](https://groq.com/) for fast, cheap inference.

**Live demo:** [outdesk-email-ai.onrender.com](https://outdesk-email-ai.onrender.com/)
*(hosted on Render's free tier — the first request after a period of
inactivity can take 30–50 seconds to wake up.)*

## Why

Cold outreach emails are tedious to write well: they need to sound human,
reference something real about the recipient, and get to the point fast.
Outreach Desk automates the first draft so a salesperson, founder, or
recruiter can spend their time personalizing and sending — not staring at a
blank page.

## Features

- **Web UI** — a distraction-free form on one side, the drafted email on the
  other. Copy the subject, the body, or both with one click.
- **CLI** — generate emails from the command line with flags, an interactive
  prompt, or a JSON file, for scripting into a bulk-outreach pipeline.
- **Structured output** — every response comes back as a clean subject +
  body pair, not a wall of text you have to parse yourself.
- **Bring your own key** — runs on your own Groq API key, so your prompts
  and data never pass through a third party's servers beyond Groq itself.

## Quickstart

```bash
git clone <your-repo-url>
cd email-drafting-agent
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # paste in your Groq API key
uvicorn email_drafting_agent.api:app --reload
```

Open **http://localhost:8000**, fill in the form, and click **Write the
email**.

Get a free Groq API key at [console.groq.com/keys](https://console.groq.com/keys).

## How it works

1. You fill in who you're writing to and why — recipient details, a
   personalization hook, your product, and the ask.
2. The FastAPI backend builds a structured prompt and sends it to Groq
   running `qwen/qwen3.6-27b`, requesting a strict JSON response
   (`{"subject": ..., "email": ...}`).
3. The web UI renders the result as a letter you can copy, edit, or
   regenerate.

```
email_drafting_agent/
  agent.py       # OutreachAgent — builds the prompt, calls the LLM
  api.py         # FastAPI server: POST /generate, GET /health, serves static/
  cli.py         # CLI: flags, --interactive, or --from-json
  models.py      # Groq LLM client configuration
  prompts.py     # the prompt template
  schemas.py     # OutreachRequest / OutreachEmail data models
  tools.py       # extension point for future LangChain tools
  utils.py       # shared helpers
  static/
    index.html   # the web UI
render.yaml       # Render deployment blueprint
```

## Using the CLI

```bash
python -m email_drafting_agent.cli \
  --executive-name "Jordan Lee" \
  --executive-role "VP of Engineering" \
  --company-name "Acme Corp" \
  --company-context "Series B fintech building payment infra" \
  --personalization-hook "Their recent talk on scaling infra" \
  --outreach-objective "Book a 20-minute intro call" \
  --solution-name "Observability platform" \
  --business-value "Cuts incident triage time by 40%" \
  --call-to-action "Open to a call next week?"
```

Or interactively: `python -m email_drafting_agent.cli --interactive`

Or from a JSON file: `python -m email_drafting_agent.cli --from-json request.json`

Once installed (`pip install -e .`), the same CLI is available as
`email-drafting-agent`.

## Configuration

Set these in `.env` (see `.env.example`):

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `GROQ_API_KEY` | yes | — | Your Groq API key |
| `GROQ_MODEL` | no | `qwen/qwen3.6-27b` | Which Groq model to use |
| `GROQ_TEMPERATURE` | no | `0.3` | Creativity of the output |
| `GROQ_MAX_TOKENS` | no | `700` | Output cap, kept under Groq's free-tier rate limit |

## Deploying

The app is a standard FastAPI service and deploys anywhere Python runs. The
included `render.yaml` makes [Render](https://render.com) a one-click option:

1. Push this repo to GitHub.
2. On Render, **New +** → **Web Service**, connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn email_drafting_agent.api:app --host 0.0.0.0 --port $PORT`
5. Add `GROQ_API_KEY` under Environment Variables.
6. Deploy — you'll get a public URL anyone can use.

Never commit your `.env` file; secrets belong in your host's environment
variable settings, not in the repo.

## Roadmap ideas

- Give the agent a research tool to pull a prospect's recent activity
  automatically, instead of requiring a manual personalization hook.
- Batch mode: generate a full sequence (initial email + two follow-ups) from
  one input.
- Save and reuse past drafts.

## License

Add a license of your choice (MIT is a common default for a project like
this) before sharing the repo publicly.