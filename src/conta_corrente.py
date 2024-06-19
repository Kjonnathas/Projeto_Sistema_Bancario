
import os
import sys
import time
from datetime import datetime, date
import pytz
from email_validator import validate_email
import re
import random
import hashlib
import logging
from database_manager import localizar_cliente, localizar_conta, transferir, depositar, sacar, consultar_saldo_bancario, armanezar_transacao, exibir_dados


# Defini o nível de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# Criação da classe ContaCorrente
class ContaCorrente:

    # Criação de um método estático
    @staticmethod
    def _data_hora():
        fuso_br = pytz.timezone('Brazil/East')
        horario_br = datetime.now(fuso_br)
        return horario_br.strftime('%d/%m/%Y %H:%M:%S')

    # Criação do método init
    def __init__(self):
        self._nome = self._validar_nome()
        self._sobrenome = self._validar_sobrenome()
        self._cpf = self._validar_cpf()
        if self.resposta_atendimento is None or self.resposta_atendimento == 'N':
            sys.exit()
        else:
            self._rg = self._validar_rg()
            self._data_nascimento = self._validar_data_nascimento()
            self._genero = self._validar_genero()
            self._email = self._validar_email()
            self._celular = self._validar_celular()
            self._profissao = self._validar_profissao()
            self._renda = self._validar_renda()
            self._endereco = self._validar_endereco()
            self._agencia = self._criar_agencia()
            self._conta = self._criar_conta()
            self._saldo = 0

    def _validar_nome(self) -> str:

        '''
        Objetivo
        --------
        A função tem como objetivo validar se é um nome válido. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n
        
        Retorno
        -------
        O retorno da função é uma string (str).
        '''

        while True:
            self._nome = input('Olá, seja bem-vindo ao J.P. Morgan. Poderia me informar o seu primeiro nome? ').strip()
            validar_nome = self._nome.replace(' ', '')
            if validar_nome.isalpha():
                os.system('cls')
                return self._nome.title()
            else:
                print('O nome digitado é inválido. Por favor, digite novamente.')
                time.sleep(5)
                os.system('cls')

    def _validar_sobrenome(self) -> str:

        '''
        Objetivo
        --------
        A função tem como objetivo validar se é um sobrenome válido. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str).
        '''

        while True:
            self._sobrenome = input(f'{self._nome}, seu nome é muito bonito. Qual seria o seu sobrenome? ').strip()
            if self._sobrenome.isalpha():
                os.system('cls')
                return self._nome.title()
            else:
                print('O sobrenome digitado é inválido. Por favor, digite novamente.')
                time.sleep(5)
                os.system('cls')

    def _validar_cpf(self) -> str:

        '''
        Objetivo
        --------
        A função tem como objetivo validar se é um CPF válido. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str).
        '''

        while True:
            self._cpf = input(f'Obrigado, {self._nome.split()[0].title()}!\n\nEstou muito feliz de poder atendê-lo (a)!\n\nAgora, você poderia me informar o seu CPF (somente números)? ').strip()
            self._cpf = '{}.{}.{}-{}'.format(self._cpf[:3], self._cpf[3:6], self._cpf[6:9], self._cpf[9:])
            localizar_cliente_ = localizar_cliente(self._cpf)
            if localizar_cliente_ != 'Cliente não encontrado':
                os.system('cls')
                print(f'{self._nome.split()[0]}, verifiquei que você é nosso (a) cliente. Seja bem-vindo (a) ao seu autoatendimento.')
                self._inicializar_atendimento_cliente()
                self.resposta_atendimento = None
                return self._cpf
            else:
                if len(str(self._cpf)) == 14 and self._cpf.replace('.', '').replace('-', '').isnumeric():
                    os.system('cls')
                    self._continuar_atendimento()
                    return self._cpf
                else:
                    print('O CPF digitado é inválido. Por favor, digite novamente.')
                    time.sleep(5)
                    os.system('cls')

    def _continuar_atendimento(self) -> str :

        '''
        Objetivo
        --------
        A função tem como objetivo interagir com o cliente ou identificar se é um possível novo cliente. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str).
        '''

        while True:
            self.resposta_atendimento = input(f'{self._nome.split()[0].title()}, eu reparei que você ainda não é nosso (a) cliente.\n\nAdoraríamos tê-lo (a) conosco. Gostaria de abrir uma conta corrente? (S/N) ').strip()
            os.system('cls')
            if self.resposta_atendimento != 'S' and self.resposta_atendimento != 'N':
                print('Você digitou uma resposta inválida. Por favor, digite novamente para que possamos continuar com o seu atendimento!')
                time.sleep(5)
                os.system('cls')
            elif self.resposta_atendimento == 'S':
                print(f'{self._nome.split()[0].title()}, que massa que você quer abrir uma conta conosco! Estamos muito felizes :)\n\nVamos fazer mais algumas perguntas para finalizar o seu cadastro, mas será rápido, não se preocupe!')
                time.sleep(10)
                os.system('cls')
                return self.resposta_atendimento
            else:
                print(f'Poxa, {self._nome.split()[0].title()}! Ficamos tristes por você não optar se juntar a nós neste momento ):\n\nMas tudo bem, entendemos. Quem sabe no futuro né? :)\n\nDe qualquer forma gostaríamos de agradecê-lo. Irei finalizar o seu atendimento neste momento.')
                time.sleep(10)
                os.system('cls')
                return self.resposta_atendimento

    def _validar_rg(self) -> str:

        '''
        Objetivo
        --------
        A função tem como objetivo validar se é um RG válido. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str).
        '''

        while True:
            self._rg = input('Dando continuidade ao seu atendimento, digite o seu RG (apenas números): ').strip()
            if not self._rg:
                print('O RG não foi informado. Por favor, digite novamente.')
                time.sleep(5)
                os.system('cls')
            else:
                if len(str(self._rg)) == 9 and self._rg.isnumeric():
                    self._rg = '{}.{}.{}-{}'.format(self._rg[:2], self._rg[2:5], self._rg[5:8], self._rg[8:])
                    os.system('cls')
                    return self._rg
                else:
                    print('O RG digitado é inválido. Por favor, digite novamente.')
                    time.sleep(5)
                    os.system('cls')

    def _validar_data_nascimento(self) -> date:

        '''
        Objetivo
        --------
        A função tem como objetivo validar se a data de nascimento é válida. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma data (date).
        '''

        while True:
            self._data_nascimento = input('Digite a sua data de nascimento (DD/MM/AAAA): ').strip()
            if not self._data_nascimento:
                print('A data de nascimento não foi informada. Por favor, digite novamente.')
                time.sleep(5)
                os.system('cls')
            else:
                try:
                    self._data_nascimento = datetime.strptime(self._data_nascimento, '%d/%m/%Y')
                    if self._data_nascimento > datetime.today():
                        print('A data de nascimento não pode ser maior do que a data atual. Por favor, digite novamente.')
                        time.sleep(5)
                        os.system('cls')
                    else:
                        os.system('cls')
                        return self._data_nascimento
                except ValueError:
                    print('A data de nascimento informada é inválida. Por favor, digite novamente')
                    time.sleep(5)
                    os.system('cls')

    def _validar_genero(self) -> str:

        '''
        Objetivo
        --------
        A função tem como objetivo validar se é um gênero válido. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str).
        '''

        while True:
            self._genero = input('Digite o seu gênero (M/F): ').strip()
            if not self._genero:
                print('O gênero não foi informado. Por favor, digite novamente.')
                time.sleep(5)
                os.system('cls')
            else:
                if self._genero == "M" or self._genero == 'F':
                    os.system('cls')
                    return self._genero
                else:
                    print('O gênero digitado é inválido. Por favor, digite novamente.')
                    time.sleep(5)
                    os.system('cls')

    def _validar_email(self) -> str | None:

        '''
        Objetivo
        --------
        A função tem como objetivo validar se é um e-mail válido. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str) ou nulo (None).
        '''

        while True:
            self._email = input('Digite o seu e-mail: ').strip()
            if not self._email:
                print('E-mail não informado.')
                time.sleep(5)
                os.system('cls')
                return None
            else:
                try:
                    self.validar_email = validate_email(self._email)
                    os.system('cls')
                    return self.validar_email.email
                except:
                    print('O e-mail informado é inválido. Por favor, digite novamente.')
                    time.sleep(5)
                    os.system('cls')

    def _validar_celular(self) -> str | None:

        '''
        Objetivo
        --------
        A função tem como objetivo validar se é um celular válido. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str) ou nulo (None).
        '''

        while True:
            self.telefone = input('Digite o seu número de telefone celular (somente números): ').strip()
            if not self.telefone:
                print('Telefone celular não informado.')
                time.sleep(5)
                os.system('cls')
                return None
            else:
                regex_telefone = re.compile(r'^[1-9]{2}9[0-9]{8}$')
                if regex_telefone.match(self.telefone):
                    self.telefone = '({}) {}-{}'.format(self.telefone[:2], self.telefone[2:7], self.telefone[7:])
                    os.system('cls')
                    return self.telefone
                else:
                    print('O número de telefone celular é inválido. Por favor, digite novamente.')
                    time.sleep(5)
                    os.system('cls')

    def _validar_profissao(self) -> str | None:

        '''
        Objetivo
        --------
        A função tem como objetivo validar se é uma profissão válida. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str) ou nulo (None).
        '''

        while True:
            self._profissao = input('Digite a sua profissão: ').strip()
            if not self._profissao:
                print('Profissão não informada.')
                time.sleep(5)
                os.system('cls')
                return None
            else:
                if len(self._profissao) < 4 or not self._profissao.isalpha():
                    print('A profissão informada é inválida. Por favor, digite novamente.')
                    time.sleep(5)
                    os.system('cls')
                else:
                    os.system('cls')
                    return self._profissao

    def _validar_valor(self, valor: str) -> float | str:

        '''
        Objetivo
        --------
        A função tem como objetivo validar se um valor é válido. \n

        Parâmetros
        ----------
        A função precisa de um valor para funcionar. \n

        Retorno
        -------
        O retorno da função é um valor numérico (float) ou uma string (str).
        '''

        valor = valor.strip()
        regex_valor = re.compile(r'^\d+(\.\d{3})*(?:,\d{1,2})?$')
        if regex_valor.match(valor):
            valor = valor.replace(',', '_')
            valor = valor.replace('.', '')
            valor = valor.replace('_', '.')
            valor = float(valor)
            if float(valor) == 0 or float(valor) < 0:
                return 'valor inválido'
            else:
                return valor
        else:
            return 'valor inválido'

    def _validar_renda(self) -> float | None:

        '''
        Objetivo
        --------
        A função tem como objetivo validar se é uma renda válida. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é um valor numérico (float) ou nulo (None).
        '''

        while True:
            self._renda = input('Digite a sua renda atual (somente números): ').strip()
            if not self._renda.strip():
                print('Renda não informada.')
                time.sleep(5)
                os.system('cls')
                return None
            else:
                validar_renda = self._validar_valor(self._renda)
                if validar_renda == 'valor inválido':
                    print('A renda informada é inválida. Por favor, digite novamente.')
                    time.sleep(5)
                    os.system('cls')
                else:
                    self._renda = self._validar_valor(self._renda)
                    os.system('cls')
                    return self._renda

    def _validar_endereco(self) -> dict:

        '''
        Objetivo
        --------
        A função tem como objetivo validar se é um endereço válido. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é um dicionário (dict).
        '''

        print(f'{self._nome.split()[0].title()}, estamos quase lá! Agora, só precisamos que nos informe o seu endereço para concluirmos o seu cadastro, ok?')
        time.sleep(10)
        os.system('cls')
        while True:
            rua = input('Qual o nome da sua rua? ').strip().title()
            os.system('cls')
            if rua:
                while True:
                    numero = input('Qual o número da sua residência? ').strip()
                    os.system('cls')
                    if numero:
                        while True:
                            bairro = input('Qual o nome do seu bairro? ').strip().title()
                            os.system('cls')
                            if bairro:
                                while True:
                                    cidade = input('Qual o nome da sua cidade? ').strip().title()
                                    os.system('cls')
                                    if cidade:
                                        while True:
                                            uf = input('Qual a sua UF? ').strip().upper()
                                            os.system('cls')
                                            if uf:
                                                if len(uf) == 2:
                                                    while True:
                                                        cep = input('Qual o seu CEP? (somente números) ').strip()
                                                        os.system('cls')
                                                        if cep:
                                                            regex_cep = re.compile(r'\d{8}')
                                                            if regex_cep.fullmatch(cep):
                                                                print(f'{self._nome.split()[0].title()}, parecia que não ia ter fim né? Mas conseguimos finalizar o seu cadastro hahahaha.\n\nSeja muito bem-vindo ao J.P. Morgan.\n\nAgora você pode desfrutar de todo o ecossistema que o nosso banco oferece, além de todo suporte que precisar!\n\nConte conosco!')
                                                                time.sleep(10)
                                                                os.system('cls')
                                                                cep = '{}-{}'.format(cep[:5], cep[5:])
                                                                self._endereco = {
                                                                    'rua': rua,
                                                                    'numero': numero,
                                                                    'bairro': bairro,
                                                                    'cidade': cidade,
                                                                    'uf': uf,
                                                                    'cep': cep
                                                                }
                                                                return self._endereco
                                                            else:
                                                                print('O CEP digitado é inválido. Por favor, digite novamente')
                                                        else:
                                                            print('Você não digitou o seu CEP. Por favor, digite novamente')
                                                else:
                                                    print('A UF digitada é inválida. Por favor, digite novamente.')
                                            else:
                                                print('Você não digitou o nome da sua UF. Por favor, digite novamente.')
                                    else:
                                        print('Você não digitou o nome da sua cidade. Por favor, digite novamente.')
                            else:
                                print('Você não digitou o nome do seu bairro. Por favor, digite novamente.')
                    else:
                        print('Você não digitou o número da sua residência. Por favor, digite novamente')
            else:
                print('Você não digitou o nome da sua rua. Por favor, digite novamente.')

    def _criar_agencia(self) -> str:

        '''
        Objetivo
        --------
        A função tem como objetivo gerar uma sequência de números randômicos para a criação de um número de agência. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str).
        '''

        self._agencia = ''.join(str(random.randint(0, 9)) for _ in range(4))
        return self._agencia

    def _criar_conta(self) -> str:

        '''
        Objetivo
        --------
        A função tem como objetivo gerar uma sequência de números randômicos para a criação de um número de conta. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str).
        '''

        self._conta = ''.join(str(random.randint(0, 9)) for _ in range(8)) + '-' + str(random.randint(0, 9))
        return self._conta

    def _inicializar_atendimento_cliente(self) -> str:

        '''
        Objetivo
        --------
        A função tem como objetivo gerar um menu de atendimento para o cliente. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str).
        '''

        print('\n')
        print('Selecione uma das opções abaixo (digite somente o número correspondente a operação desejada): ')
        print('\n')
        print('1) Meus Dados Pessoais')
        print('2) Sacar Dinheiro')
        print('3) Depositar Dinheiro')
        print('4) Transferir Dinheiro')
        print('5) Consultar Saldo')
        print('6) Sair')
        print('\n')

        while True:

            input_atendimento = int(input('Qual opção você deseja? ').strip())

            match input_atendimento:

                case 1:
                    self.exibir_dados_pessoais()
                    break
                case 2:
                    self.sacar_dinheiro()
                    break
                case 3:
                    self.depositar_dinheiro()
                    break
                case 4:
                    self.transferir_dinheiro()
                    break
                case 5:
                    self.consultar_saldo()
                    break
                case 6:
                    os.system('cls')
                    print('Opção de sair foi selecionada. Agradecemos o contato e nos desculpe qualquer coisa.')
                    time.sleep(5)
                    os.system('cls')
                    break
                case _:
                    print('Opção digitada é inválida. Por favor, digite uma opção válida.')

    def _criar_chave_hash(self, nome_cliente, cpf) -> str:

        '''
        Objetivo
        --------
        A função tem como objetivo gerar uma sequência de números e letras de forma randômica para a criação de protocolos de operações. \n

        Parâmetros
        ----------
        A função precisa de um nome e de um CPF para funcionar. \n

        Retorno
        -------
        O retorno da função é uma string (str).
        '''

        chave = '{}_{}'.format(nome_cliente, cpf)

        obj_hash = hashlib.sha256()
        obj_hash.update(chave.encode('utf-8'))

        chave_hash = obj_hash.hexdigest()
        chave_hash = chave_hash[:100]
        chave_hash = list(chave_hash)

        random.shuffle(chave_hash)
        chave_hash = ''.join(chave_hash)

        return chave_hash

    def _limite_cheque_especial(self) -> float:

        '''
        Objetivo
        --------
        A função tem como objetivo calcular o limite de cheque especial disponível para um determinado cliente. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é um valor numérico (float).
        '''

        dados_cliente = exibir_dados(self._cpf)
        if dados_cliente['Renda'] == None:
            self.limite_cheque_especial = 500
            return self.limite_cheque_especial
        else:
            self.limite_cheque_especial = dados_cliente['Renda'] * 3
            return self.limite_cheque_especial

    def exibir_dados_pessoais(self) -> str:

        '''
        Objetivo
        --------
        A função tem como objetivo exibir para o cliente as informações pessoais dele. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str).
        '''

        os.system('cls')
        dados_cliente = exibir_dados(self._cpf)
        data_nascimento = datetime.strftime(dados_cliente['Data_nascimento'], format='%d/%m/%Y')
        renda = 'Não cadastrado' if dados_cliente['Renda'] == None else 'R$ {:,.2f}'.format(dados_cliente['Renda']).replace('.', '_').replace(',', '.').replace('_', ',')
        email = 'Não cadastrado' if dados_cliente['Email'] == None else dados_cliente['Email']
        celular = 'Não cadastrado' if dados_cliente['Celular'] == None else dados_cliente['Celular']

        print(f'Dados pessoais de {self._nome}:\n')
        print(f'CPF: {dados_cliente["CPF"]}')
        print(f'RG: {dados_cliente["RG"]}')
        print(f'Data de Nascimento: {data_nascimento}')
        print(f'Gênero: {dados_cliente["Gênero"]}')
        print(f'Renda: {renda}')
        print(f'E-mail: {email}')
        print(f'Celular: {celular}')
        print(f'Rua: {dados_cliente["Rua"]}')
        print(f'Número: {dados_cliente["Número"]}')
        print(f'Bairro: {dados_cliente["Bairro"]}')
        print(f'Cidade: {dados_cliente["Cidade"]}')
        print(f'UF: {dados_cliente["UF"]}')
        print(f'CEP: {dados_cliente["CEP"]}')

        time.sleep(15)
        os.system('cls')
        retorno = None
        while retorno != 'S' and retorno != 'N':
            retorno = input('Você gostaria de realizar alguma outra operação? (S/N) ').strip()
            if retorno == 'N':
                os.system('cls')
                print(f'Sendo assim, vamos encerrar o seu atendimento, {self._nome.split()[0].title()}.\n\nObrigado e volte sempre!')
                time.sleep(5)
                os.system('cls')
                break
            elif retorno == 'S':
                return self._inicializar_atendimento_cliente()
            else:
                print('A resposta informada é inválida. Por favor, digite novamente.')
                time.sleep(5)
                os.system('cls')

    def consultar_saldo(self) -> str:

        '''
        Objetivo
        --------
        A função tem como objetivo exibir o saldo bancário do cliente. \n
        
        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str).
        '''

        os.system('cls')
        self._saldo = consultar_saldo_bancario(self._cpf)
        self._saldo = float(self._saldo['Saldo'])
        print('O saldo da sua conta bancária é de R$ {:,.2f}'.format(self._saldo).replace('.', '_').replace(',', '.').replace('_', ','))
        time.sleep(5)
        os.system('cls')

    def depositar_dinheiro(self) -> str:

        '''
        Objetivo
        --------
        A função tem como objetivo depositar um determinado valor na conta do cliente. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str).
        '''

        while True:
            os.system('cls')
            valor_deposito = input('Quanto você gostaria de depositar? ').strip()
            if not valor_deposito:
                print('Nenhum valor informado. Caso queira cancelar a operação digite "Cancelar".')
                time.sleep(5)
                os.system('cls')
            else:
                if valor_deposito == 'Cancelar':
                    print('Operação cancelada com sucesso!')
                    time.sleep(5)
                    os.system('cls')
                    break
                else:
                    deposito = self._validar_valor(valor_deposito)
                    if deposito == 'valor inválido':
                        print('O valor de depósito é inválido. Caso queira cancelar a operação digite "Cancelar".')
                        time.sleep(5)
                        os.system('cls')
                    else:
                        depositar(
                            cpf=self._cpf,
                            valor=deposito,
                            data_atualizacao=ContaCorrente._data_hora()
                        )
                        localizar_cliente_ = localizar_cliente(self._cpf)
                        armanezar_transacao(
                            id_cliente=localizar_cliente_['ID_Cliente'],
                            valor_transacao=deposito,
                            tipo_transacao="Depósito",
                            protocolo_transacao=(protocolo_operacao:= self._criar_chave_hash(self._nome, self._cpf)),
                            data_atualizacao=ContaCorrente._data_hora()
                        )
                        print(f'Depósito realizado com sucesso!\n\nO protocolo da operação é: {protocolo_operacao}')
                        time.sleep(5)
                        os.system('cls')
                        return self.consultar_saldo()

    def transferir_dinheiro(self) -> str | None:

        '''
        Objetivo
        --------
        A função tem como objetivo transferir um valor de uma conta para outra. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str) ou nulo (None).
        '''

        while True:
            os.system('cls')
            cpf_beneficiario = input('Por favor, informe o CPF do beneficiário (somente números): ').strip()
            cpf_beneficiario = '{}.{}.{}-{}'.format(cpf_beneficiario[:3], cpf_beneficiario[3:6], cpf_beneficiario[6:9], cpf_beneficiario[9:])
            if not cpf_beneficiario:
                print('Nenhum CPF informado. Por favor, digite novamente. Caso queira cancelar a operação digite "Cancelar".')
                time.sleep(5)
                os.system('cls')
            else:
                if cpf_beneficiario == 'Cancelar':
                    print('Operação cancelada com sucesso!')
                    time.sleep(5)
                    os.system('cls')
                    break
                os.system('cls')
                print('Localizando o beneficiário...')
                time.sleep(5)
                os.system('cls')
                dados_cliente = localizar_conta(cpf_beneficiario)
                if dados_cliente != 'Cliente não encontrado':
                    agencia_beneficiario = input('Por favor, informe o número da agência: ').strip()
                    conta_beneficiario = input('Por favor, informe o número da conta: ').strip()
                    os.system('cls')
                    print('Localizando agência e conta do beneficiário...')
                    time.sleep(5)
                    os.system('cls')
                    if agencia_beneficiario == dados_cliente['Agência'] and conta_beneficiario == dados_cliente['Conta']:
                        valor = input(f'Quanto você gostaria de transferir para {dados_cliente["Nome_cliente"]}? ').strip()
                        valor_transferencia = self._validar_valor(valor)
                        if valor_transferencia != 'valor inválido':
                            if (dados_cliente['Saldo'] + self._limite_cheque_especial()) >= valor_transferencia:
                                retorno_atualizar_transferencia = transferir(
                                                                        cpf=cpf_beneficiario, 
                                                                        valor=valor_transferencia, 
                                                                        data_atualizacao=ContaCorrente._data_hora(), 
                                                                        tipo_operacao='beneficiario'
                                                                        )
                                armanezar_transacao(
                                                    id_cliente=dados_cliente['ID_Cliente'],
                                                    valor_transacao=valor_transferencia,
                                                    tipo_transacao="Transferência", 
                                                    protocolo_transacao=(protocolo_operacao:= self._criar_chave_hash(self._nome, self._cpf)),
                                                    data_atualizacao=ContaCorrente._data_hora()
                                                    )
                                if retorno_atualizar_transferencia == 'Operação concluída com sucesso!':
                                        transferir(
                                                cpf=self._cpf, 
                                                valor=valor_transferencia, 
                                                data_atualizacao=ContaCorrente._data_hora()
                                                )
                                        id_cliente_titular = localizar_cliente(self._cpf)
                                        armanezar_transacao(
                                                    id_cliente=id_cliente_titular['ID_Cliente'],
                                                    valor_transacao=-valor_transferencia,
                                                    tipo_transacao="Transferência", 
                                                    protocolo_transacao=protocolo_operacao,
                                                    data_atualizacao=ContaCorrente._data_hora()
                                                    )
                                        os.system('cls')
                                        print(f'Transferência concluída com sucesso!\n\nO protocolo da operação é: {protocolo_operacao}')
                                        time.sleep(5)
                                        os.system('cls')
                                        return self.consultar_saldo()
                                else:
                                    print('Não foi possível concluir a transferência.')
                                    time.sleep(5)
                                    os.system('cls')
                                    break
                            else:
                                print('O valor informado não pode ser transferido por falta de saldo na conta.')
                                time.sleep(5)
                                os.system('cls')
                                self.consultar_saldo()
                                while retorno != 'N' and retorno != 'S':
                                    os.system('cls')
                                    retorno = input('Você gostaria de transferir outro valor? (S/N): ').strip()
                                    if retorno == 'N':
                                        os.system('cls')
                                        while novo_retorno != 'N' and novo_retorno != 'S':
                                            os.system('cls')
                                            novo_retorno = input(f'Entendemos, {self._nome.split()[0].title()}. Você gostaria de realizar alguma outra operação? (S/N) ').strip()
                                            if novo_retorno == 'N':
                                                os.system('cls')
                                                print(f'Sendo assim, vamos encerrar o seu atendimento, {self._nome.split()[0].title()}.\n\n Obrigado e volte sempre!')
                                                time.sleep(5)
                                                os.system('cls')
                                                return None
                                            elif novo_retorno == 'S':
                                                return self._inicializar_atendimento_cliente()
                                            else:
                                                print('A resposta informada é inválida. Por favor, digite novamente.')
                                
                        else:
                            print('O valor informado é inválido. Por favor, digite novamente. Caso queira cancelar a operação digite "Cancelar".')
                            time.sleep(5)
                            os.system('cls')
                    else:
                        print('Não conseguimos localizar a Conta e a Agência informadas. Por favor, digite novamente. Caso queira cancelar a operação digite "Cancelar".')
                        time.sleep(5)
                        os.system('cls')
                else:
                    print('Não conseguimos localizar o CPF do beneficiário. Por favor, digite novamente. Caso queira cancelar a operação digite "Cancelar".')
                    time.sleep(5)
                    os.system('cls')

    def sacar_dinheiro(self) -> str | None:

        '''
        Objetivo
        --------
        A função tem como objetivo sacar um determinado valor na conta do cliente. \n

        Parâmetros
        ----------
        A função não precisa de parâmetros. \n

        Retorno
        -------
        O retorno da função é uma string (str) ou nulo (None).
        '''

        while True:
            os.system('cls')
            valor = input('Qual o valor você gostaria de sacar, por gentileza? ').strip()
            if not valor:
                print('Nenhum valor de saque foi informado. Por favor, digite novamente. Caso queira cancelar a operação digite "Cancelar".')
                time.sleep(5)
                os.system('cls')
            else:
                if valor == 'Cancelar':
                    print('Operação cancelada com sucesso!')
                    time.sleep(5)
                    os.system('cls')
                    break
                else:
                    valor_saque = self._validar_valor(valor)
                    if valor_saque != 'valor inválido':
                        saldo_bancario = consultar_saldo_bancario(cpf=self._cpf)
                        if (saldo_bancario['Saldo'] + self._limite_cheque_especial()) >= valor_saque:
                            localizar_cliente_ = localizar_cliente(cpf=self._cpf)
                            sacar(
                                    cpf=self._cpf, 
                                    valor=valor_saque, 
                                    data_atualizacao=ContaCorrente._data_hora()
                                    )
                            armanezar_transacao(
                                id_cliente=localizar_cliente_['ID_Cliente'],
                                valor_transacao=valor_saque,
                                tipo_transacao='Saque',
                                protocolo_transacao=(protocolo_operacao:= self._criar_chave_hash(self._nome, self._cpf)),
                                data_atualizacao=ContaCorrente._data_hora()
                                )
                            os.system('cls')
                            print(f'Saque realizado com sucesso!\n\nO protocolo da operação é: {protocolo_operacao}')
                            time.sleep(5)
                            return self.consultar_saldo()
                        else:
                            print('O valor informado não pode ser sacado por falta de saldo na conta.')
                            time.sleep(5)
                            os.system('cls')
                            self.consultar_saldo()
                            retorno = None
                            while retorno != 'N' and retorno != 'S':
                                os.system('cls')
                                retorno = input('Você gostaria de sacar outro valor? (S/N): ').strip()
                                if retorno == 'N':
                                    os.system('cls')
                                    novo_retorno = None
                                    while novo_retorno != 'N' and novo_retorno != 'S':
                                        os.system('cls')
                                        novo_retorno = input(f'Entendemos, {self._nome.split()[0].title()}. Você gostaria de realizar alguma outra operação? (S/N) ').strip()
                                        if novo_retorno == 'N':
                                            os.system('cls')
                                            print(f'Sendo assim, vamos encerrar o seu atendimento, {self._nome.split()[0].title()}.\n\nObrigado e volte sempre!')
                                            time.sleep(5)
                                            os.system('cls')
                                            return None
                                        elif novo_retorno == 'S':
                                            return self._inicializar_atendimento_cliente()
                                        else:
                                            print('A resposta informada é inválida. Por favor, digite novamente.')
                    else:
                        print('O valor informado é inválido. Por favor, digite novamente. Caso queira cancelar a operação digite "Cancelar".')

# Verifica se é o arquivo main que está sendo executado
if __name__ == '__main__':

    logging.warning('Esse script não deve ser executado diretamente. Para utilizá-lo, execute o script "main.py"')