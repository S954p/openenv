from .grading_view import GradingView
from .grader import grade_episode
import uuid


class EnvironmentState:
    """Holds structured state that app.py expects."""
    def __init__(self, episode_id, task_id, views, scenario=None):
        self.episode_id = episode_id
        self.task_id = task_id
        self.views = views
        self.customer = type("Customer", (), {"scenario": scenario or "cooperative"})()

    def model_dump(self):
        return {
            "episode_id": self.episode_id,
            "task_id": self.task_id,
            "scenario": self.customer.scenario,
            "views": [v.__dict__ for v in self.views],
        }


class Observation:
    """Holds observation returned from reset/step."""
    def __init__(self, episode_id, task_id, views):
        self.episode_id = episode_id
        self.task_id = task_id
        self.views = views

    def model_dump(self):
        return {
            "episode_id": self.episode_id,
            "task_id": self.task_id,
            "views": [v.__dict__ for v in self.views],
        }


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
        self.used_seed = None  # ✅ app.py needs this

    # ======================================================
    # RESET
    # ======================================================
    def reset(self, task_id=None, seed=None, scenario=None, **kwargs):
        self.used_seed = seed  # ✅ store seed for app.py

        if task_id and task_id in self.TASK_VIEWS:
            self.views = [GradingView(**self.TASK_VIEWS[task_id])]
            active_task_id = task_id
        else:
            self.views = [GradingView(**cfg) for cfg in self.TASK_VIEWS.values()]
            active_task_id = "all"

        episode_id = str(uuid.uuid4())  # ✅ unique episode ID

        # ✅ state is now a structured object, not a plain list
        self.state = EnvironmentState(
            episode_id=episode_id,
            task_id=active_task_id,
            views=self.views,
            scenario=scenario,
        )

        # ✅ obs is a separate object with model_dump()
        obs = Observation(
            episode_id=episode_id,
            task_id=active_task_id,
            views=self.views,
        )
        return obs

    # ======================================================
    # STEP
    # ======================================================
    def step(self, action=None):
        if self.state is None:
            raise RuntimeError("Call reset() before step()")

        score = grade_episode(self.views)
        done = True

        obs = Observation(
            episode_id=self.state.episode_id,
            task_id=self.state.task_id,
            views=self.views,
        )
        return obs, score, done, {}

    # ======================================================
    # HELPER
    # ======================================================
    def run_episode(self, task_id=None):
        self.reset(task_id=task_id)
        _, score, _, _ = self.step()
        return score
