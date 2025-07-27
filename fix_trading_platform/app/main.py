from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Base, User, Trade
from database import engine
from auth import get_password_hash, authenticate_user, create_access_token, get_current_user
from fix_handler import start_fix_engine, send_order
from fastapi.openapi.utils import get_openapi
from datetime import timedelta
from auth import get_db
import time
import uvicorn

###### BUILDING IMAGE
'''
docker buildx build --no-cache --platform linux/amd64 -t fix-trading-platform . --load
docker buildx build -t fix-trading-platform . --load
docker compose up --build
docker compose up
'''
## DEBUG EXECUTE from CMD
# uvicorn main:app --host 127.0.0.1 --port 8000 --reload

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Start the FIX engine.
fix_app = start_fix_engine()

class UserCreate(BaseModel):
    email: str
    password: str

class TokenRequest(BaseModel):
    username: str
    password: str

class TradeRequest(BaseModel):
    symbol: str
    quantity: float
    side: str

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "registered"}

@app.post("/token")
def login(form_data: TokenRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/execute-trade")
def execute_trade(req: TradeRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    print('execute-trade')
    trade = Trade(symbol=req.symbol, quantity=req.quantity, side=req.side, status="sent", user_id=user.id)
    db.add(trade)
    db.commit()
    #### MOCK METHOD NEED TO SEE THE REAL ONE. # TODO: Panos 26/7/25
    send_order(req.symbol, req.quantity, req.side)
    return {"status": "sent", "trade_id": trade.id}

@app.get("/trades")
def list_trades(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Trade).filter(Trade.user_id == user.id).all()

print("defining custom_openapi")
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Trading API",
        version="1.0.0",
        description="Authenticated FIX trading API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema
## print('IM BEFORE custom_openapi')
app.openapi = custom_openapi
## print('IM AFTER custom_openapi')


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )