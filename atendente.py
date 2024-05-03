from usuario import Usuario

#A classe atendente é uma extensão do usuário que tem mais permissões
class Atendente(Usuario):
	def __init__(self, nome:str=None, senha:str=None, atendente=None):
		if isinstance(atendente, Atendente):
			nome = nome or atendente.nome
			senha = senha or atendente.senha

		super(Atendente, self).__init__(nome=nome, senha=senha)

	def __str__(self) -> str:
		return "{:s}".format(self.nome)