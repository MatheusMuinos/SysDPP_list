import time
import threading

counter = 0  # recurso compartilhado

counter_lock = threading.Lock()

def increment_counter_com_lock(iterations):
    global counter

    for _ in range(iterations):
        counter_lock.acquire()
        try: # região crítica
            valor_atual = counter
            time.sleep(0.0001)
            counter = valor_atual + 1
        finally:
            counter_lock.release()


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



TOTAL_ITERACOES = 10000

for n in [1, 2, 5, 10]:
    iteracoes_por_thread = TOTAL_ITERACOES // n

    valor, esperado, tempo = run_threads(
        increment_counter_com_lock,
        num_threads=n,
        iterations_per_thread=iteracoes_por_thread
    )

    print(f"Threads: {n}")
    print(f"Iterações por thread: {iteracoes_por_thread}")
    print(f"Valor final: {valor}")
    print(f"Esperado: {esperado}")
    print(f"Tempo: {tempo:.4f} s")
    print("-" * 30)
