from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import StreamingResponse
import asyncio
import strawberry
from strawberry.fastapi import GraphQLRouter

app = FastAPI(title="All API Types Example")

# --------------------------
# 1. REST API
# --------------------------
@app.get("/rest")
def rest_example():
    return {"message": "Hello from REST API!"}

# --------------------------
# 2. WebSocket API
# --------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You said: {data}")

# --------------------------
# 3. Webhook API
# --------------------------
@app.post("/webhook")
async def webhook_listener(request: Request):
    payload = await request.json()
    print("Webhook received:", payload)
    return {"status": "received", "data": payload}

# --------------------------
# 4. SSE (Server-Sent Events)
# --------------------------
async def event_stream():
    for i in range(5):
        yield f"data: Server message {i}\n\n"
        await asyncio.sleep(1)

@app.get("/sse")
async def sse_endpoint():
    return StreamingResponse(event_stream(), media_type="text/event-stream")

# --------------------------
# 5. GraphQL API
# --------------------------
@strawberry.type
class Query:
    hello: str = "Hello from GraphQL!"
    ping: str = "pong"

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# --------------------------
# 6. Composite API
# --------------------------
@app.get("/composite")
def composite():
    return {
        "user": {"id": 1, "name": "Alice"},
        "orders": [{"id": 101, "item": "Book"}, {"id": 102, "item": "Laptop"}]
    }

# --------------------------
# 7. JSON-RPC API
# --------------------------
@app.post("/rpc")
async def rpc_endpoint(request: Request):
    data = await request.json()
    if data.get("method") == "ping":
        return {"jsonrpc": "2.0", "result": "pong", "id": data.get("id")}
    return {"jsonrpc": "2.0", "error": "Method not found", "id": data.get("id")}
