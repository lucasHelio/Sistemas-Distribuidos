#ativo

import socket

Dicionario = []

class Palavra:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valores = valor


def arquivoEscrita():
    Arquivo = open("teste.txt","w")
    for x in Dicionario:
        Arquivo.write(str(x.chave))
        for y in x.valores:
            Arquivo.write("*"+ str(y))
        Arquivo.write("\n")
            
    Arquivo.close()
    return

def arquivoLeitura():
    Arquivo = open("teste.txt", "r")

    x = Arquivo.read().splitlines()
    for a in x:
        i = a.split('*')
        adicionaChave(i[0], i[1:])
    Arquivo.close()
    return


def switchFunc(entrada, adm):
    str_bytes = entrada.encode("ascii")
    sock.send(str_bytes)
    if entrada == "0" and adm =="1":
        msgServ = sock.recv(1024) #aguarda a prox instrucao
        x= input(str(msgServ,  encoding='utf-8'))
        str_bytes = x.encode("ascii")
        sock.send(str_bytes)
        msgServ = sock.recv(1024) #aguarda saber se a chave foi removida
        print(str(msgServ,  encoding='utf-8'))
        return
    elif entrada == "1":
        print("\n")
        msg = sock.recv(1024)
        x = msg.decode()
        y = x.split("*")
        for palavra in y:
            print(palavra)

        sock.send(b"msg chegou")
        print("\n")  
        return
        
    elif entrada == "2":
        msgServ = sock.recv(1024) #aguarda a prox instrucao
        x= input(str(msgServ,  encoding='utf-8'))
        str_bytes = x.encode("ascii")
        sock.send(str_bytes)

        msg = sock.recv(1024)
        print(str(msg, "utf-8"))
        print("\n")
        
        return
    
    elif entrada == "3":
        msgServ = sock.recv(1024) #aguarda a prox instrucao
        x= input(str(msgServ, 'utf-8'))
        str_bytes = x.encode("ascii")
        sock.send(str_bytes)

        msgServ = sock.recv(1024) #aguarda a prox instrucao
        x= input(str(msgServ, 'utf-8'))
        str_bytes = x.encode("ascii")
        sock.send(str_bytes)

        msgServ = sock.recv(1024) #aguarda o retorno da funcao
        print(str(msgServ, 'utf-8'))
        return
    elif entrada == "4":
        msgServ = sock.recv(1024) #aguarda a prox instrucao
        x= input(str(msgServ, 'utf-8'))#chave
        str_bytes = x.encode("ascii")
        sock.send(str_bytes)#envia chave

        msg = sock.recv(1024)
        x = (str(msg))
        if x == "1":

            msg = sock.recv(1024)   #recebe definicoes
            x = msg.decode()
            y = x.split("*")
            for palavra in y:
                print(palavra)

            #sock.send(b'mensagem recebida')
            print("\n")

            msgServ = sock.recv(1024) #aguarda a instrucao de escolher a definicao
            #t= input(str(msgServ, 'utf-8'))
            t= input(str(msgServ))
            print("passei pelo input")
            str_bytes = x.encode("ascii")
            sock.send(str_bytes)

        msgServ = sock.recv(1024) #aguarda a prox instrucao
        print(str(msgServ, 'utf-8'))
        return
    elif entrada == "5":
        msgServ = sock.recv(1024) #aguarda a prox instrucao
        x= input(str(msgServ, 'utf-8'))
        str_bytes = x.encode("ascii")
        sock.send(str_bytes)

        msg = sock.recv(1024)
        x = (str(msg, "utf-8"))
        if x == "1":
            msgServ = sock.recv(1024) #aguarda a prox instrucao
            x= input(str(msgServ, 'utf-8'))
            str_bytes = x.encode("ascii")
            sock.send(str_bytes)

        msgServ = sock.recv(1024) #aguarda a confirmacao do serv
        print(str(msgServ, 'utf-8'))
        return
    elif entrada == "6":
        arquivoLeitura()
        print("Arquivo restaurado")
        return
        
    elif entrada == "7":
        arquivoEscrita()
        #global prog
        #prog = 0
        return
        
    else:
        print("\nDigite uma entradda valida!\n")
    
    

#--------------------- funcoes no servidor e no cliente ------------------
def adicionaChave(chave, valor):
    if not encontraChave(chave):
        Dicionario.append(Palavra(chave, valor))   
        print("\nPalavra adicionada com sucesso!\n")
        return
    else:
        print("\nA palavra ja existe\n")
        return

def encontraChave(chave):
    for x in Dicionario:
        if chave == x.chave:
            return x
    return 0
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
str_bytes1 = login.encode("ascii")
str_bytes2 = senha.encode("ascii")

sock.send(str_bytes1)
sock.send(str_bytes2)

#--------------------------------------------

msg = sock.recv(1024) #guarda para saber se eh adm
adm =(str(msg, 'utf-8'))


msg = sock.recv(1024) #aguarda boas vindas
print(str(msg,  encoding='utf-8'))


while True:

    msg = sock.recv(1024) #recebe uma main
    print(str(msg,  encoding='utf-8'))

    entrada = input("Digite um comando: ")
    
    
    if entrada == "7": #sair...
        sock.close()
        break
        
    switchFunc(entrada,adm)
    


# # encerra a conexao
sock.close()
