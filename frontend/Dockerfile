# =======================
# Stage 1: Build stage
# =======================
FROM node:22.11.0-slim AS builder

RUN apt-get update && apt-get install curl -y

WORKDIR /app

COPY frontend/app/package.json frontend/app/pnpm-lock.yaml* ./

RUN npm install -g pnpm && pnpm install --frozen-lockfile --dangerously-allow-all-builds

COPY frontend/app/ .

RUN pnpm build

# =======================
# Stage 2: Production stage
# =======================
FROM nginx:alpine AS prod

# Copy build output from builder
COPY --from=builder /app/dist /usr/share/nginx/html

COPY frontend/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY logging.yaml /logging/logging.yaml

HEALTHCHECK --interval=30s --timeout=5s \
  CMD wget -q --spider http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


# =======================
# Stage 3: Development stage
# =======================
FROM node:22.11.0-slim AS dev

RUN apt-get update && apt-get install curl -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY frontend/app/package.json frontend/app/pnpm-lock.yaml* ./

RUN npm install -g pnpm && pnpm install --frozen-lockfile --dangerously-allow-all-builds

COPY frontend/app/ .

EXPOSE 80

CMD ["pnpm", "dev", "--host", "--port", "80"]
