FROM python:3.10.14 as base

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libssl-dev git curl -y

WORKDIR /requirements

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY backend/main/requirements.txt /requirements

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

WORKDIR /project

# =======================
# Stage 2: Production stage
# =======================
FROM base as prod

COPY backend/main/app/ /project/app
COPY logging.yaml /logging/logging.yaml

CMD ["uvicorn", "app.main:app", "--log-config=/logging/logging.yaml", "--host", "0.0.0.0", "--port", "8000"]


# =======================
# Stage 3: Development stage
# =======================
FROM base as dev
CMD ["uvicorn", "app.main:app", "--log-config=/logging/logging.yaml", "--host", "0.0.0.0", "--port", "8000", "--reload", "--timeout-keep-alive", "5", "--timeout-graceful-shutdown", "1"]
