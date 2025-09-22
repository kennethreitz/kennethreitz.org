# Responder: a Familiar Web Framework

Responder is a web framework for Python. It is highly experimental and is not recommended for production use. I
personally consider this project to be an academic exercise, and recommend reading through the code, however!

<span class="sidenote">Responder pioneered several concepts that later appeared in FastAPI, including automatic async/await handling and type-aware response serialization. While it never reached production maturity, its ideas influenced the evolution of modern Python web frameworks.</span>

I think it was a little ahead of its time. FastAPI is a more mature and production-ready alternative.

## The Basic Idea

The primary concept here is to bring the niceties that are brought forth from both Flask and Falcon and unify them into a single framework, along with some new ideas I have. I also wanted to take some of the API primitives that are instilled in the Requests library and put them into a web framework. So, you'll find a lot of parallels here with Requests.

- Setting `resp.content` sends back bytes.
- Setting `resp.text` sends back unicode, while setting resp.html sends back HTML.
- Setting `resp.media` sends back JSON/YAML (`.text`/`.html`/`.content` override this).
- Case-insensitive `req.headers` dict (from Requests directly).
- `resp.status_code`, `req.method`, `req.url`, and other familiar friends.
- The `async` keyword is optional for route functions. You must use `await` within any route that is reading from the network.

## Installation

```bash
$ uv pip install responder
```

## Example Application

Here's a simple web application built with Responder:

```python
import responder

# Create an API instance
api = responder.API()

# Basic route with dynamic parameter
@api.route("/{greeting}")
async def greet_world(req, resp, *, greeting):
    resp.text = f"{greeting}, world!"

# Return JSON data
@api.route("/data")
def get_data(req, resp):
    resp.media = {"message": "Hello from Responder!", "status": "success"}

# Serve a simple HTML page
@api.route("/")
def home(req, resp):
    resp.html = "<h1>Welcome to Responder</h1><p>A familiar web framework for Python.</p>"

# Run the application
if __name__ == '__main__':
    api.run()
```

<span class="sidenote">This example demonstrates Responder's core philosophy: familiar Requests-like semantics applied to web responses. The pattern of setting `resp.text`, `resp.media`, and `resp.html` mirrors how you might work with a requests Response object, but in reverse.</span>

## Status

I wanted to reboot this project, but I think FastAPI is a better choice for most people. I recommend using that instead.

## The Code

https://github.com/kennethreitz/responder
