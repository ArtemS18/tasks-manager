FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Инструменты для сборки нативных пакетов + установка Poetry
RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# Сначала зависимости, чтобы кешировалось
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-interaction

# Потом код
COPY . .

# Если у тебя это установленный пакет:
# RUN poetry install --no-interaction

# Пример команды запуска
# CMD ["python", "-m", "task_api"]
