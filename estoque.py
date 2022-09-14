import psycopg2

from usuario import Usuario

class Estoque(Usuario):

    def __init__(self):

        print('\nVocê está na aba de controle de estoque!')
        print('Qual funcionalidade deseja?')
        print('[1] - Entrada de estoque.')
        print('[2] - Saida de estoque.')
        print('[3] - Menu.')
        print('[4] - Sair.')
        resposta = input('--> ')

        if resposta == '1':
            self.entrada_estoque()

        elif resposta == '2':
            self.saida_estoque()

        elif resposta == '3':
            self.menu_login()

        elif resposta == '4':
            exit()

        else:
            print('\nOpção inválida!')
            self.__init__()

    def entrada_estoque(self):

        print('Você está na aba de entrada de estoque!\n')
        nome_produto = input('Digite o nome do produto: ')

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

        print('Produto não encontrado no banco de dados, cadastre!\n')

        quantidade = input('Digite a quantidade: ')
        valor_de_compra = input('Digite o valor de compra: ')
        valor_de_venda = input('Digite o valor de venda: ')

        cur.execute("INSERT INTO public.estoque (nome_produto, quantidade, valor_de_compra, valor_de_venda) VALUES (%s, %s, %s, %s)", (nome_produto, quantidade, valor_de_compra, valor_de_venda))
        con.commit()
        cur.close()
        con.close()

        print('\nProduto cadastrado com sucesso!\n')
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