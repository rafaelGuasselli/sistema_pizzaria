#A classe mercadoria é usada para abstrair as funções da pizza, bebida, extra pra que quem esteja usando eles possa ter certeza de que tem essas funções. 
class Mercadoria:
	def __init__(self, nome:str=None, preco:float=None, quantidade:int=None, mercadoria=None):
		if isinstance(mercadoria, Mercadoria):
			nome = nome or mercadoria.nome
			preco = preco or mercadoria.preco
			quantidade = quantidade or mercadoria.quantidade

		self.nome = nome or ""
		self.preco = preco or 0
		self.quantidade = quantidade
		
	#Função padrão de calcular o preço
	def calcularTotal(self) -> float:
		quantidade = self.quantidade or 1
		return self.preco * quantidade

	#Formata a mercadoria para ser printada no sistema
	def __str__(self) -> str:
		return "{:n}x{:s} - R${:.2f}".format(self.quantidade, self.nome, self.calcularTotal())