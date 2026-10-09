# FastAPI Expense Tracker

A modern Python expense tracking API built with FastAPI. Track your spending, browse records, and summarize totals using a lightweight SQLite database.

## Features
- Add, list, update, and delete expenses
- Filter by category or date range
- View total spending and category totals
- Built with FastAPI and SQLite
- Swagger UI available at `/docs`

## Project Structure
```text
vscode-expense-tracker/
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── main.py
│   ├── models.py
│   └── routes.py
├── .env.example
├── .gitignore
├── README.md
├── main.py
├── requirements.txt
├── expenses.db
├── LICENSE
└── .gitignore
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate it:
- macOS/Linux:
```bash
source venv/bin/activate
```
- Windows:
```bash
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the API:
```bash
python main.py
```

5. Open the docs:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Example Requests

Create an expense:
```bash
curl -X POST "http://127.0.0.1:8000/expenses/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Groceries",
    "category": "Food",
    "amount": 42.50,
    "spent_on": "2026-10-09",
    "notes": "Weekly groceries"
  }'
```

Get all expenses:
```bash
curl "http://127.0.0.1:8000/expenses/"
```

Get summary:
```bash
curl "http://127.0.0.1:8000/expenses/summary/overview"
```

## License
MIT
