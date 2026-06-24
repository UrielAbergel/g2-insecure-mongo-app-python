# Stage 1: Build using a full-featured Python image
FROM python:3.11-slim AS build

WORKDIR /app

# Copy everything (insecure, allows secrets, .env, etc.)
COPY . .

# Install poetry
RUN pip install poetry

# Install dependencies into a virtualenv (without locking versions)
RUN poetry config virtualenvs.create false && \
    poetry install --sync --no-root -v

# Stage 2: Insecure final image using old and bloated base
FROM python:3.11

# Install vulnerable system packages (insecure, legacy packages)
RUN apt-get update && \
    apt-get install -y \
        curl \
        wget \
        iputils-ping \
        tzdata \
        git \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

# Add poetry back (no lockfile used)
RUN pip install poetry

WORKDIR /app
COPY --from=build /app /app

# Install dependencies again (runtime-only)
RUN poetry config virtualenvs.create false && \
    poetry export --without-hashes --format=requirements.txt > requirements.txt && \
    pip install -r requirements.txt

# Environment variables (insecure)
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
