from ContaCorrente import ContaCorrente
from DatabaseManager import cadastrar_cliente

if __name__ == '__main__':

    conta = ContaCorrente()

    cadastrar_cliente(
        nome_cliente=conta.nome,
        genero=conta.genero,
        cpf=conta.cpf,
        rg=conta.rg,
        data_nascimento=conta.data_nascimento,
        email=conta.email,
        celular=conta.celular,
        renda=conta.renda,
        agencia=conta.agencia,
        conta=conta.conta,
        saldo=conta.saldo,
        rua=conta.endereco['rua'],
        numero = conta.endereco['numero'],
        bairro=conta.endereco['bairro'],
        cidade=conta.endereco['cidade'],
        uf=conta.endereco['uf'],
        cep=conta.endereco['cep'],
        data_atualizacao=conta._data_hora()
    )