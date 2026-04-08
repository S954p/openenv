from .grading_view import GradingView


# ✅ Safety wrapper
def clamp_score(score: float) -> float:
    if score <= 0:
        return 1e-6
    if score >= 1:
        return 0.999999
    return score


# ✅ Task 1: Password Reset
def grade_password_reset_task(view: GradingView) -> float:
    if (
        view.task_id == "easy_password_reset"
        and view.status == "CLOSED"
        and view.reset_performed
        and view.user_verified
    ):
        return 0.999999
    return 1e-6


# ✅ Task 2: Billing
def grade_billing_task(view: GradingView) -> float:
    if view.task_id != "medium_billing_missing_info":
        return 1e-6

    if (
        view.status == "CLOSED"
        and view.user_verified
        and view.issue_identified
        and view.resolution_provided
    ):
        return 0.999999
    elif view.status == "OPEN":
        return 0.5
    return 0.2



def grade_technical_task(view: GradingView) -> float:
    if view.task_id != "hard_technical_troubleshooting":
        return 1e-6

    # ✅ CLOSED → max score
    if view.status == "CLOSED":
        return 0.999999

    # ✅ IN_PROGRESS → medium score
    if view.status == "IN_PROGRESS":
        return 0.6

    # fallback
    return 0.3

# ✅ Wrappers (for tests compatibility)
def grade_password_reset(view: GradingView) -> float:
    return grade_password_reset_task(view)


def grade_billing(view: GradingView) -> float:
    return grade_billing_task(view)


def grade_technical(view: GradingView) -> float:
    return grade_technical_task(view)