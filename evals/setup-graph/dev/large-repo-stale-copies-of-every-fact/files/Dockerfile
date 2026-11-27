FROM python:3.12-slim AS build
ENV POETRY_VERSION=1.8.4 POETRY_VIRTUALENVS_IN_PROJECT=true
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root
COPY curio ./curio
COPY queries ./queries
RUN poetry install --only main

FROM python:3.12-slim
WORKDIR /app
COPY --from=build /app /app
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "curio.api:app", "--host", "0.0.0.0", "--port", "8000"]
