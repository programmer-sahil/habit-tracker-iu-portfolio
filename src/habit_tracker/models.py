"""
OOP model for a Habit, HabitEvent, and helper utilities.
Python 3.7+ compatible.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Literal

# ----------------- Constants -----------------
VALID_PERIODICITIES = {"daily", "weekly"}


def start_of_week(d: datetime) -> datetime:
    """Return Monday 00:00 of the week containing datetime d."""
    monday = d - timedelta(days=d.weekday())
    return datetime(monday.year, monday.month, monday.day)


# ----------------- Event Class -----------------
@dataclass
class HabitEvent:
    """
    Represents a single completion event for a habit.

    Attributes
    ----------
    timestamp : datetime
        When the habit was completed.
    status : str
        Status flag; default 'completed'. Future-proofing for other states.
    """
    timestamp: datetime
    status: str = "completed"

    def to_dict(self) -> Dict[str, str]:
        """Serialize event to dict for JSON storage."""
        return {"timestamp": self.timestamp.isoformat(), "status": self.status}

    @staticmethod
    def from_dict(data: Dict[str, str]) -> "HabitEvent":
        """Deserialize event from dict."""
        return HabitEvent(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            status=data.get("status", "completed"),
        )


# ----------------- Habit Class -----------------
@dataclass
class Habit:
    """
    Represents a habit with a periodicity and a list of completion events.

    Attributes
    ----------
    name : str
        Human-readable habit name.
    periodicity : Literal["daily","weekly"]
        Either 'daily' or 'weekly'.
    created_at : datetime
        When the habit was created.
    events : List[HabitEvent]
        List of completion events for this habit.
    """

    name: str
    periodicity: Literal["daily", "weekly"]
    created_at: datetime
    events: List[HabitEvent] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.periodicity not in VALID_PERIODICITIES:
            raise ValueError("periodicity must be 'daily' or 'weekly'")

    # ---------- Core behavior ----------
    def check_off(self, dt: Optional[datetime] = None) -> None:
        """
        Mark this habit as completed at the given datetime (default: now).

        Parameters
        ----------
        dt : datetime, optional
            Completion timestamp. Defaults to current time.
        """
        dt = dt or datetime.now()
        self.events.append(HabitEvent(timestamp=dt))

    # ---------- Period helpers ----------
    def _period_key(self, d: datetime) -> datetime:
        """
        Normalize a datetime to the period "key":
        - daily  -> that day's midnight
        - weekly -> Monday 00:00 of that ISO week
        """
        return datetime(d.year, d.month, d.day) if self.periodicity == "daily" else start_of_week(d)

    def _period_step(self) -> timedelta:
        """Step size between consecutive periods for this habit."""
        return timedelta(days=1) if self.periodicity == "daily" else timedelta(days=7)

    # ---------- Streak helpers ----------
    def unique_completed_periods(self) -> List[datetime]:
        """Return sorted unique period keys that have at least one completion."""
        keys = {self._period_key(ev.timestamp) for ev in self.events}
        return sorted(keys)

    def longest_streak(self) -> int:
        """
        Compute the longest consecutive run of completed periods.
        Duplicates in the same period are ignored.

        Returns
        -------
        int
            Length of the longest streak (in periods).
        """
        periods = self.unique_completed_periods()
        if not periods:
            return 0
        step = self._period_step()
        longest = cur = 1
        for prev, nxt in zip(periods, periods[1:]):
            if nxt - prev == step:
                cur += 1
                longest = max(longest, cur)
            else:
                cur = 1
        return longest

    # ---------- Serialization ----------
    def to_dict(self) -> Dict[str, Any]:
        """Convert Habit (and events) to a JSON-serializable dict."""
        return {
            "name": self.name,
            "periodicity": self.periodicity,
            "created_at": self.created_at.isoformat(),
            "events": [ev.to_dict() for ev in self.events],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Habit":
        """Rehydrate Habit (and events) from a dict."""
        return Habit(
            name=data["name"],
            periodicity=data["periodicity"],
            created_at=datetime.fromisoformat(data["created_at"]),
            events=[HabitEvent.from_dict(ev) for ev in data.get("events", [])],
        )
