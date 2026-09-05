import socket
import threading


HOST = '127.0.0.1' 
PORT = 5000


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(f"\n[Servidor] {message}")
        except:
            print("Ocorreu um erro!")
            client_socket.close()
            break

def run_client():
    # AF_INET usa IPv4 , SOCK_STREAM = protocolo TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT)) # Conecta ao servidor.
    nome = input("Digite seu nome: ").strip()
    receive_thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
    receive_thread.start()
    while True:
        message = input("")
        if message.lower() == 'sair':
            client.send(f"{nome}: sair".encode('utf-8'))
            break
        client.send(f"{nome}: {message}".encode('utf-8'))
    client.close()


if __name__ == "__main__":
    run_client()