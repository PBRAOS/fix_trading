1. api (FastAPI app)
Role: Main backend application (FastAPI) that handles:
User registration and login
JWT-protected trade execution
Communication with db and mock_broker
Expected Behavior:
Starts on http://localhost:8000 with Swagger UI at /docs
Connects to db on startup and prints Connected to PostgreSQL

Allows me to:
POST to /register with an email/password
POST to /token to get a JWT token
POST to /execute-trade to trigger an order (requires token)
GET from /trades to view own trades
When /execute-trade is called:

Validates and binds cash

Logs trade to DB
Sends HTTP POST to mock_broker:9000/orders
Updates or rolls back cash based on response

2. db (MS SQL)
Role: Relational database for storing users and trades.
Expected Behavior:
Exposes MSSQL on localhost:1433
Accepts connections from api via:

bash
Copy
Edit
mssql+pyodbc://MySQL:Fraoules12@mssql:1433/db?driver=ODBC+Driver+17+for+SQL+Server


Stores:
Users (users table)
Trades (trades table)
Cash reservations (if I've added that table)

3. mock_broker (Mock REST broker)
Role: Simulates an external broker system receiving trade orders via REST.

Expected Behavior:
Starts on http://localhost:9000
Accepts POST requests to /orders with trade JSON
Responds with:
json
Copy
Edit
{
  "status": "accepted",
  "broker_order_id": "some-uuid"
}
Logs received trades to console
Returns 400 errors for invalid input (e.g., quantity ≤ 0)

