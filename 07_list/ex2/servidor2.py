# Perguntas da atividade:
# 1) Como o servidor guarda os produtos?
#    Os produtos são armazenados em memória em um dicionário Python.
# 2) O que acontece quando o servidor é reiniciado?
#    Todos os produtos desaparecem, porque o estado não é persistido em arquivo ou banco de dados.
# 3) Qual seria a solução para manter os dados após reiniciar o servidor?
#    Salvar os dados em disco (por exemplo, em JSON ou banco de dados) e carregá-los na inicialização.
#
# Exercício 02: serviço remoto de produtos.
# Regras do exercício:
# - O servidor deve manter o catálogo em memória.
# - O cliente envia pedidos para adicionar, listar, buscar e remover produtos.
# - Cada operação deve responder com um dicionário contendo ok, resultado e erro.
# - Quando o servidor reinicia, a memória é apagada.

import json
import socket
import threading

HOST = '127.0.0.1'
PORT = 5002

# Estado do servidor em memória.
produtos = {}


def adicionar_produto(nome, preco):
    """Cadastra um produto no catálogo."""
    nome = str(nome).strip()
    if not nome:
        return {"ok": False, "resultado": None, "erro": "Nome do produto é obrigatório."}

    try:
        preco = float(preco)
    except (TypeError, ValueError):
        return {"ok": False, "resultado": None, "erro": "Preço inválido."}

    if preco < 0:
        return {"ok": False, "resultado": None, "erro": "Preço não pode ser negativo."}

    if nome in produtos:
        return {"ok": False, "resultado": None, "erro": f"Produto '{nome}' já existe."}

    produtos[nome] = preco
    return {"ok": True, "resultado": f"Produto '{nome}' cadastrado com sucesso.", "erro": None}


def listar_produtos():
    """Lista todos os produtos cadastrados."""
    catalogo = [{"nome": nome, "preco": preco} for nome, preco in produtos.items()]
    return {"ok": True, "resultado": catalogo, "erro": None}


def buscar_produto(nome):
    """Busca um produto pelo nome."""
    nome = str(nome).strip()
    if nome not in produtos:
        return {"ok": False, "resultado": None, "erro": f"Produto '{nome}' não encontrado."}
    return {"ok": True, "resultado": {"nome": nome, "preco": produtos[nome]}, "erro": None}


def remover_produto(nome):
    """Remove um produto do catálogo."""
    nome = str(nome).strip()
    if nome not in produtos:
        return {"ok": False, "resultado": None, "erro": f"Produto '{nome}' não encontrado."}

    produto = produtos.pop(nome)
    return {"ok": True, "resultado": f"Produto '{nome}' removido. Preço: {produto}", "erro": None}


def executar_requisicao(dados):
    """Executa uma operação recebida do cliente."""
    acao = dados.get("acao")
    parametros = dados.get("dados", {})

    funcoes = {
        "adicionar_produto": adicionar_produto,
        "listar_produtos": listar_produtos,
        "buscar_produto": buscar_produto,
        "remover_produto": remover_produto,
    }

    if acao not in funcoes:
        return {"ok": False, "resultado": None, "erro": "Operação inválida."}

    return funcoes[acao](**parametros)


def handle_client(conn, addr):
    """Processa as requisições do cliente."""
    print(f"[CONEXAO] {addr} conectado.")
    with conn:
        while True:
            try:
                dados = conn.recv(4096)
                if not dados:
                    break

                requisicao = json.loads(dados.decode('utf-8'))
                resposta = executar_requisicao(requisicao)
                conn.sendall(json.dumps(resposta).encode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                resposta = {"ok": False, "resultado": None, "erro": "Requisição inválida."}
                conn.sendall(json.dumps(resposta).encode('utf-8'))
            except ConnectionError:
                break

    print(f"[CONEXAO] {addr} encerrada.")


def run_server():
    """Inicia o servidor do serviço remoto."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Servidor rodando em {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    finally:
        server.close()


if __name__ == '__main__':
    run_server()
