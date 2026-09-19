# Cliente do exercício 03: serviço remoto de notas.
# Envia requisições para o servidor e mostra a resposta retornada.

import json
import socket

HOST = '127.0.0.1'
PORT = 5003


def enviar_requisicao(acao, **dados):
    """Envia uma operação para o servidor e recebe o resultado."""
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))
    mensagem = json.dumps({"acao": acao, "dados": dados}).encode('utf-8')
    cliente.sendall(mensagem)

    resposta = cliente.recv(4096)
    cliente.close()
    return json.loads(resposta.decode('utf-8'))


def run_client():
    """Cliente interativo para testar o serviço de notas."""
    print('=== Serviço de Notas ===')
    print('1 - adicionar nota')
    print('2 - calcular média')
    print('3 - verificar situação')
    print('4 - sair')

    while True:
        opcao = input('\nEscolha uma opção: ').strip()

        if opcao == '1':
            nome = input('Nome do aluno: ').strip()
            nota = input('Nota: ').strip()
            print(enviar_requisicao('adicionar_nota', nome=nome, nota=nota))

        elif opcao == '2':
            nome = input('Nome do aluno: ').strip()
            print(enviar_requisicao('calcular_media', nome=nome))

        elif opcao == '3':
            nome = input('Nome do aluno: ').strip()
            print(enviar_requisicao('verificar_situacao', nome=nome))

        elif opcao == '4':
            print('Encerrando cliente.')
            break

        else:
            print('Opção inválida.')


if __name__ == '__main__':
    run_client()
