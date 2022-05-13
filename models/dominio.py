from models.exceptions import LanceInvalido


class Usuario:
    def __init__(self, nome:str, conta:int):
        self.__nome = nome
        self.__conta = conta
        self.__congelado = 0

    def __str__(self):
        return self.nome
    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def saldo(self):
        return self.__conta

    def depositar(self, valor:int):
        if valor < 0: raise LanceInvalido("Não é possivel depositar um valor negativo")
        self.__conta += valor

    def sacar(self, valor:int):
        if valor < 0: raise LanceInvalido("Não é possivel sacar um valor negativo")
        if valor > self.saldo: raise LanceInvalido(f"Saldo insuficiente: {self.saldo}")
        self.__conta -= valor
    
    def preparar_transação(self, valor:int):
        self.sacar(valor)
        self.__congelado += valor
        return valor

    def confirmar_transação(self, valor:int):
        self.__congelado -= valor

    def recusar_transação(self, valor:int):
        self.__congelado -= valor
        self.depositar(valor)

class Lance:
    def __init__(self, usuario:Usuario, valor:int):
        self.usuario = usuario
        self.__valor = self.usuario.preparar_transação(valor)
    
    @property
    def valor(self):
        return self.__valor
    
    def ganhou(self):
            self.usuario.confirmar_transação(self.__valor)

    def perdeu(self):
        self.usuario.recusar_transação(self.__valor)

class Leilao:
    def __init__(self, descricao):
        self.descricao = descricao
        self.__lances = []

    @property
    def lances(self):
        return self.__lances

    @property
    def maior_lance(self):
        maior_lance = 0
        for lance in self.lances:
            if not maior_lance: maior_lance = lance
            if lance.valor > maior_lance.valor: maior_lance = lance
        return maior_lance
    
    def adicionar_lance(self, lance:Lance):
        if self.maior_lance:
            if lance.valor <= self.maior_lance.valor:
                raise LanceInvalido(f"O novo lance precisa ser maior que {self.maior_lance}")
        return self.__lances.append(lance)
    
    def remover_lance(self, lance:Lance):
        return self.__lances.remove(lance)
    
    def encerrar(self):
        if self.maior_lance:
            maior_lance = self.maior_lance 
            maior_lance.ganhou()
            self.remover_lance(maior_lance)
            for lance in self.lances:
                lance.perdeu()
            return maior_lance
            