# Dockerfile optimisé pour production Render

FROM python:3.12-slim

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Changer les permissions pour l'utilisateur non-root
RUN chown -R appuser:appuser /app

# Basculer vers l'utilisateur non-root
USER appuser

# Exposer le port (Render utilise la variable $PORT)
EXPOSE 8000

# Healthcheck pour surveiller l'état de l'application
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/', timeout=5)" || exit 1

# Commande de démarrage avec workers pour la concurrence
# Render va override le PORT avec sa propre variable d'environnement
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 4
