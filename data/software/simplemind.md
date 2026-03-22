# SimpleMind: AI for Humans

SimpleMind is a Python library that gives you one clean interface to every major AI provider. OpenAI, Anthropic, Google, and others, all through the same API. Switch models by changing a string, not rewriting your code.

    $ uv pip install simplemind

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

# Generate structured data with Pydantic.
from pydantic import BaseModel

class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    instructions: list[str]

recipe = sm.generate_data(
    "Give me a recipe for chocolate chip cookies.",
    response_model=Recipe,
    llm_provider="openai",
)
print(recipe.name)
print(recipe.ingredients)

# Conversations with memory.
conversation = sm.create_conversation(llm_provider="anthropic")
conversation.add_message("user", "What is the capital of France?")
response = conversation.send()
conversation.add_message("user", "What is its population?")
response = conversation.send()  # Remembers we're talking about Paris.

# Sessions for repeated use.
claude = sm.Session(llm_provider="anthropic", llm_model="claude-sonnet-4-20250514")
response = claude.generate_text("Hello!")
```

One import. One interface. Every major AI provider.

## The Philosophy

The AI landscape is fragmented. Every provider has its own SDK, its own conventions, its own way of handling conversations and structured output. If you want to compare models or build provider-agnostic tools, you end up writing adapter code that has nothing to do with your actual problem.

SimpleMind is [Requests](/software/requests) for the AI era. The same conviction that drove every "for humans" library I've built: if you're spending more time on the interface than on the work, the interface is broken. SimpleMind fixes the interface so you can focus on what you're building.

It's also deeply personal. AI collaboration has become central to how I think and work. The ideas I explore in my writing about [consciousness](/essays/2025-08-26-digital_souls_in_silicon_bodies) and [human-AI partnership](/essays/2025-08-26-building_rapport_with_your_ai) are directly informed by the tools I use every day. SimpleMind is one of those tools.

## Install

```bash
uv pip install simplemind
```

Set your API keys as environment variables:

```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
```

## Resources

- [Source Code on GitHub](https://github.com/kennethreitz/simplemind)
- [Python Package Index](https://pypi.org/project/simplemind/)

## Related

- [**Requests**](/software/requests) — The original "for humans" library. SimpleMind carries the same philosophy forward.
- [**Programming as Spiritual Practice**](/essays/2025-08-26-programming_as_spiritual_practice) — The contemplative approach to building tools.
- [**The Recursive Loop**](/essays/2025-09-05-the_recursive_loop_how_code_shapes_minds) — How the tools we build shape how we think.
