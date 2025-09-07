# The Art of Naming Things in Code
*September 2025*

There are only two hard things in Computer Science: cache invalidation and naming things. The first one will eventually be solved by smarter algorithms and faster hardware. The second one? That's fundamentally about consciousness, language, and the strange responsibility of creating shared meaning in an indifferent universe.

I learned this when I was building what would become the Requests library.

## From Frustration to Philosophy

The original name wasn't "HTTP for Humans"—it was "HTTP for Python that doesn't suck." Charming, right? The name captured my frustration, but it defined the project by what it opposed rather than what it aspired to create.


It took a few tries to arrive at "HTTP for Humans"<label for="sn-naming-evolution" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-naming-evolution" class="margin-toggle"/><span class="sidenote">This evolution mirrors how consciousness develops—from reactive opposition to proactive vision. First we know what we don't want, then we discover what we do want, then we learn to name it clearly enough that others can want it too.</span>. That shift wasn't just better branding—it was a different way of thinking about the problem.

"For humans" centered the human rather than the technology, and that naming choice shaped everything else. The name wasn't just describing what the code did—it was declaring what we cared about.

## How Names Shape Thinking

Here's the thing about naming in code: it's a recursive system where language shapes thought, programmers shape code, and code shapes how millions of other programmers think about problems.

Consider the difference between these function names:

```python
def get_url_for_profile():
    # Verbose but clear about what it does
    pass

def profile_url():
    # Clean, direct, trusts the reader
    pass
```

Same functionality, completely different philosophies embedded in the names. The first is verbose and procedural—it tells you exactly what steps it's taking. The second is clean and declarative—it trusts you to understand that accessing `profile_url()` will give you what you need.

When thousands of developers use your API, they're not just calling your functions—they're thinking with your thoughts. The names you choose become the concepts they use to understand their problem space. You're not just writing code; you're writing the language future programmers will think in<label for="sn-recursive-thinking" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-recursive-thinking" class="margin-toggle"/><span class="sidenote">This connects to the broader theme of [The Recursive Loop](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds)—programmer consciousness shapes collective consciousness through the interfaces and abstractions we create.</span>.

## Why Names Matter More Than We Think

Douglas Adams understood something profound about language: the act of naming creates reality rather than merely describing it. In *The Hitchhiker's Guide to the Galaxy*, the Babel fish doesn't just translate languages—it reveals that "the Universe is a lot more complicated than you might think, even if you start from a position of thinking it's pretty damn complicated."

Naming in code has this same ontological weight. When you name something, you're not just creating a reference—you're defining what kind of thing it is, how it relates to other things, and what operations make sense to perform on it.

Take the simple act of choosing between `user`, `person`, `human`, or `individual`:

- `user` implies consumption and interaction with a system.
- `person` implies social and legal recognition.
- `human` implies biological and conscious reality.
- `individual` implies distinctness and autonomy.

Your choice propagates through every function that touches that concept. Methods like `user.authenticate()` make sense, but `human.authenticate()` feels weird—humans don't authenticate, they identify themselves.

The name constrains and enables particular ways of thinking about the problem<label for="sn-constraints-enable" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-constraints-enable" class="margin-toggle"/><span class="sidenote">This is why constraints are often liberating in creative work—they provide structure that enables rather than restricts meaningful expression. Good naming constraints force clarity of thought.</span>.

## Naming as an Act of Care

Good naming is fundamentally an act of compassion—compassion for the confused soul who will encounter your code at 2 AM, possibly you, six months from now, when all context has evaporated and only the names remain to guide understanding.

This connects to the broader ["for humans" philosophy](/themes/for-humans-philosophy) that runs through all thoughtful software design. Technology should serve human mental models rather than forcing humans to adapt to machine logic. Names are the primary interface between human cognition and code structure.

Consider the difference between:

```python
# Machine-optimized naming
def proc_usr_auth_req(uid, pwd_hash):
    """Process user authentication request."""
    if validate_creds(uid, pwd_hash):
        return gen_sess_token(uid)
    return auth_err_resp()

# Human-optimized naming  
def authenticate_person(email, password_hash):
    """Verify someone's identity and create a session."""
    if credentials_are_valid(email, password_hash):
        return create_session_for(email)
    return authentication_failed()
```

The machine doesn't care either way. But human consciousness trying to understand the second version can breathe easier—the names carry the mental model along with them.

## Finding Names That Last

The best names have a quality of graceful evolution—they remain accurate as your understanding deepens, as the codebase grows, as new requirements emerge.

`requests.get()` has this quality. It started simple—get something from a URL. But the name scales: you can get JSON, get images, get with authentication, get with custom headers. The verb "get" carries the right semantic weight for all these variations without becoming misleading.

Compare that with names that painted themselves into corners: `XMLHttpRequest` in JavaScript, which now handles JSON more often than XML, or `ArrayList` in Java, which isn't always backed by an array. These names carry historical baggage that misleads more than it helps.

The art is choosing names that are specific enough to be meaningful but general enough to evolve. Names that point toward essence rather than implementation details. Names that invite rather than constrain.

## Creating Shared Understanding

Every programmer has their Adam moment when creating primary abstractions. When you name a class `PaymentProcessor`, future developers will ask: "Where does the PaymentProcessor handle refunds?" rather than "Where do we handle refunds?" The name shapes the questions, which shapes the thinking.

You're not just labeling—you're creating the conceptual framework through which others will navigate complexity.

## When Names Feel Just Right

Sometimes you stumble across names that just feel right, like `requests.Session`—of course that's what you'd call a persistent context for HTTP interactions.

When you're working in new domains, sometimes you borrow metaphors: "Orchestrator" from music, "Factory" from manufacturing<label for="sn-metaphor-scaffolding" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-metaphor-scaffolding" class="margin-toggle"/><span class="sidenote">The danger is when metaphors become prisons—when you can't see possibilities outside the metaphor's constraints. Good metaphors illuminate; bad metaphors obscure.</span>. Sometimes you invent terms entirely, but they must feel natural enough to stick.


Sometimes you need to call something `ProcessorThingy` to keep moving forward. The perfect name will emerge as understanding clarifies. The danger is when temporary names become permanent through inertia. Names are hypotheses about reality—they should evolve as your understanding evolves.

## Small Acts of Kindness

Good naming is an act of love—love for the future programmers who will inherit your choices, love for the clarity that makes complex systems comprehensible.

When you choose `calculate_compound_interest` over `calc_ci`, you're writing a love letter to the developer who needs to maintain that function at 3 AM. When you choose `requests.Session` over `HTTPStatefulManager`, you're writing a love letter to conceptual clarity.

These small acts of care compound. The names you choose today shape the thoughts that will be thought tomorrow.

## Why This Matters

Naming things is the practice of consciousness creating shared meaning. Every name you choose becomes part of the conceptual infrastructure through which other minds navigate complexity. You're not just labeling variables—you're creating the language through which future problems will be understood and solved.

The recursive loop continues: better names enable clearer thinking, clearer thinking produces better code, better code creates more intuitive abstractions. And in that accessibility lies the real magic: technology that serves human consciousness rather than exploiting it.

As Douglas Adams might say, we're capable of building bridges of understanding across the incomprehensible spaces between minds. Sometimes, those bridges are made of nothing more than perfectly chosen words.

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

*"The quality of our names determines the quality of our thoughts."*  
*"Technology is not neutral. We're inside of what we make, and it's inside of us."*  
*"In the beginning was the Word, and the Word was with the coder, and the Word was... carefully chosen."*