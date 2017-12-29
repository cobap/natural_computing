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

	def __str__(self):
		return self.nome

class HQ:
	def __init__(self, numero_abelhas, pontoAtual):
		self.numero_abelhas = numero_abelhas
		self.setNome()
		self.pontoAtual = pontoAtual
		self.pontoAtual.setObjeto(True)
		self.abelhas = []
		self.id = 0
		self.criaAbelhas()
		self.abelhasAtual = numero_abelhas

	def setID(self, new_id):
		self.id = new_id

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
		print('ABELHAS RETORNANDO AO HQ')
		for abelha in pelotao:
			abelha.pontoAtual.setObjeto(False)
			abelha.cleanBlackList()
		abelha.pontoAtual = self.pontoAtual
		self.abelhasAtual = self.abelhasAtual+1
		self.abelhas.append(abelha)

	def __str__(self):
		return self.nome

class Evento:
	def __init__(self, pontoAtual):
		self.setIntensidadeRange()
		self.setNome()
		self.pontoAtual = pontoAtual
		self.pontoAtual.setObjeto(True)

	def setNome(self):
		letras = ['Assalto', 'Briga', 'Corrida de Rua', 'Depredação', 'Extermínio', 'Fuga', 'Golpe de Estado', 'Hospital em Chamas', 'Individuo Suspeito', 'Joalheiria Roubada', 'Ladrão', 'Mulher em Trabalho de Parto', 'Navio Afundando', 'Operação Policial', 'PM na Área', 'Quadrilha', 'Resgate', 'Soldado Ferido', 'Tiroteio', 'Vítima de Acidente']
		letra = random.randint(0, len(letras)-1)
		self.nome =  str(letras[letra]) +str(letra)

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
	def __init__(self, n_vertices, chance_aresta, alfa, beta, iteracoes, qtdFormigas):
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
			print(no, g.node[no]['ponto'].nome, g.node[no]['ponto'].x, g.node[no]['ponto'].y)

		# Para cada aresta dentro do grafo
		for aresta in g.edges():
			# Criamos um caminho que liga 
			caminho = Caminho(g.node[aresta[0]]['ponto'], g.node[aresta[1]]['ponto'])
			g[aresta[0]][aresta[1]]['caminho'] = caminho
			# print(caminho)
			# print(g[aresta[0]][aresta[1]]['caminho'].feromonio)

		self.g = g
		self.iteracoes = iteracoes
		self.formigas = []
		self.eventos = []
		self.eventos_hold = []
		self.hqs = []
		self.mediaAbelhas = random.randint(2,4)
		self.qtdFormigasIndex = qtdFormigas

		nx.draw(g, with_labels=True)
		plt.savefig("grafico.png")
		plt.show()

	def getPontoAleatorio(self):
		return self.g.node[random.randint(1, self.n_vertices-1)]['ponto']

	def criaFormigas(self):
		# O número de formigas sempre será 1/3 do número de vertices
		# self.qtdFormigas = int(round((float) (self.n_vertices * 1)/self.qtdFormigasIndex))
		self.qtdFormigas = self.qtdFormigasIndex
		print('QTD DE FORMIGAS: ', self.qtdFormigas)
		formigas_temp = [Formiga('PATRULHA', self.getPontoAleatorio()) for i in range(self.qtdFormigas)]

		for formiga in formigas_temp:
			print(formiga.nome, formiga.pontoAtual.numero)
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
			hqTemp = HQ(self.mediaAbelhas, no_aleatorio)
			self.hqs.append(hqTemp)
			hqTemp.setID(self.hqs.index(hqTemp))
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
			print(str(pontoAntigo.numero) + " -> " + str(formiga.pontoAtual.numero), str(g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho']), g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho'].feromonio)

	def caminhaAbelhaOtimizado(self, abelha, g):
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
		print(abelha.nome, str(pontoAntigo.numero) + " -> " + str(abelha.pontoAtual.numero), str(g[pontoAntigo.numero][abelha.pontoAtual.numero]['caminho']), g[pontoAntigo.numero][abelha.pontoAtual.numero]['caminho'].feromonio)

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
		# print(ratio_probabilidades)
		# somatoria_ratio_probabilidades = sum(float(prob) for prob in ratio_probabilidades)
		# print(somatoria_ratio_probabilidades)
		# print(ratio_probabilidades.index(max(ratio_probabilidades)))

		formiga.pontoAtual = g.node[caminhos2[ratio_probabilidades.index(max(ratio_probabilidades))]]['ponto']
		formiga.pontoAtual.setObjeto(True)
		g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho'].aumentaFeromonio()
		# print(formiga.nome, str(pontoAntigo.numero), str(formiga.pontoAtual.numero), str(g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho']), g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho'].feromonio, 'PROBABILIDADE', max(ratio_probabilidades))
		formiga.addVerticeBlackList(pontoAntigo.numero)
		print(formiga.nome, str(pontoAntigo.numero), str(formiga.pontoAtual.numero), g[pontoAntigo.numero][formiga.pontoAtual.numero]['caminho'].feromonio, max(ratio_probabilidades))

	def selecionaHQ(self, evento):
		hqDisponiveis = [hq for hq in  self.hqs if hq.abelhasAtual is not 0]
		distancias = [math.sqrt(pow(hqSelecionado.pontoAtual.x - evento.pontoAtual.x ,2) + pow(hqSelecionado.pontoAtual.y - evento.pontoAtual.y ,2)) for hqSelecionado in hqDisponiveis]
		
		if len(distancias) == 0:
			self.eventos_hold.append(evento)
			return None
		
		hqSelecionado = self.hqs[distancias.index(min(distancias))]
		print('MENOR DISTANCIA:', hqSelecionado.nome)
		return hqSelecionado

	def acionaPelotaoParaAtaque(self, pelotoes, hqSelecionado, evento):
		# Criamos um pelotao com o nome do evento
		pelotoes[evento.nome] = hqSelecionado.lancaPelotao(evento)
		
		# Caso o pelotao seja mais fraco que o que a colmeia suporte, precisamos reduzir sua força esperando alguns rounds...
		while(pelotoes[evento.nome] == None):
			evento.intensidade = evento.intensidade - 1
			pelotoes[evento.nome] = hqSelecionado.lancaPelotao(evento)

		print('ABELHAS PRONTAS PARA O ATAQUE ->->')
		for abelha in pelotoes[evento.nome]:
			print abelha

	#Problemas para criar eventos em vertices vazios
	def iniciaCidade(self):
		# Inicia cidade - criando formigas, HQs, eventos, etc...
		# random.seed(42)
		iterador = 1
		self.criaFormigas()
		self.criaHQs()
		pelotoes = {}
		# MAIN 
		while(iterador <= self.iteracoes):
			#Para cada loop de interação, ande com as formigas
			for formiga in self.formigas:
				# Andar aleatóriaamente
				# self.caminhaAleatoriamente(formiga, self.g)
				# Andar otimizando os caminhos = maior feromonio & menor distancia
				self.caminhaFormigaACO(formiga, self.g)

			# A cada 3 iterações, criamos um novo evento na cidade
			if iterador % 3 == 0:
				print('NOVO EVENTO NA CIDADE')
				evento = self.criaEvento()
				print(evento)
				
				# Adicionamos o evento na lista de eventos e também como uma propriedade de um Nó
				self.g.node[evento.pontoAtual.numero]['evento'] = evento
				self.eventos.append(self.g.node[evento.pontoAtual.numero]['evento'])
				hqSelecionado = self.selecionaHQ(evento)
				
				if(hqSelecionado is None):
					self.eventos.remove(evento)
					print("EVENTO: " , evento.nome, 'INTENSIDADE: ', evento.intensidade, 'LOCAL', evento.pontoAtual.numero, "ITER", iterador, "STATUS", 'ON-HOLD')
				else:
					print("EVENTO: " , evento.nome, 'INTENSIDADE: ', evento.intensidade, 'LOCAL', evento.pontoAtual.numero, "ITER", iterador, 'STATUS', 'ATIVO')
					self.acionaPelotaoParaAtaque(pelotoes, hqSelecionado, evento)
					
			eventos_mortos = []
			for evento in self.eventos:
				abelhaLider = pelotoes[evento.nome]
				self.caminhaAbelhaOtimizado(abelhaLider[0], self.g)

				#Caso tenha chego no evento
				if(abelhaLider[0].pontoAtual == evento.pontoAtual):
					print('PELOTAO CHEGOU AO EVENTO!')
					print("EVENTO: " , evento.nome, 'INTENSIDADE: ', evento.intensidade, 'LOCAL', evento.pontoAtual.numero, "ITER", iterador)
					eventos_mortos.append(evento)
					self.eventos.remove(evento)

					# TODO
					print('ABELHA LIDER: ', abelhaLider[0].id_hq) 
					print('HQ DA ABELHA: ', self.hqs[abelhaLider[0].id_hq])
					self.hqs[abelhaLider[0].id_hq].retornaPelotao(pelotoes[evento.nome])

					if len(self.eventos_hold) > 0:
						evento_on_hold = self.eventos_hold.pop()
						print("EVENTO: " , evento_on_hold.nome, 'INTENSIDADE: ', evento_on_hold.intensidade, 'LOCAL', evento_on_hold.pontoAtual.numero, "ITER", iterador, 'STATUS', 'ATIVO')
						self.acionaPelotaoParaAtaque(pelotoes, self.hqs[abelhaLider[0].id_hq], evento_on_hold)
					
			# print('NUMERO EVENTOS: ', len(self.eventos))

			iterador = iterador + 1

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

	cidade = Cidade(n_vertices,chance_aresta, alfa, beta, 5, 20)
	cidade.iniciaCidade()

	# print(g.node[no_ale]['formiga'])

	# Mostra todas as Formigas no mapa
	# for no in g.nodes():
		# print(g.node[no]['formiga'])

	# Mostra todo os vizinhos de um nó aleatório
	# print(no_ale, g.neighbors(no_ale))

	# no_ale = random.randint(6,10)
	# print('------------ABELHAS-------------')
	# abelha1 = Abelha('BATEDORA',1,g.node[no_ale]['ponto'])
	# caminhaOtimizadoAbelha(abelha1, g)

	# pos=nx.spring_layout(g)
	# nx.draw_networkx_labels(g, pos, font_size=20,font_family='sans-serif')