# SimpleMind: AI for Humans

SimpleMind is a Python library that gives you one clean interface to every major AI provider. OpenAI, Anthropic, Google, and others — all through the same API. Switch models by changing a string, not rewriting your code.

    $ uv add simplemind

## What It Looks Like

```python
import simplemind as sm

# Generate text. Pick your provider.
response = sm.generate_text(
    "Explain quantum computing in one paragraph.",
    llm_provider="anthropic",
    llm_model="claude-sonnet-4-20250514",
)
print(response)
```

That's the simple case. Here's where it gets interesting:

```python
# Generate structured data with Pydantic.
from pydantic import BaseModel

class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    instructions: list[str]
    prep_time_minutes: int

recipe = sm.generate_data(
    "Give me a recipe for chocolate chip cookies.",
    response_model=Recipe,
    llm_provider="openai",
    llm_model="gpt-4o",
)
print(recipe.name)
print(recipe.ingredients)

# Conversations with memory.
conversation = sm.create_conversation(
    llm_provider="anthropic",
    llm_model="claude-sonnet-4-20250514",
)
conversation.add_message("user", "What is the capital of France?")
response = conversation.send()
conversation.add_message("user", "What is its population?")
response = conversation.send()  # Remembers we're talking about Paris.

# Sessions for repeated use.
claude = sm.Session(
    llm_provider="anthropic",
    llm_model="claude-sonnet-4-20250514",
)
response = claude.generate_text("Hello!")
```

One import. One interface. Every major AI provider.

## Plugins

SimpleMind supports a plugin system for extending conversations:

```python
import simplemind as sm

class MemoryPlugin(sm.BasePlugin):
    """Remember facts across conversations."""

    def pre_send_hook(self, conversation):
        # Inject remembered context before each message.
        memory = load_memory()
        if memory:
            conversation.add_message(
                "system",
                f"Previously remembered: {memory}",
            )

    def post_send_hook(self, conversation, response):
        # Extract and store facts from the response.
        facts = extract_facts(response.text)
        save_memory(facts)

conversation = sm.create_conversation(
    llm_provider="anthropic",
    llm_model="claude-sonnet-4-20250514",
    plugins=[MemoryPlugin()],
)
```

Plugins hook into the conversation lifecycle — before sending, after receiving, on errors. Build memory systems, logging, content filters, or whatever your application needs.

## The Philosophy

The AI landscape is fragmented. Every provider has its own SDK, its own conventions, its own way of handling conversations and structured output. If you want to compare models or build provider-agnostic tools, you end up writing adapter code that has nothing to do with your actual problem.

SimpleMind is [Requests](/software/requests) for the AI era. The same conviction that drove every "for humans" library I've built: if you're spending more time on the interface than on the work, the interface is broken. SimpleMind fixes the interface so you can focus on what you're building.

It's also deeply personal. AI collaboration has become central to how I think and work. The ideas I explore in my writing about [consciousness](/essays/2025-08-26-digital_souls_in_silicon_bodies) and [human-AI partnership](/essays/2025-08-26-building_rapport_with_your_ai) are directly informed by the tools I use every day. SimpleMind is one of those tools — built because I needed it, refined because I use it constantly.

## Install

```bash
$ uv add simplemind
```

Set your API keys as environment variables:

```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_API_KEY=...
```

## Resources

- [Source Code on GitHub](https://github.com/kennethreitz/simplemind)
- [Python Package Index](https://pypi.org/project/simplemind/)

## Related

- [**Requests**](/software/requests) — The original "for humans" library. SimpleMind carries the same philosophy forward.
- [**Programming as Spiritual Practice**](/essays/2025-08-26-programming_as_spiritual_practice) — The contemplative approach to building tools.
- [**The Recursive Loop**](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds) — How the tools we build shape how we think.
- [**From HTTP to Consciousness**](/essays/2025-08-27-from_http_to_consciousness) — The through-line from Requests to SimpleMind.
