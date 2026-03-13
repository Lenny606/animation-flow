# Stage 1: Build stage
FROM node:20-slim AS builder

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

ARG VITE_DISABLE_AUTH
ENV VITE_DISABLE_AUTH=$VITE_DISABLE_AUTH

COPY frontend/ .
RUN npm run build

# Stage 2: Production stage
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY infrastructure/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
