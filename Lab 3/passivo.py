#passivo

import rpyc


# define a localizacao do servidor

PORT = 5000 # porta de acesso

from rpyc.utils.server import ForkingServer

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
    Arquivo = open("dicionario.txt", "r+")

    x = Arquivo.read().splitlines()
    for a in x:
        i = a.split('*')
        adicionaChaveServidor(i[0], i[1:])
    Arquivo.close()
    return

Dicionario = []

class Palavra:
    def __init__(self, chave, valor):
        self.chave = chave
        self.valores = [valor]




def encontraChave(chave):
        for x in Dicionario:
            if chave == x.chave:
                return x
        return 0



class Echo(rpyc.Service):
    def on_connect(self, conn):
        print("Conexao iniciada: ")
    
    def on_disconnect(sel, conn):
        print("Conexão finalizada")
    
    def exposed_listaPalavras(self):
        palavras = " "
        for x in Dicionario:
            palavras = palavras +"\n"+ x.chave
        return palavras
    
    def exposed_printaChave(self, chave):
        for x in Dicionario:
            if chave == x.chave:
                y = ("\nPalavra: "+ x.chave+ "\t\tDefinicao: ")
                for d in x.valores:
                    y = y +d
                y= y+"\n"
                return y
        msg = "\npalavra nao encontrada\n"
        return msg
    
    def exposed_adicionaChave(self, chave, valor):
        if not encontraChave(chave):
            Dicionario.append(Palavra(chave, valor+"; "))   
            msg = "\nPalavra adicionada com sucesso!\n"
        else:
            msg = "\nA palavra ja existe\n"
        return msg
    
    def exposed_mostraDefinicoes(self, chave):
        Obj = encontraChave(chave)
        if Obj:
            y=''
            for x in Obj.valores:
                y = y + str(Obj.valores.index(x))+ " - "+x+"\n"
            return y #temos que retornar a msg
        return 0

    def exposed_alteraValorChave(self, chave, idOldDef, novaDefinicao):
        Obj = encontraChave(chave)
        if Obj:
            #y=''
            #for x in Obj.valores:
            #    y = y + str(Obj.valores.index(x))+ " - "+x+"*"
            valorN = idOldDef
            if Obj.valores[int(valorN)] != "":
                Obj.valores.pop(int(valorN))
                Obj.valores.insert(int(valorN), novaDefinicao+"; ")
                msg = "\nA definicao foi alterada\n"
            else:
                msg = "\nDefinicao escolhida nao existe\n"
        else:
            msg = "\nA palavra nao foi encontrada\n" 
        return msg
    
    def exposed_adicionaValor(self, chave, valor):
        Obj = encontraChave(chave)
        if Obj:
            novoValor = valor
            Obj.valores.append(novoValor + "; ")
            msg = "\nO valor foi adicionado com sucesso!\n"    
        else:
            msg = "\nA palavra nao foi encontrada\n"
        return msg
    


if __name__ == "__main__":
    srv = ForkingServer(Echo, port = PORT)
    srv.start()
