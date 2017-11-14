# -*- coding: utf-8 -*-
import math, random, copy

class Caminho:
	def __init__(self, pontoA, pontoB):
		self.pontoA = pontoA
		self.pontoB = pontoB
		self.distancia = 0
		self.feromonio = (random.randint(5,9)/10000.0) + (random.randint(1,9)/100000.0)
		# self.feromonio = 400	

	def setDistancia(self, distancia):
		self.distancia = distancia

class Ponto:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.caminhos = []
		self.alfa=1.0
		self.beta=5.0
		self.objeto = False
		self.nome = self.setNome()

	def setNome(self):
		letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
		letra = random.randint(0, len(letras)-1)
		numero = random.randint(1,100)
		return str(letra) + str(letras[letra])

	def criaCaminho(self, pontoA, pontoB):
		novo_caminho = Caminho(pontoA, pontoB)
		novo_caminho.setDistancia(self.setDistancia(pontoB))
		self.caminhos.append(novo_caminho)

	def setDistancia(self, pontoB):
		return math.sqrt(pow(self.x - pontoB.x ,2) + pow(self.y - pontoB.y ,2))

	def getCaminhos(self):
		return self.caminhos

	def getProbabilidade(self):
		probabilidades = []
		for ponto in self.getCaminhos():
			# print('Ponto Feromonio: ', ponto.feromonio)
			# print('Ponto Distancia: ', ponto.distancia)
			probabilidade = (math.pow(ponto.feromonio, self.alfa) * math.pow(1.0 / ponto.distancia, self.beta))
			probabilidades.append(probabilidade)
		print('------------------------------------------------------------')
		somatoria_probabilidades = sum(float(prob) for prob in probabilidades)
		self.caminho_escolhido = 0
		self.index = -1
		for index, probabilidade in zip(range(len(probabilidades)), probabilidades):
			# print('Probabilidade: ', probabilidade/somatoria_probabilidades)
			# print('Distancia: ', self.getCaminhos()[index].distancia)
			if((probabilidade/somatoria_probabilidades) > self.caminho_escolhido):
				self.caminho_escolhido = (probabilidade/somatoria_probabilidades)
				self.index = index
		
		return self.index, self.getCaminhos()[self.index], self.caminho_escolhido

	def setObjeto(self, status):
		self.objeto = status

	def getObjeto(self):
		return self.objeto

class Cidade:
	def __init__(self):
		self.numero_pontos = random.randint(5, 10)
		self.pontos = []
		self.formigas = []
		self.caminhos = []
		print('QTD PONTOS: ', self.numero_pontos)
		for ponto in range(self.numero_pontos):
			a = Ponto(random.randint(1,10), random.randint(1,10))
			self.pontos.append(a)
			print('CRIADO PONTO', a.nome)
		self.criaConexao()

	def criaConexao(self):
		self.pontos_backup = copy.copy(self.pontos)
		self.pontos_aux = []
		
		while(len(self.pontos_backup) > 0):
			ponto = self.pontos_backup.pop(random.randint(0, len(self.pontos_backup)-1))
			if(len(self.pontos_aux) > 0):
				b = self.pontos_aux[random.randint(0, len(self.pontos_aux)-1)]
				self.caminhos.append(Caminho(ponto, b))
				b.criaCaminho(b, ponto)
				ponto.criaCaminho(ponto, b)
			self.pontos_aux.append(ponto)

	def mostraCidade(self):
		for ponto in range(self.numero_pontos):
			print('Ponto: ', self.pontos[ponto].nome)
			# print('\tNome Caminho', self.pontos[ponto].getCaminhos())
			for caminhos in self.pontos[ponto].getCaminhos():
				print('\tCaminho: ', caminhos.pontoA.nome, caminhos.pontoB.nome)

	def criaFormigas(self):
		self.qtdFormigas = int(round((float) (self.numero_pontos * 1)/3))
		# print('Qtd de Formigas: ', self.qtdFormigas)
		for formiga in range(self.qtdFormigas):
			self.formigas.append(Formiga('Patrulha', self.getPontoAleatorio()))

	def getPontoAleatorio(self):
		while(True):
			pontoAleatorio = random.randint(0	, self.numero_pontos-1)
			# print(pontoAleatorio)
			# print(self.pontos[pontoAleatorio].getObjeto())
			if self.pontos[pontoAleatorio].getObjeto() == False:
				return self.pontos[pontoAleatorio]



class Formiga:
	def __init__(self, funcao, pontoAtual):
		self.funcao = funcao
		self.pontoAtual = pontoAtual
		self.pontoAtual.setObjeto(True)

	def caminhaAleatoriamente(self):
		print(self.pontoAtual.getProbabilidade())

#-------------------- MAIN --------------------#
if __name__ == "__main__":
	''' 1°TESTE
	ponto1 = Ponto(10,4)
	ponto2 = Ponto(5,4)
	ponto3 = Ponto(3,7)
	ponto4 = Ponto(1,4)
	ponto5 = Ponto(9,3)
	ponto1.criaCaminho(ponto1, ponto2)
	ponto1.criaCaminho(ponto1, ponto3)
	ponto1.criaCaminho(ponto1, ponto4)
	ponto1.criaCaminho(ponto1, ponto5)

	form1 = Formiga('Patrulha', ponto1)
	form1.caminhaAleatoriamente()
	'''

	cidade1 = Cidade()
	cidade1.criaFormigas()
	# cidade1.mostraCidade()