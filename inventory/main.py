from fastapi import FastAPI
from pydantic import BaseModel
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

redis = get_redis_connection(
    host = 'localhost', 
    port = 6379,
    decode_responses = True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.get("/products")
async def all():
    return [format(pk) for pk in Product.all_pks()]

@app.post("/products")
def create(product: Product):
    print(product)
    return product.save()

