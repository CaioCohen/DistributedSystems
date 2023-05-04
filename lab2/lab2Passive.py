# servidor de echo: lado servidor
# com finalizacao do lado do servidor
# com multithreading (usa join para esperar as threads terminarem apos digitar 'fim' no servidor)
import socket
import select
import sys
import threading
import json

# define a localizacao do servidor
HOST = ''  # vazio indica que podera receber requisicoes a partir de qq interface de rede da maquina
PORT = 10001  # porta de acesso

# define a lista de I/O de interesse (jah inclui a entrada padrao)
entradas = [sys.stdin]
# armazena historico de conexoes
conexoes = {}
dicionario = {}

class Arquivo():

	def __init__(self, nome):
		self.nome = nome
	
	def recuperarConteudo(self):
		try: #caso dê erro na hora de ler o arquivo, então não deve ter nenhum arquivo ainda e ele ignora
			with open(self.nome, 'r') as f: 
				return json.load(f)
		except:
			return {}

	def atualizarConteudo(self, dicionario):
		with open(self.nome, 'w') as f:
			json.dump(dicionario, f)

	def resetarConteudo(self):
		with open(self.nome, 'w') as f:
			f.write('')

class DicionarioInteracoes():

	def __init__(self, dicionario):
		self.dicionario = dicionario

	def adicionaDicionario(self,chave, valor):
		valores = []
		if chave in self.dicionario:
			valores = self.dicionario[chave]
		valores.append(valor)
		self.dicionario[chave] = valores

	def recuperarValores(self, chave):
		allKeys = self.dicionario.keys()
		mensagem = ""
		if(chave in allKeys):
			mensagem = ",".join(sorted(self.dicionario[chave]))
		else:
			mensagem = "chave inexistente"
		return mensagem

def iniciaServidor():
	# cria o socket
	# Internet( IPv4 + TCP)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# vincula a localizacao do servidor
	sock.bind((HOST, PORT))

	# coloca-se em modo de espera por conexoes
	sock.listen(5)

	# configura o socket para o modo nao-bloqueante
	sock.setblocking(False)

	# inclui o socket principal na lista de entradas de interesse
	entradas.append(sock)

	return sock


def aceitaConexao(sock):

	# estabelece conexao com o proximo cliente
	clisock, endr = sock.accept()

	# registra a nova conexao
	conexoes[clisock] = endr

	return clisock, endr


def atendeRequisicoes(clisock, endr, dicionario):

	while True:
		# recebe dados do cliente
		data = clisock.recv(1024)
		if not data:  # dados vazios: cliente encerrou
			print(str(endr) + '-> encerrou')
			clisock.close()  # encerra a conexao com o cliente
			return
		print(str(endr) + ': ' + str(data, encoding='utf-8'))
		msg = str(data, encoding='utf-8')
		array = [x.strip() for x in msg.split(",")] # Ele irá pegar a string 'chave, valor' e colocar em um array ['chave', 'valor']
		if len(array) >= 2:
			for v in array[1:]:
				dicionario.adicionaDicionario(array[0], v)
			clisock.send(b"valor adicionado a chave")  # retorna mensagem de sucesso ao cliente
		else:
			mensagem = dicionario.recuperarValores(array[0])
			clisock.send(mensagem.encode())
                        



def main():
	global dicionario #recuperando a variavel global
	sock = iniciaServidor()
	print("Pronto para receber conexoes...")
	arq = Arquivo('dicionary.txt')
	dicionario = DicionarioInteracoes(arq.recuperarConteudo())

	clientes = [] # armazena as threads criadas para fazer join
	while True:
		leitura, escrita, excecao = select.select(entradas, [], [])

		# tratar todas as entradas prontas
		for pronto in leitura:
			if pronto == sock:  # pedido novo de conexao
				clisock, endr = aceitaConexao(sock)
				print('Conectado com: ', endr)
				# cria nova thread para atender o cliente
				cliente = threading.Thread(target=atendeRequisicoes, args=(clisock, endr, dicionario))
				cliente.start()
				clientes.append(cliente)  # armazena a referencia da thread para usar com join()
			elif pronto == sys.stdin:  # entrada padrao
				cmd = input()
				if cmd == 'fim':  # solicitacao de finalizacao do servidor
					for c in clientes:  # aguarda todas as threads terminarem
						c.join()
					arq.atualizarConteudo(dicionario.dicionario) # atualiza o valor salvo em disco
					sock.close()
					sys.exit()
				elif cmd == 'hist':  # outro exemplo de comando para o servidor
					print(str(conexoes.values()))
				elif cmd == 'salvar':
					arq.atualizarConteudo(dicionario.dicionario)
					print("dicionario salvo")
				elif cmd == "del":
					arq.resetarConteudo()
					dicionario = DicionarioInteracoes(arq.recuperarConteudo())
					print("dicionario resetado")



main()
