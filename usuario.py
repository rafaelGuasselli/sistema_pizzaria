class Usuario:
	def __init__(self, nome:str=None, senha:str=None, usuario=None):
		if isinstance(usuario, Usuario):
			nome = nome or usuario.nome
			senha = senha or usuario.senha

		self.nome = nome or ""
		self.senha = senha or ""

	def podeAlterarMercadorias(self) -> bool:
		return False

	def __str__(self) -> str:
		return "{:s}".format(self.nome)