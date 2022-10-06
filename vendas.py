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

            layout_pesquisa = [
                [sg.Text('Quais produtos deseja vender?'), sg.Input(key='nome_produto')],
                [sg.Button('Adicionar', key='add'), sg.Button('Desfazer', key='rmv')],
                [sg.Button('Menu', key=''), sg.Button('Sair', key='')],
            ]

            layout_produtos = []

            for produto in produtos:
                layout_produtos.append([sg.Text(f'{produto[0]} - {produto[1]}')])

            sg.Window('Empire / TESTE', layout=layout_produtos).read()

            while True:
                item = [x[0] for x in produtos]
                resposta = input('--> ')

                if resposta == 'c':
                    break

                while resposta in respostas:
                    print('Produto já adicionado a lista. Tente outro item ou finalize a operação!')
                    resposta = input('--> ')

                if resposta not in str(item):
                    print('Produto não existe!')
                    return self.venda()
                
                respostas.append(resposta)
        
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