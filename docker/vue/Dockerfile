# Stage base commun
FROM node:20-slim AS base
WORKDIR /app
COPY frontend/package*.json .
RUN npm install --include=dev
ENV PATH /app/node_modules/.bin:$PATH

# Stage builder (prod)
FROM base AS builder
COPY frontend/ .
RUN npm run build

# Stage prod
FROM nginx:alpine AS prod
COPY --from=builder /app/dist /usr/share/nginx/html

# Stage dev
FROM base AS dev
COPY frontend/ .
CMD ["npm", "run", "dev", "--", "--host"]