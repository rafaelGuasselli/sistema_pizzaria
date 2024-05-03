from mercadoria import Mercadoria

#A classe extra é usada para separar os tipos de mercadoria na UI.
#Provavelmente não vai ser usada porque eu não tive tempo
class Extra(Mercadoria):
	def __init__(self, nome:str=None, preco:float=None, quantidade:int=None, mostrarPreco:bool=None, extra=None):
		if isinstance(extra, Extra):
			nome = nome or extra.nome
			preco = preco or extra.preco
			quantidade = quantidade or extra.quantidade
			mostrarPreco = mostrarPreco or extra.mostrarPreco

		self.mostrarPreco = mostrarPreco or False
		super(Extra, self).__init__(nome=nome, preco=preco, quantidade=quantidade)
		
	def __str__(self) -> str:
		string = ""
		if self.quantidade > 1:
			string = "{:n}x{:s}".format(self.quantidade, self.nome)
		else:
			string = "{:s}".format(self.nome)
		
		if self.mostrarPreco:
			string += " - R${:.2f}".format(self.calcularTotal())
		
		return string