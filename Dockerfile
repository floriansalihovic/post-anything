FROM python:3.8.9

ARG POETRY_VERSION
ARG DEVELOPMENT_ENV

RUN pip install "poetry==${POETRY_VERSION}" && mkdir /app

COPY poetry.lock pyproject.toml /app/
COPY ./src/ /app

WORKDIR /app
RUN poetry config virtualenvs.create false \
 && poetry install $(test "$DEVELOPMENT_ENV" == production && echo "--no-dev") \
 --no-interaction \
 --no-ansi

EXPOSE 8000
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8000"]
