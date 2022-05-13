from models.exceptions import LanceInvalido
from models.dominio import Leilao, Lance, Usuario
import unittest


class TestLeilao(unittest.TestCase):
    def setUp(self):
        self.leilao = Leilao("test")
        self.user1 = Usuario("Matheus", 200)
        self.user2 = Usuario("Roberto", 400)

    def fazerLances(self):
        lance = Lance(self.user1, 100)
        lance_maior = Lance(self.user2, 110)
        self.leilao.adicionar_lance(lance)
        self.leilao.adicionar_lance(lance_maior)
        return lance, lance_maior

    def test_criar_lance(self):
        lance = Lance(self.user1, 100)
        self.assertEqual(lance.usuario.nome, "Matheus")
        self.assertEqual(lance.valor, 100)
        self.assertEqual(self.user1.saldo, 100)

    def test_lance_acima_do_saldo(self):
        with self.assertRaises(LanceInvalido):
            Lance(self.user1, 400)

    def test_adicionar_lance(self):
        lance = Lance(self.user1, 100)
        self.leilao.adicionar_lance(lance)
        self.assertEqual(self.leilao.lances, [lance])

    def test_adicionar_lance_igual(self):
        lance = Lance(self.user1, 100)
        self.leilao.adicionar_lance(lance)
        lance_igual = Lance(self.user2, 100) 
        with self.assertRaises(LanceInvalido):
            self.leilao.adicionar_lance(lance_igual)

    def test_adicionar_maior_lance(self):
        lance, lance_maior = self.fazerLances()
        self.assertEqual(self.leilao.maior_lance, lance_maior)
        
    def test_encerrar(self):
        lance, lance_maior = self.fazerLances()
        # Verificando se o lance maior ganhou o leilão como previsto
        # e se o valor dos lances foram descontados ou reembolsados
        # de acordo da maneira prevista
        self.assertEqual(self.leilao.encerrar(), lance_maior)
        self.assertEqual(self.user1.saldo, 200)
        self.assertEqual(self.user2.saldo, 290)