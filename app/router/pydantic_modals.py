from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    username: str
    first_name: str 
    last_name: str


class Expense(BaseModel):
    username: str 
    purchase: str
    cost: float
    category: str
    transaction_ID: int = None
    timestamp: datetime = None
