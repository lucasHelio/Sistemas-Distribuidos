#passivo

import socket
#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE,SIG_DFL)

Dicionario = []


#sempre que um cliente logar ele deve receber o dicionario por completo e os sistemas de busca
#devem ser feitos no computador dele

#consertar funcoes 4, 6, 7



class Palavra:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valores = valor


def listaPalavras():
    palavras = " "
    for x in Dicionario:
        palavras = palavras +"*"+ x.chave
        
    str_bytes = palavras.encode("ascii")
    novoSock.send(str_bytes) 
    return
    
def encontraChave(chave):
    for x in Dicionario:
        if chave == x.chave:
            return x
    return 0
    
def printaChave(chave):
    for x in Dicionario:
        if chave == x.chave:
            y = ("\nPalavra: "+ x.chave+ "\t\tDefinicao: ")
            for d in x.valores:
                y = y + " " +d
            y= y+"\n"
            str_bytes = y.encode('ascii')
            novoSock.send(str_bytes)
            #print("\n")
            return
    novoSock.send(b"\npalavra nao encontrada")
    return

def adicionaChave(chave, valor):
    if not encontraChave(chave):
        Dicionario.append(Palavra(chave, valor))   
        novoSock.send(b"\nPalavra adicionada com sucesso!\n")
        return
    else:
        novoSock.send(b"\nA palavra ja existe\n")
        return

def removeChave(chave):
    Obj = encontraChave(chave)
    if Obj:
        Dicionario.remove(Obj)
        novoSock.send(b"\nA palavra foi removida\n")
        return
    else:
        novoSock.send(b"\nA palavra nao foi encontrada\n")
        return
    
   
def alteraValorChave(chave):
    Obj = encontraChave(chave)
    if Obj:
        novoSock.send(b"1")# encontrou o obj
        y=''
        for x in Obj.valores:
            y = y + str(Obj.valores.index(x))+ " - "+x+"*"
        str_bytes = y.encode("ascii") 
        novoSock.send(str_bytes)

        #msg = novoSock.recv(1024) # confirma o recebimento da mensagem anterior

        novoSock.send(b"escolha uma definicao para alterar: ")
        msg = novoSock.recv(1024) # espera a entrada do usuario
        y = str(msg, 'utf-8')

        novoSock.send(b"Digite a nova Definicao: ")
        msg = novoSock.recv(1024) # espera a entrada do usuario
        novaDefinicao = str(msg, 'utf-8')
        Obj.valores.pop(int(y))
        Obj.valores.insert(int(y), novaDefinicao)
        novoSock.send(b"A definicao foi alterada ")
    else:
        novoSock.send(b"0")
        novoSock.send(b"A palavra nao foi encontrada")
    return
    
def adicionaValor(chave):
    Obj = encontraChave(chave)
    if Obj:
        novoSock.send(b"1")
        novoSock.send(b"escreva uma nova definicao: ")
        msg = novoSock.recv(1024) # espera a entrada do usuario
        novoValor = str(msg, 'utf-8')
        Obj.valores.append(novoValor)

        
        
        novoSock.send(b"\nO valor foi adicionado com sucesso!\n")
        return
    else:
        novoSock.send(b"0")
        novoSock.send(b"A palavra nao foi encontrada")
        return



def switchAdm(x):
    if x == "0":
        novoSock.send(b"Digite a palavra a ser removida: ")
        msg = novoSock.recv(1024) # espera a entrada do usuario
        chave = str(msg, 'utf-8')
        removeChave(chave)
        return
    elif x == "1":
        listaPalavras()
        msg = novoSock.recv(1024) # tentando evitar o deadlock
        return 
    elif x == "2":
        
        novoSock.send(b"Digite a palavra a ser procurada: ")
        msg = novoSock.recv(1024) # espera a entrada do usuario
        chave = str(msg, 'utf-8')
        printaChave(chave)    
        return 
    elif x == "3":
        #chave = input("Digite a palavra a ser adicionada: ")
        novoSock.send(b"Digite a palavra a ser adicionada: ")
        msg = novoSock.recv(1024) # espera a entrada do usuario
        chave = str(msg, 'utf-8')
        
        novoSock.send(b"Digite uma definicao: ")
        msg = novoSock.recv(1024) # espera a entrada do usuario
        definicao = str(msg, 'utf-8')
        
        adicionaChave(chave, [definicao])
        return 
     
    elif x == "4":
        #chave = input("Digite a palavra que deseja alterar a definicao: ")
        novoSock.send(b"Digite a palavra que deseja alterar a definicao: ")
        msg = novoSock.recv(1024) # espera a entrada do usuario
        chave = str(msg, 'utf-8')
        alteraValorChave(chave)
        return 
    elif x == "5":
        #chave = input("Digite a palavra que deseja adicionar uma definicao: ")
        novoSock.send(b"Digite a palavra que deseja adicionar uma definicao: ")
        msg = novoSock.recv(1024) # espera a entrada do usuario
        chave = str(msg, 'utf-8')
        adicionaValor(chave)
        return
    elif x == "6": #dar uma olhada nisso dps
        #arquivoLeitura()
        #print("Arquivo restaurado")
        #return
        pass
    elif x == "7":
        #arquivoEscrita()
        #global prog
        #prog = 0
        #return
        pass
    else:
        #print (colored("comando nao reconhecido", 'red'))
        print ("\ncomando nao reconhecido\n")
        return


def switchUsuario(x):
    if x == "1":
        listaPalavras()
        return
    elif x == "2":
        chave = input("Digite a palavra a ser procurada: ")
        printaChave(chave)
        #for obj in Dicionario:
        #    print(obj.chave, obj.valores)
        
        return 
    elif x == "3":
        chave = input("Digite a palavra a ser adicionada: ")
        definicao = input("Digite uma definicao: ")
        adicionaChave(chave, [definicao])
        return 
    
    elif x == "4":
        chave = input("Digite a palavra que deseja alterar a definicao: ")
        alteraValorChave(chave)
        return 
    elif x == "5":
        chave = input("Digite a palavra que deseja adicionar uma definicao: ")
        adicionaValor(chave)
        return
    elif x == "6":
        arquivoLeitura()
        print("Arquivo restaurado")
        return
    elif x == "7":
        arquivoEscrita()
        global prog
        prog = 0
        return
    else:
        #print (colored("comando nao reconhecido", 'red'))
        print ("\ncomando nao reconhecido\n")
        return    

prog = 1




HOST = ''     # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5000  # porta onde chegarao as mensagens para essa aplicacao

# cria um socket para comunicacao
sock = socket.socket() # valores default: socket.AF_INET, socket.SOCK_STREAM  

# vincula a interface e porta para comunicacao
sock.bind((HOST, PORTA))

# define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
sock.listen(5) 

print('Pronto para receber conexoes...')

# aceita a primeira conexao da fila (chamada pode ser BLOQUEANTE)
novoSock, endereco = sock.accept() # retorna um novo socket e o endereco do par conectado
print ('Conectado com: ', endereco)

#--------------------------- espera o login ----------------------
msg1 = novoSock.recv(1024)
msg2 = novoSock.recv(1024)
login = (str(msg1, 'utf-8'))
#login = (str(msg1))
senha = (str(msg2, 'utf-8'))
#senha = (str(msg2))
if login == "adm" and senha == "123":
    novoSock.send(b"1") # eh adm
    novoSock.send(b"\n\t\t\t\tBem vindo ADM!\n")

    while prog:
        novoSock.send(b'\t\t\tADM o que gostaria de fazer?\n\n\t\t\t0 - Remover uma palavra\n\t\t\t1 - listar todas as palavras\n\t\t\t2 - Buscar uma palavra\n\t\t\t3 - Inserir uma palavra\n\t\t\t4 - Alterar uma definicao\n\t\t\t5 - Adicionar uma definicao\n\t\t\t6 - Restaurar sessao\n\t\t\t7 - Sair\n')
        msg = novoSock.recv(1024) # espera a entrada do usuario
        entrada = str(msg, 'utf-8')
        switchAdm(entrada)
    
    
else:
    novoSock.send(b"0") #eh usuario
    novoSock.send(b"\n\t\t\t\tBem vindo Usuario!\n")
    while prog:
        novoSock.send(b"\t\t\to que gostaria de fazer?\n\n\t\t\t1 - listar todas as palavras\n\t\t\t2 - Buscar uma palavra\n\t\t\t3 - Inserir uma palavra\n\t\t\t4 - Alterar uma definicao\n\t\t\t5 - Adicionar uma definicao\n\t\t\t6 - Restaurar sessao\n\t\t\t7 - Sair\n")
        msg = novoSock.recv(1024) # espera a entrada do usuario
        entrada = str(msg, 'utf-8')
        #switchUsuario(entrada)
        switchAdm(entrada)
    
	 

# # fecha o socket da conexao
novoSock.close() 

# # # fecha o socket principal
sock.close()
