"""
Compatibility entrypoint.

Some runners expect the ASGI app at `app:app`. We expose the FastAPI server app
from `server.app` here to avoid import/entrypoint mismatches in containers.
"""

from server.app import app  # noqa: F401


