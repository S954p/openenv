from pydantic import BaseModel


class GradingView(BaseModel):
    task_id: str
    status: str
    reset_performed: bool
    user_verified: bool
    issue_identified: bool
    resolution_provided: bool
    attempts: int
    escalation: bool
