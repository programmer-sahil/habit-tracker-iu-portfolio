"""
Analytics implemented in a functional style (pure functions).

Required by IU:
- return list of all habits
- return list of habits with the same periodicity
- return longest run streak across all habits
- return longest run streak for a given habit
"""

from datetime import datetime, timedelta
from typing import Iterable, List, Tuple, Optional
from ..models import Habit


# ---------- helpers (pure) -------------------------------------------------
def _period_key(dt: datetime, periodicity: str) -> Tuple[int, int]:
    """
    Map a datetime to a (year, ordinal) key per periodicity.
      daily  -> (year, day_of_year)
      weekly -> (iso_year, iso_week)
    """
    if periodicity == "daily":
        return (dt.year, dt.timetuple().tm_yday)
    elif periodicity == "weekly":
        iso_year, iso_week, _ = dt.isocalendar()
        return (iso_year, iso_week)
    else:
        raise ValueError("Invalid periodicity")

def _previous_period_key(key: Tuple[int, int], periodicity: str) -> Tuple[int, int]:
    """
    Get the previous period key (one day or one ISO week earlier).
    """
    if periodicity == "daily":
        year, day = key
        base = datetime(year, 1, 1) + timedelta(days=day - 1)
        prev = base - timedelta(days=1)
        return (prev.year, prev.timetuple().tm_yday)
    else:  # weekly
        year, week = key
        # Convert back to a date (Monday of the given ISO week)
        # Monday of week `week` in ISO year `year`
        # ISO week 1 is the week with the first Thursday of the year
        monday = _iso_to_monday(year, week)
        prev_monday = monday - timedelta(weeks=1)
        prev_iso_year, prev_iso_week, _ = prev_monday.isocalendar()
        return (prev_iso_year, prev_iso_week)

def _iso_to_monday(iso_year: int, iso_week: int) -> datetime:
    """
    Return the Monday datetime for a given ISO year/week.
    """
    # ISO: week starts Monday; week 01 has first Thursday of the year
    # Start with Jan 4th, guaranteed to be in week 01
    jan4 = datetime(iso_year, 1, 4)
    iso1_monday = jan4 - timedelta(days=jan4.isoweekday() - 1)
    return iso1_monday + timedelta(weeks=iso_week - 1)


# ---------- required analytics (pure) --------------------------------------
def list_all(habits: Iterable[Habit]) -> List[Habit]:
    """Return all habits as a list."""
    return list(habits)

def list_by_periodicity(habits: Iterable[Habit], periodicity: str) -> List[Habit]:
    """Filter habits by periodicity ('daily' or 'weekly')."""
    return [h for h in habits if h.periodicity == periodicity]

def longest_run_streak_for(habit: Habit) -> int:
    """
    Compute the *longest* streak of consecutive periods where the habit
    has at least one completion in each period.
    """
    if not habit.completed_datetimes:
        return 0

    # Build sorted unique period keys where completion exists
    keys = sorted({_period_key(dt, habit.periodicity) for dt in habit.completed_datetimes})

    # Sweep to find longest consecutive chain
    best = 1
    current = 1
    for prev, cur in zip(keys, keys[1:]):
        if _previous_period_key(cur, habit.periodicity) == prev:
            current += 1
            best = max(best, current)
        else:
            current = 1
    return best

def longest_run_streak_all(habits: Iterable[Habit]) -> Tuple[Optional[str], int]:
    """
    Return (habit_name, longest_streak) across all habits.
    If there are no habits, returns (None, 0).
    """
    best_name = None
    best_val = 0
    for h in habits:
        s = longest_run_streak_for(h)
        if s > best_val:
            best_val = s
            best_name = h.name
    return best_name, best_val
