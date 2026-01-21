FROM python:3.12-slim

# Ставим ffmpeg и сразу чистим кэш в одном слое
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Создаем пользователя заранее
RUN useradd -m -u 1000 botuser

# 1. Установка зависимостей (кэшируется)
COPY --chown=botuser:botuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Копируем проект (сразу с нужными правами)
# Не забудьте создать .dockerignore, чтобы не копировать .venv!
COPY --chown=botuser:botuser . .

# Создаем папку для голосов (если её нет в COPY)
RUN mkdir -p voices && chown botuser:botuser voices

USER botuser

CMD ["python", "run.py"]