from PyQt5 import uic,QtWidgets #Qwidgets para trabalhar com elementos graficos
import sqlite3 #importando o sqllite3

def chama_segunda_tela(): # Ao clicar no botão de login vai executar a lógica de comparação dos dados digitados com os que contém no sistema
    primeira_tela.label_4.setText("") #string vazia para limpar o campo 
    nome_usuario = primeira_tela.lineEdit.text() # pega a primeira caixa de texto que o usuario digitou e guarda nessa variavel
    senha = primeira_tela.lineEdit_2.text() # O mesmo para a senha
    banco = sqlite3.connect('banco_cadastro.db') #Declarado a conexão com o banco
    cursor = banco.cursor() # Criando a variavel de cursor para fazer as querys no banco
    try:
        cursor.execute("SELECT senha FROM cadastro WHERE login='{}'".format(nome_usuario)) # Pegar a senha gravada no banco de dados, passando cadastro como nome da tabela, 
                                                                                           # pegar a senha na mesma linha onde o login tem o mesmo valor que o usuario digitou
        senha_bd = cursor.fetchall()#recuperando a senha do banco para posteriormente realizar a validação
        banco.close() # Sempre fechar a conexão com o banco
    except:
        print("Erro ao validar o Login") # Criando exceção para não fechar o banco mesmo digitando usuário inexistente

    if senha == senha_bd[0][0] : #Definindo as credencias para comparação
        primeira_tela.close() # confirmação de login
        segunda_tela.show() #dentro do sistema
    else:
        primeira_tela.label_4.setText(" Dados de Login Incorretos ! ") # caso não for conforme acima não inicializa uma nova tela e informa o erro

def logout(): # Pega a segunda tela de logout e fecha e abre a primeira tela de login
    segunda_tela.close() #fechar
    primeira_tela.show() #abrir

def abre_tela_cadastro(): # Ao clicar no botão de abrir a tela de cadastro
    tela_cadastro.show() # colocando a tela na função para ser chamado posteriormente pelo botão
    


def cadastrar(): #Lógica de pegar os dados da tela e colocar no banco
    nome = tela_cadastro.lineEdit.text() # Pegar os dados do formulário, usando a line corresponde com a função teste salvando na variável
    login = tela_cadastro.lineEdit_2.text()
    senha = tela_cadastro.lineEdit_3.text()
    c_senha = tela_cadastro.lineEdit_4.text()

    if (senha == c_senha): # verificando se a senha inserida no primeiro campo é igual a do segundo campo para confirmação
        try: # tentar cadastrar no banco
            banco = sqlite3.connect('banco_cadastro.db') #Função sqlite para criar o banco, connect serve para criar o banco caso já exista o mesmo não é criado
            cursor = banco.cursor() # Objeto para manipular o banco com as query
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome text,login text,senha text)") # Criando a tabela caso não exista, caso já existir a linha é ignorada
            cursor.execute("INSERT INTO cadastro VALUES ('"+nome+"','"+login+"','"+senha+"')") # inserindo os dados inseridos no banco

            banco.commit() # Commit(fazer as alterações no banco)
            banco.close() # Fechar o banco de dados
            tela_cadastro.label.setText("Usuario cadastrado com sucesso") # informando ao usuario que foi cadastrado com sucesso

        except sqlite3.Error as erro: # caso de alguma excessão informar, informar o erro que aconteceu ao cadastrar
            print("Erro ao inserir os dados: ",erro)
    else:
        tela_cadastro.label.setText("As senhas digitadas estão diferentes") # informando que as senhas digitas são diferentes

#Declaração dos arquivos gerados no QtDesigner
app=QtWidgets.QApplication([])
primeira_tela=uic.loadUi("primeira_tela.ui") #Carregando a primeira tela para utilização no código quando necessário
segunda_tela=uic.loadUi("segunda_tela.ui") # Carregando a segunda tela
tela_cadastro =uic.loadUi("tela_cadastro.ui")# Carregando a tela de cadastro
primeira_tela.pushButton.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(logout)
primeira_tela.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password) # usando QtWidgets com o nome da Classe QlineEdit e usando para criar um campo do tipo senha
primeira_tela.pushButton_2.clicked.connect(abre_tela_cadastro) # Para quando clicar no botão chamar a tela de cadastro
tela_cadastro.pushButton.clicked.connect(cadastrar)


primeira_tela.show()
app.exec()


