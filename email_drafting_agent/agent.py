from .models import llm
from .prompts import EMAIL_PROMPT
from .schemas import OutreachRequest, OutreachEmail


class OutreachAgent:
    def __init__(self):
        self.structured_llm = llm.with_structured_output(OutreachEmail, method="json_mode")
    def generate_email(self, request: OutreachRequest) -> OutreachEmail:
        prompt = EMAIL_PROMPT.invoke(
            {
                "executive_name": request.executive_name,
                "executive_role": request.executive_role,
                "company_name": request.company_name,
                "industry": request.industry or "Not specified",
                "company_description": request.company_context,
                "recipient_context": request.recipient_context or "Not provided",
                "hook": request.personalization_hook,
                "reason": request.outreach_objective,
                "product": request.solution_name,
                "value_proposition": request.business_value,
                "cta": request.call_to_action,
                "tone": request.tone,
                "channel": request.channel,
            }
        )

        response = self.structured_llm.invoke(prompt)

        return response
