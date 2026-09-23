# Resposta da atividade:
# Este servidor recebe uma requisição do cliente e responde com o tempo atual do relógio do servidor.
# O valor retornado é obtido com time.time(), que representa o instante atual em segundos desde a época Unix.
# Esse timestamp é usado pelo cliente para estimar o deslocamento do relógio e calcular o RTT.

import json
import socket
import time

HOST, PORT = "0.0.0.0", 5000

server = socket.socket()
server.bind((HOST, PORT))
server.listen()

while True:
    conn, addr = server.accept()
    with conn:
        conn.recv(1024)  # solicitação
        resposta = {"server_time": time.time()}
        conn.sendall(json.dumps(resposta).encode())