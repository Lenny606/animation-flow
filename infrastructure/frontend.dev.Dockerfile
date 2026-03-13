FROM node:20-slim

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

# Copying source for initial existence, but docker-compose should override with volume
COPY frontend/ .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
