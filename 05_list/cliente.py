import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 5000

def comprar_passagem(numero_cliente):
    nome_cliente = f"cliente{numero_cliente}"
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        client.send(f"COMPRAR|{nome_cliente}".encode())

        resposta_entrada = client.makefile("r", encoding="utf-8")
        mensagem = resposta_entrada.readline().strip()
        if mensagem.startswith("CHEIO|"):
            print(f"[{nome_cliente}] Servidor cheio; aguardando liberar uma vaga...")
            mensagem = resposta_entrada.readline().strip()

        if mensagem.startswith("ENTROU|"):
            print(f"[{nome_cliente}] Entrou no sistema: {mensagem.split('|', 1)[1]}")

        # Recebe resposta
        resposta = resposta_entrada.readline().strip()
        
        if "SUCESSO" in resposta:
            print(f"[{nome_cliente}] Compra finalizada com sucesso: passagem comprada!")
        else:
            print(f"[{nome_cliente}] Compra negada: voo lotado.")
        
        client.close()
        print(f"[{nome_cliente}] Saiu do sistema.")
    except Exception as e:
        print(f"[{nome_cliente}] Erro: {e}")

# Cria 10 clientes concorrentes
threads = []
for i in range(1, 11):
    t = threading.Thread(target=comprar_passagem, args=(i,))
    threads.append(t)
    t.start()
    time.sleep(0.1)

for t in threads:
    t.join()

print("\n[CLIENTE] Todas as compras finalizadas!")