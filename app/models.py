from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    spent_on: Optional[str] = Field(default_factory=lambda: date.today().isoformat())
    notes: Optional[str] = Field(default=None, max_length=500)


class ExpenseUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    category: Optional[str] = Field(default=None, min_length=1, max_length=100)
    amount: Optional[float] = Field(default=None, gt=0)
    spent_on: Optional[str] = None
    notes: Optional[str] = Field(default=None, max_length=500)


class Expense(BaseModel):
    id: int
    title: str
    category: str
    amount: float
    spent_on: str
    notes: Optional[str] = None
    created_at: Optional[str] = None


class ExpenseSummary(BaseModel):
    total_spent: float
    total_count: int


class CategoryTotal(BaseModel):
    category: str
    total: float
