#ativo

import socket


def switchFunc(entrada, adm, socket):
    enviaMensagem(entrada, socket) #escolha que o usuario fez
    
    if entrada == "0" and adm =="1":
        msg = recebeMensagem(socket) #pergunta do serv
        x= input(msg)
        enviaMensagem(x, socket) #envia resposta
        
        msgServ = recebeMensagem(socket) #aguarda saber se a chave foi removida
        print(msgServ)
        return
    
    elif entrada == "1":
        x = recebeMensagem(socket)
        y = x.split("*")
        y = sorted(y)
        for palavra in y:
            print(palavra)

        #sock.send(b"msg chegou")  
        return
        
    elif entrada == "2":
        msgServ = recebeMensagem(socket) #pergunta do serv
        chave= input(msgServ)
        enviaMensagem(chave, socket) #resposta
        msg =recebeMensagem(sock)
        print(msg)        
        return
    
    elif entrada == "3":
        msgServ = recebeMensagem(socket) #chave
        chave = input(msgServ)
        enviaMensagem(chave, socket)

        msgServ = recebeMensagem(socket)
        definicao= input(msgServ)

        enviaMensagem(definicao, socket)

        msgServ = recebeMensagem(socket) #aguarda o retorno da funcao
        print(msgServ)
        return
    
    elif entrada == "4":
        msgServ = recebeMensagem(socket)
        x= input(msgServ)#chave
        enviaMensagem(x, socket)#envia chave

        
        x = recebeMensagem(socket)
        if x == "1":

            lista = recebeMensagem(socket)   #recebe definicoes
            
            print(lista)
            print("\n")

            chave = input("escolha uma definicao para alterar: ")

            enviaMensagem(chave, socket)
            #se achou a chave
            b = recebeMensagem(socket)
            if b =="1":
                definicao = input("Digite a nova Definicao: ")
                enviaMensagem(definicao, socket)
        
        msgServ = recebeMensagem(sock)
        print(msgServ)
        return
    
    elif entrada == "5":
        msgServ = recebeMensagem(socket) #aguarda a prox instrucao
        x= input(msgServ)
        enviaMensagem(x, socket)

        
        b = recebeMensagem(socket)
        if b == "1":
            definicao= input("escreva uma nova definicao: ")
            enviaMensagem(definicao, socket)

        msgServ = recebeMensagem(sock) #aguarda a confirmacao do serv
        print(msgServ)
        return
        
    elif entrada == "6":
        return
        
    else:
        print("\nDigite uma entradda valida!\n")
    
    

#--------------------- funcoes no servidor e no cliente ------------------

def enviaMensagem(input, socket):
    str_bytes = input.encode("ascii")
    tam = len(str_bytes)
    byt = tam.to_bytes(1, 'big')
    total = 0
    socket.send(byt) #envia tamanho da mensagem

    while total < tam:
        enviado = socket.send(str_bytes[total:]) #envia mensagem
        if enviado ==0:
            #retorna com erro
            return -1
            
        total = total+ enviado 
    return


def recebeMensagem(recebeSock):
    tamMsg = recebeSock.recv(1) #recebe tamanho da mensagem
    tam = int.from_bytes(tamMsg, 'big')
    recebidos = 0
    chunks = []
    while recebidos < tam:
        chunk = sock.recv(min(tam-recebidos, 2048))
        if not chunk:
            return -1
        chunks.append(chunk)
        recebidos = recebidos + len(chunk)
    y = str(b''.join(chunks), 'utf-8')
    return y



#----------------------------------------------------------------

HOST = 'localhost' # maquina onde esta o par passivo
PORTA = 5000        # porta que o par passivo esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o par passivo
sock.connect((HOST, PORTA)) 


    

        
print("\t\t\tBem vindo ao dicionario!")

print("\t\t\tEntre com sua conta!")

#---------------------- Login ------------------------

login = input('\n\t\t\tLogin: ')
senha = input('\t\t\tsenha: ')

enviaMensagem(login, sock)
enviaMensagem(senha, sock)

#--------------------------------------------

adm = recebeMensagem(sock) #guarda para saber se eh adm


msg = recebeMensagem(sock) #aguarda boas vindas
print(msg)


while True:

    menu = recebeMensagem(sock) #recebe menu

    print(menu)

    entrada = input("Digite um comando: ")
    
    if entrada == "6": #sair...
        break
        
    switchFunc(entrada,adm, sock)
    
    
    


# # encerra a conexao
sock.close()
