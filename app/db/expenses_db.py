from db.db_setup import Expense as db_Expense
from db.users_db import validate_user_exists
from router.pydantic_modals import Expense as router_Expense
from sqlalchemy import select, func
from sqlalchemy.orm import Session

def add_expense(expense: router_Expense, session: Session) -> db_Expense:
    new_expense = db_Expense(
        username = expense.username, 
        purchase = expense.purchase,
        cost = expense.cost,
        category = expense.category,
        timestamp = expense.timestamp 
    )
    session.add(new_expense)
    session.commit()
    return new_expense 

def return_total_expenses(username: str,session: Session, category: str = None) -> int:
    if not validate_user_exists(username, session):
        raise ValueError("User Does Not exist")
    query = (session.query(func.sum(db_Expense.cost)).filter(db_Expense.username == username))
    if category:
        query = query.filter(db_Expense.category == category)
    total = query.scalar()
    return total

def get_all_expenses(session: Session) -> list[db_Expense]:
    expenses = select(db_Expense)
    results = session.execute(expenses).scalars().all()
    return results

def get_latest_transaction_ID(session: Session) -> int:
    latest_transaction_ID = (session.query(func.max(db_Expense.transaction_ID)).scalar())
    return latest_transaction_ID

def users_expenses(username: str, session: Session, transaction_ID = None) -> list[db_Expense]:
    query = (session.query(db_Expense).filter(db_Expense.username == username))
    if transaction_ID is not None:
        query = query.filter(db_Expense.transaction_ID == transaction_ID)
    results = session.execute(query).scalars().all()
    if transaction_ID is not None and not results:
        raise ValueError(f"No matching expense found for user={username}, transaction_ID={transaction_ID}")
    return results

def delete_users_expenses(username: str, session: Session, transaction_ID = None):

    query = (session.query(db_Expense).filter(db_Expense.username == username))
    if transaction_ID is not None:
        query = query.filter(db_Expense.transaction_ID == transaction_ID)
    rows_deleted = query.delete()
    if rows_deleted == 0 and transaction_ID is not None:
        raise ValueError (f"No matching expense found for user={username}, transaction_ID={transaction_ID}")     
    session.commit()


