# ---------- Builder ----------
FROM python:3.12-slim AS builder

# Installer uniquement ce qui est nécessaire pour compiler
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copier uniquement requirements pour optimiser le cache
COPY requirements.txt .

# Mettre pip à jour (important avec Python 3.12 + ARM)
RUN pip install --upgrade pip setuptools wheel

# Construire les dépendances dans un prefix isolé
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt


# ---------- Final image ----------
FROM python:3.12-slim

ARG user=enroller
ARG group=enroller

ENV uid=1000
ENV gid=1000

# Créer utilisateur non-root
RUN groupadd -g ${gid} ${group} \
    && useradd -u ${uid} -g ${group} -s /bin/sh ${user}

# Créer home proprement
RUN mkdir -p /home/${user}/.udemy_enroller \
    && chown -R ${user}:${group} /home/${user}

WORKDIR /src

# Copier les dépendances construites
COPY --from=builder /install /usr/local

# Copier le code après (important pour cache Docker)
COPY . .

USER ${user}

ENTRYPOINT ["python", "run_enroller.py"]