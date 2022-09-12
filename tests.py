import unittest
from models import Fornecedor

# 'Nicolas', 41999999999, 49810576000103, 69903239

class FornecedorNome(unittest.TestCase):

    def test_nome(self):

        nome = Fornecedor.valida_nome(self, 'Nicolas')
        self.assertTrue(nome)

    def test_nome_composto(self):

        nome_composto = Fornecedor.valida_nome(self, 'Nicolas Vilela')
        self.assertTrue(nome_composto)

    def test_nome_vazio(self):

        nome_vazio = Fornecedor.valida_nome(self, '')
        # self.assertTrue(nome_vazio, 'Nome não pode ser vazio!')
        self.assertFalse(nome_vazio)

    def test_nome_com_digitos(self):

        nome_com_digitos = Fornecedor.valida_nome(self, 'Nicolas123')
        # self.assertTrue(nome_com_digitos, 'Nome não pode conter digitos!')
        self.assertFalse(nome_com_digitos)

    def test_nome_com_somente_digitos(self):

        nome_com_somente_digitos = Fornecedor.valida_nome(self, '123')
        # self.assertTrue(nome_com_somente_digitos, 'Nome não pode ser um numero!')
        self.assertFalse(nome_com_somente_digitos)
    
    def test_nome_com_caracteres_especiais(self):

        nome_com_caracteres_especiais = Fornecedor.valida_nome(self, 'N!colas')
        # self.assertTrue(nome_com_caracteres_especiais, 'Nome não pode conter caracteres especiais!')
        self.assertFalse(nome_com_caracteres_especiais)

class FornecedorNumero(unittest.TestCase):

    def test_numero(self):

        numero = Fornecedor.valida_numero(self, '41999999999')
        self.assertTrue(numero)

    def test_numero_com_letra(self):

        numero_com_letra = Fornecedor.valida_numero(self, '4199999999a9')
        # self.assertTrue(numero_com_letra, 'Numero não pode conter letras!')
        self.assertFalse(numero_com_letra)

    def test_numero_a_menos(self):

        numero_a_menos = Fornecedor.valida_numero(self, '4199999999')
        # self.assertTrue(numero_a_menos, 'Numero deve conter 11 digitos!')
        self.assertFalse(numero_a_menos)


if __name__ == "__main__":
    unittest.main()