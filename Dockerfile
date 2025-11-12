FROM python:3.11-slim

WORKDIR /code
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama && chmod +x /usr/bin/ollama

COPY ./requirements.txt /code/requirements.txt
COPY ./start.sh /code/start.sh

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./llm_main /code/llm_main/
RUN chmod +x /code/start.sh

EXPOSE 7860

CMD ["/code/start.sh"]