from mercadoria import Mercadoria

#A classe bebida é usada para separar os tipos de mercadoria na UI.
#Provavelmente não vai ser usada porque eu não tive tempo
class Bebida(Mercadoria):
	def __init__(self, nome:str=None, preco:float=None, quantidade:int=None, bebida=None):
		if isinstance(bebida, Bebida):
			nome = nome or bebida.nome
			preco = preco or bebida.preco
			quantidade = quantidade or bebida.quantidade

		super(Bebida, self).__init__(nome=nome, preco=preco, quantidade=quantidade)