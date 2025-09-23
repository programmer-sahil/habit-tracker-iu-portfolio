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

## Project Structure
<img width="708" height="374" alt="image" src="https://github.com/user-attachments/assets/b69b903d-85a1-4007-b68e-641d0b464096" />

## Setup

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

