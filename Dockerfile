# Imagen base con Python 3.13 slim
FROM python:3.13-slim AS base

# Configuración de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl gcc libpq-dev netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="$POETRY_HOME/bin:$PATH"

# Crear directorio de la app
WORKDIR /app
ENV PYTHONPATH=/app/src

# Copiar archivos de configuración de Poetry
COPY pyproject.toml poetry.lock* ./

# Instalar dependencias (sin dev para producción)
RUN poetry install --no-root --without dev

# Copiar el resto del proyecto
COPY . .

# Copiar script de arranque
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Exponer puerto de FastAPI
EXPOSE 8000

# Comando de arranque (espera a DB, migra y levanta API)
CMD ["./entrypoint.sh"]
