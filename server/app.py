from __future__ import annotations

from threading import Lock
from typing import Any, Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from support_env.environment import SupportTicketEnvironment
from support_env.tasks import TASKS

# -------------------- FastAPI App --------------------
app = FastAPI(title="Meta-Hackathon Support Ticket Environment")

# -------------------- Global Storage --------------------
_envs: Dict[str, SupportTicketEnvironment] = {}
_lock = Lock()


# -------------------- Models --------------------
class ResetRequest(BaseModel):
    task_id: Optional[str] = Field(
        default=None,
        description="easy_password_reset | medium_billing_missing_info | hard_technical_troubleshooting",
    )
    seed: Optional[int] = None
    scenario: Optional[str] = Field(
        default=None,
        description="cooperative | angry_customer | silent_customer | escalation_hint",
    )


class StepRequest(BaseModel):
    episode_id: str
    action: Dict[str, Any]


class StateRequest(BaseModel):
    episode_id: str


# -------------------- Routes --------------------
@app.get("/")
def root():
    return {
        "message": "Customer AI Command Center API is running",
        "endpoints": ["/health", "/reset", "/step", "/state"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def tasks():
    payload = []

    for task_id, spec in TASKS.items():
        difficulty = (
            "easy" if "easy" in task_id
            else "medium" if "medium" in task_id
            else "hard" if "hard" in task_id
            else "unknown"
        )

        payload.append(
            {
                "task_id": spec.task_id,
                "label": spec.task_id.replace("_", " ").title(),
                "difficulty": difficulty,
                "sla_seconds": spec.sla_seconds,
                "max_steps": spec.max_steps,
                "optimal_steps": spec.optimal_steps,
                "expected_issue_type": spec.expected_issue_type,
            }
        )

    return {"tasks": payload}


# -------------------- Core Logic --------------------
def _reset_episode(req: ResetRequest):
    env = SupportTicketEnvironment()

    try:
        obs = env.reset(
            task_id=req.task_id,
            seed=req.seed,
            scenario=req.scenario,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid task_id: {e}")

    state = env.state  # ✅ FIXED: was env.state() — state is an attribute, not a method

    with _lock:
        _envs[state.episode_id] = env

    return {
        "episode_id": state.episode_id,
        "observation": obs.model_dump(),
        "done": False,
        "info": {
            "task_id": state.task_id,
            "seed_used": env.used_seed,
            "scenario": state.customer.scenario,
        },
    }


# -------------------- API Endpoints --------------------
@app.post("/reset")
def reset(req: Optional[ResetRequest] = None):
    return _reset_episode(req or ResetRequest())


@app.post("/openenv/reset")
def openenv_reset(req: Optional[ResetRequest] = None):
    return _reset_episode(req or ResetRequest())


@app.post("/step")
def step(req: StepRequest):
    with _lock:
        env = _envs.get(req.episode_id)

    if env is None:
        raise HTTPException(status_code=404, detail="Unknown episode_id")

    obs, reward, done, info = env.step(req.action)

    return {
        "episode_id": req.episode_id,
        "observation": obs.model_dump(),
        "reward": reward.model_dump(),
        "done": done,
        "info": info,
    }


@app.post("/state")
def state(req: StateRequest):
    with _lock:
        env = _envs.get(req.episode_id)

    if env is None:
        raise HTTPException(status_code=404, detail="Unknown episode_id")

    return {"state": env.state.model_dump()}  # ✅ FIXED: was env.state()


@app.get("/state")
def state_get(episode_id: str):
    with _lock:
        env = _envs.get(episode_id)

    if env is None:
        raise HTTPException(status_code=404, detail="Unknown episode_id")

    return {"state": env.state.model_dump()}  # ✅ FIXED: was env.state()


# -------------------- Entry Point --------------------
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
