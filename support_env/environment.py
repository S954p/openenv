from .grading_view import GradingView
from .grader import grade_episode


class SupportTicketEnvironment:
    
    TASK_VIEWS = {
        "easy_password_reset": dict(
            task_id="easy_password_reset",
            status="CLOSED",
            reset_performed=True,
            user_verified=True,
            issue_identified=False,
            resolution_provided=False,
            attempts=1,
            escalation=False,
        ),
        "medium_billing_missing_info": dict(
            task_id="medium_billing_missing_info",
            status="OPEN",
            reset_performed=False,
            user_verified=True,
            issue_identified=True,
            resolution_provided=False,
            attempts=2,
            escalation=False,
        ),
        "hard_technical_troubleshooting": dict(
            task_id="hard_technical_troubleshooting",
            status="IN_PROGRESS",
            reset_performed=True,
            user_verified=True,
            issue_identified=False,
            resolution_provided=False,
            attempts=5,
            escalation=False,
        ),
    }

    def __init__(self):
        self.views = []
        self.state = None

    # ======================================================
    # RESET
    # ======================================================
    def reset(self, task_id=None, **kwargs):
        if task_id and task_id in self.TASK_VIEWS:
            self.views = [GradingView(**self.TASK_VIEWS[task_id])]
        else:
            # Load all 3 tasks by default
            self.views = [GradingView(**cfg) for cfg in self.TASK_VIEWS.values()]

        self.state = self.views
        return self.state

    # ======================================================
    # STEP
    # ======================================================
    def step(self, action=None):
        if not self.state:
            raise RuntimeError("Call reset() before step()")

        score = grade_episode(self.views)
        done = True
        self.state = self.views
        return self.state, score, done, {}

    # ======================================================
    # HELPER
    # ======================================================
    def run_episode(self, task_id=None):
        self.reset(task_id=task_id)
        _, score, _, _ = self.step()
        return score
