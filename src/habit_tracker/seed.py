"""
Seed the database with 5 predefined habits and 4 weeks of example completions.

Generates:
- 3 daily habits: "Workout", "Read Book", "Meditate"
- 2 weekly habits: "Weekly Review", "Family Call"

Each habit has 4 weeks of completion events.
"""

import os
from datetime import datetime, timedelta
from typing import List
from .models import Habit, HabitEvent
from .storage.json_store import save_habits, DEFAULT_DB_PATH


def _generate_events(periodicity: str, weeks: int = 4) -> List[HabitEvent]:
    """
    Generate completion events for the last `weeks` weeks.

    Parameters
    ----------
    periodicity : str
        Either 'daily' or 'weekly'.
    weeks : int
        Number of weeks of events to generate.

    Returns
    -------
    List[HabitEvent]
        List of HabitEvent objects for given periodicity.
    """
    now = datetime.now()
    events: List[HabitEvent] = []
    if periodicity == "daily":
        # One event per day for last N weeks
        for i in range(7 * weeks):
            day = now - timedelta(days=i)
            events.append(HabitEvent(timestamp=day))
    elif periodicity == "weekly":
        # One event per week for last N weeks (on Sundays)
        for i in range(weeks):
            week = now - timedelta(weeks=i)
            events.append(HabitEvent(timestamp=week))
    else:
        raise ValueError("Invalid periodicity for event generation")
    return list(reversed(events))  # chronological order


def create_predefined_habits() -> List[Habit]:
    """
    Create 5 predefined habits with events for testing/demo.

    Returns
    -------
    List[Habit]
        List of Habit objects with generated events.
    """
    habits: List[Habit] = [
        Habit(name="Workout", periodicity="daily", created_at=datetime.now(), events=_generate_events("daily")),
        Habit(name="Read Book", periodicity="daily", created_at=datetime.now(), events=_generate_events("daily")),
        Habit(name="Meditate", periodicity="daily", created_at=datetime.now(), events=_generate_events("daily")),
        Habit(name="Weekly Review", periodicity="weekly", created_at=datetime.now(), events=_generate_events("weekly")),
        Habit(name="Family Call", periodicity="weekly", created_at=datetime.now(), events=_generate_events("weekly")),
    ]
    return habits


def load_fixture_into_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """
    Seed the database with predefined habits and events.

    Parameters
    ----------
    db_path : str
        Path to the JSON file to store habits.
    """
    habits = create_predefined_habits()
    save_habits(habits, db_path)
    print(f"Seeded {len(habits)} habits with 4 weeks of events into {db_path}")


if __name__ == "__main__":
    load_fixture_into_db()
