# -*- coding: utf-8 -*-
import math, random, copy, hashlib, sys
import networkx as nx
import matplotlib.pyplot as plt
from random import choice
import numpy as np

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
		# self.feromonio = 1.0+ (random.randint(5,9)/10000.0) + (random.randint(1,9)/100000.0)
		self.feromonio = 0.00001
		self.feromonioInicial = self.feromonio
		self.setDistancia(self.pontoA, self.pontoB)

	def setDistancia(self, pontoA, pontoB):
		self.distancia = math.sqrt(pow(pontoA.x - pontoB.x ,2) + pow(pontoA.y - pontoB.y ,2))
		if self.distancia == 0:
			self.distancia = 0.001

	def setFeromonio(self, novoFeromonio):
		self.feromonio = novoFeromonio

	def aumentaFeromonio(self):
		# temp = (float) (self.feromonio/2.0)
		# self.feromonio = (random.randint(5,9)/10000.0) + (random.randint(1,9)/100000.0) + temp
		fator_aumento = 0.1
		self.feromonio = (1 - fator_aumento) * self.feromonio + self.feromonioInicial

	def decaiFeromonio(self):
		# self.feromonio = (float) (self.feromonio/3.0)
		fator_decaimento = 0.1
		# self.feromonio = (1 - fator_decaimento) * self.feromonio + fator_decaimento * cost_best_solution
		self.feromonio = (1 - fator_decaimento) * self.feromonio + self.feromonioInicial

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
		self.black_list = []

	def addVerticeBlackList(self, n_vertice):
		self.black_list.append(n_vertice)

	def cleanBlackList(self):
		del self.black_list[:]

	def isOnBlackList(self, n_vertice):
		return n_vertice in self.black_list

	def setNome(self):
		letras = ['Corine', 'Nina', 'Laraine', 'Gaspard', 'Bartolemo', 'Rebe', 'Gasper', 'Pauli', 'Sheila-kathryn', 'Gus', 'Christabella', 'Thalia', 'Tyrone', 'Dennison', 'Udale', 'Annaliese', 'Rufus', 'Zebedee', 'Philbert', 'Collin', 'Colver', 'Marcile', 'Cherie', 'Janene', 'Ainslie', 'Bernardina', 'Ursula', 'Alene', 'Horatio', 'Edita', 'Sidnee', 'Gianna', 'Ashton', 'Cymbre', 'Adda', 'Charlena', 'Karly', 'York', 'Shanna', 'Tracie', 'Brook', 'Hilario', 'Darcy', 'Lisette', 'Jakie', 'Teodoro', 'Rochell', 'Jenn', 'Annadiana', 'Clint', 'Wilbur', 'Cariotta', 'Kinnie', 'Diarmid', 'Jocko', 'Mortie', 'Jarib', 'Westleigh', 'Mair', 'Trumaine', 'Emlyn', 'Abagael', 'Em', 'Dolores', 'Erina', 'Lou', 'Golda', 'Herold', 'Bryn', 'Christiane', 'Oralia', 'Bella', 'Kathi', 'Kerry', 'Lindsay', 'Claudetta', 'Manny', 'Cosette', 'Gordy', 'Jordan', 'Dean', 'Elaine', 'Andrey', 'Solly', 'Renie', 'Pepito', 'Godfree', 'Sabina', 'Liana', 'Stevana', 'Onfre', 'Hubert', 'Leslie', 'Chev', 'Caryn', 'Rollins', 'Adriane', 'Bealle', 'Catharine', 'Ulrich', 'Ikey']
		letra = random.randint(0, len(letras)-1)
		numero = random.randint(1,100)
		self.nome = 'ANT-' + str(letras[letra]) + str(letra)

class Abelha:
	def __init__(self, funcao, id_hq, pontoAtual):
		self.funcao = funcao
		self.id_hq = id_hq
		self.setNome()
		self.pontoAtual = pontoAtual
		self.pontoAtual.setObjeto(True)
		self.black_list = []

	def setNome(self):
		letras = ['Corine', 'Nina', 'Laraine', 'Gaspard', 'Bartolemo', 'Rebe', 'Gasper', 'Pauli', 'Sheila-kathryn', 'Gus', 'Christabella', 'Thalia', 'Tyrone', 'Dennison', 'Udale', 'Annaliese', 'Rufus', 'Zebedee', 'Philbert', 'Collin', 'Colver', 'Marcile', 'Cherie', 'Janene', 'Ainslie', 'Bernardina', 'Ursula', 'Alene', 'Horatio', 'Edita', 'Sidnee', 'Gianna', 'Ashton', 'Cymbre', 'Adda', 'Charlena', 'Karly', 'York', 'Shanna', 'Tracie', 'Brook', 'Hilario', 'Darcy', 'Lisette', 'Jakie', 'Teodoro', 'Rochell', 'Jenn', 'Annadiana', 'Clint', 'Wilbur', 'Cariotta', 'Kinnie', 'Diarmid', 'Jocko', 'Mortie', 'Jarib', 'Westleigh', 'Mair', 'Trumaine', 'Emlyn', 'Abagael', 'Em', 'Dolores', 'Erina', 'Lou', 'Golda', 'Herold', 'Bryn', 'Christiane', 'Oralia', 'Bella', 'Kathi', 'Kerry', 'Lindsay', 'Claudetta', 'Manny', 'Cosette', 'Gordy', 'Jordan', 'Dean', 'Elaine', 'Andrey', 'Solly', 'Renie', 'Pepito', 'Godfree', 'Sabina', 'Liana', 'Stevana', 'Onfre', 'Hubert', 'Leslie', 'Chev', 'Caryn', 'Rollins', 'Adriane', 'Bealle', 'Catharine', 'Ulrich', 'Ikey']
		letra = random.randint(0, len(letras)-1)
		numero = random.randint(1,100)
		self.nome = 'BEE-' + str(letras[letra]) + str(letra)

	def addVerticeBlackList(self, n_vertice):
		self.black_list.append(n_vertice)

	def cleanBlackList(self):
		del self.black_list[:]

	def isOnBlackList(self, n_vertice):
		return n_vertice in self.black_list

	def calculaMelhorCaminho(self, g, ponto_evento):
		# print('INDO DE ', self.pontoAtual.numero, 'ATÉ ', ponto_evento)
		# print(nx.shortest_path(g,source=self.pontoAtual.numero, target=ponto_evento))
		# print('MELHOR CAMINHO COM PESO')
		shortest_path = nx.shortest_path(g,source=self.pontoAtual.numero, target=ponto_evento, weight='feromonio')
		# shortest_path.pop(0)
		if(self.pontoAtual.numero != ponto_evento):
			shortest_path.pop(0)
		# print(shortest_path)
		# print(self.pontoAtual.numero)
		# print(type(shortest_path))
		self.shortest_path = shortest_path

	def __str__(self):
		return self.nome

class HQ:
	def __init__(self, numero_abelhas, pontoAtual, id):
		self.numero_abelhas = numero_abelhas
		self.setNome()
		self.pontoAtual = pontoAtual
		self.pontoAtual.setObjeto(True)
		self.abelhas = []
		self.id = id
		self.criaAbelhas()
		self.abelhasAtual = numero_abelhas

	def criaAbelhas(self):
		for iterador in range(0, self.numero_abelhas):
			abelhaTemp = Abelha('Tropa', self.id, self.pontoAtual)
			self.abelhas.append(abelhaTemp)

	def setNome(self):
		letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
		letra = random.randint(0, len(letras)-1)
		numero = random.randint(1,100)
		self.nome =  'COL-' + str(letra) + str(letras[letra])

	def lancaPelotao(self, evento):
		if self.abelhasAtual < evento.intensidade:
			return None
		else:
			pelotao = []
			while len(pelotao) != evento.intensidade:
				pelotao.append(self.abelhas.pop())
			self.abelhasAtual = self.abelhasAtual - evento.intensidade
			return pelotao

	def retornaPelotao(self, pelotao):
		# print('ABELHAS RETORNANDO AO HQ')
		# print(pelotao)
		for abelha in pelotao:
			# print(abelha, 'retornando ao HQ')
			abelha.pontoAtual.setObjeto(False)
			abelha.cleanBlackList()
			abelha.pontoAtual = self.pontoAtual
			self.abelhasAtual = self.abelhasAtual+1
			self.abelhas.append(abelha)

class Evento:
	def __init__(self, pontoAtual):
		self.setIntensidadeRange()
		self.setNome()
		self.pontoAtual = pontoAtual
		self.pontoAtual.setObjeto(True)

	def setNome(self):
		letras = ['Assalto', 'Briga', 'Corrida de Rua', 'Depredação', 'Extermínio', 'Fuga', 'Golpe de Estado', 'Hospital em Chamas', 'Individuo Suspeito', 'Joalheiria Roubada', 'Ladrão', 'Mulher em Trabalho de Parto', 'Navio Afundando', 'Operação Policial', 'PM na Área', 'Quadrilha', 'Resgate', 'Soldado Ferido', 'Tiroteio', 'Vítima de Acidente']
		letra = random.randint(0, len(letras)-1)
		self.nome =  str(letras[letra]) +str(letra) + str(random.getrandbits(128))

	def setInicio(self, iterador):
		self.inicio = iterador

	def setIntensidadeRange(self):
		self.intensidade = random.randint(1,3)
		# Intensidade é sempre o número de envolvidos x3 que precisa para solucionar o problema
		# self.range = random.randint(1,2)
		self.range = 1

	def __str__(self):
		resultado = "| Intensidade: " + str(self.intensidade) 
		resultado += " | Local: " + str(self.pontoAtual.numero)
		return self.nome + resultado

class Cidade:
	def __init__(self, n_vertices, chance_aresta, alfa, beta, iteracoes, qtdFormigas, rodadas, algoritmo_formiga, reduz_grafo, calcula_path):
		# Cria gráfico aleatório com n_vertices e % de existir uma aresta entre dois vertices
		self.n_vertices = n_vertices
		g = nx.fast_gnp_random_graph(n_vertices, chance_aresta)
		# Verifica se vertíce é conexo
		while(nx.is_connected(g) is not True):
			# Caso não seja, o recrie até que seja - comoqueremos facilitar as coisas, só podemos avançar com um vertice que permite andar por uma aresta
			g = nx.fast_gnp_random_graph(5, 0.4)

		g.graph['alfa'] = alfa
		g.graph['beta'] = beta

		# Para cada nó dentro do grafo
		for no in g.nodes():
			# Criamos o ponto que irá definir aquele nó - sendo um número com uma coordenada aleatória entre 1~10. Recebe também o numero do vertice
			ponto = Ponto(random.randint(1,10), random.randint(1,10), no)
			# Definimos o Ponto como a variável 'ponto' dentro do verdadeiro nó do grafo
			g.node[no]['ponto'] = ponto
			# Também definimos que começa sem nenhuma formiga
			g.node[no]['formiga'] = None
			# Damos um print no nome real vs nome ficticio do nó - para podermos comparar depois
			# print(no, g.node[no]['ponto'].nome, g.node[no]['ponto'].x, g.node[no]['ponto'].y)

		# Para cada aresta dentro do grafo
		for aresta in g.edges():
			# Criamos um caminho que liga 
			caminho = Caminho(g.node[aresta[0]]['ponto'], g.node[aresta[1]]['ponto'])
			g[aresta[0]][aresta[1]]['caminho'] = caminho

			# print(caminho)
			# print(g[aresta[0]][aresta[1]]['caminho'].feromonio)

		self.g = g
		self.iteracoes = iteracoes
		self.rodadas = rodadas
		self.formigas = []
		self.eventos = []
		self.eventos_hold = []
		self.hqs = []
		self.mediaAbelhas = random.randint(2,4)
		self.qtdFormigasIndex = qtdFormigas
		self.algoritmo_formiga = algoritmo_formiga
		self.reduz_grafo = reduz_grafo
		self.calcula_path = calcula_path

		# plt.figure()
		# nx.draw(g, with_labels=True)
		nx.draw_networkx(g, with_labels=True)
		plt.savefig("grafico" + sys.argv[1] + ".png")
		# plt.show()

	def getPontoAleatorio(self):
		return self.g.node[random.randint(1, self.n_vertices-1)]['ponto']

	def criaFormigas(self):
		# O número de formigas sempre será 1/3 do número de vertices
		# self.qtdFormigas = int(round((float) (self.n_vertices * 1)/self.qtdFormigasIndex))
		self.qtdFormigas = self.qtdFormigasIndex
		print('QTD DE FORMIGAS: ', self.qtdFormigas)
		formigas_temp = [Formiga('PATRULHA', self.getPontoAleatorio()) for i in range(self.qtdFormigas)]

		for formiga in formigas_temp:
			# print(formiga.nome, formiga.pontoAtual.numero)
			self.g.node[formiga.pontoAtual.numero]['formiga'] = formiga
			self.formigas.append(self.g.node[formiga.pontoAtual.numero]['formiga'])

	def criaEvento(self):
		no_aleatorio = self.getPontoAleatorio()
		return Evento(no_aleatorio)

	def criaHQs(self):
		# Número de HQ é sempre 1/5 do número de vertices do grafo
		self.qtdHQs = int(round((float) (self.n_vertices * 1)/5))
		print('QTD DE HQs: ', self.qtdHQs)
		print('QTD DE Abelhas: ', self.mediaAbelhas)
		# Adiciona todos os HQ criados dentro da cidade
		for hq in range(self.qtdHQs):
			no_aleatorio = self.getPontoAleatorio()
			hqTemp = HQ(self.mediaAbelhas, no_aleatorio, hq)
			self.hqs.append(hqTemp)
			# hqTemp.setID(self.hqs.index(hqTemp))
			print('NOME ', hqTemp.nome, " | LOCAL: ", hqTemp.pontoAtual.numero)

	def caminhaFormigaAleatoriamente(self, formiga, g):
			# print(formiga.pontoAtual.numero)
			pontoAntigo = formiga.pontoAtual
			# print(g.neighbors(pontoAntigo.numero))
			caminhos2 = g.neighbors(pontoAntigo.numero)
			# Filtra por caminhos que estejam livres
			# caminhos2 = [caminho for caminho in caminhos2 if g.node[caminho]['ponto'].objeto == False]
			caminhoEscolhido2 = random.choice(caminhos2)
			# print(caminhoEscolhido2)
			formiga.pontoAtual.setObjeto(False)
			# print(g.node[caminhoEscolhido2]['ponto'])
			formiga.pontoAtual = g.node[caminhoEscolhido2]['ponto']
			formiga.pontoAtual.setObjeto(True)
			g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho'].aumentaFeromonio()
			# print(str(pontoAntigo.numero) + " -> " + str(formiga.pontoAtual.numero), str(g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho']), g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho'].feromonio)

	def caminhaAbelhaOtimizado(self, abelha, g):
		# print(formiga.pontoAtual.numero)
		# print('CAMINHO', abelha.shortest_path)
		pontoAntigo = abelha.pontoAtual
		# print('ABELHA ESTAVA EM', pontoAntigo.numero)
		# print(abelha.pontoAtual.numero)
		abelha.pontoAtual.setObjeto(False)

		abelha.pontoAtual = g.node[abelha.shortest_path.pop(0)]['ponto']
		abelha.pontoAtual.setObjeto(True)
		# print('ABELHA FOI PARA', abelha.pontoAtual.numero)
		# print(abelha.nome, abelha.id_hq ,str(pontoAntigo.numero) + " -> " + str(abelha.pontoAtual.numero))

	def caminhaAbelhaFeromonio(self, abelha, g):
		# print(formiga.pontoAtual.numero)
		pontoAntigo = abelha.pontoAtual
		# print(abelha.pontoAtual.numero)
		abelha.pontoAtual.setObjeto(False)
		# print(g.neighbors(pontoAntigo.numero))
		caminhos2 = g.neighbors(pontoAntigo.numero)

		# Filtrando para eliminar vizinhos ja visitados
		caminhos2 = [caminho for caminho in caminhos2 if not abelha.isOnBlackList(caminho)]

		# Caso não tenha conseguido chegar até agora, limpamos a back_list e começamos novamente
		if len(caminhos2) == 0:
			abelha.cleanBlackList()
			caminhos2 = g.neighbors(pontoAntigo.numero)

		# print('CAMINHOS POS BLACK_LIST', caminhos2)
		# print(g.neighbors(pontoAntigo.numero))
		# g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho']
		feromoniosCaminhos = [g[pontoAntigo.numero][numero_vertice]['caminho'].feromonio for numero_vertice in caminhos2]
		# print(feromoniosCaminhos)
		abelha.pontoAtual = g.node[caminhos2[feromoniosCaminhos.index(max(feromoniosCaminhos))]]['ponto']
		abelha.pontoAtual.setObjeto(True)
		# print(abelha.pontoAtual.numero)
		abelha.addVerticeBlackList(pontoAntigo.numero)
		# print(abelha.nome, abelha.id_hq ,str(pontoAntigo.numero) + " -> " + str(abelha.pontoAtual.numero), str(g[pontoAntigo.numero][abelha.pontoAtual.numero]['caminho']), g[pontoAntigo.numero][abelha.pontoAtual.numero]['caminho'].feromonio)

	def caminhaFormigaACO(self, formiga, g):
		# print(formiga.nome)
		formiga.pontoAtual.setObjeto(False)
		pontoAntigo = formiga.pontoAtual
		# print(formiga.pontoAtual.numero)
		caminhos2 = g.neighbors(pontoAntigo.numero)
		# print('PRE BLACK_LIST:', caminhos2)
		caminhos2 = [caminho for caminho in caminhos2 if not formiga.isOnBlackList(caminho)]
		# print('POS BLACK_LIST:', caminhos2)
		# Caso não tenha conseguido chegar até agora, limpamos a back_list e começamos novamente
		if len(caminhos2) == 0:
			formiga.cleanBlackList()
			caminhos2 = g.neighbors(pontoAntigo.numero)

		# Calcula a probabilidade baseado no feromonio do caminho e a sua distancia
		feromoniosCaminhos = [g[pontoAntigo.numero][numero_vertice]['caminho'].feromonio for numero_vertice in caminhos2]
		probabilidades = [(math.pow(g[pontoAntigo.numero][numero_vertice]['caminho'].feromonio, g.graph['alfa']) * math.pow(1.0 / g[pontoAntigo.numero][numero_vertice]['caminho'].distancia, g.graph['beta'])) for numero_vertice in caminhos2]
		# probabilidade = (math.pow(caminho.feromonio, alfa) * math.pow(1.0 / caminho.distancia, beta))
		# print(caminhos2)
		# print(feromoniosCaminhos)
		# print(probabilidades)
		somatoria_probabilidades = sum(float(prob) for prob in probabilidades)
		# print(somatoria_probabilidades)

		ratio_probabilidades = [probabilidade/somatoria_probabilidades for probabilidade in probabilidades]
		ratio_probabilidades.sort(reverse=True)
		chance_escolhida = None
		# print(ratio_probabilidades)
		while chance_escolhida is None:
			for chance in ratio_probabilidades:
				if random.random() < chance:
					chance_escolhida = chance
		# print(chance_escolhida)


		# somatoria_ratio_probabilidades = sum(float(prob) for prob in ratio_probabilidades)
		# print(somatoria_ratio_probabilidades)
		# print(ratio_probabilidades.index(max(ratio_probabilidades)))
		# formiga.pontoAtual = g.node[caminhos2[ratio_probabilidades.index(max(chance_escolhida))]]['ponto']
		formiga.pontoAtual = g.node[caminhos2[ratio_probabilidades.index((chance_escolhida))]]['ponto']
		formiga.pontoAtual.setObjeto(True)
		g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho'].aumentaFeromonio()
		# print(formiga.nome, str(pontoAntigo.numero), str(formiga.pontoAtual.numero), str(g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho']), g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho'].feromonio, 'PROBABILIDADE', max(ratio_probabilidades))
		formiga.addVerticeBlackList(pontoAntigo.numero)
		# print(formiga.nome, str(pontoAntigo.numero), str(formiga.pontoAtual.numero), g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho'].feromonio, max(ratio_probabilidades))

	def selecionaHQ(self, evento):
		hqDisponiveis = [hq for hq in  self.hqs if hq.abelhasAtual is not 0]
		# print('HQ DISPONIVEIS: ')
		# for hq in hqDisponiveis:
		# 	print(hq.nome, hq.id, hq.abelhasAtual)
		distancias = [math.sqrt(pow(hqSelecionado.pontoAtual.x - evento.pontoAtual.x ,2) + pow(hqSelecionado.pontoAtual.y - evento.pontoAtual.y ,2)) for hqSelecionado in hqDisponiveis]
		
		if len(distancias) == 0:
			self.eventos_hold.append(evento)
			return None
		
		# hqSelecionado = self.hqs[distancias.index(min(distancias))]
		hqSelecionado = hqDisponiveis[distancias.index(min(distancias))]
		# print('MENOR DISTANCIA:', hqSelecionado.nome)
		return hqSelecionado

	def acionaPelotaoParaAtaque(self, pelotoes, hqSelecionado, evento, g):
		# Criamos um pelotao com o nome do evento
		pelotoes[evento.nome] = hqSelecionado.lancaPelotao(evento)
		
		# Caso o pelotao seja mais fraco que o que a colmeia suporte, precisamos reduzir sua força esperando alguns rounds...
		while(pelotoes[evento.nome] == None):
			evento.intensidade = evento.intensidade - 1
			pelotoes[evento.nome] = hqSelecionado.lancaPelotao(evento)
		pelotoes[evento.nome][0].calculaMelhorCaminho(g, evento.pontoAtual.numero)
		# print('ABELHAS PRONTAS PARA O ATAQUE ->->')
		# for abelha in pelotoes[evento.nome]:
		# 	print abelha

	def reduzirGrafo(self):
		# print('-------------------------------------------------------------------------')
		# print('-------------------------REDUZINGO GRAFO--------------------')
		# print(self.g.number_of_edges())
		# eligible_edges = [(from_node,to_node,edge_attributes) for from_node,to_node,edge_attributes in self.g.edges(data=True) if edge_attributes['weight'] > threshold]
		media_feromonio = [edge_attributes['caminho'].feromonio for from_node,to_node,edge_attributes in self.g.edges(data=True)]
		media_feromonio = np.mean(media_feromonio)
		# print(media_feromonio)
		arestas_selecionadas = [(from_node,to_node,edge_attributes) for from_node,to_node,edge_attributes in self.g.edges(data=True) if edge_attributes['caminho'].feromonio > media_feromonio]
		subGrafo = nx.Graph()
		subGrafo.add_nodes_from(self.g.nodes(data=True))
		subGrafo.add_edges_from(arestas_selecionadas)

		for edge in subGrafo.edges(data=True):
			subGrafo[edge[0]][edge[1]]['feromonio'] = edge[2]['caminho'].feromonio
		# G = nx.DiGraph(((source, target, attr) for source, target, attr in my_network.edges_iter(data=True) if attr['weight'] > threshold))
		# SG=G.subgraph( [n for n,attrdict in G.node.items() if attrdict ['type'] == 'X' ] )
		# SG=networkx.Graph( [ (u,v,d) for u,v,d in G.edges(data=True) if d ['weight']>cutoff])
		# print('É CONEXO?', nx.is_connected(subGrafo))
		if(nx.is_connected(subGrafo) is False):
			sys.exit("IMPOSSÍVEL CRIAR SUBGRAFO CONEXO")
		nx.draw_networkx(subGrafo, node_color='b')
		plt.savefig("subgrafico.png")
		# print(subGrafo.number_of_edges())
		# print('-------------------------------------------------------------------------')
		return subGrafo

	def reduzGrafo(self):
		print('-------------------------------------------------------------------------')
		print('-------------------------REDUZINGO GRAFO--------------------')
		melhor_aresta = {}
		nos = {}
		for no in self.g.nodes():
			# print(no)
			vizinhos = self.g.neighbors(no)
			# print(vizinhos)
			feromonioVizinhos = [self.g[no][vizinho]['caminho'].feromonio for vizinho in vizinhos]
			melhor_aresta[self.g[no][vizinhos[feromonioVizinhos.index(max(feromonioVizinhos))]]['caminho']] = no
			nos[str(no)] = no
			# print(feromonioVizinhos)
			# print('maior feromonio', feromonioVizinhos.index(max(feromonioVizinhos)))
			# print('no com maior feromonio', vizinhos[feromonioVizinhos.index(max(feromonioVizinhos))])
			# g.node[caminhos2[feromoniosCaminhos.index(max(feromoniosCaminhos))]]['ponto']
		# print(melhor_aresta)
		# print(nos)

		subGrafo = nx.Graph()
		for no in nos.values():
			subGrafo.add_node(no)

		for aresta in melhor_aresta.keys():
			subGrafo.add_edge(aresta.pontoA.numero, aresta.pontoB.numero, caminho=aresta)
			# print(aresta)
			# print(aresta.pontoA.numero)
			# g[aresta[0]][aresta[1]]['caminho'] = caminho
		print(subGrafo.edges())
		print(self.g.edges())

		print('É CONEXO?', nx.is_connected(subGrafo))
		# nx.draw(subGrafo, with_labels=True)
		nx.draw_networkx(subGrafo, node_color='b')
		plt.savefig("subgrafico.png")
		print('-------------------------------------------------------------------------')

	def iniciaCidade(self):
		# Inicia cidade - criando formigas, HQs, eventos, etc...
		# random.seed(42)
		iterador = 1
		rodadas = 1
		self.criaFormigas()
		self.criaHQs()
		pelotoes = {}
		# MAIN 

		# Para cada iteração - rode o ACO e otimize os caminhos
		# -- IDEIA -- rodar o ACO antes dos eventos e criar um subgrafo que mostre os melhores caminhos, então implementar para que as abelhas só visitem esse subgrafo sempre levando em conta a distancia do evento e o feromonio
		# Para gerar esse subgrafo - podemos utilizar a lista de arestas que tiveram os n° maiores feromonios desde que não liguem o mesmo vertice. Assim - teremos um grafo que teve o maior feromonio entre todos os vertices

		while(iterador <= self.iteracoes):
			for formiga in self.formigas:
				self.caminhaFormigaACO(formiga, self.g) if self.algoritmo_formiga == 1 else self.caminhaFormigaAleatoriamente(formiga, self.g)
			iterador = iterador + 1

		if(self.reduz_grafo == 1):
			self.g = self.reduzirGrafo()

		while(rodadas <= self.rodadas):
			# A cada 3 iterações, criamos um novo evento na cidade
			if rodadas % 3 == 0:
				if len(self.eventos_hold) >= len(self.hqs):
					# print('LISTA CHEIA')
					if self.eventos[0].inicio + self.n_vertices <= rodadas:
						print("EVENTO:" , self.eventos[0].nome, self.eventos[0].intensidade, self.eventos[0].pontoAtual.numero, rodadas, 'TIME-OUT')
						self.hqs[abelhaLider[0].id_hq].retornaPelotao(pelotoes[self.eventos[0].nome])
						self.eventos.remove(self.eventos[0])

						evento_on_hold = self.eventos_hold.pop()
						print("EVENTO:" , evento_on_hold.nome, evento_on_hold.intensidade, evento_on_hold.pontoAtual.numero, rodadas, 'RE-ATIVO')
						evento_on_hold.setInicio(rodadas)
						self.eventos.append(self.g.node[evento_on_hold.pontoAtual.numero]['evento'])
						self.acionaPelotaoParaAtaque(pelotoes, self.hqs[abelhaLider[0].id_hq], evento_on_hold, self.g)
				else: 
					# print('NOVO EVENTO NA CIDADE')
					evento = self.criaEvento()
					
					# Adicionamos o evento na lista de eventos e também como uma propriedade de um Nó
					self.g.node[evento.pontoAtual.numero]['evento'] = evento
					self.eventos.append(self.g.node[evento.pontoAtual.numero]['evento'])
					hqSelecionado = self.selecionaHQ(evento)
					
					if(hqSelecionado is None):
						self.eventos.remove(evento)
						# print("EVENTO: " , evento.nome, 'INTENSIDADE: ', evento.intensidade, 'LOCAL', evento.pontoAtual.numero, "ITER", rodadas, "STATUS", 'ON-HOLD')
						print("EVENTO:" , evento.nome, evento.intensidade, evento.pontoAtual.numero, rodadas, 'ON-HOLD')
					else:
						print("EVENTO:" , evento.nome, evento.intensidade, evento.pontoAtual.numero, rodadas, 'ATIVO')
						evento.setInicio(rodadas)
						self.acionaPelotaoParaAtaque(pelotoes, hqSelecionado, evento, self.g)
					
			eventos_mortos = []
			for evento in self.eventos:
				# print('ABELHAS EM MOVIMENTO')
				abelhaLider = pelotoes[evento.nome]
				if(self.calcula_path == 0):
					# Caminha baseado no maior feromonio que encontra
					self.caminhaAbelhaFeromonio(abelhaLider[0], self.g)
				else:
					self.caminhaAbelhaOtimizado(abelhaLider[0], self.g)

				#Caso tenha chego no evento
				if(abelhaLider[0].pontoAtual == evento.pontoAtual):
					# print('PELOTAO CHEGOU AO EVENTO!')
					print("EVENTO:" , evento.nome, evento.intensidade, evento.pontoAtual.numero, rodadas, 'COMPLETO')
					eventos_mortos.append(evento)
					self.eventos.remove(evento)

					self.hqs[abelhaLider[0].id_hq].retornaPelotao(pelotoes[evento.nome])

					if len(self.eventos_hold) > 0:
						evento_on_hold = self.eventos_hold.pop()
						# print('RE-ATIVANDO EVENTO - AGORA FALTAM:', len(self.eventos_hold))
						print("EVENTO:" , evento_on_hold.nome, evento_on_hold.intensidade, evento_on_hold.pontoAtual.numero, rodadas, 'RE-ATIVO')
						evento_on_hold.setInicio(rodadas)
						self.eventos.append(self.g.node[evento_on_hold.pontoAtual.numero]['evento'])
						self.acionaPelotaoParaAtaque(pelotoes, self.hqs[abelhaLider[0].id_hq], evento_on_hold, self.g)
					
			# print('NUMERO EVENTOS: ', len(self.eventos))

			rodadas = rodadas + 1

		# Para cada aresta dentro do grafo, decaia o feromonio
		for aresta in self.g.edges():
			# print(self.g[aresta[0]][aresta[1]]['caminho'].feromonio)
			self.g[aresta[0]][aresta[1]]['caminho'].decaiFeromonio()
			# print(self.g[aresta[0]][aresta[1]]['caminho'].feromonio)



########################
#-------------------- MAIN --------------------#
########################
if __name__ == "__main__":
	n_vertices = 15
	chance_aresta = 0.4
	alfa = 0.1
	beta = 2.5

	cidade = Cidade(n_vertices,chance_aresta, alfa, beta, 50, 20, 1000, 1, 1, 1)
	cidade.iniciaCidade()

	# Proximos passos
		#número de arestas vs número de vértices 
		#número de arestas vs numero de vertices com aumento da probabilidade
		# Graficos mostrando nós que mais são afetados - quais são suas caracteristicas pré e pós redução? tinham maior grau? 
		# Qt tempo em média se demora para atingit o evento - qd as formigas são ativadas ou qd andam aleatóriamente
		# Como o item acima varia de acordo com o tempo
		# Como tudo isso varia de acordo com o número de vertices, numero de arestas que começa o grafo, alfa e beta
		# Qt de diferença faz caso as formigas rodem 10, 100 ou 10000 vezes antes das abelhas começarem? 
		#? Implementar para que realmente o caminho das abelhas seja uma chance de ida, não uma verdade
		# percentual resultados eliminação de arestas
		# percentual de resultados que da errado - quais os possíveis erros
