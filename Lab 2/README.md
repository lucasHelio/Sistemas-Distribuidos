# Laboratório 2 - Dicionario distribuído


## Arquitetura
Esse projeto foi construído com a ideia de base em camadas, onde o usuário faria todas suas requisições ao servidor. Sendo assim, o servidor teria o trabalho de processar as informações e ceder o banco de dados ao mesmo tempo.

## componentes

## camada de interface do usuário:

O Client era encarregado de fazer a conversão de mensagens entre o servidor e usuário, tendo métodos de interação para exibir as funções e respostas do servidor. 

## camada de processamento:
Se encontra no servidor e faz todo o processamento desde encontrar as palavras até manipular suas definições.

## camada de dados: Armazena as informações do dicionário e se encontra no servidor, sendo invocada pela camada de processamento para execução das funções requeridas.


## troca de mensagens
a troca de mensagens entre servidor e clientes é feita de forma concorrente, sendo assim, o servidor guarda o socket do cliente e segue seu fluxo interativo com aquele usuário até sua desconexão.

As chamadas são de certa forma "bloqueantes" pois quando um lado envia uma mensagem o outro espera para seguir a execução. Entretanto,  no momento que o servidor está esperando uma resposta de um cliente ele pode interagir com outros que o solicitarem.