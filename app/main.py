from fastapi import FastAPI
from datetime import datetime
from app import auth
from app import models
from app.db import engine, Base
from fastapi import FastAPI
from app.routes import users, dashboard, products
models.Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

app = FastAPI()
start_time  = datetime.now()

app.include_router(auth.router)

@app.get("/")
def test():
    return {"message": "This is an API for health check"}
@app.get("/check")
def health_check():
    current_time = datetime.now()
    return {"status": "OK",
            "uptime": current_time - start_time,
            "current time": current_time,
            "started at ": start_time}



app.include_router(products.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(dashboard.router)