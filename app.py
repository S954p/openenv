"""
Compatibility entrypoint.

Some runners expect the ASGI app at `app:app`. We expose the FastAPI server app
from `server.app` here to avoid import/entrypoint mismatches in containers.
"""

from server.app import app  # noqa: F401
from fastapi import FastAPI
from support_env.environment import SupportTicketEnvironment

app = FastAPI()


@app.get("/")
def home():
    return {"message": "App running 🚀"}


@app.get("/run")
def run():
    env = SupportTicketEnvironment()
    score = env.run_episode()

    return {
        "final_score": score
    }

