# Implementation Plan - Fix Vercel Deployment for Backend

Vercel deployment is failing because `uv` (the package installer used by Vercel for Python) requires a `[project]` section in `pyproject.toml`. This plan outlines updating `backend/pyproject.toml` to include the necessary configuration based on the working example provided.

## User Review Required

> [!IMPORTANT]
> I am upgrading several dependency versions to match your "working example" (e.g., FastAPI from `0.109.0` to `0.129.0`). Please confirm if these upgrades are compatible with your code.

- **Dependency Upgrades**:
  - `fastapi`: `0.109.0` -> `0.129.0`
  - `uvicorn`: `0.27.0` -> `0.41.0`
  - `motor`: `3.3.0` -> `3.7.1`
  - `pydantic-settings`: `2.1.0` -> `2.13.0`
- **New Dependencies**: `sentry-sdk`, `loguru`, `python-dotenv`, `aiosmtplib`, `httpx` (Added to match your example).

## Proposed Changes

### Backend Configuration

#### [UPDATE] `backend/pyproject.toml`

Add the `[project]` and `[tool.uv]` sections and update `[tool.poetry]` to be consistent.

```toml
[project]
name = "animation-flow-api"
version = "0.1.0"
description = "FastAPI app with LangChain, LangGraph, MongoDB, and Redis"
authors = [
    {name = "Tomas", email = "thomas.kravcik@gmail.com"},
]
dependencies = [
    "fastapi>=0.129.0",
    "uvicorn[standard]>=0.41.0",
    "motor>=3.7.1",
    "redis>=5.0.0",
    "langchain>=0.1.0",
    "langgraph>=0.0.10",
    "langchain-openai>=0.0.2",
    "langchain-google-genai>=0.0.1",
    "pydantic-settings>=2.13.0",
    "sentry-sdk[fastapi]>=2.53.0",
    "passlib[bcrypt]>=1.7.4",
    "python-jose[cryptography]>=3.5.0",
    "python-multipart>=0.0.22",
    "loguru>=0.7.3",
    "python-dotenv>=1.2.1",
    "email-validator>=2.2.0",
    "slowapi>=0.1.9",
    "aiosmtplib>=3.0.0",
    "httpx>=0.27.0",
    "aiohttp>=3.9.0",
    "fakeredis>=2.20.0",
]
requires-python = ">=3.11"

[tool.poetry]
name = "animation-flow-api"
version = "0.1.0"
description = "FastAPI app with LangChain, LangGraph, MongoDB, and Redis"
authors = ["Tomas <tomas@example.com>"]
readme = "README.md"
package-mode = false

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.129.0"
uvicorn = {extras = ["standard"], version = "^0.41.0"}
motor = "^3.7.1"
redis = "^5.0.0"
langchain = "^0.1.0"
langgraph = "^0.0.10"
langchain-openai = "^0.0.2"
langchain-google-genai = "^0.0.1"
pydantic-settings = "^2.13.0"
sentry-sdk = {extras = ["fastapi"], version = "^2.53.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
python-jose = {extras = ["cryptography"], version = "^3.5.0"}
python-multipart = "^0.0.22"
loguru = "^0.7.3"
python-dotenv = "^1.2.1"
email-validator = "^2.2.0"
slowapi = "^0.1.9"
aiosmtplib = "^3.0.0"
httpx = "^0.27.0"
aiohttp = "^3.9.0"
fakeredis = "^2.20.0"

[tool.uv]
package = false

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## Verification Plan

### Automated Tests
- Run `poetry lock` locally to ensure the new configuration is valid and dependencies can be resolved.
- Run `uv lock` (if available) to verify the `[project]` table is correctly parsed.

### Manual Verification
- Re-trigger Vercel deployment and monitor the build logs for the "uv lock" step.
