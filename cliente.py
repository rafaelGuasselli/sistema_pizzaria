from usuario import Usuario

#A classe atendente é uma extensão do usuário que tem menos permissões.
class Cliente(Usuario):
	def __init__(self, nome:str=None, senha:str=None, cliente=None):
		if isinstance(cliente, Cliente):
			nome = nome or cliente.nome
			senha = senha or cliente.senha

		super(Cliente, self).__init__(nome=nome, senha=senha)

	def __str__(self) -> str:
		return "{:s}".format(self.nome)