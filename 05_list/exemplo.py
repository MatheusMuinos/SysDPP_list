import time
import threading
import random


assentos = 5
semaforo = threading.Semaphore(3)
lock = threading.Lock()

def comprar_passagem(cliente):
    global assentos
    print(f"Cliente {cliente} tentando comprar passagem...")
    with semaforo:
        print(f"Cliente {cliente} entrou no sistema")
        time.sleep(random.uniform(0.5, 2))
        with lock:
            if assentos > 0:
                assentos -= 1
                print(f"Cliente {cliente} comprou! Assentos: {assentos}")
            else:
                print(f"Cliente {cliente} não conseguiu (voo lotado)")
        print(f"Cliente {cliente} saiu do sistema")


# Criando e executando 10 threads para simular 10 clientes  
threads = []
for i in range(10):
    t = threading.Thread(target=comprar_passagem, args=(i+1,))
    threads.append(t)
    t.start()

# Aguardando todas as threads terminarem
for t in threads:
    t.join()

print(f"\n--- Simulação finalizada ---")
print(f"Total de assentos restantes: {assentos}")