
# Fast Api
````markdown
# 🚀 FastAPI – All API Types Example (13 Types)

This project demonstrates different API types using **FastAPI** + extensions.  
Covers REST, WebSockets, Webhooks, SSE, GraphQL, gRPC, SOAP, and more.

---

## 🔹 1. REST API
**Description:** Standard request–response API over HTTP.  
**Use Cases:** CRUD apps, microservices, integrations.

**Code:**
```python
@app.get("/rest")
def rest_example():
    return {"message": "Hello from REST API!"}
````

**Request:**

```http
GET /rest
```

**Response:**

```json
{ "message": "Hello from REST API!" }
```

---

## 🔹 2. WebSocket API

**Description:** Real-time, two-way communication.
**Use Cases:** Chat apps, multiplayer gaming, live dashboards.

**Code:**

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You said: {data}")
```

**Client Example (JS):**

```js
const ws = new WebSocket("ws://127.0.0.1:8000/ws");
ws.onmessage = e => console.log(e.data);
ws.send("Hello");
```

---

## 🔹 3. Webhook API

**Description:** Event-driven callback – server sends POST requests to your app.
**Use Cases:** Payments (Stripe), GitHub events, Slack bots.

**Code:**

```python
@app.post("/webhook")
async def webhook_listener(request: Request):
    payload = await request.json()
    print("Webhook received:", payload)
    return {"status": "received", "data": payload}
```

**Request:**

```http
POST /webhook
Content-Type: application/json

{ "event": "payment_success", "amount": 100 }
```

**Response:**

```json
{ "status": "received", "data": { "event": "payment_success", "amount": 100 } }
```

---

## 🔹 4. Server-Sent Events (SSE)

**Description:** One-way streaming from server → client.
**Use Cases:** Live feeds, sports scores, IoT dashboards.

**Code:**

```python
async def event_stream():
    for i in range(5):
        yield f"data: Server message {i}\n\n"
        await asyncio.sleep(1)

@app.get("/sse")
async def sse_endpoint():
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

**Response Stream:**

```
data: Server message 0
data: Server message 1
...
```

---

## 🔹 5. GraphQL API

**Description:** Client defines the data it needs.
**Use Cases:** Complex UIs, flexible queries, data aggregation.

**Code (Strawberry):**

```python
@strawberry.type
class Query:
    hello: str = "Hello from GraphQL!"
    ping: str = "pong"

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
```

**Query:**

```graphql
{
  hello
  ping
}
```

**Response:**

```json
{ "data": { "hello": "Hello from GraphQL!", "ping": "pong" } }
```

---

## 🔹 6. gRPC API

**Description:** High-performance binary protocol using HTTP/2.
**Use Cases:** Microservices, streaming, low-latency APIs.

**.proto file (example):**

```proto
syntax = "proto3";

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply);
}

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

**Server (Python, grpcio):**

```python
import grpc
from concurrent import futures
import helloworld_pb2, helloworld_pb2_grpc

class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message=f"Hello {request.name}")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()
```

---

## 🔹 7. SOAP API

**Description:** XML-based protocol, used in enterprise.
**Use Cases:** Banking, legacy integrations.

**Server (Spyne):**

```python
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class SoapService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def say_hello(ctx, name):
        return f"Hello {name}"

application = Application([SoapService], 'soap.example',
    in_protocol=Soap11(), out_protocol=Soap11())
soap_app = WsgiApplication(application)
```

---

## 🔹 8. Composite API

**Description:** Combines multiple services in one response.
**Use Cases:** Travel booking (flight + hotel + car).

**Example (REST + GraphQL merge):**

```python
@app.get("/composite")
def composite():
    return {
        "user": {"id": 1, "name": "Alice"},
        "orders": [{"id": 101, "item": "Book"}, {"id": 102, "item": "Laptop"}]
    }
```

---

## 🔹 9. Open API

**Description:** Public APIs available to anyone.
**Use Cases:** OpenWeather, Twitter, GitHub API.

> In FastAPI → just expose routes without auth, document with OpenAPI.

---

## 🔹 10. Partner API

**Description:** Shared with trusted partners only.
**Use Cases:** Payment gateways, B2B integrations.

**Implementation:**

* Use API keys or OAuth2 in FastAPI.

---

## 🔹 11. Internal (Private) API

**Description:** Used only inside the company.
**Use Cases:** Netflix recommendation engine APIs.

**Implementation:**

* Deploy behind firewall or require internal VPN.

---

## 🔹 12. Event-driven API (Webhooks, Pub/Sub)

Already covered **Webhooks + SSE + WebSockets**.
For Pub/Sub → use message brokers (Kafka, RabbitMQ).

---

## 🔹 13. RPC (JSON-RPC / XML-RPC)

**Description:** Call methods like local functions.
**Use Cases:** Blockchain (Bitcoin JSON-RPC).

**Example (JSON-RPC in FastAPI):**

```python
@app.post("/rpc")
async def rpc_endpoint(request: Request):
    data = await request.json()
    if data["method"] == "ping":
        return {"jsonrpc": "2.0", "result": "pong", "id": data["id"]}
```

**Request:**

```json
{ "jsonrpc": "2.0", "method": "ping", "id": 1 }
```

**Response:**

```json
{ "jsonrpc": "2.0", "result": "pong", "id": 1 }
```

---

## ▶️ Run the App

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

**Endpoints:**

* REST → `/rest`
* WebSocket → `/ws`
* Webhook → `/webhook`
* SSE → `/sse`
* GraphQL → `/graphql`
* RPC → `/rpc`

For **gRPC** → run separate server (`python grpc_server.py`).
For **SOAP** → mount Spyne app with `WSGIMiddleware`.

---
