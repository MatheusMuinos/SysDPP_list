import time
import threading
import random

# Respostas para analise:
# 1) O valor obtido foi igual em todas as execucoes?
#    Nao necessariamente. Em geral, sem Lock, os resultados variam entre execucoes.

# 2) Por que o resultado pode variar mesmo sem alterar o codigo?
#    Porque ocorre condicao de corrida: multiplas threads leem e escrevem o mesmo contador
#    sem sincronizacao, entao incrementos podem se sobrepor e ser perdidos.

# Professor, para visualizar melhor as fariações dos valores obtidos em cada execucao, 
# adicionei uma pausa aleatoria na secao critica, alem de aumentar o numero de threads e iteracoes por thread.

counter = 0  # recurso compartilhado

def increment_counter_sem_lock(iterations):
    global counter

    # Secao critica sem Lock: leitura, pequena pausa e escrita.
    for _ in range(iterations):
        valor_atual = counter
        time.sleep(random.uniform(0.00001, 0.0002))
        counter = valor_atual + 1

def run_threads(funcao, num_threads, iterations_per_thread):
    global counter
    # Reinicia o contador para cada rodada de teste.
    counter = 0
    threads = []
    inicio = time.perf_counter()

    # Cria e inicia as threads concorrentes.
    for _ in range(num_threads):
        thread = threading.Thread(
            target=funcao,
            args=(iterations_per_thread,)
        )
        threads.append(thread)
        thread.start()

    # Aguarda todas as threads finalizarem.
    for thread in threads:
        thread.join()

    tempo = time.perf_counter() - inicio
    # Valor esperado = total de incrementos solicitados.
    esperado = num_threads * iterations_per_thread
    return counter, esperado, tempo

# Parametros fixos do exercicio.
num_threads = 20
iterations_per_thread = 5000

# Executa pelo menos 3 vezes para observar variacao da Race Condition.
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
