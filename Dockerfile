FROM python:3.11-slim

# Evita que Python genere archivos .pyc y fuerza unbuffering para ver logs al instante
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema requeridas para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Comando de producción con Gunicorn (3 workers paralelos)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "app:create_app()"]