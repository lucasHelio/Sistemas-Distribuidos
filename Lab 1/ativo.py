# Exemplo basico socket (lado ativo)

import socket

HOST = '192.168.15.7' # maquina onde esta o par passivo
PORTA = 5000        # porta que o par passivo esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o par passivo
sock.connect((HOST, PORTA)) 



while True:
    entrada = input("Digite uma mensagem: ")
    
    str_bytes = entrada.encode("ascii")

    if (entrada == 'fim'):
        print("Sessao finalizada")
        break

    # envia uma mensagem para o par conectado
    sock.send(str_bytes)

    

    #espera a resposta do par conectado (chamada pode ser BLOQUEANTE)
    msg = sock.recv(1024) # argumento indica a qtde maxima de bytes da mensagem


    # imprime a mensagem recebida
    print(str(msg,  encoding='utf-8'))

# # encerra a conexao
sock.close() 
