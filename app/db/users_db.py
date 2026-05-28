from db.db_setup import User as db_User
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from router.pydantic_modals import User as router_User


def add_user(user:router_User, session: Session) -> db_User:
    new_user = db_User(username=user.username, first_name=user.first_name, last_name=user.last_name)
    session.add(new_user)
    session.commit()
    return new_user 

def validate_user_exists(username: str, session: Session) -> bool:
    user = session.query(db_User).filter(db_User.username == username).first()
    return user is not None 


def get_all_users(session: Session) -> list[db_User]:
    users = select(db_User)
    results = session.execute(users).scalars().all()
    return results

def delete_user(username: str, session: Session):
    user_to_delete = session.query(db_User).filter(db_User.username == username).first()
    if user_to_delete:
        session.delete(user_to_delete)
    session.commit()

def update_user(username:str, value: str, category: str, session: Session):
    user = session.query(db_User).filter(db_User.username == username).first()
    if "first" in category.lower():
        user.first_name = value
    elif "last" in category.lower():
        user.last_name = value
    elif "user" in category.lower():
        if validate_user_exists(value, session):
            raise ValueError(f"{value} already an existing user")
        else:
            user.username = value
    
    session.commit()
    session.refresh(user)
    return user


    