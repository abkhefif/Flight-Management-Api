FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# NE PAS UTILISER RUN pour créer la DB !
# Utiliser CMD pour l'exécuter au démarrage
CMD sh -c "python init_db.py && python seed_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"
