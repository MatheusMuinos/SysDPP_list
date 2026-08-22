import time
import threading

# Resposta da questao: o valor esperado e calculado por
# valor_esperado = numero_de_threads * iteracoes_por_thread,
# pois cada thread incrementa o contador exatamente esse numero de vezes.

counter = 0  # recurso compartilhado

counter_lock = threading.Lock()

def increment_counter_com_lock(iterations):
    global counter

    # Cada iteracao incrementa o contador em 1, protegendo a secao critica.
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
    # Reinicia o contador para uma nova execucao.
    counter = 0
    threads = []
    inicio = time.perf_counter()

    # Cria e inicia todas as threads.
    for _ in range(num_threads):
        thread = threading.Thread(
            target=funcao,
            args=(iterations_per_thread,)
        )
        threads.append(thread)
        thread.start()

    # Aguarda a finalizacao de todas as threads.
    for thread in threads:
        thread.join()

    tempo = time.perf_counter() - inicio
    # Valor esperado: total de incrementos executados por todas as threads.
    esperado = num_threads * iterations_per_thread
    return counter, esperado, tempo

def ler_inteiro_positivo(mensagem):
    # Le um inteiro positivo e repete ate receber uma entrada valida.
    while True:
        try:
            valor = int(input(mensagem))
            if valor <= 0:
                print("Informe um inteiro positivo maior que zero.")
                continue
            return valor
        except ValueError:
            print("Entrada invalida. Digite um numero inteiro.")


# Parametros informados pelo usuario.
num_threads = ler_inteiro_positivo("Numero de threads: ")
iterations_per_thread = ler_inteiro_positivo("Numero de iteracoes por thread: ")

# Executa o contador concorrente com Lock.
valor, esperado, tempo = run_threads(
    increment_counter_com_lock,
    num_threads=num_threads,
    iterations_per_thread=iterations_per_thread
)

# Exibe resultados da execucao.
print("Valor final:", valor)
print("Valor esperado:", esperado)
print(f"Tempo: {tempo:.4f} s")

# Verifica se o contador chegou ao valor previsto.
if valor == esperado:
    print("Resultado correto: o contador atingiu o valor esperado.")
else:
    print("Resultado incorreto: o contador NAO atingiu o valor esperado.")
