import threading
import time


# Respostas da atividade:
#
# 1) O comportamento das duas versoes foi o mesmo?
#    Nao. Com start(), as threads executam ao mesmo tempo. Com run(), cada
#    thread termina antes que a proxima seja chamada.
#
# 2) Qual delas apresentou menor tempo total?
#    A versao com start() apresentou menor tempo total, aproximadamente 2
#    segundos, enquanto a versao com run() levou aproximadamente 4 segundos.
#
# 3) O que acontece quando start() e utilizado?
#    O Python cria uma nova linha de execucao para a thread e chama o metodo
#    run() nessa nova thread.
#
# 4) O que acontece quando run() e chamado diretamente?
#    O metodo run() e executado como uma chamada comum na thread atual, sem
#    criar uma nova linha de execucao.
#
# 5) Em qual das versoes novas linhas de execucao sao criadas?
#    Somente na versao que utiliza start().


class MinhaThread(threading.Thread):
    def run(self):
        print(f"Inicio da execucao da {self.name}.", flush=True)
        time.sleep(2)
        print(f"Termino da execucao da {self.name}.", flush=True)


def executar_com_start():
    t1 = MinhaThread(name="Thread-1")
    t2 = MinhaThread(name="Thread-2")
    inicio = time.perf_counter()

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    return time.perf_counter() - inicio


def executar_com_run():
    t1 = MinhaThread(name="Thread-1")
    t2 = MinhaThread(name="Thread-2")
    inicio = time.perf_counter()

    t1.run()
    t2.run()
    return time.perf_counter() - inicio


if __name__ == "__main__":
    print("=== Execucao usando start() ===")
    tempo_start = executar_com_start()
    print(f"Tempo total com start(): {tempo_start:.4f} segundos")

    print("\n=== Execucao usando run() diretamente ===")
    tempo_run = executar_com_run()
    print(f"Tempo total com run(): {tempo_run:.4f} segundos")
