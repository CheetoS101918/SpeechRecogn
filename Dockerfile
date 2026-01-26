# FROM python:3.12-slim
# # Ставим ffmpeg и сразу чистим кэш в одном слое
# RUN apt-get update && apt-get install -y \
#     ffmpeg \
#     && rm -rf /var/lib/apt/lists/*
# WORKDIR /app
# RUN useradd -m -u 1000 botuser
# COPY --chown=botuser:botuser requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY --chown=botuser:botuser . .
# RUN mkdir -p voices && chown botuser:botuser voices
# USER botuser
# CMD ["python", "run.py"]

FROM python:3.12-slim
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN useradd -m -u 1000 botuser
RUN pip install --no-cache-dir torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
COPY --chown=botuser:botuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Теперь, если ты изменишь код, шаги выше (с установкой библиотек) просто пропустятся!
COPY --chown=botuser:botuser . .
RUN mkdir -p voices whisper_models && chown -R botuser:botuser /app 
USER botuser
CMD ["python", "run.py"]