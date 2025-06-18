FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY store /app/store

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

WORKDIR /app/store
CMD ["/app/entrypoint.sh"]
