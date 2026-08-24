import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


# Respostas da atividade:
# 1) Por que soma e media exigem um raciocinio diferente do Exercicio 1?
#    Porque sao operacoes de reducao: os dados precisam ser divididos e os
#    resultados parciais precisam ser combinados ao final.
# 2) O que sao resultados parciais nesse contexto?
#    Sao a soma e a quantidade de elementos calculadas em cada bloco do vetor.
# 3) Os resultados finais das tres versoes foram equivalentes?
#    Sim. Todas usaram os mesmos blocos e combinaram soma e quantidade.
# 4) Qual versao apresentou menor tempo de execucao?
#    O programa informa a versao mais rapida. Para apenas 400 inteiros, a
#    versao sequencial normalmente apresenta menor overhead.


NUM_WORKERS = 4
random.seed(2026)
numeros = [random.randint(1, 1_000) for _ in range(400)]


def reduzir_bloco(bloco):
    return sum(bloco), len(bloco)


def dividir_em_blocos(valores):
    tamanho = (len(valores) + NUM_WORKERS - 1) // NUM_WORKERS
    return [valores[i:i + tamanho] for i in range(0, len(valores), tamanho)]


def combinar(resultados):
    soma = sum(parcial_soma for parcial_soma, _ in resultados)
    quantidade = sum(parcial_quantidade for _, parcial_quantidade in resultados)
    return soma, soma / quantidade


def executar_sequencial():
    inicio = time.perf_counter()
    resultado = reduzir_bloco(numeros)
    soma, media = combinar([resultado])
    return soma, media, time.perf_counter() - inicio


def executar_com_threads():
    inicio = time.perf_counter()
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        parciais = list(executor.map(reduzir_bloco, dividir_em_blocos(numeros)))
    soma, media = combinar(parciais)
    return soma, media, time.perf_counter() - inicio


def executar_com_processos():
    inicio = time.perf_counter()
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        parciais = list(executor.map(reduzir_bloco, dividir_em_blocos(numeros)))
    soma, media = combinar(parciais)
    return soma, media, time.perf_counter() - inicio


def exibir(nome, resultado):
    soma, media, tempo = resultado
    print(f"{nome}: soma={soma}, media={media:.6f}, tempo={tempo:.6f} segundos")


if __name__ == "__main__":
    resultados = {
        "Sequencial": executar_sequencial(),
        "ThreadPoolExecutor": executar_com_threads(),
        "ProcessPoolExecutor": executar_com_processos(),
    }
    print("=== Reducao: soma e media ===")
    for nome, resultado in resultados.items():
        exibir(nome, resultado)
    valores = list(resultados.values())
    print("Resultados equivalentes:", all(item[:2] == valores[0][:2] for item in valores))
    print("Mais rapida:", min(resultados, key=lambda nome: resultados[nome][2]))
