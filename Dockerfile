FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p voices
CMD ['python', 'run.py']
 