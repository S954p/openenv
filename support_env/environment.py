from .grading_view import GradingView
from .grader import grade_episode


class SupportTicketEnvironment:
    """
    Environment for validator
    Must implement reset() and step() in some frameworks
    """

    def __init__(self):
        self.views = []

    # ======================================================
    # ✅ REQUIRED: RESET FUNCTION
    # ======================================================
    def reset(self):
        """
        Initializes the environment and returns initial state
        """

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

        return self.views  # initial state

    # ======================================================
    # ✅ OPTIONAL: STEP FUNCTION (for RL style env)
    # ======================================================
    def step(self, action=None):
        """
        In simple case, we don't modify state
        Just return current state + score
        """

        score = grade_episode(self.views)

        done = True  # episode ends immediately

        return self.views, score, done, {}

    # ======================================================
    # ✅ HELPER: RUN FULL EPISODE
    # ======================================================
    def run_episode(self):
        self.reset()
        _, score, _, _ = self.step()
        return score
