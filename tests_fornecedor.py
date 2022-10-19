import unittest
from fornecedor import CadastroFornecedor

# 'Nicolas', 41999999999, 49810576000103, 69903239

class TestFornecedorNome(unittest.TestCase):

    """Teste para verificar se as entradas de Nome do representante de Fornecedor estão corretas."""

    def setUp(self):

        self.nome = CadastroFornecedor.valida_nome(self, 'Nicolas')
        self.nome_composto = CadastroFornecedor.valida_nome(self, 'Nicolas Vilela')
        self.nome_vazio = CadastroFornecedor.valida_nome(self, '')
        self.nome_com_digitos = CadastroFornecedor.valida_nome(self, 'Nicolas123')
        self.nome_com_somente_digitos = CadastroFornecedor.valida_nome(self, '123')
        self.nome_com_caracteres_especiais = CadastroFornecedor.valida_nome(self, 'N!colas')

    def test_nome(self):

        self.assertTrue(self.nome)

    def test_nome_composto(self):

        self.assertTrue(self.nome_composto)

    def test_nome_vazio(self):

        # self.assertTrue(self.nome_vazio, 'Nome não pode ser vazio!')
        self.assertFalse(self.nome_vazio)

    def test_nome_com_digitos(self):
        
        # self.assertTrue(self.nome_com_digitos, 'Nome não pode conter digitos!')
        self.assertFalse(self.nome_com_digitos)

    def test_nome_com_somente_digitos(self):

        # self.assertTrue(self.nome_com_somente_digitos, 'Nome não pode ser um numero!')
        self.assertFalse(self.nome_com_somente_digitos)
    
    def test_nome_com_caracteres_especiais(self):

        # self.assertTrue(self.nome_com_caracteres_especiais, 'Nome não pode conter caracteres especiais!')
        self.assertFalse(self.nome_com_caracteres_especiais)

class TestFornecedorNumero(unittest.TestCase):

    """Teste para verificar se as entradas de Numero de Telefone estão corretas."""

    def setUp(self):

        self.numero = CadastroFornecedor.valida_numero(self, '41999999999')
        self.numero_vazio = CadastroFornecedor.valida_numero(self, '')
        self.numero_com_letra = CadastroFornecedor.valida_numero(self, '4199999999a9')
        self.numero_a_menos = CadastroFornecedor.valida_numero(self, '4199999999')

    def test_numero(self):

        self.assertTrue(self.numero)

    def test_numero_vazio(self):

        # self.assertTrue(self.numero_vazio, 'Numero não pode estar em branco.')
        self.assertFalse(self.numero_vazio)

    def test_numero_com_letra(self):

        # self.assertTrue(self.numero_com_letra, 'Numero não pode conter letras!')
        self.assertFalse(self.numero_com_letra)

    def test_numero_a_menos(self):

        # self.assertTrue(self.numero_a_menos, 'Numero deve conter 11 digitos!')
        self.assertFalse(self.numero_a_menos)

class TestFornecedorCnpj(unittest.TestCase):

    """Teste para verificar se as entradas de CNPJ estão corretas."""

    def setUp(self):

        self.cnpj = CadastroFornecedor.valida_cnpj(self, '49810576000103')
        self.cnpj_vazio = CadastroFornecedor.valida_cnpj(self, '')
        self.cnpj_com_letras = CadastroFornecedor.valida_cnpj(self, '498105760001a3')

    def test_cnpj(self):

        self.assertTrue(self.cnpj)

    def test_cnpj_vazio(self):

        # self.assertTrue(self.cnpj_vazio, 'CNPJ não pode estar em branco!')
        self.assertFalse(self.cnpj_vazio)

    def test_cnpj_com_letras(self):

        # self.assertTrue(self.cnpj_com_letras, 'CNPJ não pode conter letras!')
        self.assertFalse(self.cnpj_com_letras)

class TestFornecedorCep(unittest.TestCase):

    """Teste para verificar se as entradas de CEP estão corretas."""

    def setUp(self):

        self.cep = CadastroFornecedor.valida_cep(self, '69903239')
        self.cep_vazio = CadastroFornecedor.valida_cep(self, '')
        self.cep_com_numero_diferente = CadastroFornecedor.valida_cep(self, '6990323')

    def test_cep(self):

        self.assertTrue(self.cep)

    def test_cep_vazio(self):

        # self.assertTrue(self.cep_vazio, 'CEP não pode estar em branco!')
        self.assertFalse(self.cep_vazio)

    def test_cep_com_numero_diferente(self):

        # self.assertTrue(self.cep_com_numero_diferente, 'CEP deve conter 8 numeros.')
        self.assertFalse(self.cep_com_numero_diferente)

if __name__ == "__main__":
    unittest.main()