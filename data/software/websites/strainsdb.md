# StrainsDB: AI-Generated Cannabis Database

*An experimental Django application exploring AI-powered content generation*

[`strainsdb.org`](https://strainsdb.org/) is a Django web application that catalogues various cannabis strains, built as a proof of concept for AI-generated web content<label for="sn-ai-content-generation" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-ai-content-generation" class="margin-toggle"/><span class="sidenote">This project represents an early exploration into AI-powered content generation for web applications, predating the widespread adoption of large language models for automated content creation.</span>.

## Features

The application provides:

- **Strain Browser**: Browse through different cannabis strains with detailed information
- **Search Functionality**: Find specific strains based on characteristics and effects  
- **Terpene Profiles**: Detailed terpene information for each strain
- **AI-Generated Content**: All strain descriptions and data generated using GPT-3.5

## Technical Architecture

The backend leverages modern Python tooling:

- **Django Framework**: Provides the web application structure and admin interface
- **GPT-3.5 Integration**: Generates strain descriptions and terpene profiles
- **Instructor Library**: Uses [instructor](https://python.useinstructor.com)<label for="sn-instructor-library" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-instructor-library" class="margin-toggle"/><span class="sidenote">Instructor is a Python library that uses Pydantic models to structure and validate LLM outputs, ensuring reliable data extraction from language models for programmatic use.</span> to structure and validate AI outputs with Pydantic models
- **SQLite Database**: Stores all strain and terpene data<label for="sn-sqlite-choice" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-sqlite-choice" class="margin-toggle"/><span class="sidenote">SQLite provides a lightweight, serverless database solution perfect for proof-of-concept applications, requiring no additional infrastructure while maintaining ACID compliance.</span>

## Innovation

StrainsDB demonstrates how AI can be integrated into traditional web applications to generate rich, structured content. The use of Pydantic models ensures the AI-generated data maintains consistency and validity, making it suitable for production use.

Visit: [strainsdb.org](https://strainsdb.org/)
