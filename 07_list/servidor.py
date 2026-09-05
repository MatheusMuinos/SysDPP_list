import socket
import threading


HOST = '0.0.0.0'
PORT = 5000



def handle_client(conn, addr):
	print(f"[NOVA CONEXÃO] {addr} conectado.")
	conn.send("Bem-vindo ao chat!".encode('utf-8'))
	while True:
		try:
			message = conn.recv(1024).decode('utf-8')
			if not message:
				break
			print(f"[{addr}] {message}")
			with open("chat.log", "a", encoding="utf-8") as log_file:
				log_file.write(message + "\n")
			# Envia dados para o cliente.
			conn.send(f"Servidor recebeu: {message}".encode('utf-8'))
		except:
			break
	print(f"[DESCONEXÃO] {addr} desconectado.")
	conn.close() # Fecha a conexão.



def run_server():
    # AF_INET usa IPv4 , SOCK_STREAM = protocolo TCP
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((HOST, PORT)) # Associa o socket a um endereço e porta.
	server.listen()
	print(f"Servidor escutando em: {HOST} na porta: {PORT}") # modo de escuta.
	while True:
		conn, addr = server.accept() # conexao e endereço do cliente
		thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
		thread.start()
		print(f"[CONEXÕES ATIVAS] {threading.active_count() - 1}")


if __name__ == "__main__":
	run_server()