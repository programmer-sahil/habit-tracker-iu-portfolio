"""
Analytics module for Habit Tracker.

Implements pure functions to:
- Return list of all habits
- Return list of habits with the same periodicity
- Return longest run streak across all habits
- Return longest run streak for a given habit

Streak Rules:
- Daily: A streak continues only if there is at least one event on each consecutive day.
- Weekly: A streak continues only if there is at least one event in each consecutive ISO week.
"""

from datetime import datetime, timedelta
from typing import Iterable, List, Tuple, Optional
from ..models import Habit


# -------------------- Helpers (Pure Functions) --------------------

def _period_key(dt: datetime, periodicity: str) -> Tuple[int, int]:
    """
    Map a datetime to a (year, ordinal) key per periodicity.

    Parameters
    ----------
    dt : datetime
        Event timestamp
    periodicity : str
        Either 'daily' or 'weekly'

    Returns
    -------
    Tuple[int, int]
        (year, day_of_year) for daily or (iso_year, iso_week) for weekly
    """
    if periodicity == "daily":
        return (dt.year, dt.timetuple().tm_yday)
    elif periodicity == "weekly":
        iso_year, iso_week, _ = dt.isocalendar()
        return (iso_year, iso_week)
    else:
        raise ValueError("Invalid periodicity; must be 'daily' or 'weekly'")


def _previous_period_key(key: Tuple[int, int], periodicity: str) -> Tuple[int, int]:
    """
    Get the previous period key (one day or one ISO week earlier).

    Parameters
    ----------
    key : Tuple[int, int]
        Current period key
    periodicity : str
        Either 'daily' or 'weekly'

    Returns
    -------
    Tuple[int, int]
        Previous period key
    """
    if periodicity == "daily":
        year, day = key
        base = datetime(year, 1, 1) + timedelta(days=day - 1)
        prev = base - timedelta(days=1)
        return (prev.year, prev.timetuple().tm_yday)
    else:  # weekly
        year, week = key
        monday = _iso_to_monday(year, week)
        prev_monday = monday - timedelta(weeks=1)
        prev_iso_year, prev_iso_week, _ = prev_monday.isocalendar()
        return (prev_iso_year, prev_iso_week)


def _iso_to_monday(iso_year: int, iso_week: int) -> datetime:
    """
    Return the Monday datetime for a given ISO year/week.
    """
    jan4 = datetime(iso_year, 1, 4)
    iso1_monday = jan4 - timedelta(days=jan4.isoweekday() - 1)
    return iso1_monday + timedelta(weeks=iso_week - 1)


# -------------------- Required Analytics Functions --------------------

def list_all(habits: Iterable[Habit]) -> List[Habit]:
    """
    Return all habits as a list.

    Parameters
    ----------
    habits : Iterable[Habit]

    Returns
    -------
    List[Habit]
    """
    return list(habits)


def list_by_periodicity(habits: Iterable[Habit], periodicity: str) -> List[Habit]:
    """
    Filter habits by periodicity ('daily' or 'weekly').

    Parameters
    ----------
    habits : Iterable[Habit]
    periodicity : str

    Returns
    -------
    List[Habit]
    """
    return [h for h in habits if h.periodicity == periodicity]


def longest_run_streak_for(habit: Habit) -> int:
    """
    Compute the *longest* streak of consecutive periods where the habit
    has at least one completion in each period.

    Parameters
    ----------
    habit : Habit

    Returns
    -------
    int
        Longest streak for the habit
    """
    if not habit.events:
        return 0

    # Build sorted unique period keys where completion exists
    keys = sorted({_period_key(ev.timestamp, habit.periodicity) for ev in habit.events})

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

    Parameters
    ----------
    habits : Iterable[Habit]

    Returns
    -------
    Tuple[Optional[str], int]
        (habit_name, longest_streak). If no habits, returns (None, 0).
    """
    best_name = None
    best_val = 0
    for h in habits:
        s = longest_run_streak_for(h)
        if s > best_val:
            best_val = s
            best_name = h.name
    return best_name, best_val
