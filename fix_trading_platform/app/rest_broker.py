import httpx

BROKER_API_URL = "http://localhost:9000/orders"

async def send_order_rest(symbol, quantity, side, price, user_id):
    payload = {
        "symbol": symbol,
        "quantity": quantity,
        "side": side,
        "price": price,
        "user_id": user_id
    }

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.post(BROKER_API_URL, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"Broker returned error: {e.response.text}")
        except httpx.RequestError as e:
            raise Exception(f"Network error contacting broker: {str(e)}")
