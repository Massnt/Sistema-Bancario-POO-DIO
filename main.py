from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = list()
    
    def realizar_transacao(conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self._contas.append(conta)
        
class PessoaFisica(Cliente):
    def __init__(self, nome_cliente, cpf : str, 
                 data_nascimento : datetime, endereco : str, contas = list()):
        super().__init__(endereco)
        self._nome = nome_cliente
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        
        @property
        def nome(self):
            return self._nome
        
class Conta:
    def __init__(self,numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @property
    def cliente(self):
        return self._cliente
    
    @property
    def saldo(self):
        return self._saldo or 0
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def sacar(self, valor) -> bool:
        if valor > 0:
            if valor < self._saldo:
                print("Saque efetuado com sucesso")
                self._saldo -= valor
                return True
            else:
                print("Saldo Insuficiente")
        else:
            print("Valor Inválido")
            
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito realizado com sucesso")
            return True
        else:
            print("Valor inválido")
        return False
    
class ContaCorrente(Conta):
    def __init__(self, limite, limite_saque, numero, cliente):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saque
        
    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saque(self):
        return self._limite_saque
    
    def __str__(self) -> str:
        return f"""\
                Agencia :\t{self.agencia}
                C\C: \t\t{self.numero}
                Titular:\t{self.cliente.nome}
                """
                
    def sacar(self, valor):
        num_saques = len([transacao for transacao in self.historico.transacoes
                          if transacao['tipo'] == Saque.__name__])
        
        if valor < self._limite:
            if num_saques <= self._limite_saque:
                return super().sacar(valor)
            else:
                print("Limite de saques excedido")
        else:
            print("Valor limite excedido")
        
        return False
    
class Historico:
    def __init__(self):
        self._transacoes = list()
    
    @property
    def transacoes(self):
        return self._transacoes
        
    def adicionar_transacoes(self, transacao):
        self._transacoes.append({
            "tipo" : transacao.__class__.__name__,
            "valor": transacao.valor,
            "data" : datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        })
        
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass
    
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacoes(self)
            
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacoes(self)