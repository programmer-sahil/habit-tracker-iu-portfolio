"""
JSON persistence layer for Habit Tracker.

Provides functions to load and save a list of Habit objects (with HabitEvents)
from/to a JSON file in a safe and portable way.
"""

import json
import os
from typing import List
from ..models import Habit

# Default JSON database path (overridable with HABIT_DB_PATH env var)
DEFAULT_DB_PATH = os.environ.get("HABIT_DB_PATH", os.path.join("data", "habits.json"))


def _ensure_dir(path: str) -> None:
    """
    Ensure the directory for the given path exists.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)


def save_habits(habits: List[Habit], path: str = DEFAULT_DB_PATH) -> None:
    """
    Persist the given habits (including events) to a JSON file.

    Parameters
    ----------
    habits : List[Habit]
        List of Habit objects to save.
    path : str
        Path to the JSON file. Defaults to HABIT_DB_PATH or 'data/habits.json'.
    """
    try:
        _ensure_dir(path)
        data = {"habits": [h.to_dict() for h in habits]}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except (OSError, IOError) as e:
        print(f"[ERROR] Failed to save habits to {path}: {e}")


def load_habits(path: str = DEFAULT_DB_PATH) -> List[Habit]:
    """
    Load habits (including events) from a JSON file.

    Parameters
    ----------
    path : str
        Path to the JSON file. Defaults to HABIT_DB_PATH or 'data/habits.json'.

    Returns
    -------
    List[Habit]
        List of Habit objects. Returns empty list if file not found or corrupted.
    """
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Habit.from_dict(d) for d in raw.get("habits", [])]
    except (OSError, IOError, json.JSONDecodeError) as e:
        print(f"[ERROR] Failed to load habits from {path}: {e}")
        return []
