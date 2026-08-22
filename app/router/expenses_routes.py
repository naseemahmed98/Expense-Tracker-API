from fastapi import APIRouter, Depends
from business_logic import expenses_logic
import db.db_setup as db_setup
from pydantic import BaseModel
from sqlalchemy.orm import Session
from router.pydantic_modals import User, Expense

router = APIRouter()

@router.get("/")
def root() -> str:
    return "Welcome to the Expense Tracker App"
    

@router.get("/expense_tracker/expenses/{username}")
def return_total_expenses(username: str, session: Session = Depends(db_setup.createSession), category: str = None) -> dict:
    return expenses_logic.return_total_expenses(username, session, category)

@router.put("/expense_tracker/add_user")
def add_user(user: User, session: Session = Depends(db_setup.createSession)) -> User:
    return expenses_logic.add_user(user, session)

@router.put("/expense_tracker/add_expense")
def add_user(expense: Expense, session: Session = Depends(db_setup.createSession)) -> Expense:
    return expenses_logic.add_expense(expense, session)

@router.get("/expense_tracker/get_all_expenses")
def get_all_expenses(session: Session = Depends(db_setup.createSession)) -> list[Expense]:
    return expenses_logic.get_all_expenses(session)

@router.get("/expense_tracker/get_all_users")
def get_all_users(session: Session = Depends(db_setup.createSession)) -> list[User]:
    return expenses_logic.get_all_users(session)

@router.get("/expense_tracker/expense/{username}")
def users_expenses(username: str, session: Session = Depends(db_setup.createSession), transaction_ID: int = None) -> list[Expense]:
    return expenses_logic.users_expenses(username, session, transaction_ID)

@router.delete("/expense_tracker/delete_user/{username}")
def delete_user(username: str, session: Session = Depends(db_setup.createSession)) -> dict:
    return expenses_logic.delete_user(username, session)

@router.delete("/expense_tracker/delete_expense/{username}")
def delete_user(username: str, session: Session = Depends(db_setup.createSession), transaction_ID: int = None):
    return expenses_logic.delete_expense(username, session, transaction_ID)

@router.put("/expense_tracker/update_user/{username}")
def update_user(username: str, value, category, session: Session = Depends(db_setup.createSession)) -> User:
    return expenses_logic.update_user(username, value, category, session)