import threading
import time
from concurrent.futures import ThreadPoolExecutor


# Respostas da atividade:
#
# 1) Quantas threads foram criadas na versao manual?
#    Foram criadas seis threads, uma para cada tarefa da lista numeros.
#
# 2) Quantos Thread IDs diferentes apareceram com max_workers=2?
#    Apareceram dois Thread IDs diferentes, um para cada worker do pool.
#
# 3) O mesmo Thread ID foi utilizado para mais de uma tarefa?
#    Sim. Com max_workers menor que a quantidade de tarefas, um worker executa
#    varias tarefas e seu Thread ID aparece novamente.
#
# 4) O que isso demonstra sobre a reutilizacao de threads?
#    Demonstra que o ThreadPoolExecutor reutiliza workers existentes em vez de
#    criar uma nova thread para cada tarefa.
#
# 5) Qual e o papel de max_workers?
#    Define o numero maximo de threads que podem executar tarefas ao mesmo tempo.
#
# 6) O que aconteceu com o tempo total quando max_workers foi alterado?
#    O tempo diminuiu conforme mais workers puderam executar tarefas em paralelo:
#    aproximadamente 12, 6, 4 e 2 segundos para 1, 2, 3 e 6 workers.
#
# 7) Podemos concluir que aumentar indefinidamente max_workers sempre melhora o
#    desempenho? Explique.
#    Nao. Depois que a concorrencia ja atende a carga, workers extras nao reduzem
#    o tempo e podem aumentar o custo de criacao, troca de contexto e recursos.


numeros = [1, 2, 3, 4, 5, 6]


def tarefa(numero):
    thread_id = threading.get_native_id()
    print(f"Inicio da tarefa {numero} | Thread ID: {thread_id}", flush=True)
    time.sleep(2)
    print(f"Termino da tarefa {numero} | Thread ID: {thread_id}", flush=True)
    return thread_id


def executar_manualmente():
    threads = []
    thread_ids = []
    inicio = time.perf_counter()

    for numero in numeros:
        thread = threading.Thread(
            target=lambda item=numero: thread_ids.append(tarefa(item)),
            name=f"Thread-manual-{numero}"
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    tempo = time.perf_counter() - inicio
    return tempo, thread_ids


def executar_com_pool(max_workers):
    inicio = time.perf_counter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        thread_ids = list(executor.map(tarefa, numeros))

    tempo = time.perf_counter() - inicio
    return tempo, thread_ids


if __name__ == "__main__":
    print("=== Parte A: criacao manual ===")
    tempo_manual, ids_manuais = executar_manualmente()
    print(f"Threads criadas: {len(ids_manuais)}")
    print(f"Thread IDs diferentes: {len(set(ids_manuais))}")
    print(f"Tempo total: {tempo_manual:.4f} segundos")

    print("\n=== Parte B: ThreadPoolExecutor com max_workers=2 ===")
    tempo_pool, ids_pool = executar_com_pool(max_workers=2)
    print(f"Thread IDs diferentes: {len(set(ids_pool))}")
    print(f"Tempo total: {tempo_pool:.4f} segundos")

    print("\n=== Parte C: efeito de max_workers ===")
    for quantidade_workers in [1, 2, 3, 6]:
        tempo, ids = executar_com_pool(max_workers=quantidade_workers)
        print(
            f"max_workers={quantidade_workers} | "
            f"Thread IDs diferentes: {len(set(ids))} | "
            f"Tempo total: {tempo:.4f} segundos"
        )
