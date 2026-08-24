import math
import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


# Respostas da atividade:
# 1) As tres versoes produziram os mesmos resultados?
#    Sim. As tres aplicaram a mesma funcao a cada elemento, e os resultados
#    foram comparados na mesma ordem.
# 2) Qual versao foi mais rapida na sua execucao?
#    O programa informa a versao mais rapida. Para tarefas pequenas, a versao
#    sequencial normalmente vence por ter menos overhead.
# 3) Se workers nao forem mais rapidos, isso significa que concorrencia ou
#    paralelismo nao funcionam?
#    Nao. O custo de criar, coordenar e comunicar workers pode ser maior que o
#    custo de calcular 300 raizes. Com tarefas maiores, o resultado pode mudar.


NUM_WORKERS = 4
random.seed(2026)
numeros = [random.randint(1, 10_000) for _ in range(300)]


def calcular_raiz(numero):
    return math.sqrt(numero)


def executar_sequencial():
    inicio = time.perf_counter()
    resultados = [calcular_raiz(numero) for numero in numeros]
    return resultados, time.perf_counter() - inicio


def executar_com_threads():
    inicio = time.perf_counter()
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        resultados = list(executor.map(calcular_raiz, numeros))
    return resultados, time.perf_counter() - inicio


def executar_com_processos():
    inicio = time.perf_counter()
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        resultados = list(executor.map(calcular_raiz, numeros))
    return resultados, time.perf_counter() - inicio


def exibir_resultado(nome, resultados, tempo):
    print(f"{nome}: {tempo:.6f} segundos")
    print(f"Primeiro resultado: {resultados[0]:.6f}")


if __name__ == "__main__":
    resultados_sequencial, tempo_sequencial = executar_sequencial()
    resultados_threads, tempo_threads = executar_com_threads()
    resultados_processos, tempo_processos = executar_com_processos()

    print("=== Operacao elemento a elemento ===")
    exibir_resultado("Sequencial", resultados_sequencial, tempo_sequencial)
    exibir_resultado("ThreadPoolExecutor", resultados_threads, tempo_threads)
    exibir_resultado("ProcessPoolExecutor", resultados_processos, tempo_processos)
    print("Resultados iguais:", resultados_sequencial == resultados_threads == resultados_processos)

    tempos = {
        "Sequencial": tempo_sequencial,
        "ThreadPoolExecutor": tempo_threads,
        "ProcessPoolExecutor": tempo_processos,
    }
    print("Mais rapida:", min(tempos, key=tempos.get))
