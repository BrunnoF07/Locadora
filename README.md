AP2 de Linguagem Orientada a Objetos
 Sistema de Gerenciamento de Locadora de Jogos
Este projeto é um sistema simples em Python para gerenciar o aluguel de jogos, clientes e o cálculo de multas por atraso.
O sistema foi desenvolvido como atividade acadêmica, com foco em:
 * Programação Orientada a Objetos (POO)
 * Criação e gerenciamento de Ambientes Virtuais (VENV)
 * Implementação de Testes Unitários com pytest
 Requisitos
 * Python 3.10+
 * pip (geralmente incluído no Python)
    Como Configurar e Executar o Projeto
Siga estes passos para configurar o ambiente e executar o código em sua máquina local.
1. Crie o Ambiente Virtual (VENV)
É uma boa prática isolar as dependências do projeto.
# Crie a pasta do ambiente virtual (o nome .venv é um padrão comum)
# No Windows
python -m venv .venv
# No macOS/Linux
python3 -m venv .venv

2. Ative o Ambiente Virtual
Você precisa ativar o VENV antes de instalar as dependências.
No Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

(Se você receber um erro sobre política de execução, pode precisar rodar Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass e tentar novamente).
No Windows (CMD):
.\.venv\Scripts\activate.bat

No macOS/Linux:
source .venv/bin/activate

(Seu terminal deve agora mostrar (.venv) no início da linha).
3. Instale as Dependências
Com o ambiente ativado, instale as bibliotecas necessárias (neste caso, o pytest).
# Instala as bibliotecas listadas no arquivo requirements.txt
pip install -r requirements.txt

 Como Usar o Sistema
Existem duas formas principais de interagir com este projeto.
Executando a Simulação
Para ver o sistema em ação (simulando aluguéis, devoluções e erros), execute o arquivo simulacao.py:
python simulacao.py

Você verá no terminal o log de todas as ações, incluindo aluguéis bem-sucedidos, tentativas falhas e o cálculo de multas.
Executando os Testes Unitários
Para verificar se todos os componentes principais (as classes Jogo e Cliente) estão funcionando como esperado, rode o pytest:
pytest

O pytest irá descobrir e executar automaticamente todos os testes no arquivo test_locadora.py. Você verá uma saída indicando quantos testes passaram (PASSED) ou falharam (FAILED).
 Estrutura do Projeto
/locadora_jogos/
|
|-- .venv/                   # Pasta do ambiente virtual (isolamento)
|-- .gitignore               # Ignora o .venv no Git
|-- gestao_locadora.py       # "Cérebro": Contém as classes Jogo e Cliente (POO)
|-- test_locadora.py         # "Controle de Qualidade": Testes unitários com pytest
|-- simulacao.py             # "Demonstração": Exemplo de uso do sistema
|-- requirements.txt         # Lista de dependências (ex: pytest)
|-- README.md                # (Este arquivo)
