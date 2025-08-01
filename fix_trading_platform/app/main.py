from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Base, User, Trade
from database import engine
from auth import get_password_hash, authenticate_user, create_access_token, get_current_user
# from fix_handler import start_fix_engine
from fastapi.openapi.utils import get_openapi
from datetime import timedelta
from auth import get_db
import uvicorn
from equation_helper import bind_cash, rollback_cash_reservation, finalize_cash
from rest_broker import send_order_rest

###### BUILDING IMAGE
'''
docker buildx build --no-cache --platform linux/amd64 -t fix-trading-platform . --load
docker buildx build -t fix-trading-platform . --load
docker compose up --build
docker compose up
'''
## DEBUG EXECUTE from CMD
# uvicorn main:app --host 127.0.0.1 --port 8000 --reload
## BE CAREFUL WITH THIS Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
app = FastAPI()

# Start the FIX engine.
#fix_app = start_fix_engine()

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
    price: float

@app.get("/")
def root():
    return {"msg": "Hello"}

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.system_used_id = str(db_user.id).zfill(9)  # SIX DIGITS PADDED with 9 characters

    return {"msg": "registered", "system_used_id": db_user.system_used_id}  # Optional for testing

@app.post("/token")
def login(form_data: TokenRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/execute-trade")
async def execute_trade(req: TradeRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cash_bound = bind_cash(user.id, req.symbol, req.quantity, req.price)
    if not cash_bound:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    try:
        trade = Trade(
            symbol=req.symbol,
            quantity=req.quantity,
            side=req.side,
            price=req.price,
            status="pending",
            user_id=user.id
        )
        db.add(trade)
        db.commit()
        db.refresh(trade)

        response = await send_order_rest(req.symbol, req.quantity, req.side, req.price, user.id)
        trade.status = response.get("status", "unknown")
        trade.broker_order_id = response.get("broker_order_id", None)
        db.commit()

        finalize_cash(user.id, req.symbol, req.quantity, req.price)
        return {"status": trade.status, "trade_id": trade.id}

    except Exception as e:
        #rollback_cash_reservation(user.id, req.symbol, req.quantity, req.price)
        raise HTTPException(status_code=500, detail=str(e))


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
        reload=True)
