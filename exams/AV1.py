import threading
import time
import random

# a) A combinacao escolhida foi o lock + semaforo
lock = threading.Lock()
semaforo = threading.Semaphore(0)

pedidos = []

def cliente(id):
    pedido = f"Pedido-{id}"
    print(f"Cliente {id} fez {pedido}")
    
    # b e c - adiciona o pedido com acesso exclusivo e sinaliza a cozinha
    with lock:
        pedidos.append(pedido)
    semaforo.release()

def cozinheiro():
    for _ in range(5):
        # b e c - espera por um pedido e tira ele com acesso exclusivo
        semaforo.acquire()
        with lock:
            pedido = pedidos.pop(0)
            
        print(f"Cozinhando {pedido}")
        time.sleep(random.uniform(0.5, 1.0))
        print(f"{pedido} pronto")


if __name__ == "__main__":
    # Cria e inicia a thread do cozinheiro
    cozinheiro_thread = threading.Thread(target=cozinheiro)
    cozinheiro_thread.start()

    # Cria e inicia as threads dos clientes
    clientes_threads = []
    for i in range(5):
        t = threading.Thread(target=cliente, args=(i,))
        clientes_threads.append(t)
        t.start()
        time.sleep(random.uniform(0.1, 0.3))  # Simula chegada aleatória dos clientes

    # Aguarda todas as threads dos clientes terminarem
    for t in clientes_threads:
        t.join()

    # Aguarda a thread do cozinheiro terminar
    cozinheiro_thread.join()