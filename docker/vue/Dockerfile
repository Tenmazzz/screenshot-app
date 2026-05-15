FROM node:20-slim

WORKDIR /app

COPY frontend/package*.json .

RUN npm ci && npm install -g vite

COPY frontend/ .

CMD ["vite", "--host"]