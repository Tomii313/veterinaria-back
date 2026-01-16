FROM python:3.14.2-alpine3.23

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema necesarias para mysqlclient
RUN apk add --no-cache \
    gcc \
    musl-dev \
    mariadb-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "veterinaria.wsgi:application", "--bind", "0.0.0.0:8000"]