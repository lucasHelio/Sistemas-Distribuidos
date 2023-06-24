import os
import pickle
from interface import BrokerService, Content
from rpyc.utils.server import ThreadedServer
from rpyc.utils.server import ForkingServer 
import multiprocessing

manager = multiprocessing.Manager()

PORTA = 10001
BUFFERSIZE = 10


LISTACONECTADOS = {}
LISTACONECTADOS = manager.dict()

"""LISTACONECTADOS
    key: id
    value: client_address
"""

LISTAIDCALLBACK = {}
LISTAIDCALLBACK = manager.dict()

"""LISTAIDCALLBACK
    key: id
    value: callback func
"""

LISTATOPICOS = {}
LISTATOPICOS = manager.dict()

"""LISTATOPICOS
    key: topico
    value: lista de objeto:
           objeto contem: id
                          lista de content
"""

class userListContent:
    def __init__(self, id):
        self.id = id
        self.listContent = []



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
            for key, val in LISTACONECTADOS.items():
                if val == client_address:
                    del LISTACONECTADOS[key]
                    print(LISTACONECTADOS)

#---------------------------------------------------------
    #Não sei chamar
    def create_topic(self, UserId, topicname):
        listaInscritos = []
        LISTATOPICOS[topicname] = listaInscritos
#---------------------------------------------------------

    def exposed_login(self, id, callback):
        try:
            client_address = self.current_client_address
            LISTACONECTADOS[id] = client_address
            print(LISTACONECTADOS)

            LISTAIDCALLBACK[id] = callback #, "client_address": client_address}
            print(LISTAIDCALLBACK)

            for topico in LISTATOPICOS:
                if topico.id == id:
                    if len(topico.listContent) > 0:
                        func = LISTAIDCALLBACK[topico.id]#["callback"]
                        func(topico.listContent) #Como fazer para o cliente rodar?
                        #topico.listContent.clear() #Ainda não limpar

            return True
        
        except:
            return False

    def exposed_list_topics(self):
        return LISTATOPICOS.keys()

    def exposed_publish(self, id, topico, info):
        try:
            novoPost = Content(author=id, topic=topico, data=info)
            for topico in LISTATOPICOS[topico]:
                topico.listContent.append(novoPost)
                if(topico.id in LISTAIDCALLBACK):
                    func = LISTAIDCALLBACK[topico.id]#["callback"]
                    func(topico.listContent) #Como fazer para o cliente rodar?
                    #topico.listContent.clear() #Ainda não limpar
            return True
        except: return False        

    def exposed_subscribe_to(self, id, topic):

        if topic in LISTATOPICOS:

            for obj in LISTATOPICOS[topic]:
                if id == obj.id: return False
            
            newUserSemContent = userListContent(id)

            LISTATOPICOS[topic].append(newUserSemContent)

            #for user in LISTATOPICOS[topic]:
                #print(user.id)
                #print(user.listContent)
                #print('a')
            
            #user = LISTATOPICOS[topic][0]

            #print(user.id)
            #print(user.listContent)

            return True
        
        return False

    def exposed_unsubscribe_to(self, id, topic):
        if topic in LISTATOPICOS:
            for obj in LISTATOPICOS[topic]:
                if id == obj.id: 
                    LISTATOPICOS[topic].remove(obj)
                    print(LISTATOPICOS)
                    return True
        return False



#---------------------------------------------------------   
def load(dictionary, nome):
    #Tentamos carregar o dicionario de um arquivo novo
    try: 
        with open(str(nome)+'.pickle', 'rb') as f: 
            loadDict = pickle.load(f)
            print("Dicionario carregado")
            dictionary.update(loadDict)

    #Caso nao exista um arquivo, iniciamos o dicionario
    except FileNotFoundError: 
        print("Dicionario novo criado")

def save(dictionary, nome):
	with open(str(nome)+'.pickle', 'wb') as f: 
		pickle.dump(dict(dictionary), f)
		print("Dicionario salvo")
	return
#---------------------------------------------------------

def main():

    global LISTACONECTADOS
    global LISTAIDCALLBACK
    global LISTATOPICOS 

    load(LISTATOPICOS, 'listaTopicos')

    srv = ForkingServer(BrokServ, port=PORTA)
    
 
    while True:
        os.system('clear')
        create_topic = input("Criar Topico? (s/n) ")
        if create_topic == 's':
            new_topic = input("Qual Topico? ")
            LISTATOPICOS[new_topic] = []
        else:
            break

    save(LISTATOPICOS, 'listaTopicos')

    os.system('clear')
    print("Comecando o Broker com os seguintes topicos:")
    for topico in LISTATOPICOS: print(topico)
    print('')
    srv.start()



main()