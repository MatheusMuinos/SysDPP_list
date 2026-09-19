# Cliente do exercício 02: serviço remoto de produtos.
# Envia operações ao servidor e imprime a resposta recebida.

import json
import socket

HOST = '127.0.0.1'
PORT = 5002


def enviar_requisicao(acao, **dados):
    """Envia uma operação para o servidor e recebe a resposta."""
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))
    mensagem = json.dumps({"acao": acao, "dados": dados}).encode('utf-8')
    cliente.sendall(mensagem)

    resposta = cliente.recv(4096)
    cliente.close()
    return json.loads(resposta.decode('utf-8'))


def run_client():
    """Cliente interativo para testar o serviço."""
    print('=== Sistema de Produtos ===')
    print('1 - cadastrar')
    print('2 - listar')
    print('3 - buscar')
    print('4 - remover')
    print('5 - sair')

    while True:
        opcao = input('\nEscolha uma opção: ').strip()

        if opcao == '1':
            nome = input('Nome: ').strip()
            preco = input('Preço: ').strip()
            print(enviar_requisicao('adicionar_produto', nome=nome, preco=preco))

        elif opcao == '2':
            print(enviar_requisicao('listar_produtos'))

        elif opcao == '3':
            nome = input('Nome do produto: ').strip()
            print(enviar_requisicao('buscar_produto', nome=nome))

        elif opcao == '4':
            nome = input('Nome do produto: ').strip()
            print(enviar_requisicao('remover_produto', nome=nome))

        elif opcao == '5':
            print('Encerrando cliente.')
            break

        else:
            print('Opção inválida.')


if __name__ == '__main__':
    run_client()
