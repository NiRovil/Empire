import psycopg2
import PySimpleGUI as sg

class Usuario:

    def __init__(self):

        layout = [
            [sg.Text('Nome de Usuário'), sg.InputText(key='usuario')],
            [sg.Text('Senha'), sg.InputText(key='password', password_char='*')],
            [sg.Button('Login'), sg.Button('Cadastro'), sg.Cancel()]
        ]
        window = sg.Window(title='Empire / Login - Cadastro', layout=layout)

        while True:
            event, values = window.read()

            if event in ('Login', 'Cadastro', 'Cancel') and values['usuario'] == '' or values['password'] == '':
                return self.__init__()
            
            elif event == 'Login' and values['usuario'] != '' and values['password'] != '':
                self._nome = values['usuario']
                self._senha = values['password']
                window.close()

                print(self._nome)
                print(self._senha)

                return self.login()
            
            elif event == 'Cadastro' and values['usuario'] != '' and values['password'] != '':
                self._nome = values['usuario']
                self._senha = values['password']
                window.close()

                return self.cadastro()
           
            elif event == sg.WIN_CLOSED:
                window.close()
                exit()

    def menu_login(self):

        layout = [
            [sg.Button('Controle de Estoque')],
            [sg.Button('Vendas')],
            [sg.Button('Fornecedores')],
            [sg.Button('Sair')]
        ]

        window = sg.Window(title='Empire / Menu', layout=layout)

        while True:
            event, values = window.read()

            if event == 'Controle de Estoque':
                from estoque import Estoque
                return Estoque()

            elif event == 'Vendas':
                from vendas import Vendas
                return Vendas()

            elif event == 'Fornecedores':
                
                while True:
                    print('Deseja cadastrar/atualizar/deletar fornecedor? [s/n]')
                    r = input('--> ')

                    if r == 's':
                        from fornecedor import CadastroFornecedor
                        print(
                            '\nVocê está na aba de cadastro de Fornecedor'
                            '\nPara começar digite o CNPJ:\n'
                        )

                        cnpj = input('CNPJ: ')

                        return CadastroFornecedor(cnpj)

                    if r == 'n':
                        from fornecedor import ListaFornecedor
                        return ListaFornecedor()

            elif event == 'Sair':
                return exit()
            
            elif event == sg.WIN_CLOSED:
                window.close()
                exit()

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

        print('User ' + self._nome)
        print('Senha ' + self._senha)

        con = psycopg2.connect(
            host='localhost',
            dbname='empire',
            user='postgres',
            password='nicolasvx123'
        )

        cur = con.cursor()
        cur.execute("SELECT nome, senha FROM public.usuario WHERE nome=%s;", (self._nome,))
        user = cur.fetchone()

        if user is not None:
            if self._nome == user[0] and self._senha == user[1]:
                layout = [
                    [sg.Text('Usuário logado com sucesso!')],
                    [sg.OK()]
                ]

                window = sg.Window('Empire', layout=layout)

                while True:
                    event, values = window.read()

                    if event in ('OK'):
                        cur.close()
                        con.close()
                        window.close()
                        return self.menu_login()

        cur.close()
        con.close()
        layout = [
            [sg.Text('Usuário não encontrado, verifique o usuário e senha ou cadastre-se!')],
            [sg.OK(), sg.Button('Sair')]
        ]

        window = sg.Window('Empire / Erro', layout=layout)

        while True:
            event, values = window.read()
            if event == 'OK':
                window.close()
                return self.__init__()

            if event == 'Sair':
                window.close()
                exit()