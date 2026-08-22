import time
import threading

# Respostas para analise:
# 1) O with cria um novo Lock?
#    Nao. O with usa o mesmo objeto Lock ja existente (counter_lock), apenas
#    automatiza a aquisicao na entrada e a liberacao na saida do bloco.
# 2) Qual e a vantagem de usar with para controlar a regiao critica?
#    O with reduz erros e deixa o codigo mais seguro e legivel, pois garante a
#    liberacao do Lock mesmo se ocorrer excecao dentro da secao critica.

counter = 0  # recurso compartilhado
counter_lock = threading.Lock()


def increment_counter_manual(iterations):
	global counter

	# Forma manual: acquire + try/finally + release.
	for _ in range(iterations):
		counter_lock.acquire()
		try:
			valor_atual = counter
			time.sleep(0.0001)
			counter = valor_atual + 1
		finally:
			counter_lock.release()


def increment_counter_with(iterations):
	global counter

	# Forma automatica: o contexto with controla acquire/release.
	for _ in range(iterations):
		with counter_lock:
			valor_atual = counter
			time.sleep(0.0001)
			counter = valor_atual + 1


def run_threads(funcao, num_threads, iterations_per_thread):
	global counter
	# Reinicia o contador para cada teste.
	counter = 0
	threads = []
	inicio = time.perf_counter()

	# Cria e inicia as threads.
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
	esperado = num_threads * iterations_per_thread
	return counter, esperado, tempo


def exibir_resultado(nome_versao, valor, esperado, tempo):
	# Status indica se o valor obtido corresponde ao esperado.
	status = "correto" if valor == esperado else "incorreto"
	print(f"Versao: {nome_versao}")
	print("Valor final:", valor)
	print("Valor esperado:", esperado)
	print(f"Tempo: {tempo:.4f} s")
	print("Status:", status)
	print("-" * 40)


# Parametros fixos para comparacao direta entre as duas abordagens.
num_threads = 5
iterations_per_thread = 1000

# Executa versao manual.
valor_manual, esperado_manual, tempo_manual = run_threads(
	increment_counter_manual,
	num_threads=num_threads,
	iterations_per_thread=iterations_per_thread
)

# Executa versao com with.
valor_with, esperado_with, tempo_with = run_threads(
	increment_counter_with,
	num_threads=num_threads,
	iterations_per_thread=iterations_per_thread
)

print("Comparacao: acquire()/release() x with lock")
print("Threads:", num_threads)
print("Iteracoes por thread:", iterations_per_thread)
print("=" * 40)

exibir_resultado("Manual (acquire/release)", valor_manual, esperado_manual, tempo_manual)
exibir_resultado("With lock", valor_with, esperado_with, tempo_with)
