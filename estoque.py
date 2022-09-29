import psycopg2
import PySimpleGUI as sg

from usuario import Usuario

class Estoque(Usuario):

    def __init__(self):

        layout = [
            [sg.Text('Qual funcionalidade deseja?')],
            [sg.Button('Entrada de Estoque', key='1')],
            [sg.Button('Saída de Estoque', key='2')],
            [sg.Button('Menu', key='3')],
            [sg.Button('Sair', key='4')]
        ]

        window = sg.Window('Empire / Controle de Estoque', layout=layout, size=(400,200))
        
        while True:
            event, values = window.read()

            if event == '1':
                window.close()
                self.entrada_estoque()

            elif event == '2':
                window.close()
                self.saida_estoque()

            elif event == '3':
                window.close()
                self.menu_login()

            elif event == '4':
                exit()

            elif event == sg.WIN_CLOSED:
                window.close()
                self.menu_login()

    def entrada_estoque(self):

        layout_pesquisa = [
            [sg.Text('Digite o nome do produto'), sg.Input(key='nome_produto')],
            [sg.Button('Confirma', key='1'), sg.Button('Menu', key='2')],
        ]
        window_pesquisa = sg.Window('Empire / Entrada de Estoque', layout=layout_pesquisa)

        event_pesquisa, values_pesquisa = window_pesquisa.read()

        if event_pesquisa == '1':
            if values_pesquisa['nome_produto'] == '':
                window = sg.Window('Empire / Entrada de Estoque', layout=[[sg.ErrorElement('O produto não pode estar em branco!')], [sg.Button('Voltar', key='1')]])
                event, values = window.read()

                if event == '1':
                    window.close()
                    return self.entrada_estoque()
                
                elif event == sg.WIN_CLOSED:
                    window.close()
                    return self.entrada_estoque()
            
            nome_produto = values_pesquisa['nome_produto']
            window_pesquisa.close()

        elif event_pesquisa == '2':
            window_pesquisa.close()
            return Estoque()

        elif event_pesquisa == sg.WIN_CLOSED:
            window_pesquisa.close()
            return Estoque()

        con = psycopg2.connect(
            host='localhost',
            dbname='empire',
            user='postgres',
            password='nicolasvx123'
        )

        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS public.estoque(id serial PRIMARY KEY, nome_produto varchar(50), quantidade integer, valor_de_compra float, valor_de_venda float)")
        cur.execute("SELECT * FROM public.estoque;")
        produtos = cur.fetchall()
        cadastrado = False

        for produto in produtos:
            if produto[1] == nome_produto:
                cadastrado = True
        
        if cadastrado:
            print('\nProduto já existe! Deseja atualizar? [s/n]\n')
            resposta = input('--> ')

            if resposta == 's':
                cur.execute("SELECT quantidade FROM public.estoque WHERE nome_produto=%s", (nome_produto,))
                produto_selecionado = cur.fetchone()
                quantidade = input(f'Quantidade atual {produto_selecionado[0]}. Quantidade a ser adicionada: ')
                cur.execute("UPDATE public.estoque SET quantidade=quantidade+(%s) WHERE nome_produto=(%s)", (quantidade, nome_produto))
                print(f"Quantidade agora é {int(produto_selecionado[0])+int(quantidade)}\n")
                con.commit()
                cur.close()
                con.close()
                print('Quantidade do produto atualizada!')
                return Estoque()
            
            elif resposta == 'n':
                print('Operação cancelada. O que deseja fazer a seguir?\n')
                print('[1] - Voltar ao menu de estoque.')
                print('[2] - Sair.')
                resposta = input('--> ')

                if resposta == '1':
                    return Estoque()

                elif resposta == '2':
                    print('Obrigado por usar o sistema!')
                    return exit()

        layout_cadastro = [
            [sg.Text('Produto não encontrado, cadastre!')],
            [sg.Text('Digite a quantidade: '), sg.Input(key='quantidade')],
            [sg.Text('Digite o valor de compra: '), sg.Input(key='valor_de_compra')],
            [sg.Text('Digite o valor de venda: '), sg.Input(key='valor_de_venda')],
            [sg.Button('Confirmar', key='1'), sg.Button('Cancelar', key='2')]
        ]

        window_cadastro = sg.Window('Empire / Entrada de Estoque', layout=layout_cadastro)

        event_cadastro, values_cadastro = window_cadastro.read()

        if event_cadastro == '1':

            window_cadastro.close()

            window_confirma = sg.Window('Empire / Confirmação', layout=[[sg.Text('Produto cadastrado com sucesso!')], [sg.Button('Voltar', key='1')]])
            event_confirma, values_confirma = window_confirma.read()

            if event_confirma == '1':
                window_confirma.close()
                return Estoque()
            
            elif event_confirma == sg.WIN_CLOSED:
                window_confirma.close()
                return Estoque()

            cur.execute("INSERT INTO public.estoque (nome_produto, quantidade, valor_de_compra, valor_de_venda) VALUES (%s, %s, %s, %s)", (values_pesquisa['nome_produto'], values_cadastro['quantidade'], values_cadastro['valor_de_compra'], values_cadastro['valor_de_venda']))
            con.commit()
            cur.close()
            con.close()

            print('\nProduto cadastrado com sucesso!\n')
            return Estoque()

        if event_cadastro == '2':

            window_cadastro.close()
            return Estoque()

    def saida_estoque(self):

        print('Você está na aba de saída estoque!\n')
        nome_produto = input('Digite o nome do produto: ')

        con = psycopg2.connect(
            host='localhost',
            dbname='empire',
            user='postgres',
            password='nicolasvx123'
        )

        cur = con.cursor()
        cur.execute("SELECT * FROM public.estoque;")
        produtos = cur.fetchall()
        cadastrado = False

        for produto in produtos:
            if produto[1] == nome_produto:
                cadastrado = True

        if cadastrado:
            resposta = input('Deseja deletar o item da base de dados? [s/n] ')

            if resposta == 's':
                con = psycopg2.connect(
                    host='localhost',
                    dbname='empire',
                    user='postgres',
                    password='nicolasvx123'
                )

                cur = con.cursor()
                cur.execute("DELETE FROM public.estoque WHERE nome_produto=%s", (nome_produto,))
                con.commit()
                cur.close()
                con.close()

                print('Produto deletado com sucesso!')
                
                return Estoque()

            elif resposta == 'n':
                print('Operação cancelada. O que deseja fazer a seguir?\n')
                print('[1] - Voltar ao menu de estoque.')
                print('[2] - Sair.')
                resposta = input('--> ')

                if resposta == '1':
                    return Estoque()

                elif resposta == '2':
                    print('Obrigado por usar o sistema!')
                    return exit()
                
        resposta = input('Produto não encontrado no banco de dados, deseja cadastrar? [s/n] ')
        if resposta == 's':
            return Estoque.entrada_estoque(self)

        elif resposta == 'n':
            return Estoque()