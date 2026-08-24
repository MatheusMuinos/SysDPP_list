import time
import threading

counter = 0

counter_lock = threading.Lock()

def increment_counter_com_lock(iterations):
    global counter

    for _ in range(iterations):
        counter_lock.acquire()
        try:
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

valor, esperado, tempo = run_threads(
    increment_counter_com_lock,
    num_threads=5,
    iterations_per_thread=1000
)

print("Valor final:", valor)
print("Valor esperado:", esperado)
print(f"Tempo: {tempo:.4f} s")
