from .grading_view import GradingView
from .grader import grade_episode


class SupportTicketEnvironment:

    def run_episode(self):
        """
        MUST return final score using 3 tasks
        """

        views = [
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

        return grade_episode(views)
