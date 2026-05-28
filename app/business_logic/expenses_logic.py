from db import expenses_db, users_db
from db.db_setup import Expense as db_Expense
from db.db_setup import User as db_User
from sqlalchemy.orm import Session
from router.pydantic_modals import Expense as router_Expense, User as router_User
from datetime import datetime



def add_user(user: router_User, session: Session) -> db_User:
    user_exists = users_db.validate_user_exists(user.username, session)
    if user_exists:
        raise ValueError("User Already exists")
    else:
        return users_db.add_user(user, session)
    
def add_expense(expense: router_Expense, session: Session) -> db_Expense:
    user_exists = users_db.validate_user_exists(expense.username, session)
    if not user_exists:
        raise ValueError("User Does Not exists")
    else:
        latest_transaction_ID = get_latest_transaction_ID(session)
        expense.transaction_ID = latest_transaction_ID
        expense.timestamp = datetime.now()
        return expenses_db.add_expense(expense, session)
    
def return_total_expenses(username: str, session: Session, category: str = None) -> dict: 
    user_exists = users_db.validate_user_exists(username, session)
    if not user_exists:
        raise ValueError("User Does Not exist")
    else:
        total_expense = expenses_db.return_total_expenses(username, session, category)
        formatted_dollars = f"${total_expense:,.2f}"  if total_expense else "$0.00"
        return_string = f"Total Expenses for {category}" if category else "Total Expenses"
        return {f"{return_string}": formatted_dollars}
    

def get_all_expenses(session: Session) -> list[db_Expense]: #need to refine this to be admin only
    return expenses_db.get_all_expenses(session)

def get_all_users(session: Session) -> list[db_User]: #need to refine this to be admin only
    return users_db.get_all_users(session)

def get_latest_transaction_ID(session: Session) -> int:
    latest_transaction_ID = expenses_db.get_latest_transaction_ID(session)
    if not latest_transaction_ID:
        latest_transaction_ID = 1
    else:
        latest_transaction_ID += 1 
    return latest_transaction_ID

def users_expenses(username: str, session: Session, transaction_ID: int = None) -> db_Expense:
    user_exists = users_db.validate_user_exists(username, session)
    if not user_exists:
        raise ValueError("User Does Not exist")
    return expenses_db.users_expenses(username, session, transaction_ID)

def delete_user(username: str, session: Session) -> dict:
    user_exists = users_db.validate_user_exists(username, session)
    if not user_exists:
        raise ValueError("User Does Not exist")
    expenses_db.delete_users_expenses(username, session)
    users_db.delete_user(username, session)
    return {"message": f"{username} deleted"}

def delete_expense(username: str, session: Session, transaction_ID: int = None):
    user_exists = users_db.validate_user_exists(username, session)
    if not user_exists:
        raise ValueError("User Does Not exist")
    expenses_db.delete_users_expenses(username, session, transaction_ID)

def update_user(username:str, value: str, category: str, session: Session):
    user_exists = users_db.validate_user_exists(username, session)
    if not user_exists:
        raise ValueError("User Does Not exist")
    return users_db.update_user(username, value, category, session)