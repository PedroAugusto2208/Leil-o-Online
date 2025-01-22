# Leilão Online

Este projeto consiste em um sistema de leilão online baseado em uma arquitetura cliente-servidor, utilizando Python e sockets para a comunicação entre os participantes.

## Tecnologias Utilizadas
- Python
- Sockets (para comunicação cliente-servidor)
- Threads (para gerenciar múltiplos clientes simultaneamente)
- Tkinter (para interface gráfica do cliente)

## Estrutura do Projeto

O projeto é composto por dois arquivos principais:
- `server.py`: Responsável por gerenciar os lances e manter a conexão com os clientes.
- `client.py`: Interface gráfica que permite aos usuários se conectarem ao servidor e realizarem lances.

## Como Executar

### 1. Executar o Servidor
Antes de iniciar os clientes, é necessário rodar o servidor.
```sh
python server.py
```
O servidor iniciará e ficará aguardando conexões dos clientes.

### 2. Executar o Cliente
Para conectar-se ao servidor e fazer lances, execute o cliente:
```sh
python client.py
```

## Funcionalidades
### Servidor (`server.py`)
- Aceita conexões de múltiplos clientes.
- Mantém o maior lance e rejeita lances inferiores ao atual.
- Utiliza um Relógio Lógico para sincronizar eventos.
- Informa todos os clientes quando um novo maior lance é registrado.

### Cliente (`client.py`)
- Interface gráfica (GUI) para interação do usuário.
- Conecta-se ao servidor e exibe o status do leilão.
- Permite ao usuário inserir e enviar lances.
- Exibe histórico de lances e mensagens do servidor.

## Melhorias Futuras
- Implementar autenticação de usuários.
- Adicionar suporte para diferentes itens no leilão.
- Melhorar o tratamento de erros e reconexão automática.

## Autor
Projeto desenvolvido para aprendizado de comunicação em rede e sistemas distribuídos.

## Contexto Acadêmico
Este projeto foi desenvolvido como trabalho de final de semestre da faculdade para a matéria de **Sistemas Distribuídos e de Tempo Real**.
