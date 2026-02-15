# Animation Flow Monorepo

This repository is organized as a monorepo containing both the backend and frontend components of the Animation Flow application.

## Structure

- **`backend/`**: FastAPI application with LangChain, LangGraph, MongoDB, and Redis.
  - `backend/app/`: Core application logic.
  - `backend/scripts/`: Verification and utility scripts.
  - `backend/Dockerfile`: Backend container configuration.
  - `backend/pyproject.toml`: Python dependencies and package configuration.
- **`frontend/`**: Vite-based React application.
  - `frontend/src/`: React components and logic.
  - `frontend/Dockerfile`: Frontend container configuration.
- **`docker-compose.yml`**: Orchestration for all services (api, frontend, mongodb, redis).

## Getting Started

1. **Environment Setup**:
   - Backend: Copy `backend/app/.env.example` to `backend/app/.env` and configure variables.
   - Frontend: Copy `frontend/.env.example` to `frontend/.env` and configure variables.

2. **Run with Docker**:
   ```bash
   docker-compose up --build
   ```

3. **Access the Application**:
   - Frontend: `http://localhost:5173`
   - Backend API: `http://localhost:8000/docs`

## Verification

Backend verification scripts can be found in `backend/scripts/`. Run them from the `backend/` directory:
```bash
cd backend
./scripts/verify_endpoints.sh
```
