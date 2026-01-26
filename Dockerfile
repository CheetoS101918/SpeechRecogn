FROM python:3.12-slim
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN useradd -m -u 1000 botuser
RUN pip install --no-cache-dir torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
COPY --chown=botuser:botuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=botuser:botuser . .
RUN mkdir -p voices whisper_models && chown -R botuser:botuser /app && chmod 777 voices
USER botuser
CMD ["python", "run.py"]