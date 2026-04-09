from __future__ import annotations

from threading import Lock
from typing import Any, Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from support_env.environment import SupportTicketEnvironment
from support_env.tasks import TASKS


# -------------------- FastAPI App --------------------
app = FastAPI(title="Meta-Hackathon Support Ticket Environment")


# -------------------- Global Storage --------------------
_envs: Dict[str, SupportTicketEnvironment] = {}
_lock = Lock()


# -------------------- Global Exception Handler --------------------
@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# -------------------- Models --------------------
class ResetRequest(BaseModel):
    task_id: Optional[str] = Field(default=None)
    seed: Optional[int] = None
    scenario: Optional[str] = Field(default=None)


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
        "endpoints": ["/health", "/tasks", "/reset", "/step", "/state"],
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
            else "hard"
        )

        payload.append(
            {
                "task_id": getattr(spec, "task_id", task_id),
                "label": getattr(spec, "task_id", task_id).replace("_", " ").title(),
                "difficulty": difficulty,
                "sla_seconds": getattr(spec, "sla_seconds", None),
                "max_steps": getattr(spec, "max_steps", None),
                "optimal_steps": getattr(spec, "optimal_steps", None),
                "expected_issue_type": getattr(spec, "expected_issue_type", None),
            }
        )

    return {"tasks": payload}


# -------------------- Core Logic --------------------
def _safe_model_dump(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return obj


def _reset_episode(req: ResetRequest):
    try:
        env = SupportTicketEnvironment()

        obs = env.reset(
            task_id=req.task_id,
            seed=req.seed,
            scenario=req.scenario,
        )

        state = env.state()

        with _lock:
            _envs[state.episode_id] = env

        return {
            "episode_id": state.episode_id,
            "observation": _safe_model_dump(obs),
            "done": False,
            "info": {
                "task_id": state.task_id,
                "seed_used": getattr(env, "used_seed", None),
                "scenario": state.customer.scenario,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Reset failed: {str(e)}")


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

    try:
        obs, reward, done, info = env.step(req.action)

        return {
            "episode_id": req.episode_id,
            "observation": _safe_model_dump(obs),
            "reward": _safe_model_dump(reward),
            "done": done,
            "info": info,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Step failed: {str(e)}")


@app.post("/state")
def state(req: StateRequest):
    with _lock:
        env = _envs.get(req.episode_id)

    if env is None:
        raise HTTPException(status_code=404, detail="Unknown episode_id")

    try:
        return {"state": _safe_model_dump(env.state())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/state")
def state_get(episode_id: str):
    with _lock:
        env = _envs.get(episode_id)

    if env is None:
        raise HTTPException(status_code=404, detail="Unknown episode_id")

    try:
        return {"state": _safe_model_dump(env.state())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------- Entry Point --------------------
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860, reload=True)


if __name__ == "__main__":
    main()
