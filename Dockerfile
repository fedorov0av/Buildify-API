FROM ghcr.io/withlogicco/poetry:1.7.0-python-3.12
WORKDIR /app
COPY pyproject.toml ./
RUN poetry install --no-root
COPY app app
COPY alembic alembic
COPY .env .env
COPY alembic.ini alembic.ini
COPY README.md README.md
COPY entrypoint.sh /app/entrypoint.sh
RUN apt-get update && apt-get install -y wget
RUN wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz
RUN tar -xvzf dockerize-linux-amd64-v0.6.1.tar.gz -C /usr/local/bin
ENV PYTHONPATH=/app