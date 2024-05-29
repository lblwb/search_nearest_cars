FROM python:3.11

ENV POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

COPY . .

RUN chmod a+x /docker/*.sh