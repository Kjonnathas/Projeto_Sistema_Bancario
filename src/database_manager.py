from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Float, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import Engine
from datetime import datetime, date
import os
from dotenv import load_dotenv
import logging


# Defini o nível de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv('.env')

# Cria a base declarativa - realiza o mapeamento objeto-relacional (ORM) para definir as classes que mapeiam as tabelas no banco de dados -.
Base = declarative_base()

# Definição da classe de modelo que mapeia a tabela 'd_clientes' do banco de dados
class Tb_cliente(Base):

        __tablename__ = 'd_clientes'
        __table_args__ = {'schema': 'financeiro'}

        id_cliente = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
        nome = Column(String, nullable=False)
        sobrenome = Column(String, nullable=False)
        genero = Column(String, nullable=False)
        cpf = Column(String, unique=True, nullable=False)
        rg = Column(String, unique=True, nullable=False)
        data_nascimento = Column(Date, nullable=False)
        email = Column(String)
        celular = Column(String)
        profissao = Column(String)
        renda = Column(Float)
        data_cadastro = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
        data_fim = Column(DateTime)
        data_atualizacao = Column(DateTime, nullable=False)


# Definição da classe de modelo que mapeia a tabela 'd_dados_conta' do banco de dados
class Tb_conta(Base):

        __tablename__ = 'd_dados_conta'
        __table_args__ = {'schema': 'financeiro'}

        id_conta = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
        id_cliente = Column(Integer, ForeignKey('financeiro.d_clientes.id_cliente'), nullable=False)
        agencia = Column(String, unique=True, nullable=False)
        conta = Column(String, unique=True, nullable=False)
        tipo_conta = Column(String, nullable=False)
        saldo = Column(Float)
        data_abertura = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
        data_fechamento = Column(DateTime)
        data_atualizacao = Column(DateTime, nullable=False)


# Definição da classe de modelo que mapeia a tabela 'd_enderecos' do banco de dados
class Tb_endereco(Base):

        __tablename__ = 'd_enderecos'
        __table_args__ = {'schema': 'financeiro'}

        id_endereco = Column(Integer, primary_key=True, nullable=False)
        id_cliente = Column(Integer, ForeignKey('financeiro.d_clientes.id_cliente'), nullable=False)
        rua = Column(String, nullable=False)
        numero = Column(String, nullable=False)
        bairro = Column(String, nullable=False)
        cidade = Column(String, nullable=False)
        uf = Column(String, nullable=False)
        cep = Column(String, nullable=False)
        data_atualizacao = Column(DateTime, nullable=False)


# Definição da classe de modelo que mapeia a tabela 'f_transacoes' do banco de dados
class Tb_transacao(Base):

        __tablename__ = 'f_transacoes'
        __table_args__ = {'schema': 'financeiro'}

        id_transacao = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
        id_cliente = Column(Integer, ForeignKey('financeiro.d_clientes.id_cliente'), nullable=False)
        valor_transacao = Column(Float, nullable=False)
        tipo_transacao = Column(String, nullable=False)
        protocolo_transacao = Column(String, nullable=False)
        data_atualizacao = Column(DateTime, nullable=False)


def conectar_db() -> Engine:

    '''
    Objetivo
    --------
    A função como o próprio nome sugere tem como objetivo realizar a conexão ao banco de dados. \n

    Parâmetros
    ----------
    A função não precisa de parâmetros, pois os parâmetros necessários (usuário, senha, hostname e nome do banco de dados) já são incluídos dentro da própria função. \n

    Retorno
    -------
    O retorno da função é a engine de conexão ao banco de dados, que servirá posteriormente para interação de outras ações como "INSERT", "UPDATE" e "DELETE".
    '''

    # Carrega as variáveis de ambiente do arquivo .env

    # POSTGRES_USER = os.getenv('POSTGRES_USER')
    # POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    # POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    # POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    # POSTGRES_DB = os.getenv('POSTGRES_DB')

    POSTGRES_USER = 'postgres'
    POSTGRES_PASSWORD = 'postgre527961'
    POSTGRES_HOST = 'localhost'
    POSTGRES_PORT = '5432'
    POSTGRES_DB = 'db_transacional'

    connection = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

    engine = create_engine(connection)

    return engine

def localizar_cliente(cpf: str) -> dict | str:

    '''
    Objetivo
    --------
    A função tem como objetivo localizar um determinado cliente no banco de dados. \n

    Parâmetros
    ----------
    A função espera receber um CPF/CNPJ para funcionar. \n

    Retorno
    -------
    O retorno da função é um dicionário com o ID_Cliente quando o mesmo existe ou uma `string` com a informação de "Cliente não encontrado".
    '''

    # Conecta ao banco de dados
    engine = conectar_db()

    # Cria uma sessão para interagir com o banco de dados
    Session = sessionmaker(bind=engine)
    session = Session()

    # Basicamente faz um filtro na tabela de clientes a partir do CPF/CNPJ do cliente
    cliente = session.query(Tb_cliente).filter_by(cpf=cpf).first()

    # Fecha a sessão
    session.close()

    # Retorno da função
    return {"ID_Cliente": cliente.id_cliente} if cliente else "Cliente não encontrado"

def localizar_conta(cpf: str) -> dict:

    '''
    Objetivo
    --------
    A função tem como objetivo localizar a conta corrente de um determinado cliente no banco de dados. \n

    Parâmetros
    ----------
    A função espera receber um CPF/CNPJ para funcionar. \n

    Retorno
    -------
    O retorno da função é um `dicionário` com o ID_Cliente, Agência, Conta e Saldo.
    '''

    # Conecta ao banco de dados
    engine = conectar_db()

    # Cria uma sessão para interagir com o banco de dados
    Session = sessionmaker(bind=engine)
    session = Session()

    # Basicamente faz um filtro na tabela de clientes a partir do CPF/CNPJ do cliente 
    cliente = session.query(Tb_cliente).filter_by(cpf=cpf).first()

    # Basicamente faz um filtro na tabela contas a partir do id cliente que retornou na variável cliente
    conta = session.query(Tb_conta).filter_by(id_cliente=cliente.id_cliente).first()

    # Fecha a sessão
    session.close()

    # Retorno da função
    return {
                "ID_Cliente": conta.id_cliente,
                "Nome_cliente": cliente.nome,
                "Agência": conta.agencia, 
                "Conta": conta.conta, 
                "Saldo": conta.saldo
            }

def cadastrar_cliente(
        nome: str,
        sobrenome: str,
        genero: str, 
        cpf: str, 
        rg: str, 
        data_nascimento: date, 
        email: str, 
        celular: str,
        profissao: str,
        renda: float, 
        agencia: str,
        conta: str,
        tipo_conta: str,
        saldo: float,
        rua: str,
        numero: str,
        bairro: str,
        cidade: str,
        uf: str,
        cep: str,
        data_atualizacao: datetime
    ) -> str:

    '''
    Objetivo
    --------
    A função como o próprio nome sugere tem como objetivo cadastrar os dados de um determinado cliente no banco de dados. \n

    Parâmetros
    ----------
    A função espera receber nome_cliente, genero, cpf, rg, data_nascimento, email, celular, renda, agencia, conta, saldo, rua, numero, bairro, cidade, uf, cep e data_atualizacao. Porém, os parâmetros obrigatórios são apenas o nome_cliente, genero, cpf, rg, data_nascimento, agencia, conta, saldo, rua, numero, bairro, cidade, uf, cep e data_atualizacao. \n

    Retorno
    -------
    O retorno da função é uma string "Conta cadastrada com sucesso!" em caso de sucesso ou uma exceção em caso de erro durante o cadastramento.
    '''

    # Bloco try-except para tratamento de exceção
    try:

        # Cria a conexão com o banco de dados
        engine = conectar_db()

        # Cria uma sessão para interagir com o banco de dados
        Session = sessionmaker(bind=engine)
        session = Session()

        # Cria uma nova instância da tabela de clientes mapeando os atributos correspondentes aos campos na tabela 
        criar_cliente = Tb_cliente(
                nome = nome,
                sobrenome = sobrenome,
                genero = genero,
                cpf = cpf,
                rg = rg,
                data_nascimento = data_nascimento,
                email = email,
                celular = celular,
                profissao = profissao,
                renda = renda,
                data_atualizacao = data_atualizacao
        )

        # Adiciona a instância ao banco de dados
        session.add(criar_cliente)

        # Basicamente faz um filtro na tabela de clientes a partir do CPF/CNPJ do cliente
        cliente_aux = session.query(Tb_cliente).filter_by(cpf=cpf).first()

        # Checa se há alguma coisa na variável cliente_aux
        if cliente_aux:

            # Cria uma nova instância da tabela de contas mapeando os atributos correspondentes aos campos na tabela
            criar_conta = Tb_conta(
                id_cliente = cliente_aux.id_cliente,
                agencia = agencia,
                conta = conta,
                tipo_conta = tipo_conta,
                saldo = saldo,
                data_atualizacao = data_atualizacao
            )

            # Adiciona a instância ao banco de dados
            session.add(criar_conta)

            # Cria uma nova instância da tabela de enderecos mapeando os atributos correspondentes aos campos na tabela
            adicionar_endereco = Tb_endereco(
                id_cliente = cliente_aux.id_cliente,
                rua = rua,
                numero = numero,
                bairro = bairro,
                cidade = cidade,
                uf = uf,
                cep = cep,
                data_atualizacao = data_atualizacao
            )

            # Adiciona a instância ao banco de dados
            session.add(adicionar_endereco)

        # Commita (confirma) as transações no banco de dados
        session.commit()

        # Fecha a sessão
        session.close()

        # Retorno da função
        return 'Conta cadastrada com sucesso!'

    # Bloco de exceção
    except Exception as e:

        return f'Não foi possível concluir a operação devido a um erro identificado.\n\nErro: {e}'

def sacar(cpf: str, valor: float, data_atualizacao: datetime) -> str:

    '''
    Objetivo
    --------
    A função tem como objetivo realizar a operação de saque na conta do cliente. \n

    Parâmetros
    ----------
    A função espera receber um CPF/CNPJ, um valor e uma data de atualização para funcionar. \n

    Retorno
    -------
    O retorno da função é uma string "Operação concluída com sucesso!" em caso de sucesso ou uma exceção em caso de erro durante o processamento.
    '''

    # Bloco try-except para tratamento de exceção
    try:

        # Cria a conexão com o banco de dados
        engine = conectar_db()

        # Chama a função localizar_cliente
        retorno_cliente = localizar_cliente(cpf)

        # Cria a sessão para interagir com o banco de dados
        Session = sessionmaker(bind=engine)
        session = Session()

        # Basicamente faz um filtro na tabela de conta através do ID_Cliente
        conta = session.query(Tb_conta).filter_by(id_cliente=retorno_cliente['ID_Cliente']).first()

        # Realiza a operação reduzindo o valor de saque desejado
        conta.saldo -= valor

        # Incluí a data de atualização da operação
        conta.data_atualizacao = data_atualizacao

        # Commita (confirma) as transações no banco de dados
        session.commit()

        # Fecha a sessão
        session.close()

        # Retorno da função
        return 'Operação concluída com sucesso!'

    # Bloco de exceção
    except Exception as e:

        return f'Não foi possível concluir a operação devido a um erro identificado.\n\nErro: {e}'

def consultar_saldo_bancario(cpf: str) -> str:

    '''
    Objetivo
    --------
    A função tem como objetivo realizar a operação de consultar o saldo atual na conta bancária do cliente. \n

    Parâmetros
    ----------
    A função espera receber um CPF/CNPJ para funcionar. \n

    Retorno
    -------
    O retorno da função é uma string com o saldo bancário em caso de sucesso ou uma exceção em caso de erro durante o processamento.
    '''

    # Bloco try-except para tratamento de exceção
    try:

        # Cria a conexão com o banco de dados
        engine = conectar_db()

        # Chama a função localizar_cliente
        retorno_cliente = localizar_cliente(cpf)

        # Cria uma sessão para interagir com o banco de dados
        Session = sessionmaker(bind=engine)
        session = Session()

        # Basicamente faz um filtro na tabela de conta a partir do ID_Cliente
        conta = session.query(Tb_conta).filter_by(id_cliente=retorno_cliente['ID_Cliente']).first()

        # Fecha a sessão
        session.close()

        # Retorno da função
        return {"Saldo": conta.saldo}

    # Bloco de exceção
    except Exception as e:

        return print(f'Não foi possível concluir a operação devido a um erro identificado.\n\nErro: {e}')

def depositar(cpf: str, valor: float, data_atualizacao: datetime) -> str:

    '''
    Objetivo
    --------
    A função tem como objetivo realizar a operação de depositar um valor na conta bancária do cliente. \n

    Parâmetros
    ----------
    A função espera receber um CPF/CNPJ, um valor e uma data de atualização para funcionar. \n

    Retorno
    -------
    O retorno da função é uma string "Operação concluída com sucesso!" em caso de sucesso ou uma exceção em caso de erro durante o processamento.
    '''

    # Bloco try-except para tratamento de exceção
    try:

        # Cria a conexão com o banco de dados
        engine = conectar_db()

        # Chama a função localizar_cliente
        retorno_cliente = localizar_cliente(cpf)

        # Cria a sessão para interagir com o banco de dados
        Session = sessionmaker(bind=engine)
        session = Session()

        # Basicamente faz um filtro na tabela de conta a partir do ID_Cliente
        conta = session.query(Tb_conta).filter_by(id_cliente=retorno_cliente['ID_Cliente']).first()

        # Realiza a operação adicionando o valor de depósito desejado
        conta.saldo += valor

        # Incluí a data de atualização da operação
        conta.data_atualizacao = data_atualizacao

        # Commita (confirma) as transações no banco de dados
        session.commit()

        #Fecha a sessão
        session.close()

        # Retorno da função
        return 'Operação concluída com sucesso!'

    # Bloco de exceção
    except Exception as e:

        return f'Não foi possível concluir a operação devido a um erro identificado.\n\nErro: {e}'

def transferir(
        cpf: str, 
        valor: float, 
        data_atualizacao: datetime, 
        tipo_operacao: str = None
    ) -> str:

    '''
    Objetivo
    --------
    A função tem como objetivo realizar a operação de transferir um valor na conta bancária de um cliente para outro. \n

    Parâmetros
    ----------
    A função espera receber um CPF/CNPJ, um valor, uma data de atualização e o tipo de operação. \n

    Retorno
    -------
    O retorno da função é uma string "Operação concluída com sucesso!" em caso de sucesso ou uma exceção em caso de erro durante o processamento.
    '''

    # Bloco try-except para tratamento de exceção
    try:

        # Condicional que verifica se o valor do parâmetro tipo_operacao é "beneficiario" ou None
        if tipo_operacao not in ['beneficiario', None]:

            raise ValueError('O tipo de operação deve ser "beneficiario" ou "None".')

        else:

            # Cria a conexão com o banco de dados
            engine = conectar_db()

            # Chama a função localizar_cliente
            retorno_cliente = localizar_cliente(cpf)

            # Cria a sessão para interagir com o banco de dados
            Session = sessionmaker(bind=engine)
            session = Session()

            # Basicamente faz um filtro na tabela de conta a partir do ID_Cliente
            conta = session.query(Tb_conta).filter_by(id_cliente=retorno_cliente['ID_Cliente']).first()

            # Condicional que vai determinar qual conta será debitada e qual conta será creditada
            if tipo_operacao == 'beneficiario':
                conta.saldo += valor
                conta.data_atualizacao = data_atualizacao
            elif tipo_operacao is None:
                conta.saldo -= valor
                conta.data_atualizacao = data_atualizacao

            # Commita (confirma) as transações no banco de dados
            session.commit()

            # Fecha a sessão
            session.close()

            # Retorno da função
            return 'Operação concluída com sucesso!'

    # Bloco de exceção
    except Exception as e:

        return f'Não foi possível concluir a operação devido a um erro identificado.\n\nErro: {e}'

def armanezar_transacao(
        id_cliente: int, 
        valor_transacao: float, 
        tipo_transacao: str, 
        protocolo_transacao: str, 
        data_atualizacao: datetime
    ) -> str:

    '''
    Objetivo
    --------
    A função tem como objetivo armazenar todas as transações que ocorrerem nas operações bancárias. \n

    Parâmetros
    ----------
    A função espera receber um id_cliente, valor de transação, tipo de transação, o protocolo da transação e uma data de atualização para funcionar. \n

    Retorno
    -------
    O retorno da função é uma string "Operação concluída com sucesso!" em caso de sucesso ou uma exceção em caso de erro durante o processamento.
    '''

    # Bloco try-except para tratamento de exceção
    try:

        # Cria a conexão com o banco de dados
        engine = conectar_db()

        # Cria a sessão para interagir com o banco de dados
        Session = sessionmaker(bind=engine)
        session = Session()

        # Cria uma nova instância da tabela de transação mapeando os atributos correspondentes aos campos na tabela
        transacao = Tb_transacao(
                id_cliente = id_cliente,
                valor_transacao= valor_transacao,
                tipo_transacao = tipo_transacao,
                protocolo_transacao = protocolo_transacao,
                data_atualizacao = data_atualizacao
        )

        # Adiciona a instância ao banco de dados
        session.add(transacao)

        # Commita (confirma) as transações no banco de dados
        session.commit()

        # Fecha a sessão
        session.close()

        # Retorno da função
        return 'Operação concluída com sucesso!'

    # Bloco de exceção
    except Exception as e:

        return f'Não foi possível commitar a transação realizada devio a um erro identificado.\n\nErro: {e}'

def exibir_dados(cpf: str) -> dict:

    '''
    Objetivo
    --------
    A função tem como objetivo exibir os dados do cliente. \n

    Parâmetros
    ----------
    A função espera receber CPF/CNPJ para funcionar. \n

    Retorno
    -------
    O retorno da função é um dicionário com as informações de id_cliente, nome, gênero, cpf, rg, data de nascimento, agência, conta, email, celular, renda, rua, numero, bairro, cidade, uf e cep.
    '''

    # Cria a conexão com o banco de dados
    engine = conectar_db()

    # Cria a sessão para interagir com o banco de dados
    Session = sessionmaker(bind=engine)
    session = Session()

    # Basicamente faz um filtro na tabela de clientes a partir do CPF/CNPJ do cliente 
    cliente = session.query(Tb_cliente).filter_by(cpf=cpf).first()

    # Basicamente faz um filtro na tabela de contas a partir do id cliente que retornou na variável cliente
    conta = session.query(Tb_conta).filter_by(id_cliente=cliente.id_cliente).first()

    # Basicamente faz um filtro na tabela de enderecos a partir do id cliente que retornou na variável cliente
    endereco = session.query(Tb_endereco).filter_by(id_cliente=cliente.id_cliente).first()

    # Fecha a sessão
    session.close()

    # Retorno da função
    return {
                "ID_Cliente": cliente.id_cliente,
                "Nome_cliente": cliente.nome,
                "Sobrenome_cliente": cliente.sobrenome,
                "Gênero": cliente.genero,
                "CPF": cliente.cpf, 
                "RG": cliente.rg,
                "Data_nascimento": cliente.data_nascimento,
                "Agência": conta.agencia,
                "Conta": conta.conta,
                "Saldo": conta.saldo,
                "Email": cliente.email,
                "Celular": cliente.celular,
                "Renda": cliente.renda,
                "Rua": endereco.rua,
                "Número": endereco.numero,
                "Bairro": endereco.bairro,
                "Cidade": endereco.cidade,
                "UF": endereco.uf,
                "CEP": endereco.cep
            }

# Verifica se é o arquivo main que está sendo executado
if __name__ == '__main__':

    logging.warning('Esse script não deve ser executado diretamente. Para utilizá-lo, execute o script "main.py"')
