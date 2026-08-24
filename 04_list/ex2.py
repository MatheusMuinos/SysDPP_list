import time
import threading
import random

# Respostas para analise:
# 1) O valor obtido foi igual em todas as execucoes?
#    Nao necessariamente. Em geral, sem Lock, os resultados variam entre execucoes.

# 2) Por que o resultado pode variar mesmo sem alterar o codigo?
#    Porque ocorre condicao de corrida: multiplas threads leem e escrevem o mesmo contador
#    sem sincronizacao, entao incrementos podem se sobrepor e ser perdidos.

counter = 0

def increment_counter_sem_lock(iterations):
    global counter

    for _ in range(iterations):
        valor_atual = counter
        time.sleep(random.uniform(0.00001, 0.0002))
        counter = valor_atual + 1

def run_threads(funcao, num_threads, iterations_per_thread):
    global counter
    counter = 0
    threads = []
    inicio = time.perf_counter()

    for _ in range(num_threads):
        thread = threading.Thread(
            target=funcao,
            args=(iterations_per_thread,)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    tempo = time.perf_counter() - inicio
    esperado = num_threads * iterations_per_thread
    return counter, esperado, tempo

num_threads = 20
iterations_per_thread = 5000

for execucao in range(1, 4):
    valor, esperado, tempo = run_threads(
        increment_counter_sem_lock,
        num_threads=num_threads,
        iterations_per_thread=iterations_per_thread
    )
    diferenca = esperado - valor

    print(f"Execucao {execucao}")
    print("Valor obtido:", valor)
    print("Valor esperado:", esperado)
    print("Diferenca (esperado - obtido):", diferenca)
    print(f"Tempo: {tempo:.4f} s")
    print("-" * 40)
