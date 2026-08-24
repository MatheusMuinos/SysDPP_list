import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


# Respostas da atividade:
# 1) Por que as linhas podem ser processadas independentemente?
#    Cada elemento da linha resultante depende somente da mesma linha de A e da
#    matriz B, sem depender do calculo de outra linha.
# 2) Quantas tarefas podem ser criadas se cada linha for uma tarefa?
#    Podem ser criadas 50 tarefas, uma para cada linha da matriz.
# 3) As tres versoes produziram a mesma matriz resultante?
#    Sim. Todas somaram os mesmos elementos correspondentes de A e B.
# 4) Para uma matriz 50 x 50, o custo compensou?
#    Normalmente nao. O trabalho de cada linha e pequeno diante do overhead de
#    coordenar threads ou processos; os tempos exibidos permitem confirmar isso.


NUM_WORKERS = 4
TAMANHO = 50
random.seed(2026)
matriz_a = [[random.randint(1, 100) for _ in range(TAMANHO)] for _ in range(TAMANHO)]
matriz_b = [[random.randint(1, 100) for _ in range(TAMANHO)] for _ in range(TAMANHO)]


def somar_linha(argumentos):
    linha_a, linha_b = argumentos
    return [valor_a + valor_b for valor_a, valor_b in zip(linha_a, linha_b)]


def executar_sequencial():
    inicio = time.perf_counter()
    resultado = [somar_linha((linha_a, linha_b)) for linha_a, linha_b in zip(matriz_a, matriz_b)]
    return resultado, time.perf_counter() - inicio


def executar_com_threads():
    inicio = time.perf_counter()
    argumentos = list(zip(matriz_a, matriz_b))
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        resultado = list(executor.map(somar_linha, argumentos))
    return resultado, time.perf_counter() - inicio


def executar_com_processos():
    inicio = time.perf_counter()
    argumentos = list(zip(matriz_a, matriz_b))
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        resultado = list(executor.map(somar_linha, argumentos))
    return resultado, time.perf_counter() - inicio


if __name__ == "__main__":
    resultados = {
        "Sequencial": executar_sequencial(),
        "ThreadPoolExecutor": executar_com_threads(),
        "ProcessPoolExecutor": executar_com_processos(),
    }
    print("=== Soma de matrizes 50 x 50 ===")
    for nome, (resultado, tempo) in resultados.items():
        print(f"{nome}: {tempo:.6f} segundos")
        print(f"Primeira linha: {resultado[0]}")
    matrizes = [resultado for resultado, _ in resultados.values()]
    print("Matrizes iguais:", all(matriz == matrizes[0] for matriz in matrizes))
