"""
JSON persistence layer.

Provides functions to load and save a list of Habit objects from/to a JSON file.
"""

import json
import os
from typing import List
from . import __init__  # noqa: F401  # keep package importable
from ..models import Habit


DEFAULT_DB_PATH = os.environ.get("HABIT_DB_PATH", os.path.join("data", "habits.json"))


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def save_habits(habits: List[Habit], path: str = DEFAULT_DB_PATH) -> None:
    """
    Persist the given habits to a JSON file.
    """
    _ensure_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"habits": [h.to_dict() for h in habits]}, f, indent=2)


def load_habits(path: str = DEFAULT_DB_PATH) -> List[Habit]:
    """
    Load habits from a JSON file. If the file doesn't exist, return an empty list.
    """
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [Habit.from_dict(d) for d in raw.get("habits", [])]
