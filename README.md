# Security LLM Agent

Esse repositório serve como submódulo do repositório "risk-security-platform".

Tudo relacionado ao agente LLM e à RAG dele será configurado e executado neste e a partir deste repositório.

Para garantir a reprodutibilidade e evitar conflitos de dependências, este projeto utiliza [Conda](https://docs.conda.io/en/latest/) para gerenciar seu ambiente virtual.

A proposta desse projeto - e especificamente deste agente LLM - é utilizar apenas ferramentas Open Source.

# 1. Pré-requisitos

- **Conda:** Necessário ter uma distribuição do Conda instalada (seja [Anaconda](https://www.anaconda.com/products/distribution) ou [Miniconda](https://docs.conda.io/en/latest/miniconda.html), que é mais leve e recomendado). Entre na [preparação do ambiente do projeto](./environment/README.md), na "seção 1", para instalar e preparar o ambiente Conda, assim, possuindo acesso a todas as bibliotecas necessárias.

- **Pytest:** Para conseguir rodar os testes dos métodos/funções corretamente, entre na [preparação do ambiente do projeto](./environment/README.md), na "seção 2.", para configurar corretamente a biblioteca no VSCode. 

# 2. Recursos utilizados

A ideia por trás do agente LLM é utilizar a ferramenta [Ollama](https://docs.ollama.com/) com o modelo de LLM do [Deepseek](https://www.deepseek.com/) e, para o programa ter um funcionamento perene/contínuo, será utilizada a plataforma [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces) para possuir um container Docker para o projeto.

## 2.1. Explicação da escolha da plataforma em nuvem

As duas principais plataformas em nuvem pesquisadas e focadas foram o [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces) e o [Oracle Cloud (Always Free Tier)](https://www.oracle.com/cloud/free/). Ambas escolhas eram excelentes para o intuito do projeto, porém, mesmo a Oracle oferecendo um plano totalmente gratuito para a criação de uma Virtual Machine (VM), ainda houve obstáculos.

### 2.1.1. Oracle Cloud

A Oracle Cloud possibilita que os usuários criem máquinas virtuais em nuvem. O planejamento seria, através desta máquina virtual, criar um container [Docker](https://docs.docker.com/) para servir como ambiente em nuvem do Ollama. Porém, ao tentar criar o container, fui travado pelo domínio da Oracle estar sobrecarregado. Seria possível tentar, através dos dias, criar a máquina virtual, todavia, devido ao tempo e necessidade de progredir no projeto, foi decidido prosseguir com o Hugging Face Spaces.

### 2.1.2. Hugging Face Spaces

O Hugging Face Spaces é uma - traduzindo literalmente - plataforma como serviço (PaaS) que servirá como o ambiente em nuvem que já possui todos os recursos, sem ser necessário se preocupar com a criação de um container Docker, por exemplo. 

### 2.1.3. Conclusão

Neste projeto, tentei focar ao máximo explorar ferramentas e recursos que não conhecia/nunca tinha trabalhado antes com, ou seja, utilizar o serviço do Oracle Cloud era visto como mais interessante, pela necessidade de desenvolver e trabalhar mais em cima dessa plataforma em nuvem e dos containers Dockers. Porém, pelo prazo do trabalho, foi necessário deixar de lado essa tentativa, por enquanto, para a conclusão dele.

# 3. Testes

Os testes feitos para este repositório envolvem apenas testes de códigos feitos para a criação do agente LLM.

## 3.1. Testes do Google Colab

Os primeiros testes foram feitos através do [Google Colab](https://colab.google/), para ser possível - principalmente - visualizar o agente LLM e montar o código sem ser necessário instalar na máquina local bibliotecas que talvez não fossem ser utilizadas no futuro.

Os testes se encontram na [pasta de testes do Colab](./tests/colab/) e todos os códigos dentro dela não foram testados na versão final do repositório, servindo, assim, apenas para documentação dos testes feitos no Colab.

*Será possível ver pelos, por exemplo, códigos dos testes do Colab que há outras bibliotecas sendo utilizadas para a ambientação em nuvem, como o Ngrok, que não foram utilizadas na versão final do código*

## 3.2. Testes de métodos/funções

Os arquivos contidos na [pasta de testes](./tests/), fora da pasta de testes do Colab, são testes relacionados à criação de métodos/funções para o código.

Utilizei do princípio [Test-Driven Development (TDD)](https://pt.wikipedia.org/wiki/Test-driven_development) para o desenvolvimento deste repositório, consistindo onde os testes são escritos antes dos métodos/funções e que funciona em um ciclo curto e repetitivo, conhecido como [Red-Green-Refactor](https://www.codecademy.com/article/tdd-red-green-refactor).

### 3.2.1. Pytest

Para botar em prática o TDD, utilizei a biblioteca [Pytest](https://docs.pytest.org/en/stable/) para a criação dos testes. Todos os testes tem o objetivo de testar lógicas dos métodos para que garanta, se houver retorno, o retorno dos valores corretos por aquele método.