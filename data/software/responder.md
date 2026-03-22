# Responder: A Familiar HTTP Service Framework

Responder is a web framework for Python that flips [Requests](/software/requests) inside out. If Requests is how you consume HTTP, Responder is how you serve it, using the same mental model.

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

`resp.text` sends text. `resp.html` sends HTML. `resp.media` sends JSON. `req.headers` is a case-insensitive dict, just like in Requests. The `async` keyword is optional. If you know Requests, you already know half of Responder.

## The Idea

I wanted to take the API primitives from Requests and put them into a web framework. The niceties of Flask and the performance philosophy of Falcon, unified with a Requests-like interface for responses. Setting `resp.content` sends bytes. Setting `resp.media` sends JSON. Case-insensitive headers. Familiar status codes.

It was a bit ahead of its time. Some of these ideas, like automatic async handling and type-aware serialization, showed up later in FastAPI, which I'd recommend for production use today. Responder was always more of an experiment in API design than a production framework. But as an exercise in "what if the server-side felt like the client-side?" I think it holds up.

## Install

```bash
uv pip install responder
```

## Resources

- [Documentation](https://responder.kennethreitz.org)
- [Source Code on GitHub](https://github.com/kennethreitz/responder)

## Related

- [**Requests**](/software/requests) — The client-side library whose philosophy Responder mirrors.
- [**From HTTP to Consciousness**](/essays/2025-08-27-from_http_to_consciousness) — The design thinking behind both libraries.
