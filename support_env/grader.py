from .task_graders import (
    grade_password_reset,
    grade_billing,
    grade_technical,
)

# ✅ TASK REGISTRATION
TASK_GRADERS = {
    "easy_password_reset": grade_password_reset,
    "medium_billing_missing_info": grade_billing,
    "hard_technical_troubleshooting": grade_technical,
}

# ✅ DEBUG
print("DEBUG: TASK_GRADERS LOADED")
for task, func in TASK_GRADERS.items():
    print(f"{task} → {func.__name__}")


# ======================================================
# ✅ SINGLE TASK GRADER
# ======================================================
def grade_task(view):
    if view.task_id not in TASK_GRADERS:
        return 0.1  # safe fallback

    score = TASK_GRADERS[view.task_id](view)

    # ensure strict (0,1)
    if score <= 0:
        score = 0.1
    elif score >= 1:
        score = 0.9

    return score


# ======================================================
# ✅ 🔥 REQUIRED FUNCTION (THIS FIXES YOUR ERROR)
# ======================================================
def grade_episode(views):
    """
    This function is REQUIRED by environment.py
    It takes a list of GradingView objects
    """

    print("\n[GRADE_EPISODE CALLED]")

    if not views:
        return 0.1

    scores = []

    for view in views:
        print(f"Grading task: {view.task_id}")
        score = grade_task(view)
        print(f"Score: {score}")
        scores.append(score)

    # average score
    final_score = sum(scores) / len(scores)

    print(f"[FINAL EPISODE SCORE]: {final_score}")

    return final_score
