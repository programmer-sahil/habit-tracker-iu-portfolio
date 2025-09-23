"""
Interactive CLI for the Habit Tracker.

Features:
- Create/delete habits
- Mark completions (now)
- List habits (all / by periodicity)
- View analytics (longest streaks)
- Load demo data (5 habits, 4 weeks)
"""

from datetime import datetime
from typing import List
from .models import Habit
from .storage.json_store import load_habits, save_habits, DEFAULT_DB_PATH
from .analytics.analytics import (
    list_all,
    list_by_periodicity,
    longest_run_streak_all,
    longest_run_streak_for,
)
from .seed import load_fixture_into_db


# -------------------- Helper Functions --------------------

def _choose(prompt: str, options: List[str]) -> int:
    """Display options and return user choice (1-based index)."""
    print(prompt)
    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt}")
    while True:
        try:
            n = int(input("Select option: "))
            if 1 <= n <= len(options):
                return n
        except ValueError:
            pass
        print("Invalid choice. Try again.")


def _input_nonempty(prompt: str) -> str:
    """Prompt until user enters a non-empty string."""
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Value cannot be empty.")


# -------------------- Main CLI --------------------

def main() -> None:
    print("🌱 Habit Tracker (IU Portfolio) – JSON DB:", DEFAULT_DB_PATH)
    habits: List[Habit] = load_habits()

    MENU = [
        "List all habits",
        "List habits by periodicity",
        "Create a habit",
        "Delete a habit",
        "Mark habit as completed (now)",
        "Analytics: longest streak across all habits",
        "Analytics: longest streak for a habit",
        "Seed demo data (5 habits, 4 weeks)",
        "Save & Exit",
    ]

    while True:
        print("\n" + "-" * 50)
        choice = _choose("Main menu:", MENU)

        # 1) List all
        if choice == 1:
            if not habits:
                print("No habits found.")
            for h in list_all(habits):
                print(f" - {h.name} [{h.periodicity}] created {h.created_at.date()} | completions={len(h.events)}")

        # 2) List by periodicity
        elif choice == 2:
            p = _choose("Choose periodicity:", ["daily", "weekly"])
            period = "daily" if p == 1 else "weekly"
            filtered = list_by_periodicity(habits, period)
            if not filtered:
                print(f"No {period} habits.")
            else:
                for h in filtered:
                    print(f" - {h.name}")

        # 3) Create
        elif choice == 3:
            name = _input_nonempty("Habit name: ")
            per = "daily" if _choose("Periodicity:", ["daily", "weekly"]) == 1 else "weekly"
            habit = Habit(name=name, periodicity=per, created_at=datetime.now())
            habits.append(habit)
            save_habits(habits)
            print(f"Created habit '{name}' [{per}].")

        # 4) Delete
        elif choice == 4:
            if not habits:
                print("No habits to delete.")
                continue
            for i, h in enumerate(habits, start=1):
                print(f"  {i}. {h.name}")
            idx = int(input("Choose habit number to delete: "))
            if 1 <= idx <= len(habits):
                removed = habits.pop(idx - 1)
                save_habits(habits)
                print(f"Deleted '{removed.name}'.")
            else:
                print("Invalid selection.")

        # 5) Mark completion
        elif choice == 5:
            if not habits:
                print("No habits found.")
                continue
            for i, h in enumerate(habits, start=1):
                print(f"  {i}. {h.name} [{h.periodicity}]")
            idx = int(input("Choose habit to mark complete: "))
            if 1 <= idx <= len(habits):
                habits[idx - 1].check_off()  # Updated API usage
                save_habits(habits)
                print(f"Marked '{habits[idx-1].name}' complete at now.")
            else:
                print("Invalid selection.")

        # 6) Longest streak overall
        elif choice == 6:
            name, streak = longest_run_streak_all(habits)
            if name is None:
                print("No habits yet.")
            else:
                print(f"🏆 Longest streak overall: '{name}' with {streak}")

        # 7) Longest streak for a habit
        elif choice == 7:
            if not habits:
                print("No habits yet.")
                continue
            for i, h in enumerate(habits, start=1):
                print(f"  {i}. {h.name}")
            idx = int(input("Choose habit: "))
            if 1 <= idx <= len(habits):
                h = habits[idx - 1]
                s = longest_run_streak_for(h)
                print(f"'{h.name}' longest streak: {s}")
            else:
                print("Invalid selection.")

        # 8) Seed demo data
        elif choice == 8:
            load_fixture_into_db()
            habits = load_habits()
            print("Demo data loaded.")

        # 9) Save & Exit
        elif choice == 9:
            save_habits(habits)
            print("Saved. Bye! 👋")
            break


if __name__ == "__main__":
    main()
