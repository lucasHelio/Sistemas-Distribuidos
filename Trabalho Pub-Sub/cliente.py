import rpyc

#endereco do servidor
SERVER = 'localhost'
PORTA = 10001

broker = rpyc.connect(SERVER, PORTA)

def FnNotify():
    pass


def realizarLogin():
    user = str(input("Insira seu user: "))
    isLogged = broker.root.login(user)
    if(isLogged):
        return user
    else:
        return ""

def fazRequisicoes(conn):
    user = realizarLogin()
    if(user == ""):
        print("Usuario nao autorizado.")
        return
    while True:
        print("Opcoes:")
        print("\t0 - Sair")
        print("\t1 - Listar topicos")
        print("\t2 - Publicar em topico")
        print("\t3 - Inscrever em um topico")
        opcao = str(input("Selecione a opcao: "))
        
        if opcao == "0": break
        
        if opcao == '1':
            broker.root.list_topics()
        
        elif opcao == '2':
            topico = str(input("Topico da publicacao: "))
            data = str(input("Insira o conteudo do topico:"))
            if(broker.root.publish(user, topico, data)):
                print("Publicado")
            else:
                print("Erro ao publicar")
        
        elif opcao == '3':
            topico = str(input("Inscrever-se no topico: "))
            if (broker.root.subscribe_to(user, topico, FnNotify)): print("Inscricao Concluida")
            else: print("Nao foi possivel realizar a inscricao")
            #callback
            #broker.root.subscribe_to(user, topico, callback)
        
        elif opcao == '4':
            topico = str(input("Deseja se desinscrever de qual topico? "))
            if(broker.root.unsubscribe_to(user, topico)):
                print("Desinscrito do topico " + topico+" com sucesso!")
            else:
                print("Nao foi possivel desincrever-se do topico "+topico+
                ". Ou voce nao estava inscrito nele, ou o topico nao existe.")
        else:
            print("Opcao nao Reconhecida")

def iniciaConexao():
    conn = rpyc.connect(SERVER, PORTA)
    print(conn.root.get_service_name())
    return conn

def main():
    conn = iniciaConexao()
    fazRequisicoes(conn)
    conn.close()

if __name__ == '__main__':
    main()