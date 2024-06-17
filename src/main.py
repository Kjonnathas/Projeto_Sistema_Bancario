from conta_corrente import ContaCorrente
from database_manager import cadastrar_cliente

if __name__ == '__main__':

    conta = ContaCorrente()

    cadastrar_cliente(
        nome_cliente=conta._nome,
        genero=conta._genero,
        cpf=conta._cpf,
        rg=conta._rg,
        data_nascimento=conta._data_nascimento,
        email=conta._email,
        celular=conta._celular,
        profissao=conta._profissao,
        renda=conta._renda,
        agencia=conta._agencia,
        conta=conta._conta,
        tipo_conta='Corrente',
        saldo=conta._saldo,
        rua=conta._endereco['rua'],
        numero = conta._endereco['numero'],
        bairro=conta._endereco['bairro'],
        cidade=conta._endereco['cidade'],
        uf=conta._endereco['uf'],
        cep=conta._endereco['cep'],
        data_atualizacao=conta._data_hora()
    )