from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

class OrderRequest(BaseModel):
    symbol: str
    quantity: float
    side: str
    price: float
    user_id: int

@app.post("/orders")
def place_order(order: OrderRequest):
    if order.quantity <= 0 or order.price <= 0:
        raise HTTPException(status_code=400, detail="Invalid order parameters")

    broker_order_id = str(uuid.uuid4())

    print(f"✅ Order received by mock broker: {order.dict()}")
    return {
        "status": "accepted",
        "broker_order_id": broker_order_id
    }
