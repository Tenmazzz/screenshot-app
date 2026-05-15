FROM node:20-slim

WORKDIR /app

COPY frontend/package*.json .

RUN npm ci

COPY frontend/ .

CMD ["node_modules/.bin/vite", "--host"]
#  car sur le terminal de la vm(sh) ne configure pas le chemin automatiquement