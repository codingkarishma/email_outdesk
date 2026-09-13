"""FastAPI server: a /generate endpoint backed by OutreachAgent, plus the web UI."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .agent import OutreachAgent
from .schemas import OutreachEmail, OutreachRequest

app = FastAPI(title="Outreach Email Drafting Agent", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_agent: OutreachAgent | None = None


def get_agent() -> OutreachAgent:
    global _agent
    if _agent is None:
        _agent = OutreachAgent()
    return _agent


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/generate", response_model=OutreachEmail)
def generate(request: OutreachRequest) -> OutreachEmail:
    try:
        return get_agent().generate_email(request)
    except Exception as exc:  # surfaces Groq/model errors as a clean 502
        raise HTTPException(status_code=502, detail=str(exc)) from exc


_static_dir = Path(__file__).parent / "static"
if _static_dir.exists():
    app.mount("/assets", StaticFiles(directory=_static_dir), name="assets")

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(_static_dir / "index.html")
