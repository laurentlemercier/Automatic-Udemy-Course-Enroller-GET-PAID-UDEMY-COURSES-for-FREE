# syntax=docker/dockerfile:1.6

############################
#        BUILDER
############################
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel

# Build wheels (multi-arch safe)
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


############################
#        RUNTIME
############################
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG user=enroller
ARG group=enroller
ARG ENVIRONMENT=develop # develop / prod

ENV uid=1000
ENV gid=1000

# Runtime libs uniquement
RUN apt-get update && apt-get install -y \
    libffi8 \
    && rm -rf /var/lib/apt/lists/*

RUN if [ "$ENVIRONMENT" = "prod" ]; then \
      groupadd -g ${gid} ${group} && useradd -u ${uid} -g ${group} -s /usr/sbin/nologin ${user}; \
    else \
      groupadd -g ${gid} ${group} && useradd -u ${uid} -g ${group} -s /bin/sh ${user}; \
    fi

WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY . .
RUN chown -R ${user}:${group} /app

USER ${user}

ENTRYPOINT ["python", "run_enroller.py"]

