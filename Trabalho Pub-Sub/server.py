import os
import pickle
import sys
import rpyc
from interface import BrokerService, Content
from rpyc.utils.server import ThreadedServer
import atexit
from threading import Thread


PORTA = 10001
BUFFERSIZE = 10


class Usuario:
    def __init__(self, nome):
        self.nome = nome
        self.posts = []
    

def adicionaPost(listaPost, post):
    if len(listaPost) <10:
        listaPost.append(post)
    else:
        listaPost.pop(0)
        listaPost.append(post)
    return 

def removePrimeiroPost(listaPost):
    listaPost.pop(0)
    return



DICTUSERTOP = []
'''DICTUSERTOP
    Usuario user:
'''

DICTCONECTADOS = {}

"""DICTCONECTADOS
    key: id
    value: client_address
"""

DICTIDCALLBACK = {}

"""DICTIDCALLBACK
    key: id
    value: callback func
"""

DICTTOPIC = {}

"""DICTTOPIC
    key: topico
    value: lista de dict:
                        key: id
                        value: listContent
"""


class BrokServ(BrokerService):

    def __init__(self):
        self.client_addresses = {}
        self.current_client_address = None

    def on_connect(self, conn):
        client_address = conn._channel.stream.sock.getpeername()
        self.client_addresses[conn] = client_address
        self.current_client_address = client_address
        print("Conexao iniciada:  ", client_address[0] + ":" + str(client_address[1]))

    def on_disconnect(self, conn):
        client_address = self.client_addresses.pop(conn, None)
        if client_address is not None:
            print("Conexao finalizada:", client_address[0] + ":" + str(client_address[1]))
            for key, val in DICTCONECTADOS.items():
                if val == client_address:
                    user = key
            del DICTCONECTADOS[user]

#---------------------------------------------------------
    def create_topic(self, UserId, topicname):
        listaInscritos = []
        DICTTOPIC[topicname] = listaInscritos
#---------------------------------------------------------

    def exposed_login(self, id, callback):
        try:
            client_address = self.current_client_address
            DICTCONECTADOS[id] = client_address
            DICTIDCALLBACK[id] = rpyc.async_(callback)
            for usuario in DICTUSERTOP:
                if id == usuario.nome:
                    listatemporaria = []
                    while len(usuario.posts)!= 0:
                        listatemporaria.append(usuario.posts[0])
                        removePrimeiroPost(usuario.posts)
                    callback(listatemporaria)
                return True
            
            novoUsuario = Usuario(id)
            DICTUSERTOP.append(novoUsuario)
            return True
        
        except Exception as error:
            print(error)
            return False


    def exposed_list_topics(self):
        return DICTTOPIC.keys()

    def exposed_publish(self, id, topico, info):
        try:
            novoPost = Content(author=id, topic=topico, data=info)

            for user in DICTTOPIC[topico]:
                if(user in DICTCONECTADOS):
                    func = DICTIDCALLBACK[user]
                    func([novoPost])
                else:     
                    for usuario in DICTUSERTOP:
                        if usuario.nome == user:
                            adicionaPost(usuario.posts, novoPost)

                    dictUser = DICTTOPIC[topico]
                    dictUser[user].append(novoPost)
                    DICTTOPIC[topico] = dictUser
            return True
        
        except Exception as error:
            print("ERRO - Tópico "+ error+" inserido não existe")
            return False        



    def exposed_subscribe_to(self, id, topic):

        if topic in DICTTOPIC:

            for userContent in DICTTOPIC[topic]:
                if id == userContent: return False

            dictUser = DICTTOPIC[topic]
            dictUser.update({id:[]})
            DICTTOPIC[topic] = dictUser


            return True
        
        return False

    def exposed_unsubscribe_to(self, id, topic):
        try:
            if topic in DICTTOPIC:
                dictUser = DICTTOPIC[topic]
                del dictUser[id]
                DICTTOPIC[topic] = dictUser
    
                return True
        except KeyError:
            print('Algo deu errado')
        return False



#---------------------------------------------------------   
def load(dictionary, nome):
    try: 
        with open(str(nome)+'.pickle', 'rb') as f: 
            loadDict = pickle.load(f)
            print("Dicionario carregado")
            dictionary.update(loadDict)
    except FileNotFoundError: 
        print("Dicionario novo criado")

def save(dictionary, nome):
	with open(str(nome)+'.pickle', 'wb') as f: 
		pickle.dump(dict(dictionary), f)
		print("Dicionario salvo")
	return

def save_on_exit():
    save(DICTTOPIC, 'DICTTOPIC')
#---------------------------------------------------------

def selecionar_opcao(srv):
    while True:
        print("")
        print("OPCOES:")
        print("1 - Listar Topicos")
        print("2 - Criar Topico")
        print("3 - Deletar Topico")
        print("\'fim\' - Desliga servidor")
        selecionado = input("Selecionar opcao: ")
        if selecionado == '1':
            listaTopicos = DICTTOPIC.keys()
            print("╔═════════════╗")
            print("║   TOPICOS   ║")
            print("╚═════════════╝")
            for topico in listaTopicos: print("║ "+topico)
        if selecionado == '2':
            new_topic = input("Qual o Topico a ser criado? ")
            DICTTOPIC[new_topic] = dict()
        if selecionado == '3':
            delete_topic = input("Qual o Tópico a ser deletado? ")
            if delete_topic in DICTTOPIC:
                del DICTTOPIC[delete_topic]
                print("Tópico", delete_topic, "foi deletado.")
            else:
                print("O Tópico", delete_topic, "não existe.")
        if selecionado == 'fim':
            print("Interrompendo servidor...")
            srv.close()
            break

def main():

    global DICTCONECTADOS
    global DICTIDCALLBACK
    global DICTTOPIC 

    load(DICTTOPIC, 'DICTTOPIC')

    srv = ThreadedServer(BrokServ, port=PORTA, protocol_config={'allow_public_attrs':True})
    
    print("Comecando o Broker...")
    print("╔═════════════╗")
    print("║   TOPICOS   ║")
    print("╚═════════════╝")
    for topico in DICTTOPIC: print("║ "+topico)

    selecionar_opcao_thread = Thread(target=selecionar_opcao, args=(srv,))
    selecionar_opcao_thread.daemon = True
    selecionar_opcao_thread.start()

    atexit.register(save_on_exit)
    
    try:
        srv.start()
    except KeyboardInterrupt:
        save_on_exit()
        sys.exit(0)
    except Exception as error:
        srv.close()
        save_on_exit()

if __name__ == "__main__":
    main()
