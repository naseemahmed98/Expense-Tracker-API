from fastapi import FastAPI, HTTPException
from db.db_setup import Base, engine
from contextlib import asynccontextmanager
from router import expenses_routes


@asynccontextmanager
async def lifespan(server: FastAPI):
    # startup
    Base.metadata.create_all(bind=engine)
    yield

server = FastAPI(title="Expense Tracker API", lifespan=lifespan)
server.include_router(expenses_routes.router)



