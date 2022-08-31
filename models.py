import psycopg2

class Usuario:

    def __init__(self, nome, senha):
        self.nome = nome 
        self.senha = senha

    def cadastro(self):

        con = psycopg2.connect(
            host='localhost',
            dbname='empire',
            user='postgres',
            password='nicolasvx123'
        )

        print(self.nome)

        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS public.usuario (id serial PRIMARY KEY, nome varchar(50), senha varchar(50));")
        cur.execute("SELECT * FROM public.usuario;")
        users = cur.fetchall()

        cadastrado = False
        for user in users:
            if self.nome == user[1]:
                cadastrado = True
            
        if cadastrado:
            return print('Usuário já existe!')

        cur.execute("INSERT INTO public.usuario (nome,senha) VALUES (%s, %s)", (self.nome, self.senha))
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
        cur.execute("SELECT * FROM usuario;")
        users = cur.fetchall()
        for user in users:
            if self.nome == user[1] and self.senha == user[2]:
                cur.close()
                con.close()
                return True
        cur.close()
        con.close()
        return print('Usuário não cadastrado!')

class Estoque(Usuario):

    def __init__(self, usuario=Usuario):
        self.usuario = usuario

    def entrada_estoque(usuario):

        if usuario.login:
            
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
                produto_selecionado = cur.execute("SELECT quantidade FROM public.estoque WHERE nome_produto=(%s)", (nome_produto,))
                print(produto_selecionado)
                quantidade = input(f'Quantidade atual {produto_selecionado[1]}. Quantidade a ser adicionada: ')
                cur.execute("UPDATE public.estoque SET quantidade=quantidade+(%s) WHERE nome_produto=(%s)", (quantidade, nome_produto))
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

        return print('Usuario não cadastrado!')

    

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