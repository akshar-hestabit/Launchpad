from fastapi import FastAPI
from datetime import datetime
from app import auth
from app import models
from app.db import engine, Base
from fastapi import FastAPI
from app.routes import users, dashboard, products, cart_route
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

def init_elasticsearch():
    try:
        # Check if index exists
        if not es.indices.exists(index=INDEX_NAME):
            # Create index with mappings
            mappings = {
                "mappings": {
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "text"},
                        "description": {"type": "text"},
                        "price": {"type": "float"},
                        "quantity": {"type": "integer"},
                        "category": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                        "brand": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                        "vendor": {"type": "text", "fields": {"keyword": {"type": "keyword"}}}
                    }
                }
            }
            es.indices.create(index=INDEX_NAME, body=mappings)
            print(f"Created Elasticsearch index: {INDEX_NAME}")
    except Exception as e:
        print(f"Error initializing Elasticsearch: {e}")

# Call this function during app startup

app.include_router(products.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(cart_route.router)