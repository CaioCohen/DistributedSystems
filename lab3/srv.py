#Ver documentação em: https://rpyc.readthedocs.io/en/latest/

# Servidor de echo usando RPC 
import rpyc #modulo que oferece suporte a abstracao de RPC
import json

#servidor que dispara um processo filho a cada conexao
from rpyc.utils.server import ForkingServer 

# porta de escuta do servidor de echo
PORTA = 10001

class Arquivo():

	def __init__(self, nome):
		self.nome = nome
	
	def recuperarConteudo(self):
		try: #caso dê erro na hora de ler o arquivo, então não deve ter nenhum arquivo ainda e ele ignora
			with open(self.nome, 'r') as f: 
				return json.load(f)
		except:
			return -1

	def atualizarConteudo(self, dicionario):
		with open(self.nome, 'w') as f:
			json.dump(dicionario, f)

	def resetarConteudo(self):
		with open(self.nome, 'w') as f:
			f.write('{"chave": ["valor 1"]}') # deixa salvo um valor padrão para tipar a variável


# classe que implementa o servico de echo
class Echo(rpyc.Service):
	# executa quando uma conexao eh criada
	def on_connect(self, conn):
		print("Conexao iniciada:")

	# executa quando uma conexao eh fechada
	def on_disconnect(self, conn):
		print("Conexao finalizada:")

	# imprime e ecoa a mensagem recebida
	def exposed_echo(self, msg):
		print(msg)
		return msg
	
	def exposed_getDicionario(self, chave):
		try:
			arq = Arquivo("dicionario.txt")
			dic = arq.recuperarConteudo() #O programa não funcionará se não vier um dicionario
			while(dic == -1):
				arq.resetarConteudo()
				dic = arq.recuperarConteudo()
			allKeys = dic.keys()
			mensagem = ""
			if(chave in allKeys):
				mensagem = ",".join(sorted(dic[chave]))
			else:
				mensagem = "chave inexistente"
			return mensagem
		except:
			return "Error 500: Internal server error"
		
	def exposed_putDicionario(self, chave, valores):
		try:
			arq = Arquivo("dicionario.txt")
			dic = arq.recuperarConteudo() #O programa não funcionará se não vier um dicionario
			while(dic == -1):
				arq.resetarConteudo()
				dic = arq.recuperarConteudo()
			print(chave)
			print(valores)
			dic[chave] = valores
			arq.atualizarConteudo(dic)
			return "dicionario atualizado"
			
		except:
			return "Error 500: Internal server error"
		
	def exposed_deleteDicionario(self, chave):
		try:
			arq = Arquivo("dicionario.txt")
			dic = arq.recuperarConteudo() #O programa não funcionará se não vier um dicionario
			while(dic == -1):
				arq.resetarConteudo()
				dic = arq.recuperarConteudo()
			del dic[chave]
			arq.atualizarConteudo(dic)
			return "chave " + chave + " deletada"
			
		except:
			return "Error 500: Internal server error"
		
  
# dispara o servidor
if __name__ == "__main__":
	srv = ForkingServer(Echo, port = PORTA)
	srv.start()


### Tipos de servidores
#https://rpyc.readthedocs.io/en/latest/api/utils_server.html

#servidor que dispara uma nova thread a cada conexao
#from rpyc.utils.server import ThreadedServer

#servidor que atende uma conexao e termina
#from rpyc.utils.server import OneShotServer

### Configuracoes do protocolo RPC
#https://rpyc.readthedocs.io/en/latest/api/core_protocol.html#rpyc.core.protocol.DEFAULT_CONFIG