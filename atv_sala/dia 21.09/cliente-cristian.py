# Resposta da atividade:
# Este cliente conecta ao servidor, mede o tempo de ida e volta (RTT) e usa o algoritmo de Cristian para estimar o tempo correto.
# A fórmula aplicada é: tempo_estimado = server_time + RTT/2 e offset_estimado = tempo_estimado - time.time().
# Assim, o cliente pode ajustar seu relógio local em relação ao servidor sem modificar o relógio do sistema operacional.

import json
import socket
import time

client = socket.socket()
client.connect(("127.0.0.1", 5000))

inicio_rtt = time.perf_counter()
client.sendall(b"TIME")
resposta = json.loads(client.recv(1024).decode())
rtt = time.perf_counter() - inicio_rtt

tempo_estimado = resposta["server_time"] + rtt / 2
offset_estimado = tempo_estimado - time.time()

print("RTT:", rtt)
print("Tempo estimado:", tempo_estimado)
print("Offset estimado:", offset_estimado)

# O exemplo não altera o relógio do sistema operacional.
client.close()