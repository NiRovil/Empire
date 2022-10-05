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
                window = sg.Window('Empire / Entrada de Estoque', layout=[[sg.Text('O produto não pode estar em branco!')], [sg.Button('Voltar', key='1')]])
                event, values = window.read()

                if event == '1':
                    window.close()
                    window_pesquisa.close()
                    return self.entrada_estoque()
                
                elif event == '2':
                    window.close()
                    window_pesquisa.close()
                    return Estoque()

                elif event == sg.WIN_CLOSED:
                    window_pesquisa.close()
                    return Estoque()
            
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
        
        layout_pesquisa = [
            [sg.Text('Digite o nome do produto'), sg.Input(key='nome_produto')],
            [sg.Button('Confirma', key='1'), sg.Button('Menu', key='2')],
        ]
        window_pesquisa = sg.Window('Empire / Saida de Estoque', layout=layout_pesquisa)

        event_pesquisa, values_pesquisa = window_pesquisa.read()

        if event_pesquisa == '1':
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
                if values_pesquisa['nome_produto'] == produto[1]:
                    cadastrado = True
                elif values_pesquisa['nome_produto'] == '':
                    layout_vazio = [
                        [sg.Text('Nome do produto não pode estar em branco!')],
                        [sg.Button('Retornar', key='1')]
                    ]

                    window_vazio = sg.Window('Empire / Produto não encontrado!', layout=layout_vazio)

                    event_vazio, values_vazio = window_vazio.read()

                    if event_vazio == '1':
                        window_vazio.close()
                        window_pesquisa.close()
                        return self.saida_estoque()
                    
                    elif event_vazio == sg.WIN_CLOSED:
                        window_vazio.close()
                        window_pesquisa.close()
                        return self.saida_estoque()

            if cadastrado:
                layout = [
                    [sg.Text('Deseja deletar o produto selecionado?')],
                    [sg.Button('Confirma', key='s'), sg.Button('Cancela', key='n')]
                ]
                window = sg.Window('Empire / Confirmação', layout=layout)

                event, values = window.read()

                if event == 's':
                    con = psycopg2.connect(
                        host='localhost',
                        dbname='empire',
                        user='postgres',
                        password='nicolasvx123'
                    )

                    cur = con.cursor()
                    cur.execute("DELETE FROM public.estoque WHERE nome_produto=%s", (values_pesquisa['nome_produto'],))
                    con.commit()
                    cur.close()
                    con.close()

                    layout_confirma = [
                        [sg.Text('Produto deletado com sucesso!')],
                        [sg.Button('Retornar ao Menu', key='return')]
                    ]

                    window_confirma = sg.Window('Empire / Confirmação', layout=layout_confirma)

                    event_confirma, values_confirma = window_confirma.read()

                    if event_confirma == 'return':
                        window.close()
                        window_pesquisa.close()
                        window_confirma.close()
                        return Estoque()
                    
                    elif event_confirma == sg.WIN_CLOSED:
                        window.close()
                        window_pesquisa.close()
                        return Estoque()

                elif event == 'n':
                    layout_cancela = [
                        [sg.Text('Operação cancelada com sucesso!')],
                        [sg.Button('Retornar ao Menu', key='return')]
                    ]

                    window_cancela = sg.Window('Empire / Cancelar', layout=layout_cancela)

                    event_cancela, values_cancela = window_cancela.read()

                    if event_cancela == 'return':
                        window.close()
                        window_pesquisa.close()
                        window_cancela.close()
                        return Estoque()

                    elif event_cancela == sg.WIN_CLOSED:
                        window.close()
                        window_pesquisa.close()
                        return Estoque()
                
                elif event == sg.WIN_CLOSED:
                    window_pesquisa.close()
                    return Estoque()
                    
            layout_n_encontrado = [
                [sg.Text('Produto não encontrado na base de dados')],
                [sg.Button('Voltar', key='1')]
            ]
            
            window_n_encontrado = sg.Window('Empire / Não Encontrado', layout=layout_n_encontrado)

            event_n_encontrado, values_n_encontrado = window_n_encontrado.read()

            if event_n_encontrado == '1':
                window_pesquisa.close()
                window_n_encontrado.close()
                return self.saida_estoque()

            elif event_n_encontrado == sg.WIN_CLOSED:
                window_pesquisa.close()
                return Estoque()

        elif event_pesquisa == '2':
            window_pesquisa.close()
            return Estoque()