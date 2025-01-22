import socket
import threading
import tkinter as tk
from tkinter import messagebox

class AuctionClientGUI:
    def __init__(self, host='192.168.87.169', port=65432):
        self.host = host
        self.port = port
        self.logical_clock = 0
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Configuração da interface gráfica
        self.window = tk.Tk()
        self.window.title("Leilão Online")
        self.window.geometry("400x500")

        # Exibição do status do leilão
        self.status_label = tk.Label(self.window, text="Bem-vindo ao Leilão Online!", font=("Arial", 14), fg="blue")
        self.status_label.pack(pady=10)

        # Campo para exibir o maior lance
        self.highest_bid_label = tk.Label(self.window, text="Lance Atual: R$0", font=("Arial", 16), fg="green")
        self.highest_bid_label.pack(pady=20)

        # Caixa de texto para exibir as atualizações
        self.log_box = tk.Text(self.window, width=50, height=15, state="disabled", font=("Arial", 12))
        self.log_box.pack(pady=10)

        # Campo para inserir o lance
        self.bid_entry = tk.Entry(self.window, font=("Arial", 14))
        self.bid_entry.pack(pady=10)

        # Botão para enviar o lance
        self.bid_button = tk.Button(self.window, text="Enviar Lance", font=("Arial", 14), command=self.send_bid)
        self.bid_button.pack(pady=10)

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.status_label.config(text="Conectado ao servidor!", fg="green")
            threading.Thread(target=self.receive_updates, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor: {e}")
            self.window.destroy()

    def send_bid(self):
        bid = self.bid_entry.get()
        if not bid.isdigit():
            messagebox.showwarning("Aviso", "Por favor, insira um valor numérico válido!")
            return

        bid = int(bid)
        self.logical_clock += 1
        message = f"{bid},{self.logical_clock}"
        try:
            self.client_socket.sendall(message.encode())
            self.log_message(f"Você tentou enviar um lance: R${bid}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao enviar o lance: {e}")

        self.bid_entry.delete(0, tk.END)

    def receive_updates(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if "Lance rejeitado" in data:
                    self.log_message(data.strip(), "red")
                else:
                    self.update_highest_bid(data)
            except ConnectionResetError:
                self.log_message("Conexão com o servidor perdida.", "red")
                break

    def update_highest_bid(self, message):
        self.log_message(message, "blue")
        lines = message.split("\n")
        for line in lines:
            if line.startswith("Novo maior lance"):
                bid_info = line.split(": R$")
                if len(bid_info) > 1:
                    self.highest_bid_label.config(text=f"Lance Atual: R${bid_info[1]}")

    def log_message(self, message, color="black"):
        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.tag_add("color", "end-1c linestart", "end-1c")
        self.log_box.tag_config("color", foreground=color)
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")

    def run(self):
        self.connect_to_server()
        self.window.mainloop()

if __name__ == "__main__":
    client = AuctionClientGUI()
    client.run()