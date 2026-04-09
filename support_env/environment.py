from .grading_view import GradingView
from .grader import grade_episode


class SupportTicketEnvironment:

    def __init__(self):
        self.views = []
        self.state = None   # ✅ REQUIRED

    # ======================================================
    # ✅ RESET (FIXED)
    # ======================================================
    def reset(self, task_id=None, **kwargs):

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
            # ✅ ALL 3 TASKS
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

        # ✅ VERY IMPORTANT: set state
        self.state = self.views

        return self.state

    # ======================================================
    # ✅ STEP
    # ======================================================
    def step(self, action=None):
        score = grade_episode(self.views)
        done = True

        # update state (optional but safe)
        self.state = self.views

        return self.state, score, done, {}

    # ======================================================
    # ✅ HELPER
    # ======================================================
    def run_episode(self):
        self.reset()
        _, score, _, _ = self.step()
        return score
