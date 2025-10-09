# Criação / Preparação do ambiente Conda

## 1. Instalação do Conda

### 1.1 Linux.

Execute este comando no terminal (Linux ou do VSCode)
```bash
sudo apt update && sudo apt upgrade
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
conda --version
```

### 1.2 Windows.

Mesmo utilizando o terminal Git Bash no VSCode, se você está no Windows, é necessário seguir esses passos.

1. Entre no site `https://www.anaconda.com/download/success` e clique para baixar o Miniconda
2. Execute o arquivo executável que foi baixado para instalar o Miniconda
3. Rode este comando no terminal
```bash
cd environment
conda env create -f environment.yml
cd ..
```