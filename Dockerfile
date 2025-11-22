FROM python:3.11-slim

WORKDIR /code

# essa execução é para o docker baixar/instalar o Ollama
# que é necessário para o funcionamento do código
RUN apt-get update && apt-get install -y curl procps && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*

RUN ollama serve & \
    sleep 5 && \
    ollama pull qwen2.5:1.5b && \
    pkill ollama

COPY ./requirements.txt /code/requirements.txt
COPY ./start.sh /code/start.sh

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./llm_main /code/llm_main/
RUN chmod +x /code/start.sh

EXPOSE 7860

CMD ["/code/start.sh"]