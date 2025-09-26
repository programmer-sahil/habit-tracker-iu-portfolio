# IU Habit Tracker (CLI)

A command-line habit tracking application built with **Python 3.7+** using **Object-Oriented Programming (OOP)** for core logic and **Functional Programming (FP)** for analytics.  

This project is developed according to the **IU Portfolio course requirements** for the module **Object-Oriented and Functional Programming with Python (DLBDSOOFPP01)**.

---

## Features

- Create, delete, and manage **daily** and **weekly** habits  
- Mark completions and track progress automatically  
- Analyse habits using functional programming tools:  
  - List all habits  
  - List habits by periodicity (daily/weekly)  
  - Longest streak overall  
  - Longest streak for a single habit  
- Seed demo data with **5 predefined habits** and **4 weeks of events**  
- **Unit tests** for core components and analytics  

---

## Requirements

- **Python 3.7+**
- Tested with **pytest** for unit testing  

---



### Notes
- `data/habits.json` provides seed data for testing **daily** and **weekly** streaks, including examples where:
  - Consecutive days/weeks demonstrate **full streaks**.
  - Missing days/weeks demonstrate **streak breaks**.
- This file ensures reproducible results for analytics functions, unit tests, and CLI demonstrations.


---

## Project Structure
<img width="708" height="374" alt="image" src="https://github.com/user-attachments/assets/b69b903d-85a1-4007-b68e-641d0b464096" />


---
## Final Notes
- **Seed Data:** The `data/habits.json` file contains predefined daily and weekly habits with timestamps to test streak calculations and gaps.
- **Unit Tests:** Run `pytest -q` to verify all modules. All tests pass successfully.
- **Persistence:** JSON storage auto-saves habit changes; CLI allows creating, deleting, and analyzing habits.
- **Streak Rules:** Missing a day (daily) or week (weekly) breaks the streak automatically.
- **GitHub & Submission:** Identical code in GitHub and ZIP submission as per formal requirements.

---
## Setup & Installation

```bash
# 1) Create virtual environment
python -m venv .venv

# 2) Activate environment
# Mac/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Seed demo data (5 habits, 4 weeks)
python -m habit_tracker.seed

# 5) Run CLI
python -m habit_tracker.cli

# 6) Run tests
pytest -q

