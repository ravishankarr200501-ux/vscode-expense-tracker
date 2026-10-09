from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, Response

from .db import (
    add_expense,
    delete_expense,
    get_category_totals,
    get_expense,
    get_expenses,
    get_total_spent,
    update_expense,
)
from .models import CategoryTotal, Expense, ExpenseCreate, ExpenseSummary, ExpenseUpdate

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=dict, status_code=201)
def create_expense(expense: ExpenseCreate):
    expense_id = add_expense(
        title=expense.title,
        category=expense.category,
        amount=expense.amount,
        spent_on=expense.spent_on,
        notes=expense.notes,
    )
    return {"id": expense_id, "message": "Expense created successfully"}


@router.get("/", response_model=List[Expense])
def list_expenses(
    category: Optional[str] = Query(default=None, description="Filter by category"),
    start_date: Optional[str] = Query(default=None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(default=None, description="End date (YYYY-MM-DD)"),
):
    return get_expenses(category=category, start_date=start_date, end_date=end_date)


@router.get("/{expense_id}", response_model=Expense)
def get_single_expense(expense_id: int):
    expense = get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=dict)
def update_single_expense(expense_id: int, expense: ExpenseUpdate):
    existing = get_expense(expense_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Expense not found")

    title = expense.title or existing["title"]
    category = expense.category or existing["category"]
    amount = expense.amount if expense.amount is not None else existing["amount"]
    spent_on = expense.spent_on or existing["spent_on"]
    notes = expense.notes if expense.notes is not None else existing["notes"]

    updated = update_expense(expense_id, title, category, amount, spent_on, notes)
    if not updated:
        raise HTTPException(status_code=400, detail="Failed to update expense")

    return {"id": expense_id, "message": "Expense updated successfully"}


@router.delete("/{expense_id}", status_code=204)
def delete_single_expense(expense_id: int):
    existing = get_expense(expense_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Expense not found")

    delete_expense(expense_id)
    return Response(status_code=204)


@router.get("/summary/overview", response_model=ExpenseSummary)
def get_summary():
    expenses = get_expenses()
    return {"total_spent": get_total_spent(), "total_count": len(expenses)}


@router.get("/summary/by-category", response_model=List[CategoryTotal])
def get_category_summary():
    return get_category_totals()
