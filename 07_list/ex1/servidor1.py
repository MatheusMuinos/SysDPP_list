# Respostas da atividade:
# 1) O servidor deve registrar as funções soma, subtrai, multiplica e divide usando
#    SimpleXMLRPCServer e a função register_function.
# 2) O cliente deve chamar cada operação pelo proxy do servidor e apresentar o retorno
#    em formato padronizado com ok, resultado e erro.
# 3) A divisão por zero deve ser tratada no servidor para não encerrar o processo.
# 4) A estrutura retornada deve seguir o padrão: {"ok": True/False, "resultado": valor, "erro": mensagem}
#
# Esse exemplo implementa a calculadora remota em Python com XML-RPC.

import xmlrpc.server

HOST = "127.0.0.1"
PORT = 8000


def resposta(ok, resultado=None, erro=None):
    """Padroniza a resposta da operação remota."""
    return {"ok": ok, "resultado": resultado, "erro": erro}


def soma(a, b):
    return resposta(True, a + b, None)


def subtrai(a, b):
    return resposta(True, a - b, None)


def multiplica(a, b):
    return resposta(True, a * b, None)


def divide(a, b):
    try:
        if b == 0:
            return resposta(False, None, "Erro: divisão por zero.")
        return resposta(True, a / b, None)
    except Exception as exc:
        return resposta(False, None, f"Erro: {exc}")


def iniciar_servidor():
    servidor = xmlrpc.server.SimpleXMLRPCServer((HOST, PORT), allow_none=True)
    servidor.register_function(soma, "soma")
    servidor.register_function(subtrai, "subtrai")
    servidor.register_function(multiplica, "multiplica")
    servidor.register_function(divide, "divide")

    print(f"Servidor XML-RPC ativo em http://{HOST}:{PORT}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário.")
        servidor.server_close()


if __name__ == "__main__":
    iniciar_servidor()
