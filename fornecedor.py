import re
import requests
import psycopg2

from validate_docbr import CNPJ
from usuario import Usuario

class Fornecedor(Usuario):

    def __init__(self, nome, numero, cnpj, cep):
        
        if self.valida_nome(nome):
            self.nome = nome

        else:
            print(
                '\nNome inválido!'
                '\nSiga o exemplo a seguir: \'Empire Distribuidora\'\n'
                '\nNomes como \'Emp1re\\Emp!re\' ou vazios, não são válidos!\n'
            )

            while True:
                print('\nDigite o nome novamente! Ou volte ao menu principal precionando a tecla \'0\'.')
                resposta = input('--> ')

                if resposta == '0':
                    return self.menu_login()
                
                if self.valida_nome(resposta):
                    self.nome = resposta
                    break

        if self.valida_numero(numero):
            self.numero = numero

        else:
            print(
                '\nNumero inválido!'
                '\nO numero deve conter 11 dígitos, sendo composto pelo ddd e os 10 numeros restantes.'
                '\nNumero incompleto ou com letras não é válido.\n'
            )

            while True:
                print('\nDigite o numero novamente! Ou volte ao menu principal precionando a tecla \'0\'.')
                resposta = input('--> ')

                if resposta == '0':
                    return self.menu_login()

                if self.valida_numero(resposta):
                    self.numero = resposta
                    break

        if self.valida_cnpj(cnpj):
            self.cnpj = cnpj

        else:
            print(
                '\nCNPJ inválido!'
                '\nO CNPJ deve conter 14 dígitos e ser existente.'
                '\nCNPJ incompleto ou com letras não é válido.\n'
            )

            while True:
                print('\nDigite o CNPJ novamente! Ou volte ao menu principal precionando a tecla \'0\'.')
                resposta = input('--> ')

                if resposta == '0':
                    self.menu_login()

                if self.valida_cnpj(resposta):
                    self.cnpj = resposta
                    break

        if self.valida_cep(cep):
            self.cep = cep
            self.dados = self.via_cep()
            
        else:
            print(
                '\nCEP inválido!'
                '\nO CEP deve conter 8 dígitos e ser existente.'
                '\nCEP incompleto ou com letras não é válido.'
            )

            while True:
                print('\nDigite o CEP novamente! Ou volte ao menu principal precionando a tecla \'0\'.')
                resposta = input('--> ')

                if resposta == '0':
                    self.menu_login()

                if self.valida_cep(resposta):
                    self.cep = resposta
                    break      

        self.confirma()

    def valida_nome(self, nome):

        if re.match(r'[a-zA-Z ]+$', nome):
            return True

        return False
    
    def valida_numero(self, numero):

        numero_valido = "([0-9]{2})([0-9]{5})([0-9]{4})"
        numero_validado = re.findall(numero_valido, numero)

        if numero_validado:
            return True
        
        return False

    def format_numero(self):

        numero_valido = "([0-9]{2})([0-9]{5})([0-9]{4})"
        numero = re.search(numero_valido, self.numero)
        numero_formatado = f"({numero.group(1)}){numero.group(2)}-{numero.group(3)}"

        return numero_formatado
    
    def valida_cnpj(self, cnpj):
        
        documento = CNPJ()
        return documento.validate(cnpj)

    def format_cnpj(self):

        documento = CNPJ()
        return documento.mask(self.cnpj)

    def valida_cep(self, cep):

        if len(cep) == 8:
            return True
        
        return False

    def format_cep(self):

        cep_formatado = f'{self.cep[:5]}-{self.cep[5:]}'
        return cep_formatado        

    def via_cep(self):

        r = requests.get(f'https://viacep.com.br/ws/{self.cep}/json/')
        dados = r.json()

        return dados

    def confirma(self):

        print(
            '\nConfirma as informações? [s/n]'
            f'\nNome: {self.nome}'
            f'\nNumero: {self.format_numero()}'
            f'\nCNPJ: {self.format_cnpj()}'
            f'\nCEP: {self.format_cep()}'
        )
        resposta = input('--> ')

        if resposta == 's':
            self.cadastro_fornecedor()

        elif resposta == 'n':

            while True:
                print(
                    '\nQual item deseja alterar?'
                    f'\n[1] - Nome. Atual {self.nome}.'
                    f'\n[2] - Numero. Atual {self.format_numero()}.'
                    f'\n[3] - CNPJ. Atual {self.format_cnpj()}.'
                    f'\n[4] - CEP. Atual {self.format_cep()}.'
                    '\n[5] - Voltar ao menu.'
                    '\n[6] - Continuar.'
                )
                confirmacao = input('--> ')

                if confirmacao == '1':

                    while True:
                        print('\nDigite o nome novamente:')
                        resposta = input('--> ')

                        if self.valida_nome(resposta):
                            self.nome = resposta
                            print('\nNome atualizado com sucesso!')
                            break
                        else:
                            print('Nome inválido!')
                
                if confirmacao == '2':

                    while True:
                        print('\nDigite o numero novamente:')
                        resposta = input('--> ')

                        if self.valida_numero(resposta):
                            self.numero = resposta
                            print('\nNumero atualizado com sucesso!')
                            break
                        else:
                            print('\nNumero inválido!')

                if confirmacao == '3':

                    while True:
                        print('\nDigite o CNPJ novamente:')
                        resposta = input('--> ')

                        if self.valida_cnpj(resposta):
                            self.cnpj = resposta
                            print('\nCNPJ atualizado com sucesso!')
                            break
                        else:
                            print('\nCNPJ inválido!')

                if confirmacao == '4':

                    while True:
                        print('\nDigite o CEP novamente:')
                        resposta = input('--> ')

                        if self.valida_cep(resposta):
                            self.cep = resposta
                            print('\nCEP atualizado com sucesso!')
                            break
                        else:
                            print('\nCEP inválido!')

                if confirmacao == '5':
                    self.menu_login()

                if confirmacao == '6':
                    self.cadastro_fornecedor()
                    
    def cadastro_fornecedor(self):

        con = psycopg2.connect(
            host='localhost',
            dbname='empire',
            user='postgres',
            password='nicolasvx123'
        )

        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS public.fornecedor (id serial PRIMARY KEY, nome varchar(50), numero varchar(11), cnpj varchar(14), cep varchar(8), uf varchar(2), logradouro varchar(50), complemento varchar(50), bairro varchar(50), localidade varchar(50))")
        cur.execute("SELECT * FROM public.fornecedor")
        fornecedores = cur.fetchall()
        cadastrado = False

        for fornecedor in fornecedores:
            if self.cnpj == fornecedor[3]:
                cadastrado = True

        while cadastrado:

            print(
                '\nFornecedor já cadastrado! O que deseja fazer a seguir?\n'
                '\n[1] - Atualizar cadastro.'
                '\n[2] - Deletar cadastro.'
                '\n[3] - Voltar ao menu principal.'
                '\n[4] - Sair.\n'
            )

            # arrumar essa parte depois

        cur.execute("INSERT INTO public.fornecedor (nome, numero, cnpj, cep, uf, logradouro, complemento, bairro, localidade) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.nome, self.numero, self.cnpj, self.cep, self.dados['uf'], self.dados['logradouro'], self.dados['complemento'], self.dados['bairro'], self.dados['localidade']))
        
    def deleta_fornecedor(self):
        pass

    def atualiza_fornecedor(self):
        pass