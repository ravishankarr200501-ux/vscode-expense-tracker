from fastapi import FastAPI

from .db import init_db
from .routes import router

app = FastAPI(
    title="Expense Tracker API",
    description="Simple expense tracking API built with FastAPI",
    version="1.0.0",
)

init_db()
app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Expense Tracker API",
        "docs": "/docs",
        "redoc": "/redoc",
    }
