# The Art of Naming Things in Code
*September 2025*

There are only two hard things in Computer Science: cache invalidation and naming things. 

I mean, that's the joke, right? But I keep thinking about why naming is actually hard. It's not just about picking words. It's about consciousness, language, and this weird responsibility we have to create shared meaning.

Every time I stare at a blank function definition, cursor blinking after `def `, I'm reminded of this. What do you call something that doesn't quite exist yet? It's like trying to describe a dream while you're still dreaming it.

## From Frustration to Philosophy

So, funny story. The original name for what became Requests wasn't "HTTP for Humans"—it was "HTTP for Python that doesn't suck." 

Charming, right?

Looking back, that name captured my frustration perfectly. But it was defining the project by what it opposed rather than what it wanted to become. Classic teenage rebellion energy: loud, accurate, and ultimately limiting.

It took a few tries to arrive at "HTTP for Humans". That shift wasn't just better branding—it was a different way of seeing the problem entirely.

"For humans" centered the human rather than the technology. And that naming choice shaped everything that followed: API design, documentation philosophy, community culture. The name wasn't just describing what the code did—it was declaring what we cared about.

## How Names Shape Thinking

Here's what I've noticed about naming in code: it's this recursive thing where language shapes thought, programmers shape code, and code shapes how millions of other programmers think about problems.

Consider the difference between these function names:

```python
def get_url_for_profile():
    # Verbose but clear about what it does
    pass

def profile_url():
    # Clean, direct, trusts the reader
    pass
```

Same functionality, completely different philosophies. The first is verbose and procedural—it tells you exactly what steps it's taking. The second is clean and declarative—it trusts you to understand that `profile_url()` will give you what you need. One assumes you need hand-holding; the other assumes you're intelligent.

When thousands of developers use your API, they're not just calling your functions—they're thinking with your thoughts. The names you choose become the concepts they use to understand their problem space. You're not just writing code; you're writing the language future programmers will think in<label for="sn-recursive-thinking" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-recursive-thinking" class="margin-toggle"/><span class="sidenote">This connects to the broader theme of [The Recursive Loop](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds)—programmer consciousness shapes collective consciousness through the interfaces and abstractions we create.</span>.

No pressure, right?

This is probably why naming feels so hard. You're not just solving a labeling problem. You're creating the mental architecture other people will use to navigate complexity.

## Why Names Matter More Than We Think

Douglas Adams got something important about language: naming creates reality, it doesn't just describe it. When you name something in code, you're defining what kind of thing it is, how it relates to everything else, what operations make sense on it.

Take the simple act of choosing between `user`, `person`, `human`, or `individual`:

- `user` implies consumption and interaction with a system.
- `person` implies social and legal recognition.
- `human` implies biological and conscious reality.
- `individual` implies distinctness and autonomy.

Your choice propagates through every function that touches that concept. Methods like `user.authenticate()` make sense, but `human.authenticate()` feels weird—people don't authenticate, they identify themselves.

The name shapes what feels natural to build next<label for="sn-constraints-enable" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-constraints-enable" class="margin-toggle"/><span class="sidenote">Good naming constraints actually force clarity of thought. When you can't figure out what to call something, it's usually because you don't understand what it actually is yet.</span>.

## Naming as an Act of Care

I think good naming is basically an act of compassion. You're being kind to the confused person who's going to encounter your code at 2 AM. That person might be you, six months from now, when all the context has evaporated and only the names are left to guide you.

This connects to the broader ["for humans" philosophy](/themes/for-humans-philosophy)—technology should serve human mental models, not the other way around. Names are really the primary interface between how humans think and how code is structured.

Consider the difference between:

```python
# Machine-optimized naming
def proc_usr_auth_req(uid, pwd_hash):
    """Process user authentication request."""
    if validate_creds(uid, pwd_hash):
        return gen_sess_token(uid)
    return auth_err_resp()

# Human-optimized naming  
def authenticate_user(email, password_hash):
    """Verify someone's identity and create a session."""
    if credentials_are_valid(email, password_hash):
        return create_session_for(email)
    return authentication_failed()
```

The machine doesn't care either way. But humans reading the second version can actually breathe easier—the names carry the mental model along with them.

## Finding Names That Last

The best names age well. `requests.get()` started simple—get something from a URL. But the name scaled: get JSON, get with authentication, get with custom headers. The verb "get" carried the right weight for all these variations.

Compare that with `XMLHttpRequest` in JavaScript, which handles JSON more often than XML these days. That name carries historical baggage that misleads more than it helps.

There's an art to choosing names that are specific enough to be meaningful but general enough to evolve. Names that point toward what something *is* rather than how it's implemented.

## Creating Shared Understanding

Every programmer has their Adam moment when creating primary abstractions. When you name a class `PaymentProcessor`, future developers will ask: "Where does the PaymentProcessor handle refunds?" rather than "Where do we handle refunds?" The name shapes the questions, which shapes the thinking.

You're not just labeling—you're creating the conceptual framework through which others will navigate complexity.

## When Names Feel Just Right

Sometimes you stumble across names that feel inevitable. Like `requests.Session`—of course that's what you'd call a persistent context for HTTP interactions. These work because they align with how humans naturally think about the problem.

When you're working in uncharted territory, sometimes you borrow metaphors: "Orchestrator" from music, "Factory" from manufacturing<label for="sn-metaphor-scaffolding" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-metaphor-scaffolding" class="margin-toggle"/><span class="sidenote">The danger is when metaphors become prisons—when you can't see possibilities outside the metaphor's constraints. Good metaphors illuminate; bad metaphors obscure.</span>. These give people conceptual scaffolding.

And look, sometimes you need to call something `ProcessorThingy` just to keep moving. The perfect name will emerge as you understand the problem better—except when it doesn't, and your temporary name becomes permanent through inertia.

Names are hypotheses about reality. They should evolve as your understanding evolves.

## Small Acts of Kindness

At the end of the day, I think good naming is an act of love. Love for the future programmers who will inherit your choices. Love for clarity. Love for the idea that code should serve human understanding, not the other way around.

When you choose `calculate_compound_interest` over `calc_ci`, you're being kind to whoever has to maintain that function at 3 AM. When you choose `requests.Session` over `HTTPStatefulManager`, you're choosing clarity over cleverness.

These small acts of care add up. The names you choose today shape the thoughts that get thought tomorrow.

## Why This Matters

So here's what I think is actually happening: naming things is how consciousness creates shared meaning. Every name you choose becomes part of the conceptual infrastructure other people use to navigate complexity. You're not just labeling variables—you're creating the language future problems get solved in.

It's this recursive thing: better names enable clearer thinking, clearer thinking produces better code, better code creates more intuitive abstractions. And maybe that's where the real magic is—technology that serves human consciousness instead of exploiting it.

Like Douglas Adams said, we're capable of building bridges across the incomprehensible spaces between minds. Sometimes those bridges are made of nothing more than perfectly chosen words.

But hey, I could be totally wrong about all this. :)

---

## Related Reading

### On This Site
- **[The Recursive Loop: How Code Shapes Minds](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds)** - How programmer consciousness shapes collective consciousness
- [The "For Humans" Philosophy](/themes/for-humans-philosophy) - Design principles that serve human mental models
- [Programming as Spiritual Practice](/essays/2025-08-26-programming_as_spiritual_practice) - Contemplative approaches to technical work
- [Building Rapport with Your AI](/essays/2025-08-26-building_rapport_with_your_ai) - Conscious collaboration through careful communication

### External Resources
- *The Design of Everyday Things* by Donald Norman - How naming and labeling shape user understanding
- *Code Complete* by Steve McConnell - Comprehensive guide to variable naming and code clarity
- *Domain-Driven Design* by Eric Evans - How language shapes software architecture
- *The Hitchhiker's Guide to the Galaxy* by Douglas Adams - The absurd responsibility of creating meaning

---

