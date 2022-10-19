import psycopg2
import PySimpleGUI as sg

from datetime import datetime
from usuario import Usuario

class Vendas(Usuario):

    def __init__(self):
        self.venda()
        
    def venda(self):

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

        respostas = []

        if produtos:

            layout_pesquisa = [[sg.Text('Quais produtos deseja adicionar ao carrinho?')],]
            
            for produto in produtos:
                layout_pesquisa.append([sg.Button(f'{produto[0]} - {produto[1]}', key=f'{produto[1]}')])
            
            layout_pesquisa.append([[sg.Button('Cesta', key='cart'), sg.Button('Finalizar', key='end')], [sg.Button('Menu', key=''), sg.Button('Sair', key='')]])
            
            window_pesquisa = sg.Window('Empire / TESTE', layout=layout_pesquisa)

            while True:
                event_pesquisa, values_pesquisa = window_pesquisa.read()

                print(event_pesquisa)
                print(values_pesquisa)

                if respostas and event_pesquisa in respostas:
                    layout_erro = [
                        [sg.Text('Produto já adicionado, selecione outro ou finalize a operação!')],
                        [sg.Button('Voltar', key='back')]
                    ]

                    window_erro = sg.Window('Empire / Erro', layout=layout_erro)

                    event_erro, values_erro = window_erro.read()

                    if event_erro == 'back':
                        window_erro.close()
                
                elif event_pesquisa == 'cart':
                    if respostas and str(event_pesquisa) == 'cart':
                        print(respostas)
                        layout_cart = []
                        for item in respostas:
                            print(item)
                            layout_cart.append([sg.Text(f'{produto}')])
                        sg.Window('Empire / Carrinho', layout=layout_cart).read()

                    return False
                               
                else:
                    for produto in produtos:
                        if event_pesquisa == produto[1]:
                            respostas.append(event_pesquisa)       

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