from sqlalchemy import create_engine, MetaData, Table, select, Column, Integer, String, Date, DateTime, Float, Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date


Base = declarative_base()

class DadosCliente(Base):

        __tablename__ = 'd_clientes'

        id_cliente = Column(Integer, primary_key=True)
        nome_cliente = Column(String)
        genero = Column(String)
        cpf = Column(String)
        rg = Column(String)
        data_nascimento = Column(Date)
        email = Column(String)
        celular = Column(String)
        renda = Column(Float)
        data_atualizacao = Column(DateTime)


class DadosConta(Base):

        __tablename__ = 'd_dados_conta'

        id_conta = Column(Integer, primary_key=True)
        id_cliente = Column(Integer, ForeignKey('d_clientes.id_cliente'))
        agencia = Column(String, unique=True)
        conta = Column(String, unique=True)
        saldo = Column(Float)
        data_atualizacao = Column(DateTime)


class DadosEndereco(Base):

        __tablename__ = 'd_enderecos'

        id_endereco = Column(Integer, primary_key=True)
        id_cliente = Column(Integer, ForeignKey('d_clientes.id_cliente'))
        rua = Column(String)
        numero = Column(String)
        bairro = Column(String)
        cidade = Column(String)
        uf = Column(String)
        cep = Column(String)
        data_atualizacao = Column(DateTime)


class DadosTransacao(Base):

        __tablename__ = 'f_transacoes'

        id_transacao = Column(Integer, primary_key=True)
        id_cliente = Column(Integer, ForeignKey('d_clientes.id_cliente'))
        valor_transacao = Column(Float)
        tipo_transacao = Column(String)
        protocolo_transacao = Column(String)
        data_atualizacao = Column(DateTime)


def _realizar_conexao_db():

    username = 'postgres'
    password = 'postgre527961'
    hostname = 'localhost'
    database_name = 'db_banco_postgres'

    connection = f'postgresql://{username}:{password}@{hostname}/{database_name}'

    global engine

    engine = create_engine(connection)


def localizar_cliente_db(cpf):

    _realizar_conexao_db()

    Session = sessionmaker(bind=engine)
    session = Session()

    filtrar_cliente = session.query(DadosCliente).filter_by(cpf=cpf).first()

    session.close()

    return {
                "ID_Cliente": filtrar_cliente.id_cliente,
                "Nome_cliente": filtrar_cliente.nome_cliente,
                "Gênero": filtrar_cliente.genero,
                "CPF": filtrar_cliente.cpf, 
                "RG": filtrar_cliente.rg,
                "Data_nascimento": filtrar_cliente.data_nascimento,
                "Email": filtrar_cliente.email,
                "Celular": filtrar_cliente.celular,
                "Renda": filtrar_cliente.renda
            } \
    if filtrar_cliente else "Cliente não encontrado"


def localizar_agencia_conta_db(cpf):

    _realizar_conexao_db()

    Session = sessionmaker(bind=engine)
    session = Session()

    filtrar_cliente = session.query(DadosCliente).filter_by(cpf=cpf).first()

    filtrar_conta = session.query(DadosConta).filter_by(id_cliente=filtrar_cliente.id_cliente).first()

    session.close()

    return {
                "ID_Cliente": filtrar_conta.id_cliente,
                "Agência": filtrar_conta.agencia, 
                "Conta": filtrar_conta.conta, 
                "Saldo": filtrar_conta.saldo
            }


def cadastrar_cliente(
        nome_cliente: str, 
        genero: str, 
        cpf: str, 
        rg: str, 
        data_nascimento: date, 
        email: str, 
        celular: str, 
        renda: float, 
        agencia: str,
        conta: str,
        saldo: float,
        rua: str,
        numero: str,
        bairro: str,
        cidade: str,
        uf: str,
        cep: str,
        data_atualizacao: datetime
    ):

    try:

        _realizar_conexao_db()

        Session = sessionmaker(bind=engine)
        session = Session()

        criar_cliente = DadosCliente(
                nome_cliente = nome_cliente,
                genero = genero,
                cpf = cpf,
                rg = rg,
                data_nascimento = data_nascimento,
                email = email,
                celular = celular,
                renda = renda,
                data_atualizacao = data_atualizacao
        )

        session.add(criar_cliente)

        cliente_aux = session.query(DadosCliente).filter_by(cpf=cpf).first()

        if cliente_aux:

            criar_conta = DadosConta(
                id_cliente = cliente_aux.id_cliente,
                agencia = agencia,
                conta = conta,
                saldo = saldo,
                data_atualizacao = data_atualizacao
            )

            session.add(criar_conta)

            adicionar_endereco = DadosEndereco(
                id_cliente = cliente_aux.id_cliente,
                rua = rua,
                numero = numero,
                bairro = bairro,
                cidade = cidade,
                uf = uf,
                cep = cep,
                data_atualizacao = data_atualizacao
            )

            session.add(adicionar_endereco)

        session.commit()

        return print('Conta cadastrada com sucesso!')

    except Exception as e:

        return f'Não foi possível concluir a operação devido a um erro identificado.\n\nErro: {e}'

def remover_cliente():
    pass

def atualizar_dados_cliente(cpf: str, tabela_atualizacao: str,  valor_atualizado: str):

    try:

        retorno_cliente = localizar_cliente_db(cpf)

        Session = sessionmaker(bind=engine)
        session = Session()

        filtrar_conta = session.query(tabela_atualizacao).filter_by(id_cliente=retorno_cliente['ID_Cliente']).first()

        filtrar_conta.cpf = valor_atualizado

        session.commit()

        session.close()

        return 'Dado atualizado com sucesso!'

    except Exception as e:

        return f'Não foi possível concluir a operação devido a um erro identificado.\n\nErro: {e}'

def exibir_dados_cliente():
    pass

def atualizar_saque(cpf: str, valor: float, data_atualizacao: date) -> str:

    try:

        retorno_cliente = localizar_cliente_db(cpf)

        print(retorno_cliente)

        Session = sessionmaker(bind=engine)
        session = Session()

        filtrar_conta = session.query(DadosConta).filter_by(id_cliente=retorno_cliente['ID_Cliente']).first()

        filtrar_conta.saldo -= valor
        filtrar_conta.data_atualizacao = data_atualizacao

        session.commit()

        session.close()

        return "Operação concluída com sucesso!"

    except Exception as e:

        return f'Não foi possível concluir a operação devido a um erro identificado.\n\nErro: {e}'

def consultar_saldo_bancario(cpf: str) -> str:

    try:

        retorno_cliente = localizar_cliente_db(cpf)

        Session = sessionmaker(bind=engine)
        session = Session()

        filtrar_conta = session.query(DadosConta).filter_by(id_cliente=retorno_cliente['ID_Cliente']).first()

        session.close()

        return {"Saldo": filtrar_conta.saldo}

    except Exception as e:

        return print(f'Não foi possível concluir a operação devido a um erro identificado.\n\nErro: {e}')

def atualizar_deposito_bancario(cpf: str, valor: float, data_atualizacao:  datetime) -> str:

    try:

        retorno_cliente = localizar_cliente_db(cpf)

        Session = sessionmaker(bind=engine)
        session = Session()

        filtrar_conta = session.query(DadosConta).filter_by(id_cliente=retorno_cliente['ID_Cliente']).first()

        filtrar_conta.saldo += valor
        filtrar_conta.data_atualizacao = data_atualizacao

        session.commit()

        session.close()

        return 'Operação concluída com sucesso!'

    except Exception as e:

        return f'Não foi possível concluir a operação devido a um erro identificado.\n\nErro: {e}'

def atualizar_transferencia(cpf: str, valor: float, data_atualizacao: datetime, tipo_operacao: str = None) -> str:

    try:

        if tipo_operacao not in ['beneficiario', None]:

            raise ValueError('O tipo de operação deve ser "beneficiario" ou "None".')

        else:

            retorno_cliente = localizar_cliente_db(cpf)

            Session = sessionmaker(bind=engine)
            session = Session()

            filtrar_conta = session.query(DadosConta).filter_by(id_cliente=retorno_cliente['ID_Cliente']).first()

            if tipo_operacao == 'beneficiario':
                filtrar_conta.saldo += valor
                filtrar_conta.data_atualizacao = data_atualizacao
            elif tipo_operacao is None:
                filtrar_conta.saldo -= valor
                filtrar_conta.data_atualizacao = data_atualizacao

            session.commit()

            session.close()

            return 'Operação concluída com sucesso!'

    except Exception as e:

        return f'Não foi possível concluir a operação devido a um erro identificado.\n\nErro: {e}'

def armanezar_transacao(id_cliente: int, valor_transacao: float, tipo_transacao: str, protocolo_transacao: str, data_atualizacao: datetime):

    try:

        _realizar_conexao_db()

        Session = sessionmaker(bind=engine)
        session = Session()

        transacao = DadosTransacao(
                id_cliente = id_cliente,
                valor_transacao= valor_transacao,
                tipo_transacao = tipo_transacao,
                protocolo_transacao = protocolo_transacao,
                data_atualizacao = data_atualizacao
        )

        session.add(transacao)

        session.commit()

        session.close()

        return "Operação concluída com sucesso!"

    except Exception as e:

        return f'Não foi possível commitar a transação realizada devio a um erro identificado.\n\nErro: {e}'
