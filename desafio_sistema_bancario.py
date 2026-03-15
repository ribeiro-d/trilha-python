from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco: str):
        self._endereco = endereco
        self._contas = []

    @property
    def contas(self):
        return self._contas

    @property
    def endereco(self):
        return self._endereco

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        if conta in self.contas:
            print("Esta conta já está cadastrada.")
        else:
            self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco: str, cpf: str, nome: str, data_nascimento: str):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

    @property
    @abstractmethod
    def valor(self):
        pass


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

    @property
    def valor(self):
        return self._valor


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)

    @property
    def valor(self):
        return self._valor


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


class Conta:
    def __init__(self, numero: int, cliente: Cliente, agencia: str = "0001", historico=Historico()):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int):
        return cls(numero, cliente)

    def sacar(self, valor: float) -> bool:
        saldo_insuficiente = valor > self.saldo

        if saldo_insuficiente:
            print("=/=/= Saldo insuficiente. =/=/=")

        elif valor > 0:
            self._valor -= valor
            print(f"====== R$ {valor:.2f} sacados com sucesso. ======")
            return True

        else:
            print("=/=/= Valor inválido. Tente novamente. =/=/=")

        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._valor += valor
            print(f"====== R$ {valor:.2f} depositados com sucesso. ======")
            return True
        else:
            print("====== Não foi possível depositar o valor na conta. ======")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, historico, limite=500, limite_saques=3):
        super().__init__(numero, agencia, cliente, historico)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: int):
        saldo = self.saldo
        valor_invalido = valor <= 0
        saldo_insuficiente = valor > saldo
        excedeu_limite = valor > self.limite
        numero_saques = len(
            [saque for saque in self.historico if self.historico["tipo"] == "Saque"])
        atingiu_limite_saques = numero_saques >= self.limite_saques

        if valor_invalido:
            print("Valor inválido.")
        elif atingiu_limite_saques:
            print("Limite de transações atingido.")
        elif excedeu_limite:
            print("O valor excedeu o limite.")
        elif saldo_insuficiente:
            print("Saldo insuciente.")
        else:
            self._valor -= valor
            print(
                f"====== Saque de R$ {valor:.2f} realizado com sucesso. ======")
            return True
        return False
