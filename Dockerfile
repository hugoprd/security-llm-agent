FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    curl \
    procps \
    libpq-dev \
    gcc \
    && curl -fsSL https://ollama.com/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

RUN ollama serve & \
    sleep 5 && \
    ollama pull qwen2.5:1.5b && \
    pkill ollama

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./scripts /code/scripts/
COPY ./start.sh /code/start.sh

RUN chmod +x /code/start.sh

RUN mkdir -p /code/cache && chmod 777 /code/cache
ENV HF_HOME=/code/cache

EXPOSE 7860

CMD ["/code/start.sh"]