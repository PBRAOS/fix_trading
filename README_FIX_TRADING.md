# 📈 FIX Trading Platform

A containerized Python-based trading service that:

- Exposes a REST API via FastAPI
- Uses QuickFIX for FIX protocol trading
- Supports user registration, login, and per-user trade tracking
- Stores all data in PostgreSQL
- Can be run with Docker Compose or deployed to Azure

---

## 🏗️ System Architecture

```
                    +-------------------+
                    |  Web Client / CLI |
                    +--------+----------+
                             |
                             v
                    +--------+----------+
                    |     FastAPI App   |
                    |  (REST API + FIX) |
                    +--------+----------+
                             |
          +------------------+------------------+
          |                                     |
          v                                     v
+---------------------+             +----------------------+
|     PostgreSQL DB   |             |    FIX Broker/Server |
| (users + trades ORM)|             |   (via QuickFIX TCP) |
+---------------------+             +----------------------+
```

---

## 🔐 Authentication

- JWT tokens using OAuth2 password flow
- `/register` to create new user
- `/token` to log in and receive token
- Swagger UI supports JWT auth via 🔐 Authorize button

---

## 🔧 API Endpoints

| Method | Endpoint        | Description                    |
|--------|------------------|--------------------------------|
| POST   | `/register`      | Register new user              |
| POST   | `/token`         | Authenticate and get JWT token |
| POST   | `/execute-trade` | Submit a new trade             |
| GET    | `/trades`        | View user’s trade history      |

---

## 🗃️ Database Schema

- `users`: id, email, hashed_password
- `trades`: id, symbol, quantity, side, user_id, status, created_at

---

## 🧪 Testing Locally

```bash
docker-compose up --build
```

API available at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 FIX Integration

- Sends FIX messages using QuickFIX engine
- Configured with `app/trade.cfg`
- Comes with mock FIX server for local testing

---

## 🌐 Azure Deployment

Deploy using `azure-deployment.yaml` with Azure Container Apps.

---

## 🧪 Postman Collection

Import `fix_trading_postman_collection.json` to try:
- Register
- Get token
- Place trade
- View trades

---

## 📦 Stack

- FastAPI
- QuickFIX (Python binding)
- PostgreSQL
- SQLAlchemy ORM
- JWT Auth (python-jose, passlib)
- Docker + Docker Compose

---
