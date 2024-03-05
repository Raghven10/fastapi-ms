from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host='localhost',
    port=6379,
    decode_responses=True
    )

class Product(BaseModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database=redis


@app.get('/products')
def all_products():
    return Product.all_pks()

@app.post('/product')
def create_product(product: Product):
    return product.save()

