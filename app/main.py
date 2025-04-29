from fastapi import FastAPI
from datetime import datetime
from app import auth, models
from app.db import engine, Base
from app.routes import users, dashboard, products, cart_route, stripe_payment, stripe_webhook, paypal_payment, paypal_webhook


from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ELASTICSEARCH_URL = "http://localhost:9200"
from elasticsearch import Elasticsearch
es = Elasticsearch(ELASTICSEARCH_URL)
INDEX_NAME  = "products"
models.Base.metadata.create_all(bind=engine)


start_time = datetime.now()

def init_elasticsearch():
    try:
        if not es.indices.exists(index=INDEX_NAME):
            # For Elasticsearch 7.x and newer
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
            
            # This is the proper way to create an index in newer Elasticsearch versions
            es.indices.create(index=INDEX_NAME, body=body)
            print(f"✅ Created Elasticsearch index: {INDEX_NAME}")
        else:
            print(f"ℹ️ Elasticsearch index '{INDEX_NAME}' already exists.")
    except Exception as e:
        print(f"❌ Error initializing Elasticsearch: {e}")
        # Add more detailed error info
        print(f"Error details: {str(e)}")


# FastAPI Startup Event
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting application...")
    init_elasticsearch()

# ========== Routes ==========

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(products.router)
app.include_router(cart_route.router)
app.include_router(stripe_payment.router, prefix="/stripe")
app.include_router(stripe_webhook.router)
app.include_router(paypal_payment.router)
app.include_router(paypal_webhook.router)

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


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount the frontend directory
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
