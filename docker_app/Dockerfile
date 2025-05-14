# Etapa 1: Builder
FROM python:3.9-slim as builder

WORKDIR /app

# Instala dependencias sin caché
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Etapa 2: Final image
FROM python:3.9-slim

WORKDIR /app

# Copiamos lo necesario desde el builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiamos la app
COPY . .

EXPOSE 80

CMD ["python", "app.py"]

