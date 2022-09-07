import psycopg2
import datetime

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
        resposta = input('--> ')

        if resposta == '1':
            self.cadastro()
        elif resposta == '2':
            self.login()
        elif resposta == '3':
            print('\nVolte sempre!\n')
            exit()

        print('\nOpção inválida!')
        self.menu_inicial()
    
    def menu_login(self):

        print('Que função deseja fazer?\n')
        print('[1] - Controle de estoque.')
        print('[2] - Vendas.')
        print('[3] - Sair.')
        
        resposta = input('--> ')

        if resposta == '1':
            return Estoque()
        elif resposta == '2':
            return Vendas()
        elif resposta == '3':
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
            self.menu_login()

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
        print('[3] - Sair.')
        resposta = input('--> ')

        if resposta == '1':
            self.entrada_estoque()
        elif resposta == '2':
            self.saida_estoque()
        elif resposta == '3':
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
        self.venda_produto()
        
    def venda_produto(self):

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

        print('Quais produtos deseja vender? Precione \'0\' para finalizar a seleção.')

        for produto in produtos:
            if produto != None:
                print(f'[{produto[0]}] - {produto[1]}')

        respostas = []
        
        while True:

            resposta = input('--> ')
            if resposta == '0':
                if respostas:
                    for item in respostas:                     
                        for produto in produtos:
                            if item == produto[0]:
                                
                                quantidade = input(f'Selecione a quantidade de {item} a ser vendida: ')
                                cur.execute("UPDATE public.estoque SET quantidade=quantidade-(%s) WHERE id=(%s)", (quantidade, item))
                                cur.execute("INSERT INTO public.vendas (nome_produto, valor_venda, receita, data_venda) VALUES (%s, %s, %s, %s)", (produto[1], produto[4], produto[3]-produto[4], datetime))
                                con.commit()
                                cur.close()
                                con.close()
                                print('Produto vendido com sucesso')

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
                        
            if resposta not in str(produto[0]):
                print('Produto não existe!')

            if resposta in respostas:
                print('Produto já adicionado a lista. Tente outro item ou finalize a operação!')
            
            print(respostas)
            respostas.append(resposta)
            
        
    ## variaveis
    #

    ## funcoes
    # quantidade vendida
    # valor vendido
    # totais mensais/anuais

class Despesas(Estoque):

    # subclasse de estoque, assim como vendas

    ## funcoes
    # despesas gerais
    # despesas com produtos
    # totais mensais/anuais
    pass 

class Fornecedor(Usuario):

    # responde a classe de usuários

    ## variaveis
    # nome
    # numero
    # cnpj
    # endereço
    # contato principal

    ## funcoes
    # cria fornecedores
    # deleta fornecedores
    # atualiza fornecedores
    pass