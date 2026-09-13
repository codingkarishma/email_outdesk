# Outreach Desk

A small LangChain + Groq agent that drafts personalized B2B cold outreach
emails, with a CLI and a web UI ("Outreach Desk") anyone can use in the
browser.

## What was fixed from the original draft

The uploaded project didn't run. In order of how badly they broke it:

1. **`agent.py` had a syntax error.** A missing comma after
   `request.solution_name` meant the file couldn't even be imported.
2. **The prompt variables didn't match.** `agent.py` passed keys like
   `"name"` and `"role"`, but the prompt template in `prompts.py` expected
   `executive_name`, `executive_role`, etc. Every field would have come out
   blank. The template also referenced a `{goal}` variable nothing ever
   supplied. Both are now aligned.
3. **The Groq model id was invalid.** `"qwen3.6-27b"` isn't a real model id —
   Groq namespaces models by provider, so it's `"qwen/qwen3.6-27b"`. Every
   request would have 404'd. It's also now overridable via `GROQ_MODEL` so a
   future rename doesn't require a code change.
4. **There was no working entry point.** `main.py` just imported
   `create_agent` and did nothing with it; `__init__.py`'s `main()` only
   printed a placeholder string. There's now a real CLI (`cli.py`) and a web
   server (`api.py`).
5. **`tools.py` and `utils.py` were empty files.** `utils.py` now has small
   shared helpers; `tools.py` documents how to add LangChain tools later
   (the agent doesn't currently need any).
6. **Groq's JSON mode was failing (`json_validate_failed`).** `qwen/qwen3.6-27b`
   is a reasoning model that generates internal "thinking" tokens before its
   answer, and those were consuming the token budget and/or leaking into the
   output, breaking JSON validation. Fixed with `reasoning_format="hidden"`
   and `reasoning_effort="none"` in `models.py`.
7. **Free-tier rate limit (429).** Groq's free tier caps output at 1000
   tokens/minute. Added `max_tokens=700` (configurable via `GROQ_MAX_TOKENS`)
   so requests stay safely under that.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then paste in your Groq API key
```

Get a free Groq API key at https://console.groq.com/keys.

## Run the web app (recommended)

```bash
uvicorn email_drafting_agent.api:app --reload
```

Open http://localhost:8000 — fill in the form, click **Write the email**.
The browser talks to your own server, which holds the API key; the key
never touches the browser.

## Run the CLI

Flags:

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

Interactive prompts:

```bash
python -m email_drafting_agent.cli --interactive
```

From a JSON file matching `OutreachRequest`'s fields:

```bash
python -m email_drafting_agent.cli --from-json request.json
```

Or, once installed (`pip install -e .`), the `email-drafting-agent` console
script runs the same CLI.

## Project layout

```
email_drafting_agent/
  agent.py       # OutreachAgent: builds the prompt, calls the LLM
  api.py         # FastAPI server: POST /generate, GET /health, serves static/
  cli.py         # argparse-based CLI (flags, --interactive, --from-json)
  models.py      # Groq LLM client (model id, temperature, API key check)
  prompts.py     # the ChatPromptTemplate
  schemas.py     # OutreachRequest / OutreachEmail pydantic models
  tools.py       # extension point for LangChain tools (currently unused)
  utils.py       # small shared helpers
  static/
    index.html   # the web UI
```

## Deploying

`api.py` is a standard FastAPI app (`email_drafting_agent.api:app`) — it runs
anywhere Python does: `uvicorn email_drafting_agent.api:app --host 0.0.0.0
--port 8000`, or behind a process manager / Docker image of your choice. Set
`GROQ_API_KEY` (and optionally `GROQ_MODEL`) as environment variables on
whatever host you deploy to — don't ship your `.env` file.
