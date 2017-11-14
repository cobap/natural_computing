# -*- coding: utf-8 -*-
import math, random

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
			print('Ponto Feromonio: ', ponto.feromonio)
			print('Ponto Distancia: ', ponto.distancia)
			probabilidade = (math.pow(ponto.feromonio, self.alfa) * math.pow(1.0 / ponto.distancia, self.beta))
			probabilidades.append(probabilidade)
		print('------------------------------------------------------------')
		somatoria_probabilidades = sum(float(prob) for prob in probabilidades)
		self.caminho_escolhido = 0
		self.index = -1
		for index, probabilidade in zip(range(len(probabilidades)), probabilidades):
			print('Probabilidade: ', probabilidade/somatoria_probabilidades)
			print('Distancia: ', self.getCaminhos()[index].distancia)
			if((probabilidade/somatoria_probabilidades) > self.caminho_escolhido):
				self.caminho_escolhido = (probabilidade/somatoria_probabilidades)
				self.index = index
		if(index == -1):
			return None
		else:
			return self.index, self.caminho_escolhido



class Formiga:
	def __init__(self, funcao, lugar):
		self.funcao = funcao
		self.lugar = lugar

		def caminhaAleatoriamente(self):
			probabilidade = (math.pow(feromonio, self.alfa) * math.pow(1.0 / distancia, self.beta)) / (somatorio if somatorio > 0 else 1)


#-------------------- MAIN --------------------#
if __name__ == "__main__":
	ponto1 = Ponto(10,4)
	ponto2 = Ponto(5,4)
	ponto3 = Ponto(3,7)
	ponto4 = Ponto(1,4)
	ponto5 = Ponto(9,3)
	ponto1.criaCaminho(ponto1, ponto2)
	ponto1.criaCaminho(ponto1, ponto3)
	ponto1.criaCaminho(ponto1, ponto4)
	ponto1.criaCaminho(ponto1, ponto5)
	print(ponto1.getProbabilidade())