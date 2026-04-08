from __future__ import annotations

import importlib
import sys
from typing import Any, Callable, Dict, List, Tuple

import yaml


def _load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f.read()) or {}


def _collect_tasks(manifest: dict) -> List[Tuple[str, str]]:
    """
    Returns list of (task_id, grader_path).
    Supports both modern (spec_version:1) and legacy (environment.tasks) schemas.
    """
    out: List[Tuple[str, str]] = []

    for t in (manifest.get("tasks") or []):
        if isinstance(t, dict) and t.get("id") and t.get("grader"):
            out.append((str(t["id"]), str(t["grader"])))

    env = manifest.get("environment") or {}
    for t in (env.get("tasks") or []):
        if isinstance(t, dict) and t.get("id") and t.get("grader"):
            out.append((str(t["id"]), str(t["grader"])))

    # de-duplicate preserving order
    seen: set[Tuple[str, str]] = set()
    uniq: List[Tuple[str, str]] = []
    for pair in out:
        if pair in seen:
            continue
        seen.add(pair)
        uniq.append(pair)
    return uniq


def _import_callable(dotted: str) -> Callable[..., Any]:
    mod, _, name = dotted.rpartition(".")
    if not mod:
        raise ValueError(f"Invalid grader path: {dotted!r}")
    m = importlib.import_module(mod)
    fn = getattr(m, name, None)
    if not callable(fn):
        raise TypeError(f"Grader is not callable: {dotted!r}")
    return fn


def main() -> int:
    manifest = _load_yaml("openenv.yaml")
    tasks = _collect_tasks(manifest)

    # Validate: 3 distinct task IDs with graders
    task_ids = [t for (t, _g) in tasks]
    distinct_ids = list(dict.fromkeys(task_ids))
    if len(distinct_ids) < 3:
        print(f"FAIL: expected >=3 tasks with graders, got {len(distinct_ids)}: {distinct_ids}")
        return 1

    required = {"easy_password_reset", "medium_billing_missing_info", "hard_technical_troubleshooting"}
    missing = required.difference(distinct_ids)
    if missing:
        print(f"FAIL: missing required task ids in manifest: {sorted(missing)}")
        return 1

    # Validate: graders return scores strictly inside (0,1) for a known-good trajectory
    from support_env.environment import SupportTicketEnvironment
    from support_env.grading_view import build_grading_view

    # Known-good policy actions (same as inference policy)
    from inference import _make_policy_actions

    problems: List[str] = []
    for tid in sorted(required):
        grader_path = next((g for (t, g) in tasks if t == tid), None)
        if not grader_path:
            problems.append(f"{tid}: no grader path found")
            continue
        grader = _import_callable(grader_path)

        env = SupportTicketEnvironment()
        env.reset(task_id=tid, seed=1)
        done = False
        for a in _make_policy_actions(tid):
            _obs, _reward, done, _info = env.step(a)
            if done:
                break

        state = env.state()
        view = build_grading_view(state)
        # Some graders expect EnvironmentState; some expect GradingView.
        try:
            score = float(grader(state))
        except Exception:
            score = float(grader(view))
        if not (0.0 < score < 1.0):
            problems.append(f"{tid}: grader returned out-of-range score={score} via {grader_path}")

    if problems:
        print("FAIL:")
        for p in problems:
            print(" -", p)
        return 1

    print("PASS: manifest has 3 graded tasks; all grader scores are strictly within (0,1).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

