import time
import threading

# Respostas para analise:
# 1) O aumento do numero de threads reduziu o tempo de execucao?
#    Nem sempre. Com Lock unico, aumentar threads pode nao reduzir tempo e ate aumentar,
#    porque as threads disputam a mesma secao critica.
# 2) Por que mais threads podem aumentar a contencao pelo mesmo Lock?
#    Porque mais threads tentam entrar ao mesmo tempo na regiao protegida. Como so uma
#    pode segurar o Lock por vez, as outras ficam bloqueadas, gerando espera e overhead.

counter = 0
counter_lock = threading.Lock() # Lock para proteger a variavel global counter


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
		thread = threading.Thread(target=funcao,args=(iterations_per_thread,))
		threads.append(thread)
		thread.start()

	for thread in threads:
		thread.join()

	tempo = time.perf_counter() - inicio
	valor_final = counter
	return valor_final, tempo


TOTAL_ITERACOES = 10000
CENARIOS_THREADS = [1, 2, 5, 10]

resultados = []

for n in CENARIOS_THREADS:
	iteracoes_por_thread = TOTAL_ITERACOES // n
	valor_final, tempo = run_threads(
		increment_counter_com_lock,
		num_threads=n,
		iterations_per_thread=iteracoes_por_thread
	)

	resultados.append((n, iteracoes_por_thread, TOTAL_ITERACOES, valor_final, tempo))


cabecalho = (
	f"{'Threads':<8}"
	f"{'Iteracoes/thread':<20}"
	f"{'Total':<10}"
	f"{'Valor final':<14}"
	f"{'Tempo (s)':<10}"
)

print(cabecalho)
print("-" * len(cabecalho))

for threads, iter_por_thread, total, valor_final, tempo in resultados:
	print(
		f"{threads:<8}"
		f"{iter_por_thread:<20}"
		f"{total:<10}"
		f"{valor_final:<14}"
		f"{tempo:<10.4f}"
	)
