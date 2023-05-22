#Ver documentação em: https://rpyc.readthedocs.io/en/latest/

# Cliente de echo usando RPC
import rpyc #modulo que oferece suporte a abstracao de RPC

# endereco do servidor de echo
SERVIDOR = 'localhost'
PORTA = 10001

def iniciaConexao():
	'''Conecta-se ao servidor.
	Saida: retorna a conexao criada.'''
	conn = rpyc.connect(SERVIDOR, PORTA) 
	
	print(type(conn.root)) # mostra que conn.root eh um stub de cliente
	print(conn.root.get_service_name()) # exibe o nome da classe (servico) oferecido

	return conn

def fazRequisicoes(conn):
	'''Faz requisicoes ao servidor e exibe o resultado.
	Entrada: conexao estabelecida com o servidor'''
	# le as mensagens do usuario ate ele digitar 'fim'
	print("Escreva o endpoint: getDicionario para recuperar o dicionario (getDicionario, chave)")
	print("Escreva o endpoint: putDicionario para alterar o dicionario ('putDicionario, chave, valor')")
	print("Escreva o endpoint: deleteDicionario para deletar uma chave do dicionario (deleteDicionario, chave)")
	print("Escreva fim para terminar")
	while True: 

		msg = input()
		array = [x.strip() for x in msg.split(",")]
		if array[0] == 'fim': break 
		elif array[0] == 'getDicionario':
			try:
				ret = conn.root.exposed_getDicionario(array[1])
				print(ret)
			except:
				print("error 401: Bad Request")
		elif array[0] == 'putDicionario':
			try:
				ret = conn.root.exposed_putDicionario(array[1], array[2:])
				print(ret)
			except:
				print("error 401: Bad Request")
		elif array[0] == 'deleteDicionario':
			try:
				ret = conn.root.exposed_deleteDicionario(array[1])
				print(ret)
			except:
				print("error 401: Bad Request")

		else:
			print("chave invalida")

		# envia a mensagem do usuario para o servidor
		#ret = conn.root.exposed_echo(msg)

		# imprime a mensagem recebida

	# encerra a conexao
	conn.close()

def main():
	'''Funcao principal do cliente'''
	#inicia o cliente
	conn = iniciaConexao()
	#interage com o servidor ate encerrar
	fazRequisicoes(conn)

# executa o cliente
if __name__ == "__main__":
	main()