# Responder: A Familiar HTTP Service Framework

Responder is a web framework for Python that flips [Requests](/software/requests) inside out. If Requests is how you consume HTTP, Responder is how you serve it — using the same mental model.

    $ uv pip install responder

## What It Looks Like

```python
import responder

api = responder.API()

@api.route("/")
def home(req, resp):
    resp.html = "<h1>Hello, world.</h1>"

@api.route("/api/data")
def data(req, resp):
    resp.media = {"message": "Hello from Responder", "status": "ok"}

@api.route("/greet/{name}")
async def greet(req, resp, *, name):
    resp.text = f"Hello, {name}!"

if __name__ == "__main__":
    api.run()
```

`resp.text` sends text. `resp.html` sends HTML. `resp.media` sends JSON. The `async` keyword is optional — use it when you need it, skip it when you don't.

## Built-In Batteries

```python
import responder

api = responder.API()

# Built-in background tasks.
@api.route("/upload")
async def upload(req, resp):
    data = await req.media()

    @api.background.task
    def process(data):
        # This runs after the response is sent.
        expensive_operation(data)

    process(data)
    resp.media = {"status": "processing"}

# GraphQL support out of the box.
import graphene

class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="world"))
    def resolve_hello(self, info, name):
        return f"Hello, {name}!"

schema = graphene.Schema(query=Query)
api.add_route("/graph", schema)

# OpenAPI schema generation.
# Visit /docs for interactive API documentation.

# WebSocket support.
@api.route("/ws", websocket=True)
async def websocket(ws):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text(f"Echo: {data}")
```

Background tasks, GraphQL, WebSockets, OpenAPI docs, and Jinja2 templates — all built in. No extensions to install. No configuration to fumble with.

## The Idea

I wanted to take the API primitives from Requests and put them into a web framework. The niceties of Flask and the performance philosophy of Falcon, unified with a Requests-like interface for responses. Setting `resp.content` sends bytes. Setting `resp.media` sends JSON. Case-insensitive headers. Familiar status codes. If you know Requests, you already know half of Responder.

It was a bit ahead of its time. Some of these ideas — automatic async handling, type-aware serialization, built-in OpenAPI — showed up later in FastAPI, which I'd recommend for production use today. Responder was always more of an experiment in API design than a production framework. But as an exercise in "what if the server-side felt like the client-side?" I think it holds up.

The deeper question Responder tried to answer: why do we accept that consuming an API and serving an API should feel like completely different activities? They're the same protocol. The mental model should be the same.

## Install

```bash
$ uv pip install responder
```

## Resources

- [Documentation](https://responder.kennethreitz.org/)
- [Source Code on GitHub](https://github.com/kennethreitz/responder)
- [Python Package Index](https://pypi.org/project/responder/)

## Related

- [**Requests**](/software/requests) — The client-side library whose philosophy Responder mirrors.
- [**From HTTP to Consciousness**](/essays/2025-08-27-from_http_to_consciousness) — The design thinking behind both libraries.
- [**Programming as Spiritual Practice**](/essays/2025-08-26-programming_as_spiritual_practice) — Building tools as a contemplative act.
