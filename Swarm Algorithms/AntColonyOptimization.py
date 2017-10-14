# encoding:utf-8
import random, math

# classe que representa uma aresta
#Toda Aresta tem: ORIGEM, DESTINO, CUSTO (PESO) e FEROMONIO 
class Aresta:
	def __init__(self, origem, destino, custo):
		self.origem = origem
		self.destino = destino
		self.custo = custo
		self.feromonio = None

	def obterOrigem(self):
		return self.origem

	def obterDestino(self):
		return self.destino

	def obterCusto(self):
		return self.custo

	def obterFeronomio(self):
		return self.feromonio

	def setFeromonio(self, feromonio):
		self.feromonio = feromonio

# classe que representa um grafo (grafos completos)
class Grafo:

	def __init__(self, num_vertices):
		self.num_vertices = num_vertices # número de vértices do grafo
		self.arestas = {} # dicionário com as arestas
		self.vizinhos = {} # dicionário com todos os vizinhos de cada vértice

	#Cria uma nova aresta dentro do grafo
	def adicionarAresta(self, origem, destino, custo):
		aresta = Aresta(origem=origem, destino=destino, custo=custo)
		#salva dentro do dicionário a aresta como o par origem-destino
		self.arestas[(origem, destino)] = aresta
		if origem not in self.vizinhos:
			#caso a origem do grafa já não seja um vizinho, então a origem da própria aresta é o seu próprio destino
			self.vizinhos[origem] = [destino]
		else:
			#Quando entre aqui, signifca que esse vertice tem grau > 1
			self.vizinhos[origem].append(destino)

	def obterCustoAresta(self, origem, destino):
		return self.arestas[(origem, destino)].obterCusto()

	def obterFeromonioAresta(self, origem, destino):
		return self.arestas[(origem, destino)].obterFeronomio()

	def setFeromonioAresta(self, origem, destino, feromonio):
		self.arestas[(origem, destino)].setFeromonio(feromonio)

	#calcula o custo de um caminho baseado em uma lista de vertices (arestas)  que a formiga passou
	def obterCustoCaminho(self, caminho):
		custo = 0
		for i in range(self.num_vertices - 1):
			custo += self.obterCustoAresta(caminho[i], caminho[i+1])
		# adiciona o último custo
		custo += self.obterCustoAresta(caminho[-1], caminho[0])
		return custo

class GrafoCompleto(Grafo):
	# gera um grafo completo
	def gerar(self):
		for i in range(1, self.num_vertices + 1):
			for j in range(1, self.num_vertices + 1):
				if i != j:
					peso = random.randint(1, 10)
					self.adicionarAresta(i, j, peso)


# classe que representa uma formiga
#Cada formiga tem uma cidade (em que se encontra), uma solução (caminho que percorreu) e o total desse custo
class Formiga:

	def __init__(self, cidade):
		self.cidade = cidade
		self.solucao = []
		self.custo = None

	def obterCidade(self):
		return self.cidade

	def setCidade(self, cidade):
		self.cidade = cidade

	def obterSolucao(self):
		return self.solucao

	def setSolucao(self, solucao, custo):
		# atualiza a solução
		#caso o custo atual seja 0 => não percorreu nada, cria uma nova solução baseada nos parametros
		if not self.custo:
			self.solucao = solucao[:]
			self.custo = custo
		#caso negativo, caso o custo seja menor, então considere a nova solução como a solução
		else:
			if custo < self.custo:
				self.solucao = solucao[:]
				self.custo = custo

	def obterCustoSolucao(self):
		return self.custo

# classe do ACO
class ACO:
	#alfa => fator que determina o peso do feromoneo nas formigas
	#beta => fator que determina a heuristica
	#delta => taxa de evaporação
	def __init__(self, grafo, num_formigas, alfa=1.0, beta=5.0, 
						iteracoes=10, evaporacao=0.5):
		self.grafo = grafo
		self.num_formigas = num_formigas
		self.alfa = alfa # importância do feromônio
		self.beta = beta # importância da informação heurística
		self.iteracoes = iteracoes # quantidade de iterações
		self.evaporacao = evaporacao # taxa de evaporação
		self.formigas = [] # lista de formigas

		#lista todas as cidades (vertices) criados
		lista_cidades = [cidade for cidade in range(1, self.grafo.num_vertices + 1)]
		# cria as formigas colocando cada uma em uma cidade
		for k in range(self.num_formigas):
			#define cidade da formiga
			cidade_formiga = random.choice(lista_cidades)
			lista_cidades.remove(cidade_formiga)
			#cria uma formiga para a cidade (parametro cidade) e adiciona na lista de formigas
			self.formigas.append(Formiga(cidade=cidade_formiga))
			#caso todas as cidades tenham sido selecionadas, recrie a lista de cidades
			if not lista_cidades:
				lista_cidades = [cidade for cidade in range(1, self.grafo.num_vertices + 1)]


		# calcula o custo guloso pra usar na inicialização do feromônio
		custo_guloso = 0.0 # custo guloso
		vertice_inicial = random.randint(1, grafo.num_vertices) # seleciona um vértice aleatório
		vertice_corrente = vertice_inicial
		visitados = [vertice_corrente] # lista de visitados
		while True:
			#recupera todos os vertices que são adijacentes a este
			vizinhos = self.grafo.vizinhos[vertice_corrente][:]
			custos, escolhidos = [], {}
			#para cada vizinho
			for vizinho in vizinhos:
				#caso não tenha sido visitado antes
				if vizinho not in visitados:
					#calcule o custo 
					custo = self.grafo.obterCustoAresta(vertice_corrente, vizinho)
					#adiciona nas variáveis
					escolhidos[custo] = vizinho
					custos.append(custo)
			#quando visitar todos os vertices (pois o grafo é completo), saia do loop
			if len(visitados) == self.grafo.num_vertices:
				break
			min_custo = min(custos) # pega o menor custo da lista
			custo_guloso += min_custo # adiciona o custo ao total
			vertice_corrente = escolhidos[min_custo] # atualiza o vértice corrente
			visitados.append(vertice_corrente) # marca o vértice corrente como visitado

		# adiciona o custo do último visitado ao custo_guloso
		custo_guloso += self.grafo.obterCustoAresta(visitados[-1], vertice_inicial)

		# inicializa o feromônio de todas as arestas
		for chave_aresta in self.grafo.arestas:
			#o feromonio, baseado no algoritmo guloso é 1/(nVertices *custoGuloso) para todos os vertices
			feromonio = 1.0 / (self.grafo.num_vertices * custo_guloso)
			self.grafo.setFeromonioAresta(chave_aresta[0], chave_aresta[1], feromonio)


	def rodar(self):

		for it in range(self.iteracoes):

			# lista de listas com as cidades visitadas por cada formiga
			cidades_visitadas = []
			for k in range(self.num_formigas):
				# adiciona a cidade de origem de cada formiga
				cidades = [self.formigas[k].obterCidade()]
				cidades_visitadas.append(cidades)

			# para cada formiga constrói uma solução
			for k in range(self.num_formigas):
				for i in range(1, self.grafo.num_vertices):
					# obtém todos os vizinhos que não foram visitados
					cidades_nao_visitadas = list(set(self.grafo.vizinhos[self.formigas[k].obterCidade()]) - set(cidades_visitadas[k]))
					
					# somatório do conjunto de cidades não visitadas pela formiga "k"
					# servirá para utilizar no cálculo da probabilidade
					somatorio = 0.0
					for cidade in cidades_nao_visitadas:
						# calcula o feromônio
						feromonio =  self.grafo.obterFeromonioAresta(self.formigas[k].obterCidade(), cidade)
						# obtém a distância
						distancia = self.grafo.obterCustoAresta(self.formigas[k].obterCidade(), cidade)
						# adiciona no somatório
						somatorio += (math.pow(feromonio, self.alfa) * math.pow(1.0 / distancia, self.beta))
						#somatorio += (feromonioDaAresta ** alfa) * ((1.0/distancia) ** beta)

					# probabilidades de escolher um caminho
					probabilidades = {}

					for cidade in cidades_nao_visitadas:
						# calcula o feromônio
						feromonio = self.grafo.obterFeromonioAresta(self.formigas[k].obterCidade(), cidade)
						# obtém a distância
						distancia = self.grafo.obterCustoAresta(self.formigas[k].obterCidade(), cidade)
						# obtém a probabilidade
						probabilidade = (math.pow(feromonio, self.alfa) * math.pow(1.0 / distancia, self.beta)) / (somatorio if somatorio > 0 else 1)
						# adiciona na lista de probabilidades
						probabilidades[cidade] = probabilidade

					# obtém a cidade escolhida
					cidade_escolhida = max(probabilidades, key=probabilidades.get)

					# adiciona a cidade escolhida a lista de cidades visitadas pela formiga "k"
					cidades_visitadas[k].append(cidade_escolhida)

				# atualiza a solução encontrada pela formiga
				self.formigas[k].setSolucao(cidades_visitadas[k], self.grafo.obterCustoCaminho(cidades_visitadas[k]))

			# atualiza quantidade de feromônio
			for aresta in self.grafo.arestas:
				# somatório dos feromônios da aresta
				somatorio_feromonio = 0.0
				# para cada formiga "k"
				for k in range(self.num_formigas):
					arestas_formiga = []
					# gera todas as arestas percorridas da formiga "k"
					for j in range(self.grafo.num_vertices - 1):
						arestas_formiga.append((cidades_visitadas[k][j], cidades_visitadas[k][j+1]))
					# adiciona a última aresta
					arestas_formiga.append((cidades_visitadas[k][-1], cidades_visitadas[k][0]))
					# verifica se a aresta faz parte do caminho da formiga "k"
					if aresta in arestas_formiga:
						somatorio_feromonio += (1.0 / self.grafo.obterCustoCaminho(cidades_visitadas[k]))
				# calcula o novo feromônio
				novo_feromonio = (1.0 - self.evaporacao) * self.grafo.obterFeromonioAresta(aresta[0], aresta[1]) + somatorio_feromonio
				# seta o novo feromônio da aresta
				self.grafo.setFeromonioAresta(aresta[0], aresta[1], novo_feromonio)


		# percorre para obter as soluções das formigas
		solucao, custo = None, None
		for k in range(self.num_formigas):
			if not solucao:
				solucao = self.formigas[k].obterSolucao()[:]
				custo = self.formigas[k].obterCustoSolucao()
			else:
				aux_custo = self.formigas[k].obterCustoSolucao()
				if aux_custo < custo:
					solucao = self.formigas[k].obterSolucao()[:]
					custo = aux_custo
		print('Solução final: %s | custo: %d\n' % (' -> '.join(str(i) for i in solucao), custo))


if __name__ == "__main__":

	# cria um grafo passando o número de vértices
	grafo = Grafo(num_vertices=8)

	# mapeando cidades para números
	d = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8}
	# adiciona as arestas
	grafo.adicionarAresta(d['B'], d['A'], 42)
	grafo.adicionarAresta(d['A'], d['B'], 42)
	grafo.adicionarAresta(d['C'], d['A'], 61)
	grafo.adicionarAresta(d['A'], d['C'], 61)
	grafo.adicionarAresta(d['C'], d['B'], 14)
	grafo.adicionarAresta(d['B'], d['C'], 14)
	grafo.adicionarAresta(d['D'], d['A'], 30)
	grafo.adicionarAresta(d['A'], d['D'], 30)
	grafo.adicionarAresta(d['D'], d['B'], 87)
	grafo.adicionarAresta(d['B'], d['D'], 87)
	grafo.adicionarAresta(d['D'], d['C'], 20)
	grafo.adicionarAresta(d['C'], d['D'], 20)
	grafo.adicionarAresta(d['E'], d['A'], 17)
	grafo.adicionarAresta(d['A'], d['E'], 17)
	grafo.adicionarAresta(d['E'], d['B'], 28)
	grafo.adicionarAresta(d['B'], d['E'], 28)
	grafo.adicionarAresta(d['E'], d['C'], 81)
	grafo.adicionarAresta(d['C'], d['E'], 81)
	grafo.adicionarAresta(d['E'], d['D'], 34)
	grafo.adicionarAresta(d['D'], d['E'], 34)
	grafo.adicionarAresta(d['F'], d['A'], 82)
	grafo.adicionarAresta(d['A'], d['F'], 82)
	grafo.adicionarAresta(d['F'], d['B'], 70)
	grafo.adicionarAresta(d['B'], d['F'], 70)
	grafo.adicionarAresta(d['F'], d['C'], 21)
	grafo.adicionarAresta(d['C'], d['F'], 21)
	grafo.adicionarAresta(d['F'], d['D'], 33)
	grafo.adicionarAresta(d['D'], d['F'], 33)
	grafo.adicionarAresta(d['F'], d['E'], 41)
	grafo.adicionarAresta(d['E'], d['F'], 41)
	grafo.adicionarAresta(d['G'], d['A'], 31)
	grafo.adicionarAresta(d['A'], d['G'], 31)
	grafo.adicionarAresta(d['G'], d['B'], 19)
	grafo.adicionarAresta(d['B'], d['G'], 19)
	grafo.adicionarAresta(d['G'], d['C'], 8)
	grafo.adicionarAresta(d['C'], d['G'], 8)
	grafo.adicionarAresta(d['G'], d['D'], 91)
	grafo.adicionarAresta(d['D'], d['G'], 91)
	grafo.adicionarAresta(d['G'], d['E'], 34)
	grafo.adicionarAresta(d['E'], d['G'], 34)
	grafo.adicionarAresta(d['G'], d['F'], 19)
	grafo.adicionarAresta(d['F'], d['G'], 19)
	grafo.adicionarAresta(d['H'], d['A'], 11)
	grafo.adicionarAresta(d['A'], d['H'], 11)
	grafo.adicionarAresta(d['H'], d['B'], 33)
	grafo.adicionarAresta(d['B'], d['H'], 33)
	grafo.adicionarAresta(d['H'], d['C'], 29)
	grafo.adicionarAresta(d['C'], d['H'], 29)
	grafo.adicionarAresta(d['H'], d['D'], 10)
	grafo.adicionarAresta(d['D'], d['H'], 10)
	grafo.adicionarAresta(d['H'], d['E'], 82)
	grafo.adicionarAresta(d['E'], d['H'], 82)
	grafo.adicionarAresta(d['H'], d['F'], 32)
	grafo.adicionarAresta(d['F'], d['H'], 32)
	grafo.adicionarAresta(d['H'], d['G'], 59)
	grafo.adicionarAresta(d['G'], d['H'], 59)

	# cria uma instância de ACO
	aco = ACO(grafo=grafo, num_formigas=grafo.num_vertices, alfa=1.0, beta=5.0, 
				iteracoes=1000, evaporacao=0.5)
	# roda o algoritmo
	aco.rodar()
	
	# teste com grafo completo
	'''
	num_vertices = 20
	print('Teste de grafo com %d vertices...\n' % num_vertices)
	grafo_completo = GrafoCompleto(num_vertices=num_vertices)
	grafo_completo.gerar()
	aco2 = ACO(grafo=grafo_completo, num_formigas=grafo_completo.num_vertices, 
				alfa=1, beta=5, iteracoes=100, evaporacao=0.5)
	aco2.rodar()
	'''
