# Simplemind: AI for Humans

Simplemind is a Python library that makes working with AI APIs straightforward and intuitive. It provides a unified interface to popular AI services like OpenAI, Anthropic, Google's Gemini, and others, letting you focus on building rather than wrestling with different API implementations. With its "for humans" philosophy, Simplemind handles the complexity while giving you a clean, consistent way to interact with AI capabilities.


```bash
$ pip install simplemind
```

Getting started is as simple as installing the package and setting your API keys as environment variables. Whether you need basic text generation, structured data responses, or conversational AI, Simplemind makes it accessible with just a few lines of code:

```python
import simplemind as sm

# Simple text generation
response = sm.generate_text("What is the meaning of life?", llm_provider="openai")

# Structured data with Pydantic
from pydantic import BaseModel

class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    instructions: list[str]

recipe = sm.generate_data(
    "Write a recipe for chocolate chip cookies",
    response_model=Recipe,
    llm_provider="anthropic"
)

# Conversational AI
conversation = sm.create_conversation()
conversation.add_message("user", "Hi there!")
response = conversation.send()
```

Want to stick with one AI provider? Create a session to avoid repeating configuration:

```python
claude = sm.Session(llm_provider="anthropic", llm_model="claude-3-5-sonnet-20241022")
response = claude.generate_text("Hello!")
```

Simplemind is open source under the Apache 2.0 License and welcomes contributions from the community. For more examples and documentation, visit the [GitHub repository](https://github.com/kennethreitz/simplemind).
