FROM node:20-slim

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

ARG VITE_DISABLE_AUTH
ENV VITE_DISABLE_AUTH=$VITE_DISABLE_AUTH

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
