# Respostas da atividade:
# 1) O cliente deve criar um proxy para o servidor XML-RPC usando xmlrpc.client.ServerProxy.
# 2) Cada operação é chamada remotamente, e o retorno deve ser validado usando a chave ok.
# 3) Para testar a divisão por zero, o cliente envia b = 0 e lê a mensagem de erro do servidor.
# 4) O cliente pode imprimir o resultado em cada caso para validar o comportamento do sistema.

import xmlrpc.client

HOST = "127.0.0.1"
PORT = 8000


def testar_operacoes():
    try:
        servidor = xmlrpc.client.ServerProxy(f"http://{HOST}:{PORT}")

        operacoes = [
            ("soma", 10, 5),
            ("subtrai", 10, 5),
            ("multiplica", 10, 5),
            ("divide", 10, 5),
            ("divide", 10, 0),
        ]

        for nome, a, b in operacoes:
            resposta = getattr(servidor, nome)(a, b)
            print(f"{nome}({a}, {b}) -> {resposta}")

    except Exception as exc:
        print(f"Erro ao conectar com o servidor: {exc}")


if __name__ == "__main__":
    testar_operacoes()
