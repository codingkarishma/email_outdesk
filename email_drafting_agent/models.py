import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# NOTE: the original code used "qwen3.6-27b", which is not a valid Groq model
# id and would fail every request with a 404. Groq model ids are namespaced
# by provider, e.g. "qwen/qwen3.6-27b". Overridable via GROQ_MODEL so this
# doesn't need a code change if Groq deprecates/renames the model.
DEFAULT_MODEL = "qwen/qwen3.6-27b"


def _require_api_key() -> None:
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError(
            "GROQ_API_KEY is not set. Create a .env file (see .env.example) "
            "or export GROQ_API_KEY, using a free key from "
            "https://console.groq.com/keys"
        )


_require_api_key()

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", DEFAULT_MODEL),
    temperature=float(os.getenv("GROQ_TEMPERATURE", "0.3")),
    max_tokens=int(os.getenv("GROQ_MAX_TOKENS", "700")),
    reasoning_format="hidden",
    reasoning_effort="none",
)
