# Contributing to Animation Flow

Welcome! This guide outlines the basic instructions and rules for working with this monorepo.

## Monorepo Structure

The project is divided into two main parts:
- **`backend/`**: FastAPI application (Python 3.12).
- **`frontend/`**: Vite-based React application (TypeScript/JavaScript).

Root-level files like `docker-compose.yml` and `README.md` manage the overall project orchestration.

---

## General Rules

1.  **Dependency Management**:
    - Backend: Use `pyproject.toml` and `poetry` or `pip` to manage dependencies.
    - Frontend: Use `package.json` and `npm` or `yarn` (check for existing lock files).
2.  **Environment Variables**:
    - Never commit `.env` files.
    - Update `.env.example` when adding new environment variables.
3.  **Code Style**:
    - Backend: Follow PEP 8. Use `ruff` for linting/formatting if configured.
    - Frontend: Use `eslint` and `prettier` if configured.
4.  **Testing**:
    - Always include verification scripts or tests for new features.
    - Run existing verification scripts in `backend/scripts/` before submitting.

---

## Development Workflow

### 1. Local Environment Setup

Ensure you have Docker and Docker Compose installed.

```bash
# Backend setup
cd backend
cp app/.env.example app/.env
# Edit app/.env with your keys (OpenAI, MongoDB, etc.)

# Frontend setup
cd ../frontend
cp .env.example .env
# Edit .env if necessary
```

### 2. Running the Project

The easiest way to run the entire stack is using Docker Compose:

```bash
docker-compose up --build
```

### 3. Backend Development

-   **Location**: `backend/app/`
-   **Models**: Add new database schemas in `backend/app/models/`.
-   **Routers**: Register new API endpoints in `backend/app/routers/` and include them in `backend/app/main.py`.
-   **Services/Core**: Complex logic, agents, and integrations belong in `backend/app/services/` or `backend/app/core/`.
-   **Verification**: Create scripts in `backend/` or `backend/scripts/` to test your changes. See `verify_*.py` files for examples.

### 4. Frontend Development

-   **Location**: `frontend/src/`
-   **Components**: Add UI components in `frontend/src/components/`.
-   **Pages/Views**: Add main views in `frontend/src/pages/` or `frontend/src/views/`.
-   **API Integration**: Use a consistent method for API calls (e.g., `fetch` or `axios`).

---

## Deployment & CI/CD

-   **Docker**: Each service has its own `Dockerfile`.
-   **Orchestration**: `docker-compose.yml` defines how services interact.
-   **Future**: CI/CD pipelines (e.g., GitHub Actions) should run tests for both backend and frontend on every PR.

---

## Best Practices

-   **Git**: Use descriptive commit messages.
-   **Documentation**: Keep `README.md` and this guide up to date.
-   **Separation of Concerns**: Keep business logic out of routers. Use services or repositories.
-   **Async First**: In the backend, prefer `async` functions for I/O bound tasks.
