"""
OOP model for a Habit and helper utilities.
Python 3.7+ compatible.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any


VALID_PERIODICITIES = {"daily", "weekly"}


def start_of_week(d: datetime) -> datetime:
    """Return Monday 00:00 of the week containing d."""
    monday = d - timedelta(days=d.weekday())
    return datetime(monday.year, monday.month, monday.day)


@dataclass
class Habit:
    """
    Represents a habit with a periodicity and a list of completion timestamps.

    Attributes
    ----------
    name : str
        Human-readable habit name.
    periodicity : str
        Either 'daily' or 'weekly'.
    created_at : datetime
        When the habit was created.
    completed_datetimes : List[datetime]
        When the habit was checked off by the user.
    """
    name: str
    periodicity: str  # 'daily' | 'weekly'
    created_at: datetime
    completed_datetimes: List[datetime] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.periodicity not in VALID_PERIODICITIES:
            raise ValueError("periodicity must be 'daily' or 'weekly'")

    # ---------- Core behavior ----------
    def mark_complete(self, when: datetime = None) -> None:
        """Mark this habit as completed at a given datetime (default: now)."""
        when = when or datetime.now()
        self.completed_datetimes.append(when)

    # ---------- Streak helpers ----------
    def _period_key(self, d: datetime) -> datetime:
        """
        Normalize a datetime to the period "key":
        - daily  -> that day's midnight
        - weekly -> Monday 00:00 of that ISO week
        """
        if self.periodicity == "daily":
            return datetime(d.year, d.month, d.day)
        else:
            return start_of_week(d)

    def _period_step(self) -> timedelta:
        """Step size between consecutive periods for this habit."""
        return timedelta(days=1) if self.periodicity == "daily" else timedelta(days=7)

    def unique_completed_periods(self) -> List[datetime]:
        """Return sorted unique period keys that have at least one completion."""
        keys = {self._period_key(d) for d in self.completed_datetimes}
        return sorted(keys)

    def longest_streak(self) -> int:
        """
        Compute the longest consecutive run of completed periods.
        Duplicates in the same period are ignored.
        """
        periods = self.unique_completed_periods()
        if not periods:
            return 0
        step = self._period_step()
        longest = cur = 1
        for prev, nxt in zip(periods, periods[1:]):
            if nxt - prev == step:
                cur += 1
                if cur > longest:
                    longest = cur
            else:
                cur = 1
        return longest

    # ---------- Serialization ----------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "periodicity": self.periodicity,
            "created_at": self.created_at.isoformat(),
            "completed_datetimes": [d.isoformat() for d in self.completed_datetimes],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Habit":
        return Habit(
            name=data["name"],
            periodicity=data["periodicity"],
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_datetimes=[
                datetime.fromisoformat(x) for x in data.get("completed_datetimes", [])
            ],
        )
