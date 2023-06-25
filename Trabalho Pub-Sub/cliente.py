import rpyc
from interface import Content

#endereco do servidor
SERVER = 'localhost'
PORTA = 10001
user = ''

def printLC(listOfContent):
    for content in listOfContent:
        print()
        print("Autor:  " + content.author)
        print("Topico: " + content.topic)
        print(content.data)
        print()
    return None


def realizarLogin():
    user = str(input("Insira seu user: "))
    isLogged = conn.root.login(user, printLC)
    if(isLogged):
        return user
    else:
        return ''

def fazRequisicoes(conn):
    global user
    user = realizarLogin()
    if(user == ''):
        print("Usuario nao autorizado.")
        return
    while True:
        print()
        print("Opcoes:")
        print("0 - Sair")
        print("1 - Listar topicos")
        print("2 - Publicar em topico")
        print("3 - Inscrever em um topico")
        print("4 - Desinscrever em um topico")
        
        opcao = str(input("Selecione a opcao: "))
        print()
        
        if opcao == "0": break
        
        if opcao == '1':
            listaTopicos = conn.root.list_topics()
            print("Os Topicos são:")
            for topico in listaTopicos: print(topico)
            
        
        elif opcao == '2':
            topico = str(input("Topico da publicacao: "))
            data = str(input("Insira o conteudo do topico:"))
            if(conn.root.publish(user, topico, data)):
                print("Publicado")
            else:
                print("Erro ao publicar")
        
        elif opcao == '3':
            topico = str(input("Inscrever-se no topico: "))
            if (conn.root.subscribe_to(user, topico)): print("Inscricao Concluida")
            else: print("Nao foi possivel realizar a inscricao")
        
        elif opcao == '4':
            topico = str(input("Deseja se desinscrever de qual topico? "))
            if(conn.root.unsubscribe_to(user, topico)):
                print("Desinscrito do topico " + topico+" com sucesso!")
            else:
                print("Nao foi possivel desincrever-se do topico "+topico+
                ". Ou voce nao estava inscrito nele, ou o topico nao existe.")
        

        else:
            print("Opcao nao Reconhecida")


def iniciaConexao():
    conn = rpyc.connect(SERVER, PORTA)
    return conn

def main():
    
    global conn
    global bgsrv
    conn = iniciaConexao()
    bgsrv = rpyc.BgServingThread(conn)
    fazRequisicoes(conn)
    bgsrv.stop()
    conn.close()
    

if __name__ == '__main__':
    main()
