import psycopg2
import PySimpleGUI as sg

from datetime import datetime
from usuario import Usuario

class Vendas(Usuario):

    def __init__(self):
        self.venda()
        
    def venda(self):

        # Conecta ao banco de dados.
        con = psycopg2.connect(
            host='localhost',
            dbname='empire',
            user='postgres',
            password='nicolasvx123'
        )

        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS public.vendas (id serial PRIMARY KEY, nome_produto varchar(50), valor_venda integer, receita integer, data_venda date)")
        cur.execute("SELECT * FROM public.estoque;")
        produtos = cur.fetchall()

        respostas = {}

        # Se houver produto no estoque inicia o módulo vendas.
        if produtos:

            layout_pesquisa = [[sg.Text('Quais produtos deseja adicionar ao carrinho?')]]
            
            # Define o layout da aba de vendas.
            # O for abaixo, lista todos os produtos disponíveis no banco de dados.
            for produto in produtos:
                layout_pesquisa.append(
                    [sg.Text(f'{produto[0]} - {produto[1]}'), sg.Text(f'quantidade: {produto[2]}'), sg.Button('Adicionar', key=f'{produto[1]}')]
                )
        
            layout_pesquisa.append(
                [[sg.Button('Cesta', key='cart'), sg.Button('Finalizar', key='end')], 
                [sg.Button('Menu', key=''), sg.Button('Sair', key='')]]
            )
           
            window_pesquisa = sg.Window('Empire / Venda', layout=layout_pesquisa)

            # Enquanto a janela estiver aberta as ações feitas pelo usuário serão identificadas.
            while True:
                event_pesquisa, values_pesquisa = window_pesquisa.read()

                # Se o produto estiver nos itens previamente adicionados uma janela de aviso é mostrada.
                if respostas and event_pesquisa in respostas:
                    layout_erro = [
                        [sg.Text('Produto já adicionado, selecione outro ou finalize a operação!')],
                        [sg.Button('Voltar', key='back')]
                    ]

                    window_erro = sg.Window('Empire / Erro', layout=layout_erro)

                    event_erro, values_erro = window_erro.read()

                    if event_erro == 'back':
                        window_erro.close()
                
                # Mostra o atual estado do carrinho de compras.
                elif event_pesquisa == 'cart':
                    if respostas and str(event_pesquisa) == 'cart':
                        print(respostas)
                        layout_cart = [[sg.Text('Produtos adicionados:')]]
                        for item in respostas:
                            print(item)
                            layout_cart.append([sg.Text(f'{item}')])
                        window = sg.Window('Empire / Carrinho', layout=layout_cart)
                        event, values = window.read()

                        if event == sg.WIN_CLOSED:
                            window.close()

                    # Se não houver nenhum item no carrinho, um aviso é mostrado.
                    else:
                        layout_cart = [[sg.Text('Nenhum produto selecionado!')]]
                        window = sg.Window('Empire / Carrinho', layout=layout_cart)
                        event, values = window.read()

                        if event == sg.WIN_CLOSED:
                            window.close()

                # Adiciona um item ao carrinho.          
                else:
                    for produto in produtos:
                        if event_pesquisa == produto[1]:
                            layout = [
                                [sg.Text('Selecione a quantidade: '), sg.InputText(key='q')]
                            ]

                            sg.Window('Empire / Quantidade', layout=layout).read()
                            respostas[event_pesquisa] = produto[2]
                            print(respostas)      

        # Se não houver produto, uma mensagem é exibida.
        else:
            print('Nenhum produto no estoque!')
            print('O que deseja fazer a seguir?\n')
            print('[1] - Voltar ao menu.')
            print('[2] - Sair.')
            
            while True:
                resposta = input('--> ')

                if resposta == '1':
                    self.menu_login()

                elif resposta == '2':
                    exit()

                print('Resposta inválida')
        
        if respostas:

            for item in respostas:
                for produto in produtos:
                    if item == str(produto[0]):
                        quantidade = input(f'Selecione a quantidade de {produto[1]} a ser vendida, atualmente o estoque de {produto[1]} é de {produto[2]} unidades: ')

                        while int(quantidade) > int(produto[2]):
                            print("Quantidade maior do que o disponível em estoque!")
                            quantidade = input(f'Selecione a quantidade de {produto[1]} a ser vendida, atualmente o estoque de {produto[1]} é de {produto[2]} unidades: ')

                        cur.execute("UPDATE public.estoque SET quantidade=quantidade-(%s) WHERE id=(%s)", (quantidade, produto[0]))
                        cur.execute("INSERT INTO public.vendas (nome_produto, valor_venda, receita, data_venda) VALUES (%s, %s, %s, %s)", (produto[1], produto[4], produto[4]-produto[3], datetime.now()))

                        print('Produto vendido com sucesso')
            
            con.commit()
            cur.close()
            con.close()

        print('Nenhum item selecionado!')
        print('O que deseja fazer a seguir?\n')
        print('[1] - Voltar ao menu.')
        print('[2] - Sair.')
        
        con.commit()
        cur.close()
        con.close()
        
        while True:
            resposta = input('--> ')

            if resposta == '1':
                self.menu_login()

            elif resposta == '2':
                exit()

            print('Resposta inválida')