import os
import pickle
import rpyc
from interface import BrokerService, Content
from rpyc.utils.server import ThreadedServer


PORTA = 10001
BUFFERSIZE = 10


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
            print(DICTCONECTADOS)

#---------------------------------------------------------
    #Não sei chamar
    #Não sei nem se será relevante
    def create_topic(self, UserId, topicname):
        listaInscritos = []
        DICTTOPIC[topicname] = listaInscritos
#---------------------------------------------------------

    def exposed_login(self, id, callback):
        try:
            client_address = self.current_client_address
            DICTCONECTADOS[id] = client_address
            DICTIDCALLBACK[id] = rpyc.async_(callback)

            for topico in DICTTOPIC:
                if id in DICTTOPIC[topico]:
  
                    callback(DICTTOPIC[topico][id]) 
                    dictUser = DICTTOPIC[topico]
                    dictUser[id].clear() 
                    DICTTOPIC[topico] = dictUser

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
                    dictUser = DICTTOPIC[topico]
                    dictUser[user].append(novoPost)
                    DICTTOPIC[topico] = dictUser

            
            return True
        except Exception as error:
            print(error)
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
#---------------------------------------------------------

def main():

    global DICTCONECTADOS
    global DICTIDCALLBACK
    global DICTTOPIC 

    load(DICTTOPIC, 'DICTTOPIC')

    srv = ThreadedServer(BrokServ, port=PORTA, protocol_config={'allow_public_attrs':True})
    
 
    while True:
        os.system('clear')
        create_topic = input("Criar Topico? (s/n) ")
        if create_topic == 's':
            new_topic = input("Qual Topico? ")
            DICTTOPIC[new_topic] = dict()
        else:
            break

    

    os.system('clear')
    print("Comecando o Broker com os seguintes topicos:")
    for topico in DICTTOPIC: print(topico)
    
    try:
        srv.start()
    
    #Não consegui salvar o dict num keyboard interrupt
    except KeyboardInterrupt:
        save(DICTTOPIC, 'DICTTOPIC')
        srv.close()
    except Exception as error:
        print(error)
        srv.close()
        save(DICTTOPIC, 'DICTTOPIC')

if __name__ == "__main__":
    main()