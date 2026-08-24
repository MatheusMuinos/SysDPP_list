import time
import threading

# Resposta da questao: o valor esperado e calculado por
# valor_esperado = numero_de_threads * iteracoes_por_thread,
# pois cada thread incrementa o contador exatamente esse numero de vezes.

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

def ler_inteiro_positivo(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            if valor <= 0:
                print("Informe um inteiro positivo maior que zero.")
                continue
            return valor
        except ValueError:
            print("Entrada invalida. Digite um numero inteiro.")


num_threads = ler_inteiro_positivo("Numero de threads: ")
iterations_per_thread = ler_inteiro_positivo("Numero de iteracoes por thread: ")

valor, esperado, tempo = run_threads(
    increment_counter_com_lock,
    num_threads=num_threads,
    iterations_per_thread=iterations_per_thread
)

print("Valor final:", valor)
print("Valor esperado:", esperado)
print(f"Tempo: {tempo:.4f} s")

if valor == esperado:
    print("Resultado correto: o contador atingiu o valor esperado.")
else:
    print("Resultado incorreto: o contador NAO atingiu o valor esperado.")
