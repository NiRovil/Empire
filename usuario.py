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
            [sg.Text('Selecione o que deseja fazer:')],
            [sg.Button('Controle de Estoque')],
            [sg.Button('Vendas')],
            [sg.Button('Fornecedores')],
            [sg.Button('Sair')]
        ]

        window = sg.Window(title='Empire / Menu Principal', layout=layout, size=(400,200))

        while True:
            event, values = window.read()

            if event == 'Controle de Estoque':
                from estoque import Estoque
                window.close()
                return Estoque()

            elif event == 'Vendas':
                from vendas import Vendas
                window.close()
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

            layout = [
                [sg.Text('Usuário já cadastrado, deseja fazer login?')],
                [sg.Button('Login'), sg.Button('Sair')]
            ]
            window = sg.Window('Empire / Cadastro', layout=layout)

            while True:
                event, values = window.read()

                if event == 'Login':
                    window.close()
                    return self.login()
                
                elif event == 'Sair':
                    window.close()
                    exit()

        cur.execute("INSERT INTO public.usuario (nome,senha) VALUES (%s, %s)", (self._nome, self._senha))
        con.commit()        
        cur.close()
        con.close()

        layout = [
            [sg.Text('Usuário cadastrado com sucesso!')],
            [sg.Button('Login'), sg.Button('Sair')]
        ]

        window = sg.Window('Empire / Concluído', layout=layout)

        while True:
            event, values = window.read()

            if event == 'Login':
                window.close()
                return self.menu_login()

            if event == 'Sair':
                window.close()
                exit()

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