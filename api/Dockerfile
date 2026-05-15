FROM python:3.11-slim

# Paramètres de l'utilisateur (PUID/PGID)
ARG PUID=1026
ARG PGID=1026

# Création de l'utilisateur pour correspondre aux permissions de l'hôte
RUN groupadd -g ${PGID} appgroup && \
    useradd -u ${PUID} -g appgroup -m appuser

WORKDIR /app

# Installation des dépendances système si nécessaire
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code de l'API
COPY . .

# Droits sur le dossier app
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
