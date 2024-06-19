## Objetivo do projeto

O projeto está sendo desenvolvido com o objetivo de colocar em prática o conhecimento adquirido sobre POO (programação orientada à ojetos) e mais alguns outros conceitos.

## Estrutura do projeto

O projeto foi estruturado para receber dados de uma aplicação - inicialmente vindo do terminal - e posteriormente carregados em um banco de dados PostgreSQL. Nesse projeto foi desenvolvido um Diagrama Entidade-Relacionamento (DER) para idealizar o schema do banco de dados.

![DER](images/DER.png)

![Arquitetura da aplicação](images/arquitetura_aplicacao.png)

## Tecnologias utilizadas

<br>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

- sqlalchemy -> gerenciamento/interação com o banco de dados;
- datetime -> manipulação de datas;
- time -> manipulação de datas/tempo;
- pytz -> manipulação de timezone;
- hashlib -> criação de protocolos com sha256;
- sys -> manipulação do sistema operacional;
- os -> manipulação do sistema operacional;
- email_validator -> validação de e-mail;
- re -> manipulação de regular expressions;
- random -> manipulação de números randômicos;
- dotenv -> manipulação de variáveis de ambiente;
- psycopg2 -> conexão com o postgres.

<br>

![POSTGRES](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

- create database -> cria o banco de dados;
- create schema -> cria o schema o banco de dados;
- create table -> cria as tabelas do banco de dados.

## Requisitos obrigatórios

- Python 3.10 ou superior
- Postgres (servidor) e pgAdmin (interface gráfica de usuário)
- Git 2.40.1 ou superior

## Instrução de uso

1. Crie o banco de dados, o schema e as tabelas no SGBD (Postgres). Os códigos SQL estão na pasta src no arquivo "schema.sql". Execute na ordem que está no arquivo.

<br>

2. Crie um ambiente virtual com o seguinte comando:

```
python -m venv venv
```

<br>

3. Ative o ambiente virtual:

```
CMD -> venv/Scripts/activate

PowerShell -> venv/Scripts/Activate.ps1
```

<br>

4. Clone o repositório do GitHub:

```

git clone "link do repositório"

```

<br>

5. Faça a instalação das bibliotecas necessárias para rodar o projeto:

```

pip install requirements.txt

```

<br>

6. Navegue até a pasta onde está o arquivo main:

```

cd "nome do diretório"

```

<br>

7. Execute o seguinte comando:

```

python main.py

```

<br>

8. Desative o ambiente virtual quando terminar:

```
deactivate
```
