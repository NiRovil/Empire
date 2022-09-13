import psycopg2

from despesas import Despesas
from estoque import Estoque
from fornecedor import Fornecedor
from vendas import Vendas

class Usuario:

    def __init__(self, nome, senha):

        self._nome = nome 
        self._senha = senha
        
        self.menu_inicial()

    def menu_inicial(self):

        print('\nBem vindo!')
        print('Selecione uma das opções a seguir:\n')
        print('[1] - Cadastrar-se')
        print('[2] - Login.')
        print('[3] - Sair.')
        
        while True:

            resposta = input('--> ')
            if resposta == '1':
                self.cadastro()
            elif resposta == '2':
                self.login()
            elif resposta == '3':
                print('\nVolte sempre!\n')
                exit()
            print('\nOpção inválida!')
    
    def menu_login(self):

        print('Que função deseja fazer?\n')
        print('[1] - Controle de estoque.')
        print('[2] - Vendas.')
        print('[3] - Despesas.')
        print('[4] - Fornecedores.')
        print('[5] - Sair.')
        
        while True:
            
            resposta = input('--> ')
            if resposta == '1':
                return Estoque()
            if resposta == '2':
                return Vendas()
            if resposta == '3':
                return Despesas()
            if resposta == '4':
                print('\nVocê está na aba de cadastro de Fornecedor')
                print('Para começar precisamos de algumas informações sobre o fornecedor:\n')
                nome = input('Nome: ')
                numero = input('Numero de telefone: ')
                cnpj = input('CNPJ: ')
                cep = input('CEP: ')
                return Fornecedor(nome, numero, cnpj, cep)
            if resposta == '5':
                exit()
            print('\nOpção inválida!')

    def cadastro(self):

        con = psycopg2.connect(
            host='localhost',
            dbname='empire',
            user='postgres',
            password='nicolasvx123'
        )

        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS public.usuario (id serial PRIMARY KEY, nome varchar(50), senha varchar(50));")
        cur.execute("SELECT * FROM public.usuario;")
        users = cur.fetchall()
        cadastrado = False

        for user in users:
            if self._nome == user[1]:
                cadastrado = True
            
        while cadastrado:

            print('\nUsuário já existe! Deseja fazer o login? [s/n]')
            resposta = input('--> ')
            if resposta == 's':
                self.login()
            elif resposta == 'n':
                self.menu_inicial()
            print('\nOpção inválida!')

        cur.execute("INSERT INTO public.usuario (nome,senha) VALUES (%s, %s)", (self._nome, self._senha))
        con.commit()        
        cur.close()
        con.close()

        print('\nUsuário cadastrado com sucesso!')
        return self.menu_inicial()

    def login(self):

        con = psycopg2.connect(
            host='localhost',
            dbname='empire',
            user='postgres',
            password='nicolasvx123'
        )

        cur = con.cursor()
        cur.execute("SELECT nome, senha FROM public.usuario WHERE nome=%s;", (self._nome,))
        user = cur.fetchone()

        if self._nome == user[0] and self._senha == user[1]:
            cur.close()
            con.close()
            print('\nUsuário logado com sucesso!')
            return self.menu_login()

        cur.close()
        con.close()
        print('\nUsuário não encontrado, verifique o usuário e senha ou cadastre-se.')
        self.menu_inicial()