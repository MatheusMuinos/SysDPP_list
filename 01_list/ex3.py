import threading
import time


# Respostas da atividade:
#
# 1) Qual deveria ser o valor final do contador?
#    O valor final deveria ser 200, pois duas threads realizam 100 incrementos
#    cada uma.
#
# 2) O resultado obtido sem Lock foi o esperado?
#    Nao. Sem sincronizacao, alguns incrementos podem ser perdidos e o valor
#    final normalmente fica menor que 200.
#
# 3) Por que alguns incrementos podem ser perdidos?
#    As duas threads podem copiar o mesmo valor de contador antes que qualquer
#    uma armazene o novo resultado. A segunda escrita sobrescreve a primeira.
#
# 4) O que caracteriza uma Race Condition?
#    E uma situacao em que o resultado depende da ordem e do momento em que as
#    threads acessam e modificam um dado compartilhado.
#
# 5) Qual e o papel do Lock?
#    O Lock garante exclusao mutua, permitindo que apenas uma thread por vez
#    execute a regiao critica.
#
# 6) Por que o resultado passa a ser consistente quando a regiao critica e
#    protegida?
#    Porque cada thread conclui a leitura, a pausa, o incremento e a escrita
#    antes que outra thread possa executar essa mesma regiao.


contador = 0
lock = threading.Lock()


def incrementar_sem_lock():
    global contador

    for _ in range(100):
        valor_atual = contador
        time.sleep(0.0001)
        valor_atual += 1
        contador = valor_atual


def incrementar_com_lock():
    global contador

    for _ in range(100):
        with lock:
            valor_atual = contador
            time.sleep(0.0001)
            valor_atual += 1
            contador = valor_atual


def executar_experimento(funcao):
    global contador
    contador = 0
    threads = []

    inicio = time.perf_counter()
    for numero in range(1, 3):
        thread = threading.Thread(
            target=funcao,
            name=f"Thread-{numero}"
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    tempo = time.perf_counter() - inicio
    return contador, tempo


if __name__ == "__main__":
    valor_esperado = 2 * 100

    print("=== Parte A: sem Lock ===")
    valor_sem_lock, tempo_sem_lock = executar_experimento(incrementar_sem_lock)
    print("Valor obtido:", valor_sem_lock)
    print("Valor esperado:", valor_esperado)
    print(f"Tempo de execucao: {tempo_sem_lock:.4f} segundos")
    print("Resultado:", "correto" if valor_sem_lock == valor_esperado else "incorreto")

    print("\n=== Parte B: com Lock ===")
    valor_com_lock, tempo_com_lock = executar_experimento(incrementar_com_lock)
    print("Valor obtido:", valor_com_lock)
    print("Valor esperado:", valor_esperado)
    print(f"Tempo de execucao: {tempo_com_lock:.4f} segundos")
    print("Resultado:", "correto" if valor_com_lock == valor_esperado else "incorreto")
