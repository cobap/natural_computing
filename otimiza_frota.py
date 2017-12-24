# -*- coding: utf-8 -*-
import math, random, copy
import networkx as nx
import matplotlib.pyplot as plt
from random import choice

'''
*	Class Ponto:
*	Responsável por um vertice da cidade
*	Possui a cordenada X e Y usada para calculo da distância
*	É responsável por identificar se existe alguma outra classe utilizando de sua posição
'''
class Ponto:
	def __init__(self, x, y, numero):
		self.x = x
		self.y = y
		self.objeto = False
		self.nome = self.setNome()
		self.numero = numero

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

class Formiga:
	def __init__(self, funcao, pontoAtual):
		self.funcao = funcao
		# self.forca = forca
		self.pontoAtual = pontoAtual
		# Define que o ponto atual da formiga agora esta ocupado
		# self.pontoAtual.setObjeto(True)
		self.pontoAtual.setObjeto(True)
		# Cria um nome para a formiga
		self.setNome()

	def setNome(self):
		letras = ['Corine', 'Nina', 'Laraine', 'Gaspard', 'Bartolemo', 'Rebe', 'Gasper', 'Pauli', 'Sheila-kathryn', 'Gus', 'Christabella', 'Thalia', 'Tyrone', 'Dennison', 'Udale', 'Annaliese', 'Rufus', 'Zebedee', 'Philbert', 'Collin', 'Colver', 'Marcile', 'Cherie', 'Janene', 'Ainslie', 'Bernardina', 'Ursula', 'Alene', 'Horatio', 'Edita', 'Sidnee', 'Gianna', 'Ashton', 'Cymbre', 'Adda', 'Charlena', 'Karly', 'York', 'Shanna', 'Tracie', 'Brook', 'Hilario', 'Darcy', 'Lisette', 'Jakie', 'Teodoro', 'Rochell', 'Jenn', 'Annadiana', 'Clint', 'Wilbur', 'Cariotta', 'Kinnie', 'Diarmid', 'Jocko', 'Mortie', 'Jarib', 'Westleigh', 'Mair', 'Trumaine', 'Emlyn', 'Abagael', 'Em', 'Dolores', 'Erina', 'Lou', 'Golda', 'Herold', 'Bryn', 'Christiane', 'Oralia', 'Bella', 'Kathi', 'Kerry', 'Lindsay', 'Claudetta', 'Manny', 'Cosette', 'Gordy', 'Jordan', 'Dean', 'Elaine', 'Andrey', 'Solly', 'Renie', 'Pepito', 'Godfree', 'Sabina', 'Liana', 'Stevana', 'Onfre', 'Hubert', 'Leslie', 'Chev', 'Caryn', 'Rollins', 'Adriane', 'Bealle', 'Catharine', 'Ulrich', 'Ikey']
		letra = random.randint(0, len(letras)-1)
		numero = random.randint(1,100)
		self.nome = 'ANT-' + str(letras[letra]) + str(letra)

	def caminhaACO(self, caminhos, alfa, beta):
		# print('FORMIGA '+self.nome + ' |	LUGAR '+self.pontoAtual.nome)
		caminhos = [caminho for caminho in caminhos if caminho.pontoA.nome == self.pontoAtual.nome or caminho.pontoB.nome == self.pontoAtual.nome]
		# print('AFTER-----------------------------------')
		#ENTENDER PQ PRECISA DISSO
		for caminho in caminhos:
			if caminho.feromonio == 0:
				caminho.feromonio = 0.0001
			# print("  ", str(caminho))

		# Vetor que será armazenada as probabilidades dos caminhos
		probabilidades = []
		for caminho in caminhos:
			# Calcula a probabilidade baseado no feromonio do caminho e a sua distancia
			probabilidade = (math.pow(caminho.feromonio, alfa) * math.pow(1.0 / caminho.distancia, beta))
			# print('FERO, ALFA, DIST, BETA', caminho.feromonio, alfa, 1.0/caminho.distancia, beta)
			# print('PROB', probabilidade)
			probabilidades.append(probabilidade)
		# Somatório de todas as probabilidades
		somatoria_probabilidades = sum(float(prob) for prob in probabilidades)
		
		caminho_escolhido = 0
		index_escolhido = -1
		#Para todos as probabilidades calculadas
		for index, probabilidade in zip(range(len(probabilidades)), probabilidades):
			# print('Caminho', str(caminhos[index]) ,'Probabilidade: ', probabilidade/somatoria_probabilidades, 'Distancia', caminhos[index].distancia)
			# Selecionada caminho escolhido como maior caso sua probabilidade seja a maior de todas
			# print('############################')
			# print(probabilidade)
			# print(somatoria_probabilidades)
			if((probabilidade/somatoria_probabilidades) > caminho_escolhido):
				# Recalcula o caminho escolhido
				caminho_escolhido = (probabilidade/somatoria_probabilidades)
				# Define o index
				# print('MELHRO INDEX É', index)
				index_escolhido = index
			# print('############################')

		# print('MELHOR PONTO - INDEX', index_escolhido)
		# print('Caminho', str(caminhos[index_escolhido]) ,'Probabilidade: ', probabilidades[index_escolhido]/somatoria_probabilidades, 'Distancia', caminhos[index_escolhido].distancia)
		
		if(index_escolhido == -1):
			# print('caminhando aleatóriamente')
			return self.caminhaAleatoriamente(caminhos)

		# Sai do vertice atual
		self.pontoAtual.setObjeto(False)
		# Define o vertice atual como o novo vertice - de onde foi do ponto A para o ponto B
		if(self.pontoAtual.nome == str(caminhos[index_escolhido])):
			self.pontoAtual = caminhos[index_escolhido].pontoB
		else:
			self.pontoAtual = caminhos[index_escolhido].pontoA
		# Define que esta ocupando o ponto B agora
		self.pontoAtual.setObjeto(True)
		# Define novo feromonio (por enquanto aleatóriamente)
		# print(str(caminhos[index_escolhido]))
		# print('FEROMONIO ANTIGO: '+ str(caminhos[index_escolhido].feromonio))
		# caminhos[index_escolhido].setFeromonio((random.randint(5,9)/10000.0) + (random.randint(1,9)/100000.0))
		caminhos[index_escolhido].aumentaFeromonio()
		# print('FEROMONIO NOVO: '+ str(caminhos[index_escolhido].feromonio))

		# return index, self.getCaminhos()[index], caminho_escolhido
		return index, caminho_escolhido

def caminhaAleatoriamente(formiga, g):
		# print(formiga.pontoAtual.numero)
		pontoAntigo = formiga.pontoAtual
		# print(g.neighbors(pontoAntigo.numero))
		caminhos2 = g.neighbors(pontoAntigo.numero)
		caminhoEscolhido2 = random.choice(caminhos2)
		# print(caminhoEscolhido2)
		formiga.pontoAtual.setObjeto(False)
		# print(g.node[caminhoEscolhido2]['ponto'])
		formiga.pontoAtual = g.node[caminhoEscolhido2]['ponto']
		formiga.pontoAtual.setObjeto(True)
		g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho'].aumentaFeromonio()
		print(str(pontoAntigo.numero) + " -> " + str(formiga.pontoAtual.numero), str(g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho']), g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho'].feromonio)

#-------------------- MAIN --------------------#
if __name__ == "__main__":
	n_vertices = 15
	chance_aresta = 0.4
	# Cria gráfico aleatório com n_vertices e % de existir uma aresta entre dois vertices
	g = nx.fast_gnp_random_graph(n_vertices, chance_aresta)
	
	# Verifica se vertíce é conexo
	while(nx.is_connected(g) is not True):
		# Caso não seja, o recrie até que seja - comoqueremos facilitar as coisas, só podemos avançar com um vertice que permite andar por uma aresta
		g = nx.fast_gnp_random_graph(5, 0.4)	

	# Para cada nó dentro do grafo
	for no in g.nodes():
		# Criamos o ponto que irá definir aquele nó - sendo um número com uma coordenada aleatória entre 1~10. Recebe também o numero do vertice
		ponto = Ponto(random.randint(1,10), random.randint(1,10), no)
		# Definimos o Ponto como a variável 'ponto' dentro do verdadeiro nó do grafo
		g.node[no]['ponto'] = ponto
		# Também definimos que começa sem nenhuma formiga
		g.node[no]['formiga'] = None
		# Damos um print no nome real vs nome ficticio do nó - para podermos comparar depois
		print(no, g.node[no]['ponto'].nome)

	# Para cada aresta dentro do grafo
	for aresta in g.edges():
		# Criamos um caminho que liga 
		caminho = Caminho(g.node[aresta[0]]['ponto'], g.node[aresta[1]]['ponto'])
		g[aresta[0]][aresta[1]]['caminho'] = caminho
		# print(caminho)
		# print(g[aresta[0]][aresta[1]]['caminho'].feromonio)

	# Escolhe um nó aleatório para criar a formiga
	no_ale = random.randint(1,4)
	# Cria uma formiga do tipo patrulha que tem como ponto, o ponto indicado aleatóriamente pelo número
	formiga1 = Formiga('PATRULHA', g.node[no_ale]['ponto'])
	print('FORMIGA 1', formiga1.pontoAtual.numero)
	# Inicializamos a formiga no grafo, criando o atributo formiga dentro do vertice que antes não havia nada
	g.node[no_ale]['formiga'] = formiga1
	
	for iterador in range(1,10):
		for no in g.nodes():
			if(g.node[no]['formiga'] is not None):
				caminhaAleatoriamente(g.node[no]['formiga'], g)

	# print(g.node[no_ale]['formiga'])

	# Mostra todas as Formigas no mapa
	# for no in g.nodes():
		# print(g.node[no]['formiga'])

	# Mostra todo os vizinhos de um nó aleatório
	# print(no_ale, g.neighbors(no_ale))

	nx.draw(g, with_labels=True)
	# pos=nx.spring_layout(g)
	# nx.draw_networkx_labels(g, pos, font_size=20,font_family='sans-serif')
	plt.show()