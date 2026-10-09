import sqlite3
from pathlib import Path
from typing import List, Optional

DB_PATH = Path(__file__).resolve().parent.parent / "expenses.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            spent_on TEXT NOT NULL,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def add_expense(title: str, category: str, amount: float, spent_on: str, notes: Optional[str] = None) -> int:
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO expenses (title, category, amount, spent_on, notes) VALUES (?, ?, ?, ?, ?)",
        (title, category, amount, spent_on, notes),
    )
    conn.commit()
    expense_id = cursor.lastrowid
    conn.close()
    return expense_id


def get_expense(expense_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_expenses(
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> List[dict]:
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if start_date:
        query += " AND spent_on >= ?"
        params.append(start_date)

    if end_date:
        query += " AND spent_on <= ?"
        params.append(end_date)

    query += " ORDER BY spent_on DESC, id DESC"

    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_expense(
    expense_id: int,
    title: str,
    category: str,
    amount: float,
    spent_on: str,
    notes: Optional[str] = None,
) -> bool:
    conn = get_connection()
    cursor = conn.execute(
        "UPDATE expenses SET title = ?, category = ?, amount = ?, spent_on = ?, notes = ? WHERE id = ?",
        (title, category, amount, spent_on, notes, expense_id),
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def delete_expense(expense_id: int) -> bool:
    conn = get_connection()
    cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def get_total_spent() -> float:
    conn = get_connection()
    total = conn.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses").fetchone()[0]
    conn.close()
    return float(total)


def get_category_totals() -> List[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT category, ROUND(SUM(amount), 2) AS total FROM expenses GROUP BY category ORDER BY total DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
