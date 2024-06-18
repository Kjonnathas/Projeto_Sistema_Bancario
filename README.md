## Objetivo do Projeto

O projeto está sendo desenvolvido com o objetivo de colocar em prática o conhecimento adquirido sobre POO (programação orientada à ojetos) e mais alguns outros conceitos.

## Estrutura do Projeto

O projeto foi estruturado para receber dados de uma aplicação - inicialmente vindo do terminal - e posteriormente carregados em um banco de dados PostgreSQL. Nesse projeto foi desenvolvido um Diagrama Entidade-Relacionamento (DER) para idealizar o schema do banco de dados.

![DER](images/DER.png)

![Arquitetura da aplicação](images/arquitetura_aplicacao.png)

## Tecnologias utilizadas

Python:

- sqlalchemy
- datetime
- time
- pytz
- hashlib
- sys
- os
- email_validator
- re
- random
- dotenv
- psycopg2

SQL:

- create database
- create schema
- create table

### Requisitos Obrigatórios

- Python 3.10 ou superior
- Postgres (servidor) e pgAdmin (interface gráfica de usuário)
- Git 2.40.1 ou superior

## Como utilizar o Projeto

1. Crie o banco de dados, o schema e as tabelas no SGBD (Postgres)

2. Crie um ambiente virtual com o seguinte comando:

```
python -m venv venv
```

3. Ative o ambiente virtual:

```
venv\Scripts\activate
```

4. Clone o repositório do GitHub:

```

git clone "link do repositório"

```

5. Faça a instalação das bibliotecas necessárias para rodar o projeto:

```

pip install requirements.txt

```

6. Navegue até a pasta onde está o arquivo main:

```

cd "nome do diretório"

```

7. Execute o seguinte comando:

```

python main.py

```

8. Desative o ambiente virtual quando terminar:

```
deactivate
```
