# strainsdb.org


[`strainsdb.org`](https://strainsdb.org/) is a simple Django app that contains information about various strains of cannabis. It was made as a proof of concept for using AI to generate content for a website<label for="sn-ai-content-generation" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-ai-content-generation" class="margin-toggle"/><span class="sidenote">This project represents an early exploration into AI-powered content generation for web applications, predating the widespread adoption of large language models for automated content creation.</span>.

The app allows users to browse different strains, view details about each strain, and search for specific strains based on their characteristics.

Each strain also contains terpene information, which is extracted from `gpt-3.5` using [instructor](https://python.useinstructor.com)<label for="sn-instructor-library" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-instructor-library" class="margin-toggle"/><span class="sidenote">Instructor is a Python library that uses Pydantic models to structure and validate LLM outputs, ensuring reliable data extraction from language models for programmatic use.</span> and stored in SQLite<label for="sn-sqlite-choice" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-sqlite-choice" class="margin-toggle"/><span class="sidenote">SQLite provides a lightweight, serverless database solution perfect for proof-of-concept applications, requiring no additional infrastructure while maintaining ACID compliance.</span>.

https://strainsdb.org/
