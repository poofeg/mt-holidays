FROM python:3.10-slim

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

COPY README.md ./
COPY mt_holidays mt_holidays
RUN poetry install --no-dev

ENTRYPOINT ["poetry", "run", "mt-holidays"]
