from support_env.grading_view import GradingView
from support_env.task_graders import (
    grade_password_reset_task,
    grade_billing_task,
    grade_technical_task,
)


def build_grading_view(state):
    ticket = state.ticket

    return GradingView(
        task_id=state.task_id,
        status=ticket.status,
        user_verified=getattr(ticket, "user_verified", True),
        reset_performed=getattr(ticket, "reset_performed", True),
        issue_identified=getattr(ticket, "issue_identified", True),
        resolution_provided=getattr(ticket, "resolution_provided", True),
        # steps_taken=len(getattr(state, "trajectory", [])),  # safe
        steps_taken=len(getattr(state, "steps", getattr(state, "trajectory", []))),
        escalation_needed=False,
    )


def grade_episode(state):
    view = build_grading_view(state)

    if state.task_id == "easy_password_reset":
        return grade_password_reset_task(view)

    elif state.task_id == "medium_billing_missing_info":
        return grade_billing_task(view)

    elif state.task_id == "hard_technical_troubleshooting":
        return grade_technical_task(view)

    return 1e-6