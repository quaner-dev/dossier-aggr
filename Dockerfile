FROM python:3.14-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY pyproject.toml ./
RUN pip install --no-cache-dir --group runtime

COPY main.py alembic.ini ./
COPY alembic ./alembic
COPY api ./api
COPY core ./core
COPY models ./models
COPY repo ./repo
COPY services ./services

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
