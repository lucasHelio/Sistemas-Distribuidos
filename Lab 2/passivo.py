#passivo

import socket
import select
import sys
import threading

# define a localizacao do servidor
HOST = '' # vazio indica que podera receber requisicoes a partir de qq interface de rede da maquina
PORT = 5000 # porta de acesso

#define a lista de I/O de interesse (jah inclui a entrada padrao)
entradas = [sys.stdin]
#armazena as conexoes ativas
conexoes = {}
#lock para acesso do dicionario 'conexoes'
lock = threading.Lock()

#Dicionario do servidor
Dicionario = []

class Palavra:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valores = valor





def iniciaServidor():
	'''Cria um socket de servidor e o coloca em modo de espera por conexoes
	Saida: o socket criado'''
	# cria o socket 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP) 

	# vincula a localizacao do servidor
	sock.bind((HOST, PORT))

	# coloca-se em modo de espera por conexoes
	sock.listen(5) 

	# configura o socket para o modo nao-bloqueante
	sock.setblocking(False)

	# inclui o socket principal na lista de entradas de interesse
	entradas.append(sock)

	return sock

def aceitaConexao(sock):
	'''Aceita o pedido de conexao de um cliente
	Entrada: o socket do servidor
	Saida: o novo socket da conexao e o endereco do cliente'''

	# estabelece conexao com o proximo cliente
	clisock, endr = sock.accept()

	# registra a nova conexao
	lock.acquire()
	conexoes[clisock] = endr 
	lock.release()

	return clisock, endr


def listaPalavras(socket):
    palavras = " "
    for x in Dicionario:
        palavras = palavras +"*"+ x.chave

    enviaMensagem(palavras, socket)    
    return
    
def encontraChave(chave):
    for x in Dicionario:
        if chave == x.chave:
            return x
    return 0
    
def printaChave(chave, socket):
    for x in Dicionario:
        if chave == x.chave:
            y = ("\nPalavra: "+ x.chave+ "\t\tDefinicao: ")
            for d in x.valores:
                y = y + " " +d +";"
            y= y+"\n"

            enviaMensagem(y, socket)
            return
    msg = "\npalavra nao encontrada\n"
    enviaMensagem(msg, socket)
    return

def adicionaChave(chave, valor, socket):
    if not encontraChave(chave):
        Dicionario.append(Palavra(chave, valor))   
        msg = "\nPalavra adicionada com sucesso!\n"
        enviaMensagem(msg, socket)
        return
    else:
        msg = "\nA palavra ja existe\n"
        enviaMensagem(msg, socket)
        return

def removeChave(chave, socket):
    Obj = encontraChave(chave)
    if Obj:
        Dicionario.remove(Obj)
        msg = "\nA palavra foi removida\n"
        enviaMensagem(msg, socket)
        return
    else:
        msg = "\nA palavra nao foi encontrada\n"
        enviaMensagem(msg, socket)
        return
    
   
def alteraValorChave(chave, socket):
    Obj = encontraChave(chave)
    if Obj:
        enviaMensagem("1", socket) # encontrou o obj
        y=''
        for x in Obj.valores:
            y = y + str(Obj.valores.index(x))+ " - "+x+"*"

        enviaMensagem(y, socket)


        chave = recebeMensagem(socket)
        
        # se a chave n existir? if chave
        if Obj.valores[int(chave)] != "":
            enviaMensagem("1", socket) #achou a definicao
            novaDefinicao = recebeMensagem(socket)
            Obj.valores.pop(int(chave))
            Obj.valores.insert(int(chave), novaDefinicao)
            msg = "A definicao foi alterada "
            enviaMensagem(msg, socket)
        else:
            enviaMensagem("0", socket)
            msg = "\nDefinicao escolhida nao existe\n"
            enviaMensagem(msg, socket)
        return
    else:
        enviaMensagem("0", socket)
        enviaMensagem("A palavra nao foi encontrada", socket)  
    return
    
def adicionaValor(chave, socket):
    Obj = encontraChave(chave)
    if Obj:
        
        enviaMensagem("1", socket)
        novoValor = recebeMensagem(socket)
        Obj.valores.append(novoValor)

        
        msg = "\nO valor foi adicionado com sucesso!\n"
        enviaMensagem(msg, socket)
        return
    else:
        enviaMensagem("0", socket)
        msg = "\nA palavra nao foi encontrada\n"
        enviaMensagem(msg, socket)
        return



def switchAdm(x, socket):
    if x == "0":
        msg = "Digite a palavra a ser removida: "
        enviaMensagem(msg,socket)
        chave = recebeMensagem(socket)
        removeChave(chave, socket)
        return
    elif x == "1":
        listaPalavras(socket)
        return 
    elif x == "2":
        
        msg = "Digite a palavra a ser procurada: "
        enviaMensagem(msg, socket)
        chave = recebeMensagem(socket)# espera a entrada do usuario
        printaChave(chave, socket)    
        return 
    
    elif x == "3":
        msg ="Digite a palavra a ser adicionada: "
        enviaMensagem(msg, socket)
        chave = recebeMensagem(socket)  # espera a entrada do usuario
        
        msg = "Digite uma definicao: "
        enviaMensagem(msg, socket)
        
        definicao = recebeMensagem(socket) # espera a entrada do usuario
        
        adicionaChave(chave, [definicao], socket)
        return 
     
    elif x == "4":
        msg = "Digite a palavra que deseja alterar a definicao: "
        enviaMensagem(msg, socket)

        chave = recebeMensagem(socket)
        alteraValorChave(chave, socket)
        return 
    elif x == "5":
        msg = "Digite a palavra que deseja adicionar uma definicao: "
        enviaMensagem(msg, socket)
        chave = recebeMensagem(socket) # espera a entrada do usuario
        adicionaValor(chave, socket)
        return
    elif x == "6": #dar uma olhada nisso dps
        pass
        
    else:
        #print (colored("comando nao reconhecido", 'red'))
        print ("\ncomando nao reconhecido\n")
        return


def switchUsuario(x, socket):
    if x == "1":
        listaPalavras(socket)
        #msg = novoSock.recv(1024) # tentando evitar o deadlock
        return 
    elif x == "2":
        
        msg = "Digite a palavra a ser procurada: "
        enviaMensagem(msg, socket)
        chave = recebeMensagem(socket)# espera a entrada do usuario
        printaChave(chave, socket)    
        return 
    
    elif x == "3":
        msg ="Digite a palavra a ser adicionada: "
        enviaMensagem(msg, socket)
        chave = recebeMensagem(socket)  # espera a entrada do usuario
        
        msg = "Digite uma definicao: "
        enviaMensagem(msg, socket)
        
        definicao = recebeMensagem(socket) # espera a entrada do usuario
        
        adicionaChave(chave, [definicao], socket)
        return 
     
    elif x == "4":
        msg = "Digite a palavra que deseja alterar a definicao: "
        enviaMensagem(msg, socket)

        chave = recebeMensagem(socket)
        alteraValorChave(chave, socket)
        return 
    elif x == "5":
        msg = "Digite a palavra que deseja adicionar uma definicao: "
        enviaMensagem(msg, socket)
        chave = recebeMensagem(socket) # espera a entrada do usuario
        adicionaValor(chave, socket)
        return
    elif x == "6": #dar uma olhada nisso dps
        pass

    else:
        print ("\ncomando nao reconhecido\n")
        return    

prog = 1



def recebeMensagem(recebeSock):
    tamMsg = recebeSock.recv(1) #recebe tamanho da mensagem
    tam = int.from_bytes(tamMsg, 'big')
    recebidos = 0
    chunks = []
    while recebidos < tam:
        chunk = recebeSock.recv(min(tam-recebidos, 2048))
        if not chunk:
            return -1
            
        chunks.append(chunk)
        recebidos = recebidos + len(chunk)
    #msgRec = recebeSock.recv(tam) #le mensagem de tamanho tam
    #msg = str(msgRec, 'utf-8')
    #return msg
    y = str(b''.join(chunks), 'utf-8')
    return y 

def enviaMensagem(input, socket):
    str_bytes = input.encode("ascii")
    tam = len(str_bytes)
    byt = tam.to_bytes(1, 'big')
    socket.send(byt) #envia tamanho da mensagem
    total = 0
    while total < tam:
        enviado = socket.send(str_bytes[total:]) #envia mensagem
        if enviado ==0:
            #retorna com erro
            return -1
        total = total+ enviado
    #socket.sendall(str_bytes)
    return




def atendeRequisicoes(clisock, endr):
	#'''Recebe mensagens e as envia de volta para o cliente (ate o cliente finalizar)
	#Entrada: socket da conexao e endereco do cliente
	#Saida: '''

	#--------------------------- espera o login ----------------------
    login = recebeMensagem(clisock)
    senha = recebeMensagem(clisock)
    
    
    if login == "adm" and senha == "123":
        enviaMensagem("1", clisock)# eh adm
        enviaMensagem("\n\t\t\t\tBem vindo ADM!\n", clisock)
        print('Adm loggin')
        
        while True:
            msg = '\t\t\tADM o que gostaria de fazer?\n\n\t\t\t0 - Remover uma palavra\n\t\t\t1 - listar todas as palavras\n\t\t\t2 - Buscar uma palavra\n\t\t\t3 - Inserir uma palavra\n\t\t\t4 - Alterar uma definicao\n\t\t\t5 - Adicionar uma definicao\n\t\t\t6 - Sair\n'
            enviaMensagem(msg, clisock)
            entrada = recebeMensagem(clisock)
            if not entrada: # dados vazios: cliente encerrou
                print(str(endr) + '-> encerrou')
                lock.acquire()
                del conexoes[clisock] #retira o cliente da lista de conexoes ativas
                lock.release()
                clisock.close() # encerra a conexao com o cliente
                return
            
            switchAdm(entrada, clisock)
    
    
    else:
        enviaMensagem("0", clisock)#eh usuario
        enviaMensagem("\n\t\t\t\tBem vindo Usuario!\n", clisock)
        print('Usuario loggin')
        while True:
            msg = "\t\t\to que gostaria de fazer?\n\n\t\t\t1 - listar todas as palavras\n\t\t\t2 - Buscar uma palavra\n\t\t\t3 - Inserir uma palavra\n\t\t\t4 - Alterar uma definicao\n\t\t\t5 - Adicionar uma definicao\n\t\t\t6 - Sair\n"
            enviaMensagem(msg, clisock)
            entrada = recebeMensagem(clisock)

            if not entrada: # dados vazios: cliente encerrou
                print(str(endr) + '-> encerrou')
                lock.acquire()
                del conexoes[clisock] #retira o cliente da lista de conexoes ativas
                lock.release()
                clisock.close() # encerra a conexao com o cliente
                return 
            switchUsuario(entrada, clisock)

def arquivoEscrita():
    Arquivo = open("dicionario.txt","w")
    for x in Dicionario:
        Arquivo.write(str(x.chave))
        for y in x.valores:
            Arquivo.write("*"+ str(y))
        Arquivo.write("\n")
            
    Arquivo.close()
    return

def arquivoLeitura():
    Arquivo = open("dicionario.txt", "r")

    x = Arquivo.read().splitlines()
    for a in x:
        i = a.split('*')
        adicionaChave(i[0], i[1:])
    Arquivo.close()
    return


def main():
	'''Inicializa e implementa o loop principal (infinito) do servidor'''
	sock = iniciaServidor()
	print("Pronto para receber conexoes...")
	arquivoLeitura()
	while True:
		#espera por qualquer entrada de interesse
		leitura, escrita, excecao = select.select(entradas, [], [])
		#tratar todas as entradas prontas
		for pronto in leitura:
			if pronto == sock:  #pedido novo de conexao
				clisock, endr = aceitaConexao(sock)
				print ('Conectado com: ', endr)
				#cria nova thread para atender o cliente
				cliente = threading.Thread(target=atendeRequisicoes, args=(clisock,endr))
				cliente.start()
			elif pronto == sys.stdin: #entrada padrao
				cmd = input()
				if cmd == 'fim': #solicitacao de finalizacao do servidor
					if not conexoes: #somente termina quando nao houver clientes ativos
						arquivoEscrita()
						sock.close()
						sys.exit()
					else: print("ha conexoes ativas")
				elif cmd == 'hist': #outro exemplo de comando para o servidor
					print(str(conexoes.values()))

main()
