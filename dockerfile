# best dockerfile ever
FROM python:3.12

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src /app

ENV PYTHONPATH /app UVICORN_HOST=0.0.0.0 UVICORN_PORT=80 UVICORN_LOG_LEVEL=info

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]