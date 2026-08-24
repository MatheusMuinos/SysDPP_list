import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


# Respostas da atividade:
# 1) Qual etapa precisa ser realizada antes da filtragem?
#    E necessario calcular a media da lista antes de testar quais valores sao
#    maiores que ela.
# 2) Por que cada valor pode ser analisado independentemente depois que a media
#    e conhecida?
#    Porque todos os testes usam a mesma media e nao alteram os demais valores.
# 3) As tres versoes retornaram os mesmos valores?
#    Sim. Os resultados dos blocos foram combinados preservando a ordem original.
# 4) O overhead influenciou os tempos obtidos?
#    Sim. Para 400 valores, dividir blocos e coordenar workers pode custar mais
#    que executar a filtragem diretamente.


NUM_WORKERS = 4
random.seed(2026)
numeros = [random.randint(1, 1_000) for _ in range(400)]


def filtrar_bloco(argumentos):
    bloco, media = argumentos
    return [numero for numero in bloco if numero > media]


def dividir_em_blocos(valores):
    tamanho = (len(valores) + NUM_WORKERS - 1) // NUM_WORKERS
    return [valores[i:i + tamanho] for i in range(0, len(valores), tamanho)]


def calcular_media():
    return sum(numeros) / len(numeros)


def executar_sequencial():
    inicio = time.perf_counter()
    media = calcular_media()
    resultado = filtrar_bloco((numeros, media))
    return media, resultado, time.perf_counter() - inicio


def executar_com_threads():
    inicio = time.perf_counter()
    media = calcular_media()
    argumentos = [(bloco, media) for bloco in dividir_em_blocos(numeros)]
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        blocos_filtrados = list(executor.map(filtrar_bloco, argumentos))
    resultado = [numero for bloco in blocos_filtrados for numero in bloco]
    return media, resultado, time.perf_counter() - inicio


def executar_com_processos():
    inicio = time.perf_counter()
    media = calcular_media()
    argumentos = [(bloco, media) for bloco in dividir_em_blocos(numeros)]
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        blocos_filtrados = list(executor.map(filtrar_bloco, argumentos))
    resultado = [numero for bloco in blocos_filtrados for numero in bloco]
    return media, resultado, time.perf_counter() - inicio


def exibir(nome, resultado):
    media, valores, tempo = resultado
    print(f"{nome}: media={media:.6f}, quantidade={len(valores)}, tempo={tempo:.6f} segundos")


if __name__ == "__main__":
    resultados = {
        "Sequencial": executar_sequencial(),
        "ThreadPoolExecutor": executar_com_threads(),
        "ProcessPoolExecutor": executar_com_processos(),
    }
    print("=== Filtragem: valores maiores que a media ===")
    for nome, resultado in resultados.items():
        exibir(nome, resultado)
    valores = list(resultados.values())
    print("Valores iguais:", all(item[1] == valores[0][1] for item in valores))
    print("Mais rapida:", min(resultados, key=lambda nome: resultados[nome][2]))
