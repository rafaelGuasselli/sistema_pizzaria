from mercadoria import Mercadoria
from extra import Extra

class Pizza(Mercadoria):
	def __init__(self, nome:str=None, preco:float=None, quantidade:int=None, extras:list=None, pizza=None):
		if isinstance(pizza, Pizza):
			nome = nome or pizza.nome
			preco = preco or pizza.preco
			extras = extras or pizza.extras
			quantidade = quantidade or pizza.quantidade

		self.extras = extras or []
		super(Pizza, self).__init__(nome=nome, preco=preco, quantidade=quantidade)
		
	def calcularTotal(self) -> float:
		preco = self.preco
		quantidade = self.quantidade or 1

		if not isinstance(self.extras, list):
			self.extras = []

		for extra in self.extras:
			if not isinstance(extra, Extra):
				continue
			preco += extra.calcularTotal()
		
		return float(preco * quantidade)

	#Formata a pizza junto com os extras
	def __str__(self) -> str:
		if not isinstance(self.extras, list):
			self.extras = []

		string = ""
		if self.quantidade: 
			string += "{:n}x{:s}".format(self.quantidade, self.nome)
		else:
			string += "{:s}".format(self.nome)

		for i in range(1, len(self.extras)+1):
			if i == 1:
				string += "com: "
			else:
				string += ", "

			string += str(self.extras[i])
		
		string += " - R${:.2f}".format(self.calcularTotal())
		return string