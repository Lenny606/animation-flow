FROM node:20-slim

RUN npm install -g pnpm

WORKDIR /app

COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY frontend/ ./

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

ARG VITE_DISABLE_AUTH
ENV VITE_DISABLE_AUTH=$VITE_DISABLE_AUTH

EXPOSE 5173

CMD ["pnpm", "run", "dev", "--", "--host"]
