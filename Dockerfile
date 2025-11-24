FROM python:3.12-slim

WORKDIR /src

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY pyproject.toml .
COPY poetry.lock* .

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY src /src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
