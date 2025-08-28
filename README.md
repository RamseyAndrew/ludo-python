# Ludo CLI

Terminal-based Ludo game with colorful UI, SQLAlchemy persistence, and Alembic migrations.

## Features
- Rich-powered colorful board and prompts
- Correct per-player finish entries and lanes
- Capture rules and safe squares
- SQLAlchemy ORM models: `Player`, `Game`, `Move` (3+ tables)
- Alembic migrations split: create DB, create tables

## Requirements
- Python 3.10+
- Pipenv (recommended)

## Setup
```bash
pipenv install
```

Initialize the database and run migrations:
```bash
# Create the SQLite file and version it
alembic upgrade head
```

## Run
```bash
pipenv run python ludo.py
```

## Project Structure
```
.
├── ludo.py                  # CLI entry and game loop
├── ludo_cli/
│   ├── __init__.py
│   ├── db.py                # Engine/session factory
│   └── models.py            # ORM models
├── alembic.ini              # Alembic config
├── alembic/
│   ├── env.py
│   └── versions/
│       ├── 0001_create_database.py
│       └── 0002_create_tables.py
└── Pipfile
```

## Usage
- Press Enter to roll the dice.
- Choose a token when prompted.
- Rolling a 6 grants another turn (three 6s penalty applies).
- Game data is saved to `ludo.db`.

## Notes
- If you want to run without a database, the game still works. Persistence is optional.
- Extend rules (stack immunity, etc.) by updating `move_token` and capture logic.

