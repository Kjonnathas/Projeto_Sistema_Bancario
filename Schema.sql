
CREATE TABLE d_clientes(
	id_cliente SERIAL,
	nome_cliente VARCHAR(100) NOT NULL,
	genero CHAR(1) NOT NULL,
	cpf VARCHAR(14) NOT NULL,
	rg VARCHAR(12) NOT NULL,
	data_nascimento DATE NOT NULL,
	email VARCHAR(100),
	celular VARCHAR(15),
	profissao VARCHAR(100),
	renda FLOAT,
	data_atualizacao TIMESTAMP NOT NULL,
	CONSTRAINT id_cliente_d_clientes_pk PRIMARY KEY (id_cliente),
	CONSTRAINT cpf_d_clientes_un UNIQUE (cpf),
	CONSTRAINT rg_d_clientes_un UNIQUE (rg),
	CONSTRAINT renda_d_clientes_ck CHECK (renda >= 0 or renda IS NULL)
);

CREATE TABLE d_dados_conta(
	id_conta SERIAL,
	id_cliente INTEGER NOT NULL,
	agencia VARCHAR(4) NOT NULL,
	conta VARCHAR(10) NOT NULL,
	tipo_conta VARCHAR(15) NOT NULL,
	saldo FLOAT NOT NULL,
	data_atualizacao TIMESTAMP NOT NULL,
	CONSTRAINT id_conta_d_dados_conta_pk PRIMARY KEY (id_conta),
	CONSTRAINT id_cliente_d_dados_conta_fk FOREIGN KEY (id_cliente) REFERENCES d_clientes(id_cliente),
	CONSTRAINT agencia_d_dados_conta_un UNIQUE (agencia),
	CONSTRAINT conta_d_dados_conta_un UNIQUE (conta)
);

CREATE TABLE d_enderecos(
	id_endereco SERIAL,
	id_cliente INTEGER NOT NULL,
	rua VARCHAR(100) NOT NULL,
	numero VARCHAR(10) NOT NULL,
	bairro VARCHAR(100) NOT NULL,
	cidade VARCHAR(100) NOT NULL,
	uf VARCHAR(2) NOT NULL,
	cep VARCHAR(9) NOT NULL,
	data_atualizacao TIMESTAMP NOT NULL,
	CONSTRAINT id_endereco_d_enderecos_pk PRIMARY KEY (id_endereco),
	CONSTRAINT id_cliente_d_enderecos_fk FOREIGN KEY (id_cliente) REFERENCES d_clientes(id_cliente)
);

CREATE TABLE f_transacoes(
	id_transacao SERIAL,
	id_cliente INTEGER NOT NULL,
	valor_transacao FLOAT,
	tipo_transacao VARCHAR(100) NOT NULL,
	protocolo_transacao VARCHAR(100) NOT NULL,
	data_atualizacao TIMESTAMP NOT NULL,
	CONSTRAINT id_transacao_f_transacoes_pk PRIMARY KEY (id_transacao),
	CONSTRAINT id_cliente_f_transacoes_fk FOREIGN KEY (id_cliente) REFERENCES d_clientes(id_cliente)
);
