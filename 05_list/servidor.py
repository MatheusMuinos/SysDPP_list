import socket
import threading
import time

HOST = "0.0.0.0"
PORT = 5000

# somente três passagens disponíveis nesta simulação.
assentos = 3
sem = threading.Semaphore(3)  # No máximo 3 clientes simultâneos
lock = threading.Lock()  # Protege acesso a assentos
condicao = threading.Condition(lock)
clientes_ativos = 0
fila_espera = []
proximo_numero = 0

def atender_cliente(conn, addr):
    global assentos, clientes_ativos, proximo_numero
    nome_cliente = str(addr)
    entrou = False
    numero_fila = None
    try:
        requisicao = conn.recv(1024).decode().strip()
        if "|" in requisicao:
            _, nome_cliente = requisicao.split("|", 1)

        with condicao:
            proximo_numero += 1
            numero_fila = proximo_numero
            fila_espera.append(numero_fila)

            if clientes_ativos >= 3 or fila_espera[0] != numero_fila:
                print(f"[SISTEMA CHEIO] {nome_cliente} aguardando uma vaga")
                conn.sendall(b"CHEIO|Aguardando liberar uma vaga...\n")

            while clientes_ativos >= 3 or fila_espera[0] != numero_fila:
                condicao.wait()

            fila_espera.pop(0)
            clientes_ativos += 1
            entrou = True
            print(f"[ENTRADA] {nome_cliente} entrou no sistema ({addr})")
            conn.sendall(b"ENTROU|Compra em andamento...\n")

        with sem:
            time.sleep(1)  # Simula processamento

            with lock:
                if assentos > 0:
                    assentos -= 1
                    msg = f"SUCESSO: Passagem comprada! Assentos restantes: {assentos}\n"
                    print(f"[COMPRA OK] {nome_cliente} finalizou a compra - Assentos: {assentos}")
                else:
                    msg = "ERRO: Voo lotado! Nenhum assento disponível.\n"
                    print(f"[VOO LOTADO] {nome_cliente} finalizou sem passagem")

            conn.send(msg.encode())
            print(f"[SAÍDA] {nome_cliente} saiu do sistema")
    finally:
        if entrou:
            with condicao:
                clientes_ativos -= 1
                condicao.notify_all()
        conn.close()


def iniciar_servidor():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVIDOR INICIADO] Porta {PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(
            target=atender_cliente,
            args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    iniciar_servidor()