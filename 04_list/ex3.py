import time
import threading

# Respostas para analise:
# 1) Qual versao garante o resultado esperado?
#    A versao com Lock, pois sincroniza o acesso ao contador e evita condicao de corrida.
# 2) A versao correta foi necessariamente a mais rapida?
#    Nao. Em muitos cenarios, a versao sem Lock pode parecer mais rapida, mas pode estar incorreta.
# 3) Que custo e introduzido pelo mecanismo de sincronizacao?
#    O Lock adiciona overhead de aquisicao/liberacao e pode reduzir o paralelismo efetivo,
#    aumentando o tempo total em troca de consistencia do resultado.

counter = 0  # recurso compartilhado
counter_lock = threading.Lock()


def increment_counter_sem_lock(iterations):
	global counter

	# Secao critica sem sincronizacao para evidenciar condicao de corrida.
	for _ in range(iterations):
		valor_atual = counter
		time.sleep(0.0001)
		counter = valor_atual + 1


def increment_counter_com_lock(iterations):
	global counter

	# Secao critica protegida por Lock para garantir consistencia.
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
	# Reinicia o contador antes de cada experimento.
	counter = 0
	threads = []
	inicio = time.perf_counter()

	# Cria e inicia as threads com os mesmos parametros.
	for _ in range(num_threads):
		thread = threading.Thread(
			target=funcao,
			args=(iterations_per_thread,)
		)
		threads.append(thread)
		thread.start()

	# Aguarda todas as threads terminarem.
	for thread in threads:
		thread.join()

	tempo = time.perf_counter() - inicio
	esperado = num_threads * iterations_per_thread
	return counter, esperado, tempo


def ler_inteiro_positivo(mensagem):
	# Le um inteiro positivo e repete ate entrada valida.
	while True:
		try:
			valor = int(input(mensagem))
			if valor <= 0:
				print("Informe um inteiro positivo maior que zero.")
				continue
			return valor
		except ValueError:
			print("Entrada invalida. Digite um numero inteiro.")


def exibir_resultado(nome_versao, num_threads, iterations_per_thread, valor, esperado, tempo):
	# Define o status comparando resultado real e esperado.
	status = "correto" if valor == esperado else "incorreto"

	print(f"Versao: {nome_versao}")
	print("Numero de threads:", num_threads)
	print("Numero de iteracoes por thread:", iterations_per_thread)
	print("Valor obtido:", valor)
	print("Valor esperado:", esperado)
	print(f"Tempo de execucao: {tempo:.4f} s")
	print("Status:", status)
	print("-" * 50)


num_threads = ler_inteiro_positivo("Numero de threads: ")
iterations_per_thread = ler_inteiro_positivo("Numero de iteracoes por thread: ")

# Executa primeiro a versao sem Lock com os parametros informados.
valor_sem_lock, esperado_sem_lock, tempo_sem_lock = run_threads(
	increment_counter_sem_lock,
	num_threads=num_threads,
	iterations_per_thread=iterations_per_thread
)

# Executa depois a versao com Lock com os mesmos parametros.
valor_com_lock, esperado_com_lock, tempo_com_lock = run_threads(
	increment_counter_com_lock,
	num_threads=num_threads,
	iterations_per_thread=iterations_per_thread
)

print("\nComparacao automatica: sem Lock x com Lock")
print("=" * 50)

exibir_resultado(
	"Sem Lock",
	num_threads,
	iterations_per_thread,
	valor_sem_lock,
	esperado_sem_lock,
	tempo_sem_lock
)

exibir_resultado(
	"Com Lock",
	num_threads,
	iterations_per_thread,
	valor_com_lock,
	esperado_com_lock,
	tempo_com_lock
)
