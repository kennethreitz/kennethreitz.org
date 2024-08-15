# Responder: a Familiar Web Framework

Responder is a web framework for Python. It is highly experimental and is not recommended for production use.

## The Basic Idea

The primary concept here is to bring the niceties that are brought forth from both Flask and Falcon and unify them into a single framework, along with some new ideas I have. I also wanted to take some of the API primitives that are instilled in the Requests library and put them into a web framework. So, you'll find a lot of parallels here with Requests.

- Setting `resp.content` sends back bytes.
- Setting `resp.text` sends back unicode, while setting resp.html sends back HTML.
- Setting `resp.media` sends back JSON/YAML (`.text`/`.html`/`.content` override this).
- Case-insensitive `req.headers` dict (from Requests directly).
- `resp.status_code`, `req.method`, `req.url`, and other familiar friends.

https://github.com/kennethreitz/responder
