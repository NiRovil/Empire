import psycopg2

class Usuario:

    def __init__(self, nome, senha):

        self._nome = nome 
        self._senha = senha
        
        self.menu_inicial()

    def menu_inicial(self):

        print(
            '\nBem vindo!\n'
            '\nSelecione uma das opções a seguir:'
            '\n[1] - Cadastrar-se'
            '\n[2] - Login.'
            '\n[3] - Sair.\n'
        )

        while True:

            resposta = input('--> ')
            if resposta == '1':
                return self.cadastro()
            elif resposta == '2':
                return self.login()
            elif resposta == '3':
                print('\nVolte sempre!\n')
                return exit()
            print('\nOpção inválida!\n')

    def menu_login(self):
        
        print(
            '\nQue função deseja fazer?\n'
            '\n[1] - Controle de estoque.'
            '\n[2] - Vendas.'
            '\n[3] - Despesas.'
            '\n[4] - Fornecedores.'
            '\n[5] - Sair.\n'
        )
        
        while True:
            
            resposta = input('--> ')
            if resposta == '1':
                from estoque import Estoque
                return Estoque()
            if resposta == '2':
                from vendas import Vendas
                return Vendas()
            if resposta == '3':
                from despesas import Despesas
                return Despesas()
            if resposta == '4':
                from fornecedor import Fornecedor
                print(
                    '\nVocê está na aba de cadastro de Fornecedor'
                    '\nPara começar precisamos de algumas informações sobre o fornecedor:\n'
                )

                nome = input('Nome: ')
                numero = input('Numero de telefone: ')
                cnpj = input('CNPJ: ')
                cep = input('CEP: ')
                return Fornecedor(nome, numero, cnpj, cep)
            if resposta == '5':
                return exit()
            print('\nOpção inválida!\n')

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

        print('\nUsuário cadastrado com sucesso!\n')
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
            print('\nUsuário logado com sucesso!\n')
            return self.menu_login()

        cur.close()
        con.close()
        print('\nUsuário não encontrado, verifique o usuário e senha ou cadastre-se.\n')
        self.menu_inicial()