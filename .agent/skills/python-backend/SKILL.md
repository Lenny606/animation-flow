---
name: Python Backend Development (AI Focus)
description: Guidelines for building AI-powered Python backends using Poetry, Docker, and LangChain/LangGraph.
---

# Python Backend Development Skill

This skill provides a set of instructions and best practices for building robust Python backends, specifically focused on AI orchestration using LangChain and LangGraph.

## Core Principles

1. **Dependency Management**: Use **Poetry** for all projects. Avoid `pip` and `requirements.txt` directly. Maintain a clear `pyproject.toml` with version pinning.
2. **Environment Isolation**: Always run applications inside **Docker** containers for consistency. Use WSL for local development command execution.
3. **AI Orchestration**: Leverage **LangChain** and **LangGraph (>= 1.0)** for complex AI workflows. Focus on state-aware graphs and agentic patterns.
4. **Configuration**: Use `.env` files for environment variables (API keys, DB URLs). NEVER commit `.env` files to version control.
5. **Type Hinting**: Use Python's type hints (`typing` module) across the codebase to ensure maintainability and IDE support.

## Technical Stack

- **Framework**: FastAPI (recommended) or Flask.
- **Dependency Manager**: Poetry.
- **Containerization**: Docker & Docker Compose.
- **AI Stack**: LangChain Core, LangGraph (>= 1.0).
- **Tooling**: Pytest, Black/Ruff (formatting/linting).

## Implementation Guidelines

### 1. Project Initialization (Poetry)
- Use `poetry init` or `poetry new` to start a project.
- Add dependencies using `poetry add <library>`.
- Use `poetry shell` to enter the virtual environment inside WSL.

### 2. Local Development (WSL + Docker)
- Define a `Dockerfile` using a slim Python image (e.g., `python:3.11-slim`).
- Use `docker-compose.yml` to orchestrate dependencies like Redis or Postgres.
- Map the local directory as a volume to enable hot-reloading inside the container.

### 3. LangGraph (>= 1.0) Patterns
- Define a `State` class using `TypedDict` or `Pydantic`.
- Use `StateGraph` for orchestration.
- Implement nodes as focused functions or classes.
- Use `MemorySaver` or persistent checkpointers for long-running workflows.

### 4. Code Quality
- Use `ruff` for fast linting and formatting.
- Write unit tests for graph nodes and utility functions using `pytest`.

## Resource Files

Check the `resources/` directory for boilerplate configurations:
- [pyproject.toml](file:///home/tomas/my-projects/animation-flow/.agent/skills/python-backend/resources/pyproject.toml) - Base Poetry configuration.
- [docker-compose.yml](file:///home/tomas/my-projects/animation-flow/.agent/skills/python-backend/resources/docker-compose.yml) - Dev environment setup.
- [graph.py](file:///home/tomas/my-projects/animation-flow/.agent/skills/python-backend/resources/graph.py) - Template for LangGraph 1.0+ workflows.
