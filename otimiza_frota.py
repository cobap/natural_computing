# -*- coding: utf-8 -*-
import math, random, copy
import networkx as nx
import matplotlib.pyplot as plt

'''
*	Class Ponto:
*	Responsável por um vertice da cidade
*	Possui a cordenada X e Y usada para calculo da distância
*	É responsável por identificar se existe alguma outra classe utilizando de sua posição
'''
class Ponto:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.objeto = False
		self.nome = self.setNome()

	def setNome(self):
		letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
		letra = random.randint(0, len(letras)-1)
		numero = random.randint(1,100)
		return str(numero) + str(letras[letra]) + str(letra)

	def setObjeto(self, status):
		self.objeto = status

	def getObjeto(self):
		return self.objeto

	def __str__(self):
		return self.nome

class Caminho:
	def __init__(self, pontoA, pontoB):
		self.pontoA = pontoA
		self.pontoB = pontoB
		self.distancia = 0
		self.feromonio = (random.randint(5,9)/10000.0) + (random.randint(1,9)/100000.0)
		self.setDistancia(self.pontoA, self.pontoB)

	def setDistancia(self, pontoA, pontoB):
		self.distancia = math.sqrt(pow(pontoA.x - pontoB.x ,2) + pow(pontoA.y - pontoB.y ,2))

	def setFeromonio(self, novoFeromonio):
		self.feromonio = novoFeromonio

	def aumentaFeromonio(self):
		temp = (float) (self.feromonio/2.0)
		self.feromonio = (random.randint(5,9)/10000.0) + (random.randint(1,9)/100000.0) + temp

	def decaiFeromonio(self):
		self.feromonio = (float) (self.feromonio/3.0)

	def __str__(self):
		return('CAMINHO ' + self.pontoA.nome + ' - ' + self.pontoB.nome)

#-------------------- MAIN --------------------#
if __name__ == "__main__":
	g = nx.fast_gnp_random_graph(5, 0.4)
	g.nodes(data=True)
	for no in g.nodes():
		ponto = Ponto(random.randint(1,10), random.randint(1,10))
		g.node[no]['ponto'] = ponto
		# print(g.node[no]['ponto'])
	for aresta in g.edges():
		print(aresta[0], aresta[1])
	nx.draw(g, with_labels=True)
	# pos=nx.spring_layout(g)
	# nx.draw_networkx_labels(g, pos, font_size=20,font_family='sans-serif')
	plt.show()