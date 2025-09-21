from datetime import datetime, timedelta
from habit_tracker.models import Habit


def test_create_and_mark_complete():
    h = Habit(name="Test", periodicity="daily", created_at=datetime(2025, 1, 1, 9, 0))
    assert h.name == "Test"
    assert h.periodicity == "daily"
    assert h.completed_datetimes == []

    h.mark_complete(datetime(2025, 1, 1, 22, 0))
    assert len(h.completed_datetimes) == 1
    assert h.completed_datetimes[0].year == 2025


def test_serialization_roundtrip():
    h = Habit(
        name="Serialize",
        periodicity="weekly",
        created_at=datetime(2025, 1, 1, 9, 0),
        completed_datetimes=[datetime(2025, 1, 4, 12, 0)],
    )
    d = h.to_dict()
    h2 = Habit.from_dict(d)
    assert h2.name == h.name
    assert h2.periodicity == "weekly"
    assert len(h2.completed_datetimes) == 1
    assert h2.completed_datetimes[0] == datetime(2025, 1, 4, 12, 0)


def test_invalid_periodicity():
    try:
        Habit(name="X", periodicity="monthly", created_at=datetime.now())
        assert False, "Expected ValueError for invalid periodicity"
    except ValueError:
        assert True
