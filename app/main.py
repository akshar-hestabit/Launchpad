from fastapi import FastAPI
from datetime import datetime
from app import auth, models
from app.db import engine, Base
from app.routes import (
    users, dashboard, products, cart_route,
    stripe_payment, stripe_webhook,
    paypal_payment, paypal_webhook
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from elasticsearch import Elasticsearch

# Initialize FastAPI app
app = FastAPI()

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Elasticsearch configuration
ELASTICSEARCH_URL = "http://localhost:9200"
INDEX_NAME = "products"
es = Elasticsearch(ELASTICSEARCH_URL)

start_time = datetime.now()

# Initialize Elasticsearch index
def init_elasticsearch():
    try:
        if not es.ping():
            print("❌ Could not connect to Elasticsearch")
            return

        if not es.indices.exists(index=INDEX_NAME):
            body = {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "mappings": {
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "text"},
                        "description": {"type": "text"},
                        "price": {"type": "float"},
                        "quantity": {"type": "integer"},
                        "category": {"type": "keyword"},
                        "brand": {"type": "keyword"},
                        "vendor": {"type": "keyword"}
                    }
                }
            }
            es.indices.create(index=INDEX_NAME, body=body)
            print(f"✅ Created Elasticsearch index: {INDEX_NAME}")
        else:
            print(f"ℹ️ Elasticsearch index '{INDEX_NAME}' already exists.")
    except Exception as e:
        print(f"❌ Error initializing Elasticsearch: {str(e)}")

# Run on application startup
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting application...")
    init_elasticsearch()

# ========== Routes ==========

# API routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(products.router)
app.include_router(cart_route.router)
app.include_router(stripe_payment.router, prefix="/stripe")
app.include_router(stripe_webhook.router)
app.include_router(paypal_payment.router)
app.include_router(paypal_webhook.router)

# Health check endpoints
@app.get("/")
def root(): 
    return {"message": "This is an API for health check"}

@app.get("/check")
def health_check():
    current_time = datetime.now()
    return {
        "status": "OK",
        "uptime": current_time - start_time,
        "current time": current_time,
        "started at": start_time
    }

# Serve frontend static HTML pages
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/login")
async def serve_login_page():
    return FileResponse("frontend/login.html")

@app.get("/signup")
async def serve_signup_page():
    return FileResponse("frontend/signup.html")

@app.get("/products")
async def serve_products_page():
    return FileResponse("frontend/products.html")

@app.get("/cart")
async def serve_cart_page():
    return FileResponse("frontend/cart.html")

@app.get("/wishlist")
async def serve_wishlist_page():
    return FileResponse("frontend/wishlist.html")

@app.get("/checkout")
async def serve_checkout_page():
    return FileResponse("frontend/checkout.html")

@app.get("/orders")
async def serve_orders_page():
    return FileResponse("frontend/orders.html")
