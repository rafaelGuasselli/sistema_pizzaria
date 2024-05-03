import os
from pizza import Pizza
from pedido import Pedido
from cliente import Cliente
from atendente import Atendente

class Sistema:
	def __init__(self):
		#São usados para salvar dados
		self.extras = []
		self.bebidas = []
		
		self.pedidosAtuais = []
		self.pedidosPassados = []
		self.pizzas = [
			Pizza(nome="Calabresa", preco=50),
			Pizza(nome="4 queijo", preco=40),
			Pizza(nome="Alho e óleo", preco=40),
		]
		self.clientes = {
			"teste": Cliente(nome="teste", senha="123")
		}
		self.atendentes = {
			"admin": Atendente(nome="admin", senha="admin")
		}

		#São usados para salvar o estado do sistema atual
		self.usuarioAtual = None
		self.menuLoop = True

		#São usados para salvar o estado do pedido atual
		self.clienteAtual = None
		self.pedidoAtual = None
		self.pedidoLoop = False
	
	# O menu principal mostra todas as ações que o usuario atual pode realizar
	def menuPrincipal(self):
		opcoes = {
			"deslogado": [
				("Registrar", self.registrar),
				("Logar", self.login),
				("Sair", self.sair),
			],
			"atendente": [
				("Adicionar pizza", self.adicionarPizza),
				("Listar pizzas", self.listarPizzas),
				("Editar pizza", self.editarPizza),
				("Remover pizza", self.removerPizza),
				("Listar clientes", self.listarClientes),
				("Listar pedidos não entregues", self.listarPedidosAtuais),
				("Listar pedidos entregues", self.listarPedidosPassados),
				("Registrar pedido", self.registrarPedido),
				("Entregar pedido", self.entregarPedido),
				("Deslogar", self.deslogar),
				("Sair", self.sair),
			],
			"cliente": [
				("Fazer pedido", self.fazerPedido),
				("Receber pedido", self.receberPedido),
				("Deslogar", self.deslogar),
				("Sair", self.sair),
			]
		}

		while self.menuLoop:
			modo = ""
			if isinstance(self.usuarioAtual, Atendente):
				modo = "atendente"
			elif isinstance(self.usuarioAtual, Cliente):
				modo = "cliente"
			else:
				modo = "deslogado"

			self.exibirMenuDeOpcoes(opcoes[modo])


	#-----------------------------------Opções do menu-----------------------------------

	#Seleciona o cliente e abre o menu de pedidos
	def registrarPedido(self) -> str:
		cliente = Cliente()
		nome = input("Qual o nome do cliente? ")
		if nome in self.clientes:
			cliente = self.clientes[nome]
		else:
			cliente.nome = nome
			cliente.senha = "123"
			self.clientes[nome] = cliente

		self.clienteAtual = cliente
		self.pedidoAtual = Pedido(entregue=False, cliente=self.clienteAtual, mercadorias=[])
		self.menuPedido()

		return "Pedido realizado!"
	

	#Seleciona o cliente e abre o menu de pedidos
	def fazerPedido(self) -> str:
		self.clienteAtual = self.usuarioAtual
		self.pedidoAtual = Pedido(entregue=False, cliente=self.clienteAtual, mercadorias=[])
		self.menuPedido()

		return "Pedido realizado!"

	#Abre um menu com opções do pedido atual
	def menuPedido(self):
		opcoes = [
			("Selecionar pizza", self.selecionarPizza),
			("Finalizar pedido", self.finalizarPedido)
		]

		self.pedidoLoop = True
		while self.pedidoLoop:
			self.exibirMenuDeOpcoes(opcoes)

	#Abre um menu para selecionar uma pizza
	def selecionarPizza(self):
		while True:
			id = self.pegarIndexLista("Qual pizza você deseja?", self.pizzas)
			if id != -1:
				quantidade = 0
				while True:
					quantidade = input("Quantas? ")
					if quantidade.isnumeric():
						quantidade = int(quantidade)
						if quantidade > 0:
							self.clear()
							break
					print("Quantidade invalida!")

				self.pedidoAtual.mercadorias.append(Pizza(pizza=self.pizzas[id], quantidade=quantidade))
				break
			self.clear()
			print("Id invalido!\n")
			
	#Finaliza um pedido
	def finalizarPedido(self):
		self.pedidoLoop = False

		endereco = input("Qual o endereco? ")
		self.pedidoAtual.endereco = endereco

		self.pedidosAtuais.append(self.pedidoAtual)
		self.pedidoAtual = None
		self.clienteAtual = None


	#Remove um pedido dos pedidos atuais - Usado pelo atendente
	def entregarPedido(self) -> str:
		if len(self.pedidosAtuais) == 0:
			return "Não existem pedidos atualmente!"

		id = self.pegarIndexLista("Qual o numero do pedido? ", self.pedidosAtuais)
		if id == -1:
			return "Id invalido!"
		pedido = self.pedidosAtuais[id]
		pedido.entregue = True
		self.pedidosAtuais.remove(pedido)
		self.pedidosPassados.append(pedido)
		return "Entregue: " + str(pedido)
	
	#Remove um pedido dos pedidos atuais - Usado pelo cliente
	def receberPedido(self) -> str:
		pedidosDoCliente = []
		for pedido in self.pedidosAtuais:
			if pedido.cliente == self.usuarioAtual:
				pedidosDoCliente.append(pedido)

		if len(pedidosDoCliente) == 0:
			return "Não existem pedidos atualmente!"

		id = self.pegarIndexLista("Qual o numero do pedido? ", pedidosDoCliente)
		if id == -1:
			return "Id invalido!"
		
		pedido = pedidosDoCliente[id]
		pedido.entregue = True
		self.pedidosAtuais.remove(pedido)
		self.pedidosPassados.append(pedido)
		return "Entregue: " + str(pedido)

	#-----------------------------------CRUD-----------------------------------
	#Adicionar uma pizza na lista de pizzas
	def adicionarPizza(self) -> str:
		entradas = ["Nome: ", "Preço: "]
		nome = ""
		preco = 0
		while True:
			valores = self.exibirMenuDeEntradas(entradas)
			nome = valores["Nome: "]
			preco = valores["Preço: "]

			if preco.isnumeric():
				preco = float(preco)
				break

			self.clear()
			print("Preço invalido")

		pizza = Pizza(nome=nome, preco=float(preco))
		self.pizzas.append(pizza)
		return "Pizza adicionada!"

	#Edita uma pizza na lista de pizzas
	def editarPizza(self) -> str:
		id = self.pegarIndexLista("Qual numero da pizza para editar?", self.pizzas)
		if id == -1:
			return "Id invalido!"

		entradas = ["Nome: ", "Preço: "]
		nome = ""
		preco = 0
		while True:
			valores = self.exibirMenuDeEntradas(entradas)
			nome = valores["Nome: "]
			preco = valores["Preço: "]

			if preco.isnumeric():
				preco = float(preco)
				break

			self.clear()
			print("Preço invalido")

		self.pizzas[id].nome = nome
		self.pizzas[id].preco = preco
		return "Pizza editada!"
	
	#Remove uma pizza na lista de pizzas
	def removerPizza(self) -> str:
		id = self.pegarIndexLista("Qual numero da pizza para remover?", self.pizzas)
		if id == -1:
			return "Id invalido!"

		del self.pizzas[id]
		return "Pizza removida!"
	
	#Retorna uma lista de clientes formatada
	def listarClientes(self) -> str:
		return self.formatarLista(self.clientes)

	#Retorna uma lista de pizzas formatada
	def listarPizzas(self) -> str:
		return self.formatarLista(self.pizzas)
	
	#Retorna uma lista de pedidos atuais formatada
	def listarPedidosAtuais(self) -> str:
		return self.formatarLista(self.pedidosAtuais)
	
	#Retorna uma lista de pedidos passados formatada
	def listarPedidosPassados(self) -> str:
		return self.formatarLista(self.pedidosPassados)
	



	#-----------------------------------Entrada/Saida utils-----------------------------------
 	#Exibe uma lista e pede para o usuário selecionar um index
	def pegarIndexLista(self, mensagem, lista) -> int:
		self.clear()
		print(self.formatarLista(lista))
		id = input(mensagem)

		if id.isnumeric():
			id = int(id)-1
		else:
			return -1
		
		if id < 0 or id >= len(lista):
			return -1
		
		return id

	#Pede uma lista de informações e retorna em um dict
	def exibirMenuDeEntradas(self, entradas):
		valores = {}
		for entrada in entradas:
			valores[entrada] = input(entrada)
		return valores

	#Retorna uma string de uma lista formatada
	def formatarLista(self, lista) -> str:
		string = ""
		i = 1
		for elemento in lista:
			string += "{:n}. {:s}\n".format(i, str(elemento))
			i += 1
		return string

	#Pega uma lista de tuplas com (Nome, função) e exibe um menu de opções para o usuario
	def exibirMenuDeOpcoes(self, opcoes):
		for i in range(0, len(opcoes)):
			nome, func = opcoes[i]
			print("{:n}. {:s}".format(i+1, nome))
		
		escolha = input("Digite o numero da opção: ")
		if escolha.isnumeric():
			escolha = int(escolha)-1
		else:
			escolha = -1

		if escolha >= 0 and escolha < len(opcoes):
			self.clear()
			nome, func = opcoes[escolha]
			mensagemFinal = func()
			if isinstance(mensagemFinal, str):
				self.clear()
				print(mensagemFinal)
				print("------------")
		else:
			self.clear()
			print("Opção não existe!\n")

	#Limpa o terminal
	def clear(self):
		os.system('clear')

	#Fecha o sistema
	def sair(self):
		self.menuLoop = False
		return "Finalizando o sistema!"





	#-----------------------------------Login-----------------------------------
	#Desloga o usuário atual
	def deslogar(self) -> str:
		self.usuarioAtual = None
		return "Deslogado!"

	#Menu login
	def login(self) -> str:
		modo = input("Logar como cliente ou atendente? (C ou A)")
		if modo.lower() == "c":
			return self.__login(self.clientes)
		else:
			return self.__login(self.atendentes)

	#Loga um atendente ou cliente
	def __login(self, usuarios) -> str:
		print("Login\n")
		nome = input("Nome: ")
		senha = input("Senha: ")

		if nome in usuarios:
			usuario = usuarios[nome]
			if usuario.senha == senha:
				self.usuarioAtual = usuario
				return "Logado!"
		return "Usuário ou senha invalido!"

	#Menu registro
	def registrar(self) -> str:
		modo = input("Criar cliente ou atendente? (C ou A)")
		if modo.lower() == "c":
			self.__registrar(self.clientes, Cliente)
		else:
			self.__registrar(self.atendentes, Atendente)

		return "Usuario registrado!"

	#Registra um atendente ou cliente
	def __registrar(self, usuarios, instanciar):
		nome = ""

		print("Registrar")
		while True:
			nome = input("Nome: ")
			if not nome in usuarios:
				break
			else:
				print("Nome já existe!")

		senha = input("Senha: ")
		usuarios[nome] = instanciar(nome=nome, senha=senha)