# base image
FROM python:3.12-slim-bookworm AS base

WORKDIR /app/api

# Install Poetry
ENV UV_VERSION=0.6.11

RUN apt-get update && apt-get install -y libpq-dev
RUN apt-get update && apt-get install -y libpq5


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade uv==${UV_VERSION}

# Configure Poetry
ENV UV_CACHE_DIR=/tmp/uv_cache
ENV UV_NO_INTERACTION=1
ENV UV_VIRTUALENVS_IN_PROJECT=true
ENV UV_VIRTUALENVS_CREATE=true

FROM base AS packages

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ libc-dev libffi-dev libgmp-dev libmpfr-dev libmpc-dev \
    libpq-dev postgresql-client

# Install Python dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync
# production stage
FROM base AS production



EXPOSE 5001

# set timezone
ENV TZ=UTC

WORKDIR /app/api

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl wget vim nodejs ffmpeg libgmp-dev libmpfr-dev libmpc-dev \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

# Copy Python environment and packages
ENV VIRTUAL_ENV=/app/api/.venv
COPY --from=packages ${VIRTUAL_ENV} ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Copy source code
COPY . /app/api/

CMD ["uv", "run", "app.py"]

