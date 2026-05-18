FROM node:20-slim

WORKDIR /app

COPY frontend/package*.json .

RUN npm install --include=dev

ENV PATH /app/node_modules/.bin:$PATH

COPY frontend/ .

CMD ["npm", "run", "dev", "--", "--host"]