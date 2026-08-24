import threading
import time


# Respostas da atividade:
# 1) Por que o saldo pode se tornar inconsistente?
#    Uma thread pode ler um saldo antigo enquanto outra atualiza o mesmo saldo.
#    A escrita posterior pode sobrescrever a primeira atualizacao.
# 2) Onde esta a regiao critica?
#    Ela esta entre a leitura do saldo, a pausa e a escrita do novo saldo nos
#    metodos depositar() e sacar().
# 3) Como o Lock resolve o problema?
#    Ele garante que somente uma thread por vez execute a regiao critica.
# 4) Qual e a relacao com o contador da Lista 01?
#    Os dois exemplos possuem leitura, pausa e escrita sobre um dado compartilhado.
#    Sem Lock ocorre race condition; com exclusao mutua, o resultado e consistente.


class ContaBancaria:
    def __init__(self):
        self.saldo = 0
        self.lock = threading.Lock()

    def depositar(self, valor, usar_lock=False):
        if usar_lock:
            with self.lock:
                self._atualizar_saldo(valor)
        else:
            self._atualizar_saldo(valor)

    def sacar(self, valor, usar_lock=False):
        if usar_lock:
            with self.lock:
                self._atualizar_saldo(-valor)
        else:
            self._atualizar_saldo(-valor)

    def _atualizar_saldo(self, valor):
        saldo_atual = self.saldo
        time.sleep(0.001)
        self.saldo = saldo_atual + valor


def executar_experimento(usar_lock):
    conta = ContaBancaria()
    threads = []

    for _ in range(4):
        threads.append(threading.Thread(target=realizar_depositos, args=(conta, usar_lock)))
        threads.append(threading.Thread(target=realizar_saques, args=(conta, usar_lock)))

    inicio = time.perf_counter()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return conta.saldo, time.perf_counter() - inicio


def realizar_depositos(conta, usar_lock):
    for _ in range(100):
        conta.depositar(10, usar_lock)


def realizar_saques(conta, usar_lock):
    for _ in range(100):
        conta.sacar(10, usar_lock)


if __name__ == "__main__":
    saldo_sem_lock, tempo_sem_lock = executar_experimento(False)
    saldo_com_lock, tempo_com_lock = executar_experimento(True)

    print("=== Desafio: conta bancaria concorrente ===")
    print(f"Sem Lock: saldo={saldo_sem_lock}, tempo={tempo_sem_lock:.6f} segundos")
    print(f"Com Lock: saldo={saldo_com_lock}, tempo={tempo_com_lock:.6f} segundos")
    print("Saldo esperado:", 0)
