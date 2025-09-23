"""
Unit tests for Habit and HabitEvent model functionality.
Covers check_off, to_dict/from_dict, and streak calculations.
"""

from datetime import datetime, timedelta
from habit_tracker.models import Habit, HabitEvent


def test_habit_event_serialization():
    now = datetime(2025, 1, 1, 9, 0)
    ev = HabitEvent(timestamp=now, status="completed")
    d = ev.to_dict()
    ev2 = HabitEvent.from_dict(d)
    assert ev2.timestamp == now
    assert ev2.status == "completed"


def test_habit_check_off_and_serialization():
    h = Habit(name="Read", periodicity="daily", created_at=datetime(2025, 1, 1))
    h.check_off(datetime(2025, 1, 1, 10, 0))
    h.check_off(datetime(2025, 1, 2, 11, 0))

    # Serialize and reload
    d = h.to_dict()
    h2 = Habit.from_dict(d)

    assert h2.name == "Read"
    assert h2.periodicity == "daily"
    assert len(h2.events) == 2
    assert h2.events[0].timestamp == datetime(2025, 1, 1, 10, 0)


def test_longest_streak_daily_with_gap():
    start = datetime(2025, 1, 1, 9, 0)
    h = Habit("Run", "daily", start)
    # 3 consecutive days, gap, then 2 consecutive days
    for day in [0, 1, 2, 4, 5]:
        h.check_off(start + timedelta(days=day))
    # Longest streak should be 3 (gap breaks it)
    assert h.longest_streak() == 3


def test_longest_streak_weekly_with_gap():
    start = datetime(2025, 1, 1)
    h = Habit("Weekly Review", "weekly", start)
    # 2 consecutive weeks, gap, then 2 consecutive weeks
    for d in [0, 7, 21, 28]:  # skipping week at day=14
        h.check_off(start + timedelta(days=d))
    assert h.longest_streak() == 2
