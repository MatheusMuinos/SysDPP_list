import os
import time
from concurrent.futures import ProcessPoolExecutor


# Respostas da atividade:
#
# 1) Quantos PIDs diferentes apareceram na versao sequencial?
#    Um PID diferente: o PID do processo principal executou todas as tarefas.
#
# 2) Quantos PIDs apareceram com ProcessPoolExecutor(max_workers=2)?
#    Normalmente aparecem dois PIDs diferentes, um para cada processo worker.
#    A quantidade observada e exibida pelo programa e pode ser menor caso uma
#    tarefa termine antes que o segundo worker seja utilizado.
#
# 3) Um mesmo processo executou mais de uma tarefa?
#    Sim. Os processos do pool sao reutilizados e podem executar varias tarefas.
#
# 4) O que diferencia essa abordagem daquela realizada com ThreadPoolExecutor?
#    O ThreadPoolExecutor utiliza threads dentro do mesmo processo e compartilha
#    o PID. O ProcessPoolExecutor utiliza processos separados, com PIDs proprios.
#
# 5) Qual versao apresentou menor tempo?
#    O tempo depende do computador e da quantidade de nucleos. Em tarefas
#    CPU-bound, o ProcessPoolExecutor pode ser mais rapido que a versao
#    sequencial quando ha nucleos disponiveis para executar em paralelo.
#
# 6) Por que multiplos processos podem ser vantajosos em tarefas CPU-bound?
#    Cada processo possui seu proprio interpretador Python, permitindo executar
#    trabalho de CPU em paralelo e contornar o GIL do CPython.
#
# 7) Qual e a diferenca entre concorrencia e paralelismo observada nos
#    experimentos?
#    Concorrencia significa organizar varias tarefas para progredirem juntas.
#    Paralelismo significa executar tarefas simultaneamente em nucleos
#    diferentes, algo possibilitado pelos varios processos do pool.
#
# 8) Aumentar o numero de processos sempre reduz o tempo de execucao? Explique.
#    Nao. Depois de utilizar os nucleos disponiveis, processos extras aumentam
#    a disputa por CPU e o custo de criacao, comunicacao e gerenciamento. Por
#    isso, o desempenho pode parar de melhorar ou ate piorar.


numeros = [1, 2, 3, 4, 5, 6]
ITERACOES = 10_000_000


def tarefa(numero):
    total = 0
    for i in range(ITERACOES):
        total += i

    pid = os.getpid()
    return numero, pid, total


def executar_sequencialmente():
    inicio = time.perf_counter()
    resultados = []

    for numero in numeros:
        resultado = tarefa(numero)
        resultados.append(resultado)
        print(f"Tarefa {numero} | PID: {resultado[1]}", flush=True)

    tempo = time.perf_counter() - inicio
    return resultados, tempo


def executar_com_process_pool(max_workers):
    inicio = time.perf_counter()

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        resultados = list(executor.map(tarefa, numeros))

    for numero, pid, _ in resultados:
        print(
            f"Tarefa {numero} | PID: {pid} | max_workers: {max_workers}",
            flush=True
        )

    tempo = time.perf_counter() - inicio
    return resultados, tempo


def exibir_resultado_pool(max_workers):
    resultados, tempo = executar_com_process_pool(max_workers)
    pids = [pid for _, pid, _ in resultados]
    print(f"PIDs diferentes: {len(set(pids))}")
    print(f"Tempo total: {tempo:.4f} segundos")
    print("-" * 50)
    return resultados, tempo


if __name__ == "__main__":
    print("=== Parte A: execucao sequencial ===")
    resultados_sequenciais, tempo_sequencial = executar_sequencialmente()
    pids_sequenciais = [pid for _, pid, _ in resultados_sequenciais]
    print(f"PIDs diferentes: {len(set(pids_sequenciais))}")
    print(f"Tempo total: {tempo_sequencial:.4f} segundos")

    print("\n=== Parte B: ProcessPoolExecutor(max_workers=2) ===")
    exibir_resultado_pool(max_workers=2)

    print("\n=== Parte C: quantidade de processos ===")
    for quantidade_processos in [1, 2, 4]:
        print(f"\nmax_workers={quantidade_processos}")
        exibir_resultado_pool(max_workers=quantidade_processos)
