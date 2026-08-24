import os
import threading
import time


# Respostas da atividade:
#
# 1) As threads apresentaram o mesmo PID? Por quê?
#    Sim. Todas pertencem ao mesmo processo Python, portanto compartilham o PID
#    do processo que criou as threads.
#
# 2) Os Thread IDs foram iguais ou diferentes?
#    Foram diferentes, pois cada thread possui seu proprio identificador.
#
# 3) Qual é o papel da thread principal?
#    A thread principal inicia as demais threads, exibe seu proprio Thread ID e,
#    quando o join() e usado, aguarda a finalizacao delas.
#
# 4) Qual é a função do método join()?
#    O join() bloqueia a thread que o chamou ate que a thread indicada termine.
#
# 5) O que mudou no comportamento do programa quando o join() foi removido?
#    A thread principal continuou sua execucao sem esperar pelas outras threads.
#    Por isso, a mensagem de finalizacao da execucao apareceu antes de algumas
#    mensagens das threads. Como elas nao sao daemon, o processo continuou vivo
#    ate que todas terminassem.


def imprimir_numeros():
	pid = os.getpid()
	thread_id = threading.get_native_id()
	nome = threading.current_thread().name

	for numero in range(1, 6):
		print(
			f"Nome: {nome} | PID: {pid} | Thread ID: {thread_id} "
			f"| Numero: {numero}",
			flush=True
		)
		time.sleep(1)


def executar_threads(usar_join):
	threads = []
	for numero in range(1, 6):
		thread = threading.Thread(
			target=imprimir_numeros,
			name=f"Thread-{numero}"
		)
		threads.append(thread)
		thread.start()

	if usar_join:
		for thread in threads:
			thread.join()

	print(
		f"Thread principal: ID {threading.get_native_id()} "
		f"| join() usado: {'sim' if usar_join else 'nao'}",
		flush=True
	)


if __name__ == "__main__":
	print(f"Thread principal iniciada: ID {threading.get_native_id()}")

	print("\n=== Execucao com join() ===")
	executar_threads(usar_join=True)

	print("\n=== Execucao sem join() ===")
	executar_threads(usar_join=False)

	print("Thread principal finalizada.")
