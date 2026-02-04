# AI Orchestration App

This is a skeleton FastAPI application with LangChain, LangGraph, MongoDB, and Redis.

## Setup

1.  Run `docker-compose up --build`.
2.  Access API at `http://localhost:8000/docs`.

## Auth

Login with `POST /auth/signup` and `POST /auth/token`.

## Agent

Use `POST /agent/chat` with the Bearer token.
