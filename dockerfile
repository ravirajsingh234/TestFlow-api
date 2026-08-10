FROM python:3.9-slim as BUILDER
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get upgrade -y && \
	apt-get install -y --no-install-recommends build-essential gcc libpq-dev && \
	rm -rf /var/lib/apt/lists/*
RUN python -m venv /app/venv
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
RUN useradd -m fastapi_usr
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
COPY --from=BUILDER /app/venv /app/venv
COPY app .
USER fastapi_usr
EXPOSE 8000
CMD ["/app/venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]