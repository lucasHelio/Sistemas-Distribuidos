from interface import BrokerService, Content
from rpyc.utils.server import ThreadedServer
#import pickle


PORTA = 10001

LISTAID = []
LISTATOPICOS = []
BUFFERSIZE = 10

"""
dicionario
-chave = topico
-valor = inscrito

{topico1: eu, lucas, di,
 topico2: lucas
 topico3: 
 topicox: []}

listavazia = []
LISTATOPICOS[topix] = listavazia

LISTATOPICOS[topix].append(inscrotp)

LISTATOPICOS[topix].remove(inscrito)


topico1:
    obj1:
        id: usuario
        --address: client_address
        --func: callback
        listContent: Jogo
                     Autor
                     novo champ

                     Esporte
                     Autor 2
                     Time venceu

                     [max = 10]
    
    obj2:
        id: j
        address: client_address2
        func: callback


{topico1: obj1, obj2, obj3,
 topico2: obj5,
 topico3: 
 topicox: []}



"""

class userFunc:
    def __init__(self, id):
        self.id = id
        #self.func = callback
        self.listContent = []


def escreveArquivo(Lista, arquivo):
    f1 = open(str(arquivo) +".txt", "w")
    f1.write(Lista)
    f1.close()
    return

def lerArquivo(Lista, arquivo):
    f1 = open(arquivo+"txt", "r")
    Lista = f1.read()
    f1.close()
    return Lista

def create_post(id, topic, data):
    novoPost = Content()
    novoPost.author = id
    novoPost.topic = topic
    novoPost.data = data
    return novoPost


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
            client_id = None
            for id, values in LISTAID.items():
                if values["client_address"] == client_address:
                    client_id = id
                    break
            if client_id is not None:
                del LISTAID[client_id]


    def create_topic(self, UserId, topicname):
        listaInscritos = []
        LISTATOPICOS[topicname] = listaInscritos

    def exposed_login(self, id, callback):
        """if id in LISTAID:
            client_address = self.current_client_address
            LISTAID[id] = {"callback": callback, "client_address": client_address}
            return True"""
        try:
            client_address = self.current_client_address
            LISTAID[id] = {"callback": callback, "client_address": client_address}
            #chamar o FnNotify tambem
            for topico in LISTATOPICOS:
                if topico.id == id:
                    if len(topico.listContent) > 0:
                        func = LISTAID[topico.id]["callback"]
                        func(topico.listContent) #Como fazer para o cliente rodar?
                        topico.listContent.clear()
            return True
        
        except:
            return False


    def exposed_list_topics(self):
        return LISTATOPICOS.keys()


    def exposed_publish(self, id, topic, data):
        novoPost = create_post(id, topic, data)
        for topico in LISTATOPICOS[topic]:
            topico.listContent.append(novoPost)
            if(topico.id in LISTAID):
                func = LISTAID[topico.id]["callback"]
                func(topico.listContent) #Como fazer para o cliente rodar?
                topico.listContent.clear()
                
        #pensar em como saber se o usuario recebeu o callback ou não
        #Agora buscar todos os inscritos e
        #chamar FnNotify para cada um inscrito com novoPost
        #pass

    def exposed_subscribe_to(self, id, topic):
        if topic in LISTATOPICOS:
            for x in LISTATOPICOS[topic]:
                if id == x.id: return False
            
            novoUser = userFunc(id)
            LISTATOPICOS[topic].append(novoUser)
            return True
        return False

    def exposed_unsubscribe_to(self, id, topic):
        if topic in LISTATOPICOS:
            for x in LISTATOPICOS[topic]:
                if id == x.id: 
                    LISTATOPICOS[topic].remove(x)
                    return True
        return False
        

def main():

    global LISTATOPICOS 
    global LISTAID

    
    srv = ThreadedServer(BrokServ, port=PORTA)
    lerArquivo(LISTATOPICOS, "Topicos")
    lerArquivo(LISTATOPICOS, "Id")
    
    srv.start()

    escreveArquivo(LISTATOPICOS, "Topicos")
    escreveArquivo(LISTAID, "Id")
    

main()