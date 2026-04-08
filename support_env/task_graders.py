from .grading_view import GradingView


# ✅ Strictly keep scores inside (0,1)
def clamp_score(score: float) -> float:
    if score <= 0:
        return 0.1
    if score >= 1:
        return 0.9
    return score


# ===============================
# Task 1
# ===============================
def grade_password_reset_task(view: GradingView) -> float:
    if (
        view.task_id == "easy_password_reset"
        and view.status == "CLOSED"
        and view.reset_performed
        and view.user_verified
    ):
        return 0.9
    return 0.1


# ===============================
# Task 2
# ===============================
def grade_billing_task(view: GradingView) -> float:
    if view.task_id != "medium_billing_missing_info":
        return 0.1

    if (
        view.status == "CLOSED"
        and view.user_verified
        and view.issue_identified
        and view.resolution_provided
    ):
        return 0.9

    if view.status == "OPEN":
        return 0.5

    return 0.3


# ===============================
# Task 3
# ===============================
def grade_technical_task(view: GradingView) -> float:
    if view.task_id != "hard_technical_troubleshooting":
        return 0.1

    if view.status == "CLOSED":
        return 0.9

    if view.status == "IN_PROGRESS":
        return 0.6

    return 0.3


# ===============================
# Wrappers (IMPORTANT)
# ===============================
def grade_password_reset(view: GradingView) -> float:
    return clamp_score(grade_password_reset_task(view))


def grade_billing(view: GradingView) -> float:
    return clamp_score(grade_billing_task(view))


def grade_technical(view: GradingView) -> float:
    return clamp_score(grade_technical_task(view))
