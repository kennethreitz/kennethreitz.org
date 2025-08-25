# Simplemind: AI for Humans

*A unified Python library for seamless AI integration*

Simplemind is a Python library that makes working with AI APIs straightforward and intuitive. Following Kenneth's signature "for humans" philosophy, it provides a unified interface to popular AI services like OpenAI, Anthropic, Google's Gemini, and others, letting you focus on building rather than wrestling with different API implementations.

<span class="sidenote">Simplemind applies Kenneth's signature "for humans" approach to the rapidly evolving AI landscape. By providing a consistent interface across different AI providers, it addresses the fragmentation problem that developers face when integrating multiple AI services into their applications.</span>

## Philosophy

Just as Requests made HTTP "for humans," Simplemind makes AI "for humans." The library abstracts away the complexity of different AI providers while maintaining the power and flexibility developers need. Whether you're switching between models for testing or building applications that leverage multiple AI services, Simplemind provides a consistent, intuitive interface.


```bash
$ pip install simplemind
```

## Getting Started

Installation is simple, and setup requires only environment variables for your API keys:

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

## Sessions for Consistency

For applications using a single AI provider, sessions eliminate repeated configuration:

```python
claude = sm.Session(llm_provider="anthropic", llm_model="claude-3-5-sonnet-20241022")
response = claude.generate_text("Hello!")
```

## Key Features

- **Unified Interface**: One API for multiple AI providers (OpenAI, Anthropic, Google, etc.)
- **Pydantic Integration**: Generate structured data with automatic validation
- **Session Management**: Persistent configurations for consistent provider usage
- **Conversation Handling**: Built-in conversation state management
- **Type Safety**: Full type hints for better development experience
- **Environment-Based Config**: Simple setup through environment variables

Simplemind is open source under the Apache 2.0 License and welcomes contributions from the community. For more examples and documentation, visit the [GitHub repository](https://github.com/kennethreitz/simplemind).

<span class="sidenote">Simplemind represents Kenneth's engagement with the AI revolution, bringing his decades of API design experience to bear on one of the most significant technological shifts of our time. The library reflects his understanding that great technology should be accessible to all developers, not just AI specialists.</span>
