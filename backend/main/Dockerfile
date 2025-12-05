FROM python:3.10.14 as base

RUN apt-get update && apt-get install libpq-dev -y

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /requirements

# =======================
# Stage 2: Production stage
# =======================
FROM base as prod

COPY backend/main/requirements.prod.txt /requirements

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.prod.txt

COPY backend/main/app/ /project/app
COPY logging.yaml /logging/logging.yaml

WORKDIR /project

CMD ["uvicorn", "app.main:app", "--log-config=/logging/logging.yaml", "--host", "0.0.0.0", "--port", "8000"]


# =======================
# Stage 3: Development stage
# =======================
FROM base as dev

COPY backend/main/requirements.dev.txt /requirements

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.dev.txt

WORKDIR /project

CMD ["uvicorn", "app.main:app", "--log-config=/logging/logging.yaml", "--host", "0.0.0.0", "--port", "8000", "--reload", "--timeout-keep-alive", "5", "--timeout-graceful-shutdown", "1"]
