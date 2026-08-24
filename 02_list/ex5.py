import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


# Respostas da atividade:
# 1) Qual estrategia foi mais rapida para a matriz 30 x 30?
#    O programa informa a estrategia mais rapida na execucao realizada.
# 2) O comportamento mudou quando o tamanho da matriz aumentou?
#    Pode mudar. O custo da multiplicacao cresce muito mais que o overhead, e
#    estrategias paralelas podem se beneficiar de tarefas maiores.
# 3) Por que tarefas maiores podem favorecer o multiprocessamento?
#    O custo de distribuir e iniciar processos passa a representar uma parte
#    menor do tempo total de calculo.
# 4) Qual e a relacao entre custo computacional e overhead?
#    O paralelismo compensa quando o trabalho economizado supera o custo de criar,
#    coordenar e transportar dados entre os workers.
# 5) Usar mais threads ou processos sempre melhora o desempenho?
#    Nao. O limite de nucleos, a comunicacao e a troca de contexto podem fazer
#    workers adicionais manterem ou aumentarem o tempo.


NUM_WORKERS = 4


def multiplicar_linha(argumentos):
    linha, colunas_b = argumentos
    return [sum(valor * coluna[indice] for indice, valor in enumerate(linha)) for coluna in colunas_b]


def criar_matrizes(tamanho):
    random.seed(2026 + tamanho)
    matriz_a = [[random.randint(1, 9) for _ in range(tamanho)] for _ in range(tamanho)]
    matriz_b = [[random.randint(1, 9) for _ in range(tamanho)] for _ in range(tamanho)]
    return matriz_a, matriz_b


def preparar_colunas(matriz):
    return [list(coluna) for coluna in zip(*matriz)]


def executar_sequencial(matriz_a, colunas_b):
    inicio = time.perf_counter()
    resultado = [multiplicar_linha((linha, colunas_b)) for linha in matriz_a]
    return resultado, time.perf_counter() - inicio


def executar_com_threads(matriz_a, colunas_b):
    inicio = time.perf_counter()
    argumentos = [(linha, colunas_b) for linha in matriz_a]
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        resultado = list(executor.map(multiplicar_linha, argumentos))
    return resultado, time.perf_counter() - inicio


def executar_com_processos(matriz_a, colunas_b):
    inicio = time.perf_counter()
    argumentos = [(linha, colunas_b) for linha in matriz_a]
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        resultado = list(executor.map(multiplicar_linha, argumentos))
    return resultado, time.perf_counter() - inicio


def executar_tamanho(tamanho):
    matriz_a, matriz_b = criar_matrizes(tamanho)
    colunas_b = preparar_colunas(matriz_b)
    resultados = {
        "Sequencial": executar_sequencial(matriz_a, colunas_b),
        "ThreadPoolExecutor": executar_com_threads(matriz_a, colunas_b),
        "ProcessPoolExecutor": executar_com_processos(matriz_a, colunas_b),
    }
    matrizes = [resultado for resultado, _ in resultados.values()]
    print(f"\n=== Matrizes {tamanho} x {tamanho} ===")
    for nome, (_, tempo) in resultados.items():
        print(f"{nome}: {tempo:.6f} segundos")
    print("Resultados iguais:", all(matriz == matrizes[0] for matriz in matrizes))
    print("Mais rapida:", min(resultados, key=lambda nome: resultados[nome][1]))


if __name__ == "__main__":
    for tamanho in [30, 100, 200]:
        executar_tamanho(tamanho)
