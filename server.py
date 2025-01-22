import socket
import threading

class AuctionServer:
    def __init__(self, host='192.168.87.169', port=65432):
        self.host = host
        self.port = port
        self.clients = []
        self.highest_bid = 0
        self.highest_bidder = None
        self.logical_clock = 0
        self.lock = threading.Lock()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        print(f"Servidor iniciado em {self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            self.clients.append(client_socket)
            print(f"Conexão estabelecida com {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

    def handle_client(self, client_socket, addr):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break

                client_bid, client_clock = data.split(',')
                client_bid = int(client_bid)
                client_clock = int(client_clock)

                with self.lock:
                    self.logical_clock = max(self.logical_clock, client_clock) + 1

                    # Verifica se o lance é maior que o lance atual
                    if client_bid > self.highest_bid:
                        self.highest_bid = client_bid
                        self.highest_bidder = addr
                        print(f"Novo maior lance: R${self.highest_bid} de {addr} | Relógio Lógico: {self.logical_clock}")
                        self.broadcast_update()
                    else:
                        client_socket.sendall("Lance rejeitado: valor menor ou igual ao atual.\n".encode())

            except ConnectionResetError:
                break

        client_socket.close()

    def broadcast_update(self):
        message = f"Novo maior lance: R${self.highest_bid} | Relógio Lógico: {self.logical_clock}\n"
        for client in self.clients:
            try:
                client.sendall(message.encode())
            except BrokenPipeError:
                self.clients.remove(client)


if __name__ == "__main__":
    server = AuctionServer()
    server.start_server()