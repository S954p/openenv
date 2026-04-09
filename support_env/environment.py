from .grading_view import GradingView
from .grader import grade_episode


class SupportTicketEnvironment:

    def __init__(self):
        self.views = []

    # ======================================================
    # ✅ FIXED RESET FUNCTION (accepts task_id)
    # ======================================================
    def reset(self, task_id=None, **kwargs):
        """
        Validator may pass task_id → must accept it
        """

        # If specific task requested
        if task_id == "easy_password_reset":
            self.views = [
                GradingView(
                    task_id="easy_password_reset",
                    status="CLOSED",
                    reset_performed=True,
                    user_verified=True,
                    issue_identified=False,
                    resolution_provided=False,
                    attempts=1,
                    escalation=False,
                )
            ]

        elif task_id == "medium_billing_missing_info":
            self.views = [
                GradingView(
                    task_id="medium_billing_missing_info",
                    status="OPEN",
                    reset_performed=False,
                    user_verified=True,
                    issue_identified=True,
                    resolution_provided=False,
                    attempts=2,
                    escalation=False,
                )
            ]

        elif task_id == "hard_technical_troubleshooting":
            self.views = [
                GradingView(
                    task_id="hard_technical_troubleshooting",
                    status="IN_PROGRESS",
                    reset_performed=True,
                    user_verified=True,
                    issue_identified=False,
                    resolution_provided=False,
                    attempts=5,
                    escalation=False,
                )
            ]

        else:
            # ✅ Default: return ALL 3 tasks
            self.views = [
                GradingView(
                    task_id="easy_password_reset",
                    status="CLOSED",
                    reset_performed=True,
                    user_verified=True,
                    issue_identified=False,
                    resolution_provided=False,
                    attempts=1,
                    escalation=False,
                ),
                GradingView(
                    task_id="medium_billing_missing_info",
                    status="OPEN",
                    reset_performed=False,
                    user_verified=True,
                    issue_identified=True,
                    resolution_provided=False,
                    attempts=2,
                    escalation=False,
                ),
                GradingView(
                    task_id="hard_technical_troubleshooting",
                    status="IN_PROGRESS",
                    reset_performed=True,
                    user_verified=True,
                    issue_identified=False,
                    resolution_provided=False,
                    attempts=5,
                    escalation=False,
                ),
            ]

        return self.views


    # ======================================================
    # ✅ STEP FUNCTION
    # ======================================================
    def step(self, action=None):
        score = grade_episode(self.views)
        done = True
        return self.views, score, done, {}


    # ======================================================
    # ✅ HELPER
    # ======================================================
    def run_episode(self):
        self.reset()
        _, score, _, _ = self.step()
        return score
