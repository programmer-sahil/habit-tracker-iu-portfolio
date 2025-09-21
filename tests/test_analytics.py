from datetime import datetime, timedelta
from habit_tracker.models import Habit
from habit_tracker.analytics.analytics import (
    list_all, list_by_periodicity, longest_run_streak_for, longest_run_streak_all
)


def _make_daily(name, start: datetime, days: int, skip_every: int = 0):
    h = Habit(name=name, periodicity="daily", created_at=start)
    d = start
    for i in range(days):
        if skip_every and (i % skip_every == 0) and i != 0:
            d += timedelta(days=1)
            continue
        h.mark_complete(d)
        d += timedelta(days=1)
    return h


def test_list_filters():
    habits = [
        Habit("A", "daily", datetime(2025, 1, 1)),
        Habit("B", "weekly", datetime(2025, 1, 1)),
    ]
    assert len(list_all(habits)) == 2
    assert [h.name for h in list_by_periodicity(habits, "daily")] == ["A"]


def test_longest_streak_for_daily():
    start = datetime(2025, 1, 1, 9, 0)
    h = Habit("Run", "daily", start)
    # mark 3 consecutive days, break, then 5 consecutive days
    for day in [0, 1, 2, 4, 5, 6, 7, 8]:
        h.mark_complete(start + timedelta(days=day, hours=20))
    assert longest_run_streak_for(h) == 5


def test_longest_streak_all():
    start = datetime(2025, 1, 1, 8, 0)
    h1 = _make_daily("Read", start, 4)      # streak 4
    h2 = Habit("Weekly Review", "weekly", start)
    # three consecutive ISO weeks
    for d in [datetime(2025, 1, 4), datetime(2025, 1, 11), datetime(2025, 1, 18)]:
        h2.mark_complete(d)
    name, streak = longest_run_streak_all([h1, h2])
    assert name in ("Read", "Weekly Review")
    assert streak == 4
