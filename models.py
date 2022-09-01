import psycopg2

class Usuario:

    def __init__(self, nome, senha):
        self._nome = nome 
        self._senha = senha

        print('\nBem vindo!')
        print('Primeiramente cadastre-se[1], faça login[2] ou sair[3]!')
        resposta = input('--> ')

        if resposta == '1':
            self.cadastro()
        elif resposta == '2':
            self.login()
        elif resposta == '3':
            print('\nVolte sempre!\n')
            exit()
        else:
            print('Opção inválida!')
            self.__init__(self._nome, self._senha)

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
            
        if cadastrado:
            print('\nUsuário já existe! Deseja fazer o login? [s/n]')
            resposta = input('--> ')
            if resposta == 's':
                self.login()
            elif resposta == 'n':
                exit()
            print('\nOpção inválida!')
            return self.cadastro()

        cur.execute("INSERT INTO public.usuario (nome,senha) VALUES (%s, %s)", (self._nome, self._senha))
        con.commit()        
        cur.close()
        con.close()

        return('Usuário cadastrado com sucesso!')

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
            print('Que função deseja fazer? Controle de estoque[1]')
            resposta = input('--> ')

            if resposta == '1':
                return Estoque()

            print('\nOpção inválida!')
            self.login()

        cur.close()
        con.close()
        return False

class Estoque(Usuario):

    def __init__(self):

        print('\nVocê está na aba de controle de estoque!')
        print('Qual funcionalidade deseja?')
        print('Entrada de estoque[1]')
        print('Saida de estoque[2]')
        resposta = input('--> ')

        if resposta == '1':
            self.entrada_estoque()
        elif resposta == '2':
            self.saida_estoque()
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
            print('Produto já existe!\n')
            cur.execute("SELECT quantidade FROM public.estoque WHERE nome_produto=%s", (nome_produto,))
            produto_selecionado = cur.fetchone()
            quantidade = input(f'Quantidade atual {produto_selecionado[0]}. Quantidade a ser adicionada: ')
            cur.execute("UPDATE public.estoque SET quantidade=quantidade+(%s) WHERE nome_produto=(%s)", (quantidade, nome_produto))
            print(f"Quantidade agora é {int(produto_selecionado[0])+int(quantidade)}\n")
            con.commit()
            cur.close()
            con.close()
            return print('Quantidade do produto atualizada!')

        print('Produto não encontrado no banco de dados, cadastre!\n')
        quantidade = input('Digite a quantidade: ')
        valor_de_compra = input('Digite o valor de compra: ')
        valor_de_venda = input('Digite o valor de venda: ')

        cur.execute("INSERT INTO public.estoque (nome_produto, quantidade, valor_de_compra, valor_de_venda) VALUES (%s, %s, %s, %s)", (nome_produto, quantidade, valor_de_compra, valor_de_venda))
        con.commit()
        cur.close()
        con.close()

        print('Produto cadastrado com sucesso!\n')
        return print('Tudo certo!')

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
                
                return Estoque.entrada_estoque(self)

            elif resposta == 'n':
                
                print('Operação cancelada. O que deseja fazer a seguir?\n')
                print('[1] - Entrada de estoque.')
                print('[2] - Sair.')
                resposta = input('--> ')

                if resposta == '1':
                    return Estoque.entrada_estoque(self)
                elif resposta == '2':
                    print('Obrigado por usar o sistema!')
                    return exit()
                
        resposta = input('Produto não encontrado no banco de dados, deseja cadastrar? [s/n] ')
        if resposta == 's':
            return Estoque.entrada_estoque(self)
        elif resposta == 'n':
            print('Obrigado por usar o sistema!')
            return exit()

class Vendas(Estoque):

    ## variaveis
    #

    ## funcoes
    # quantidade vendida
    # valor vendido
    # totais mensais/anuais
    pass

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