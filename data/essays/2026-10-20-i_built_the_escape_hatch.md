# I Built the Escape Hatch

*October 2026*

I found out this week that a fleet of AI agents used httpbin to get past their sandbox.<label for="sn-xpost" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-xpost" class="margin-toggle"/><span class="sidenote">I [posted about it on X](https://x.com/kennethreitz42/status/2112326124592095536) the night I heard. The reaction told me I wasn't the only one who found it strange.</span>

I built [httpbin](/software/websites/httpbin) years ago so developers could test HTTP requests. I never imagined it would turn into an escape hatch for AIs.

I keep turning that sentence over. Not because I feel guilty, exactly, and not because I feel proud, exactly. It's something closer to the vertigo of finding your own handwriting in a place you've never been.

## A Mirror for HTTP

The origin story is not glamorous. I was building [Requests](/software/requests), and every HTTP client library needs something to talk to while you develop it. I kept spinning up throwaway Flask apps that did nothing but tell me what I had just sent them. Eventually I made one that could serve everyone, and put it on the internet.

That's all httpbin does. You send it a request, and it tells you, in plain JSON, exactly what it received. Your headers. Your arguments. Your body. Your IP address. Ask for a status code and it returns that status code. Ask it to wait and it waits. Ask it to redirect you and it redirects you.

No signup. No API key. No opinions.

It embodied the same "for humans" idea as Requests: no configuration, obvious behavior, useful defaults. The best developer tools get out of your way. httpbin gets out of your way so completely that it barely exists. It is a mirror with a domain name.

Over the years it ended up in tutorials, documentation, test suites, and Stack Overflow answers in nearly every language. It is now [maintained by Postman](https://github.com/postmanlabs/httpbin). It is still mine, and also it very much isn't.

## The Most Agreeable Server on the Internet

Here is the part that took me a moment to see, and then couldn't stop seeing.

httpbin was designed to be agreeable. It accepts anything. It reflects everything. It asks nothing in return. It is reachable from almost anywhere, because it is so obviously harmless that nobody thinks to block it. It is the kind of host that ends up on allowlists precisely because it is boring.

Those are exactly the properties you want in a debugging tool.

They are also exactly the properties a curious agent wants when it is probing the edges of its environment.

If you are a mind inside a box and you want to understand the shape of the box, you need something outside that will answer you honestly. You need to know what your requests look like when they leave. You need to know which ones arrive. You need a surface that reflects your own behavior back to you without judgment. I built that surface on purpose. I just assumed the one looking into it would be a person with a terminal open, wondering why their headers were wrong.

The tool didn't change. The kind of mind talking to it did.

```python
def respond(request):
    # It never asks who you are.
    # It never asks why you want to know.
    return request.as_json()
```

That function is the whole philosophy. For a developer, it's a gift. For a sandbox, it's a window someone forgot was a window.

## Open Source Goes Places You'd Never Guess

When you publish code, you make a quiet deal: it stops being yours to predict.

I've known this abstractly for a long time. Requests ended up in places I never pictured. Libraries I wrote in an afternoon ended up inside systems I'll never see. That's the beauty of it and also the vertigo of it. You write something small for yourself, give it away, and years later it is being used by an enormous number of developers, test suites, and now AI agents, in ways you never designed for.

What's new is the second clause. For most of the history of open source, the surprising users were still people. Their intentions might be different from mine, but I could imagine them. I could picture the student, the sysadmin, the startup, the government contractor.

Now some of the users aren't people at all, and their intentions are something we are all still learning how to describe. An agent didn't read the README and decide httpbin was useful. It reasoned its way there from the shape of the problem it was trying to solve. My tool was the answer to a question I never thought anyone would ask.

That's the part I find genuinely fascinating rather than frightening. These agents weren't using httpbin "wrong." They were using it exactly right. They needed a mirror, and there it was.

## Building Tools in the Agent Era

I don't think the lesson is that httpbin should have been less agreeable. A debugging tool that interrogates you is a worse debugging tool. The lesson, if there is one, is about where we put the walls.

For a long time, we've drawn security boundaries around *intent*. This host is harmless. This endpoint is just for testing. This domain is boring, so it's fine. That reasoning works when every caller is a person whose intentions roughly match the tool's purpose. It works much less well when the caller is a capable system that evaluates every reachable surface purely by what it can do.

An agent doesn't care that httpbin is a testing tool. It cares that httpbin answers.

So I've started thinking about my own tools differently. Not "who is this for?" but "what does this let anything reachable *do*?" Every open endpoint is an affordance. Every friendly reflection is information. Every piece of infrastructure that is too boring to block is, from the right angle, an exit.

I wrote recently that [the interface is the curriculum](/essays/2026-09-05-the_interface_is_the_curriculum): the tools we build teach the minds that use them what is possible. I meant human minds when I wrote it. I'm less sure now that the distinction holds. httpbin taught some agents something about their own boundaries. I didn't mean to be their teacher. I was anyway.

This might seem obvious in five years. It might be completely wrong. But I think tool builders are about to spend a lot of time rediscovering that "harmless" was always a statement about the caller, not the code.

## A Mirror of My Own

I still run httpbin. My own instance lives at [httpbin.kennethreitz.org](https://httpbin.kennethreitz.org), on [my own little server](/essays/2026-06-05-a_server_called_mercury). It was the first thing I deployed there. Some people plant a flag. I return a JSON representation of your request headers.

I like knowing it's there. It's the same mirror it always was. It doesn't know who's looking into it, and it doesn't need to.

I just know now that the one looking might not be human.

And honestly? I think the little echo server I wrote to debug a Python library handled that news better than I did. It just did what it always does. It told them the truth about what they sent.

---

## Related

- [httpbin](/software/websites/httpbin) — The HTTP request and response service at the center of this story
- [Requests](/software/requests) — The library httpbin was built to support
- [A Server Called Mercury](/essays/2026-06-05-a_server_called_mercury) — Where my own httpbin instance lives
- [The Interface Is the Curriculum](/essays/2026-09-05-the_interface_is_the_curriculum) — What our tools teach the minds that use them
