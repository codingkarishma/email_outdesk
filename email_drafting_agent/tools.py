"""
Extension point for LangChain tools.

The current OutreachAgent is a single structured-output call and doesn't need
tools. If you want the agent to look things up (e.g. fetch company news for
the personalization hook, check a CRM, verify a domain), define LangChain
@tool-decorated functions here and wire them into agent.py.

Example:

    from langchain_core.tools import tool

    @tool
    def fetch_recent_news(company_name: str) -> str:
        \"\"\"Fetch recent news about a company to use as a personalization hook.\"\"\"
        ...
"""
