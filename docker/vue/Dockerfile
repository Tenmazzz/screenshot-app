FROM node:20-slim

WORKDIR /app

COPY frontend/package*.json .

RUN npm install --include=dev

COPY frontend/ .

CMD ["npm", "run", "dev", "--", "--host"]