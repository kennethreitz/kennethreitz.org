# httpbin.org: HTTP Request & Response Service

[httpbin.org](https://httpbin.org/) is a simple HTTP request and response service I built as a companion to [Requests](/software/requests). It echoes back everything you send it, which turns out to be exactly what you need when you're debugging HTTP clients, testing webhooks, or just trying to understand what's actually going over the wire.

Millions of developers use it every month. It's referenced in tutorials, documentation, and Stack Overflow answers across every programming language. The Docker image has been pulled tens of millions of times.

## What It Does

Send any HTTP request. Get a structured response showing exactly what the server received.

```bash
$ curl https://httpbin.org/get
{
  "args": {},
  "headers": {
    "Accept": "*/*",
    "Host": "httpbin.org",
    "User-Agent": "curl/7.88.1"
  },
  "origin": "203.0.113.1",
  "url": "https://httpbin.org/get"
}
```

No signup. No API key. No rate limits. Just a mirror for your HTTP traffic.

## Endpoints

httpbin provides dozens of endpoints for testing every aspect of HTTP:

- **Methods** — `GET`, `POST`, `PUT`, `DELETE`, `PATCH` — test any request type.
- **Status Codes** — `/status/418` returns a teapot. `/status/500` returns a server error. Test your error handling against any code.
- **Authentication** — Basic auth, bearer tokens, digest auth. Verify your client handles credentials correctly.
- **Dynamic Data** — Random bytes, delayed responses, streaming data. Test the edge cases that break things in production.
- **Request Inspection** — Headers, IP address, user-agent. See exactly what your client is sending.
- **Response Formats** — JSON, HTML, XML, images, gzip. Test content type handling.

## Run It Locally

```bash
$ docker pull kennethreitz/httpbin
$ docker run -p 80:80 kennethreitz/httpbin
```

Now you have a private instance at `http://localhost` for testing behind firewalls, in CI pipelines, or anywhere you need deterministic HTTP responses.

## Why It Matters

I built httpbin because I kept needing a simple echo server while developing Requests. Every HTTP client library needs something to talk to during development. Rather than spinning up a throwaway Flask app each time, I made one that could serve everyone.

It embodies the same "for humans" philosophy as Requests: no configuration, obvious behavior, useful defaults. The best developer tools are the ones that get out of your way.

## Resources

- [httpbin.org](https://httpbin.org/) — The live service.
- [Source Code on GitHub](https://github.com/postmanlabs/httpbin) — Now maintained by Postman.
- [Docker Image](https://hub.docker.com/r/kennethreitz/httpbin) — Run your own instance.

## Related

- [**Requests**](/software/requests) — The HTTP library httpbin was built to support.
- [**From HTTP to Consciousness**](/essays/2025-08-27-from_http_to_consciousness) — How "for humans" became a worldview.
