import psycopg2
from datetime import datetime

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

class Vendas(Usuario):

    def __init__(self):

        print('\nVocê está na aba de vendas!')
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
            print('Quais produtos deseja vender? Precione \'c\' para finalizar a seleção.')

            for produto in produtos:
                print(f'[{produto[0]}] - {produto[1]}')


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

class Despesas(Usuario):

    def __init__(self):

        print('\nVocê está na aba de despesas.\n')
        self.despesa()       

    def despesa(self):
        exit()

    ## funcoes
    # despesas gerais
    # despesas com produtos
    # totais mensais/anuais

class Fornecedor(Usuario):

    def __init__(self, nome, numero, cnpj, cep):
        
        if self.valida_nome(nome):
            self.nome = nome
        else:
            raise ValueError('Nome inválido!')

        #if self.valida_numero(numero):
        #    self.numero = numero
        #else:
        #    raise ValueError('Numero inválido!')
        self.numero = numero
        self.cnpj = cnpj
        self.endereco = cep

    def valida_nome(self, nome):
        
        print(nome)

        return True
            
    ## variaveis
    # nome
    # numero
    # cnpj
    # endereço

    ## funcoes
    # cria fornecedores
    # deleta fornecedores
    # atualiza fornecedores