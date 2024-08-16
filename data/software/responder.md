# Responder: a Familiar Web Framework

Responder is a web framework for Python. It is highly experimental and is not recommended for production use. I
personally consider this project to be an academic exercise, and recommend reading through the code, however!

I think it was a little ahead of its time. FastAPI is a more mature and production-ready alternative.

## The Basic Idea

The primary concept here is to bring the niceties that are brought forth from both Flask and Falcon and unify them into a single framework, along with some new ideas I have. I also wanted to take some of the API primitives that are instilled in the Requests library and put them into a web framework. So, you'll find a lot of parallels here with Requests.

- Setting `resp.content` sends back bytes.
- Setting `resp.text` sends back unicode, while setting resp.html sends back HTML.
- Setting `resp.media` sends back JSON/YAML (`.text`/`.html`/`.content` override this).
- Case-insensitive `req.headers` dict (from Requests directly).
- `resp.status_code`, `req.method`, `req.url`, and other familiar friends.
- The `async` keyword is optional for route functions. You must use `await` within any route that is reading from the network.

## Status

I wanted to reboot this project, but I think FastAPI is a better choice for most people. I recommend using that instead.

Honestly, I wrote this code in a month while I was taking perscription ADHD meds, years ago, and I don't remember much about it. I recommend reading through the code, though!

## The Code

https://github.com/kennethreitz/responder
