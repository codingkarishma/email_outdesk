"""Command-line interface for the outreach email drafting agent."""

import argparse
import sys

from .agent import OutreachAgent
from .schemas import OutreachRequest
from .utils import format_email, request_from_json_file


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="email-drafting-agent",
        description="Generate a personalized B2B cold outreach email.",
    )
    parser.add_argument("--interactive", action="store_true", help="Prompt for each field interactively")
    parser.add_argument("--from-json", metavar="FILE", help="Load request fields from a JSON file")
    parser.add_argument("--executive-name")
    parser.add_argument("--executive-role")
    parser.add_argument("--company-name")
    parser.add_argument("--industry", default="")
    parser.add_argument("--company-context")
    parser.add_argument("--recipient-context", default="")
    parser.add_argument("--personalization-hook")
    parser.add_argument("--outreach-objective")
    parser.add_argument("--solution-name")
    parser.add_argument("--business-value")
    parser.add_argument("--call-to-action")
    parser.add_argument("--tone", default="Professional")
    parser.add_argument("--channel", default="Email")
    return parser


def _prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def _interactive_request() -> OutreachRequest:
    print("Enter the outreach details (press Enter to skip optional fields):\n")
    return OutreachRequest(
        executive_name=_prompt("Executive name"),
        executive_role=_prompt("Executive role"),
        company_name=_prompt("Company name"),
        industry=_prompt("Industry", ""),
        company_context=_prompt("Company context"),
        recipient_context=_prompt("About the executive (optional)", ""),
        personalization_hook=_prompt("Personalization hook"),
        outreach_objective=_prompt("Reason for outreach"),
        solution_name=_prompt("Your product/solution"),
        business_value=_prompt("Value proposition"),
        call_to_action=_prompt("Call to action"),
        tone=_prompt("Tone", "Professional"),
        channel=_prompt("Channel", "Email"),
    )


def _request_from_args(args: argparse.Namespace) -> OutreachRequest:
    missing = [
        name
        for name in (
            "executive_name",
            "executive_role",
            "company_name",
            "company_context",
            "personalization_hook",
            "outreach_objective",
            "solution_name",
            "business_value",
            "call_to_action",
        )
        if not getattr(args, name)
    ]
    if missing:
        flags = ", ".join("--" + m.replace("_", "-") for m in missing)
        print(f"Missing required arguments: {flags}", file=sys.stderr)
        sys.exit(2)

    return OutreachRequest(
        executive_name=args.executive_name,
        executive_role=args.executive_role,
        company_name=args.company_name,
        industry=args.industry,
        company_context=args.company_context,
        recipient_context=args.recipient_context,
        personalization_hook=args.personalization_hook,
        outreach_objective=args.outreach_objective,
        solution_name=args.solution_name,
        business_value=args.business_value,
        call_to_action=args.call_to_action,
        tone=args.tone,
        channel=args.channel,
    )


def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    if args.from_json:
        request = request_from_json_file(args.from_json)
    elif args.interactive:
        request = _interactive_request()
    else:
        request = _request_from_args(args)

    agent = OutreachAgent()
    result = agent.generate_email(request)
    print(format_email(result))


if __name__ == "__main__":
    main()
