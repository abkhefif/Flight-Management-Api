FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY init_db.py seed_data.py ./
COPY alembic.ini ./
COPY alembic/ ./alembic/

EXPOSE 8000

CMD ["sh", "-c", "python init_db.py && python seed_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"
