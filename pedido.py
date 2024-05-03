from cliente import Cliente
from mercadoria import Mercadoria

#O pedido é usado para salvar as mercadorias compradas e calcular o preço total
class Pedido:
	def __init__(self, mercadorias:list=None, cliente:Cliente=None, entregue:bool=None, endereco:str=None,  pedido=None):
		if isinstance(pedido, Pedido):
			cliente = cliente or pedido.cliente
			entregue = entregue or pedido.entregue
			endereco = endereco or pedido.endereco
			mercadorias = mercadorias or pedido.mercadorias

		self.cliente = cliente
		self.entregue = entregue or False
		self.endereco = endereco
		self.mercadorias = mercadorias
	
	def calcularTotal(self) -> float:
		preco = 0
		for mercadoria in self.mercadorias:
			if not isinstance(mercadoria, Mercadoria):
				continue
			preco += mercadoria.calcularTotal()
		
		return float(preco)

	#Formata o pedido em forma de nota fiscal
	def __str__(self) -> str:
		string = ""
		string += "\n------------\n"
		string += "Endereço: {:s}\n".format(self.endereco)
		string += "Cliente: {:s}\n".format(str(self.cliente))
		for mercadoria in self.mercadorias:
			string += str(mercadoria) + "\n"
		string += "Total: R${:.2f}".format(self.calcularTotal())
		string += "\n------------\n"
		return string