# IU Habit Tracker (CLI)

## Requirements
- Python 3.7+

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


# 1) create env and install deps
python -m venv .venv
# Mac/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate
pip install -r requirements.txt

# 2) seed demo data (5 habits, 4 weeks)
python -m habit_tracker.seed

# 3) run CLI
python -m habit_tracker.cli

# 4) run tests
pytest -q
```bash

# Hello
