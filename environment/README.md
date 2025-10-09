# Criação / Preparação do ambiente

# 1. Preparação do ambiente Conda

Para ser possível a utilização dos recursos do ambiente Python corretamente, é necessário instalar e ativar o ambiente Conda do repositório.

## 1.1. Instalação do Conda

### 1.1.1. Linux.

Execute este comando no terminal (Linux ou do VSCode)
```bash
sudo apt update && sudo apt upgrade
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
conda --version
```

### 1.1.2. Windows.

Mesmo utilizando o terminal Git Bash no VSCode, se você está no Windows, é necessário seguir esses passos.

1. Entre no site `https://www.anaconda.com/download/success` e clique para baixar o Miniconda
2. Execute o arquivo executável que foi baixado para instalar o Miniconda
3. Rode este comando no terminal
    ```bash
    cd environment
    conda env create -f environment.yml --prefix ./.venv
    conda activate ./environment/.venv
    cd ..
    ```
4. Para confirmar: Faça o comando `CTRL + SHIFT + P` e procure por "Developer: Reload Window"
5. Se, ao reiniciar, haver algum erro de interpretador, faça o seguinte:
    1. Faça o comando `CTRL + SHIFT + P` e procure por "Python: Select Interpreter"
    2. Selecione o `.venv(3.11.13) .\environment\.venv\python.exe` (irá estar marcado como recomendado)

# 2. Configuração dos testes

Para ser possível rodar os testes dos métodos/funções, será necessário configurar o VSCode com o Pytest corretamente.

1. Faça o comando `CTRL + SHIFT + P` e procure por "Python: Configure Test"
2. Selecione a opção que tem escrito "pytest"