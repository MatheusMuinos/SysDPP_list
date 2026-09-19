# Respostas da atividade:
# 1) O servidor guarda as notas de cada aluno em memória em um dicionário.
# 2) A operação adicionar_nota valida se a nota está entre 0 e 10.
# 3) calcular_media retorna a média das notas do aluno e verificar_situacao classifica a situação.
# 4) Se o aluno não existir ou não tiver notas, o servidor responde com ok False e uma mensagem de erro.
#
# Exercício 03: serviço remoto de notas.

import json
import socket
import threading

HOST = '127.0.0.1'
PORT = 5003

# Estado do servidor em memória.
# Ao reiniciar o servidor, todas as notas serão perdidas.
alunos = {}


def adicionar_nota(nome, nota):
    """Adiciona uma nota para um aluno."""
    nome = str(nome).strip()
    if not nome:
        return {"ok": False, "resultado": None, "erro": "Nome do aluno é obrigatório."}

    try:
        nota = float(nota)
    except (TypeError, ValueError):
        return {"ok": False, "resultado": None, "erro": "Nota inválida."}

    if nota < 0 or nota > 10:
        return {"ok": False, "resultado": None, "erro": "Nota inválida: use valores de 0 a 10."}

    if nome not in alunos:
        alunos[nome] = []

    alunos[nome].append(nota)
    return {"ok": True, "resultado": f"Nota {nota} adicionada para {nome}.", "erro": None}


def calcular_media(nome):
    """Calcula a média das notas do aluno."""
    nome = str(nome).strip()
    if nome not in alunos or not alunos[nome]:
        return {"ok": False, "resultado": None, "erro": f"Aluno '{nome}' não encontrado ou sem notas."}

    media = sum(alunos[nome]) / len(alunos[nome])
    return {"ok": True, "resultado": round(media, 2), "erro": None}


def verificar_situacao(nome):
    """Classifica a situação do aluno conforme a média."""
    nome = str(nome).strip()
    if nome not in alunos or not alunos[nome]:
        return {"ok": False, "resultado": None, "erro": f"Aluno '{nome}' não encontrado ou sem notas."}

    media = sum(alunos[nome]) / len(alunos[nome])

    if media >= 7.0:
        situacao = "Aprovado"
    elif 5.0 <= media < 7.0:
        situacao = "Recuperação"
    else:
        situacao = "Reprovado"

    return {"ok": True, "resultado": {"nome": nome, "media": round(media, 2), "situacao": situacao}, "erro": None}


def executar_requisicao(dados):
    """Executa uma operação recebida do cliente."""
    acao = dados.get('acao')
    parametros = dados.get('dados', {})

    funcoes = {
        'adicionar_nota': adicionar_nota,
        'calcular_media': calcular_media,
        'verificar_situacao': verificar_situacao,
    }

    if acao not in funcoes:
        return {"ok": False, "resultado": None, "erro": "Operação inválida."}

    return funcoes[acao](**parametros)


def handle_client(conn, addr):
    """Processa requisições concorrentes do cliente."""
    print(f"[CONEXAO] {addr} conectou.")
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
    """Inicia o servidor do serviço de notas."""
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
