from pydantic import BaseModel, Field


class OutreachRequest(BaseModel):
    executive_name: str = Field(description="Executive's full name")

    executive_role: str = Field(description="Executive's role")

    company_name: str = Field(description="Company name")

    industry: str = Field(description="Industry", default="")

    company_context: str = Field(
        description="Brief context about the company"
    )

    recipient_context: str = Field(
        description="Important information about the executive",
        default=""
    )

    personalization_hook: str = Field(
        description="Recent news, post, podcast, achievement or event"
    )

    outreach_objective: str = Field(
        description="Purpose of this outreach"
    )

    solution_name: str = Field(
        description="Product or solution"
    )

    business_value: str = Field(
        description="Why the solution matters to the recipient"
    )

    call_to_action: str = Field(
        description="Desired next step"
    )

    tone: str = Field(
        default="Professional"
    )

    channel: str = Field(
        default="Email"
    )


class OutreachEmail(BaseModel):
    subject: str = Field(
        description="Compelling subject line"
    )

    email: str = Field(
        description="Complete outreach email"
    )
