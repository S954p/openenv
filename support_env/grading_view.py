class GradingView:
    def __init__(
        self,
        task_id,
        status,
        user_verified,
        reset_performed,
        issue_identified,
        resolution_provided,
        steps_taken,
        escalation_needed,
    ):
        self.task_id = task_id
        self.status = status
        self.user_verified = user_verified
        self.reset_performed = reset_performed
        self.issue_identified = issue_identified
        self.resolution_provided = resolution_provided
        self.steps_taken = steps_taken
        self.escalation_needed = escalation_needed