#ativo

import rpyc

SERVIDOR = "localhost"
PORTA = "5000"

def iniciaConexao():
    conn = rpyc.connect(SERVIDOR, PORTA)
    print(type(conn.root))
    return conn


def switchcase(conn, entrada):
    if entrada == "1":
        ret = conn.root.exposed_listaPalavras()
        print(ret)
        return
    
    if entrada == "2":
        msg = "Digite a palavra a ser procurada: "
        envia = input(msg)
        ret = conn.root.exposed_printaChave(envia)
        print(ret)
        return
    
    if entrada == "3":
        X ="Digite a palavra a ser adicionada: "
        Y = "Digite uma definicao: "

        palavra = input(X)
        definicao = input(Y)
        ret = conn.root.exposed_adicionaChave(palavra, definicao)
        print (ret)
        return
    if entrada == "4":
        X = "Digite a palavra que deseja alterar a definicao: "
        Y = "Nova definicao: "
        palavra = input(X)
        definicao = input(Y)
        opcoes = conn.root.exposed_mostraDefinicoes(palavra)
        
        if opcoes == "0": 
            msg = "\nA palavra nao existe\n"
            return msg
        
        else:
            print(opcoes)
            id = input("Digite o id da definicao: ")
            ret = conn.root.exposed_alteraValorChave(palavra, id, definicao)
            print(ret)
            return

    if entrada == "5":
        X = "Digite a palavra que deseja adicionar uma definicao: "
        Y = "Digite o novo valor: "
        palavra = input(X)
        valor = input(Y)
        ret = conn.root.exposed_adicionaValor(palavra, valor)
        print(ret)
        return

    else:
        print("digite uma entrada valida")





def fazRequisicoes(conn):
    while True:
        msg = "\t\t\to que gostaria de fazer?\n\n\t\t\t1 - listar todas as palavras\n\t\t\t2 - Buscar uma palavra\n\t\t\t3 - Inserir uma palavra\n\t\t\t4 - Alterar uma definicao\n\t\t\t5 - Adicionar uma definicao\n\t\t\t6 - Sair\n"
        entrada = input(msg)        
        if entrada == "6":
            break
        switchcase(conn, entrada)
    conn.close()

def main():
    conn = iniciaConexao()
    fazRequisicoes(conn)

if __name__ == "__main__":
    main()
