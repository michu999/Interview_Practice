# Etap 1: Budowanie z pełnym środowiskiem
FROM python:3.9 AS builder
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt .
# Zbuduj "koła" - prekompilowane pakiety dla szybszej instalacji
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Etap 2: Finalny, odchudzony obraz produkcyjny
FROM python:3.9-slim
WORKDIR /app

# Stwórz bezpiecznego użytkownika, żeby nie działać jako root
RUN adduser --disabled-password --gecos "" appuser

# Skopiuj tylko "koła" i zainstaluj je
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

COPY . .

# Zmień właściciela plików na naszego nowego użytkownika
RUN chown -R appuser:appuser /app

# Przełącz na bezpiecznego użytkownika
USER appuser

# Komenda startowa
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "my_api.wsgi"]