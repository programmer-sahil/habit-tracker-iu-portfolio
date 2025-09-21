"""
Seed the database with 5 predefined habits and 4 weeks of example completions.
"""

import json
import os
from typing import List
from .models import Habit
from .storage.json_store import save_habits, DEFAULT_DB_PATH


FIXTURE_PATH = os.path.join("data", "fixtures", "habits_4weeks.json")


def load_fixture_into_db(path: str = FIXTURE_PATH, db_path: str = DEFAULT_DB_PATH) -> None:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fixture file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    habits: List[Habit] = [Habit.from_dict(d) for d in raw.get("habits", [])]
    save_habits(habits, db_path)


if __name__ == "__main__":
    load_fixture_into_db()
    print(f"Loaded fixture into {DEFAULT_DB_PATH}")
