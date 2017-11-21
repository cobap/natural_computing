# -*- coding: utf-8 -*-
import math, random, copy

'''
*	Class Caminho:
*	Responsável por criar um caminho entre o ponto A e o ponto B (também classes)
'''
class Caminho:
	def __init__(self, pontoA, pontoB):
		self.pontoA = pontoA
		self.pontoB = pontoB
		self.distancia = 0
		self.feromonio = (random.randint(5,9)/10000.0) + (random.randint(1,9)/100000.0)
		# self.feromonio = 400	
		self.taxa_decaimento = 1

	def setDistancia(self, distancia):
		self.distancia = distancia

	def setFeromonio(self, novoFeromonio):
		self.feromonio = novoFeromonio

	def setTaxaDecaimento(self, nova_taxa):
		self.taxa_decaimento = nova_taxa

	def decaiFeromonio(self, decaimento):
		self.feromonio = self.feromonio/self.taxa_decaimento

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
		
		# return self.index, self.getCaminhos()[self.index], self.caminho_escolhido
		return self.index, self.caminho_escolhido

	def setObjeto(self, status):
		self.objeto = status

	def getObjeto(self):
		return self.objeto

class Cidade:
	def __init__(self, iteracoes):
		self.numero_pontos = random.randint(5, 10)
		self.pontos = []
		self.iteracoes = iteracoes
		self.formigas = []
		self.caminhos = []
		self.mediaAbelhas = random.randint(2,4)
		self.hqs = []
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
		print('QTD DE FORMIGAS: ', self.qtdFormigas)
		for formiga in range(self.qtdFormigas):
			self.formigas.append(Formiga('Patrulha', self.getPontoAleatorio()))
		# for formiga in self.formigas:
		# 	print(formiga.pontoAtual.nome)

	def criaHQs(self):
		self.qtdHQs = int(round((float) (self.numero_pontos * 1)/5))
		print('QTD DE HQs: ', self.qtdHQs)
		print('QTD DE Abelhas: ', self.mediaAbelhas)
		for hq in range(self.qtdHQs):
			self.hqs.append(HQ(self.mediaAbelhas, self.getPontoAleatorio()))
		for hq in self.hqs:
			print(hq.pontoAtual.nome)
			for abelha in hq.abelhas:
				print('Bee Name: ' + abelha.nome + 'HQ Bee Length: ' + str(len(hq.abelhas)))

	def getPontoAleatorio(self):
		while(True):
			pontoAleatorio = random.randint(0, self.numero_pontos-1)
			if self.pontos[pontoAleatorio].getObjeto() == False:
				print(self.pontos[pontoAleatorio].nome)
				return self.pontos[pontoAleatorio]

	def iniciaCidade(self):
		iterador = 0
		while(iterador < self.iteracoes):
			# print("-- Iteracao ",iterador)
			for formiga in self.formigas:
				# formiga.caminhaAleatoriamente()
				pass
			iterador = iterador + 1



class Formiga:
	def __init__(self, funcao, pontoAtual):
		self.funcao = funcao
		self.pontoAtual = pontoAtual
		self.pontoAtual.setObjeto(True)
		self.setNome()

	def setNome(self):
		letras = ['Corine', 'Nina', 'Laraine', 'Gaspard', 'Bartolemo', 'Rebe', 'Gasper', 'Pauli', 'Sheila-kathryn', 'Gus', 'Christabella', 'Thalia', 'Tyrone', 'Dennison', 'Udale', 'Annaliese', 'Rufus', 'Zebedee', 'Philbert', 'Collin', 'Colver', 'Marcile', 'Cherie', 'Janene', 'Ainslie', 'Bernardina', 'Ursula', 'Alene', 'Horatio', 'Edita', 'Sidnee', 'Gianna', 'Ashton', 'Cymbre', 'Adda', 'Charlena', 'Karly', 'York', 'Shanna', 'Tracie', 'Brook', 'Hilario', 'Darcy', 'Lisette', 'Jakie', 'Teodoro', 'Rochell', 'Jenn', 'Annadiana', 'Clint', 'Wilbur', 'Cariotta', 'Kinnie', 'Diarmid', 'Jocko', 'Mortie', 'Jarib', 'Westleigh', 'Mair', 'Trumaine', 'Emlyn', 'Abagael', 'Em', 'Dolores', 'Erina', 'Lou', 'Golda', 'Herold', 'Bryn', 'Christiane', 'Oralia', 'Bella', 'Kathi', 'Kerry', 'Lindsay', 'Claudetta', 'Manny', 'Cosette', 'Gordy', 'Jordan', 'Dean', 'Elaine', 'Andrey', 'Solly', 'Renie', 'Pepito', 'Godfree', 'Sabina', 'Liana', 'Stevana', 'Onfre', 'Hubert', 'Leslie', 'Chev', 'Caryn', 'Rollins', 'Adriane', 'Bealle', 'Catharine', 'Ulrich', 'Ikey']
		letra = random.randint(0, len(letras)-1)
		numero = random.randint(1,100)
		self.nome = str(letras[letra]) + str(letra)

	def caminhaAleatoriamente(self):
		print('Formiguinha ' + self.nome)
		print(self.pontoAtual.getProbabilidade())

class Abelha:
	def __init__(self, funcao, id_hq, pontoAtual):
		self.funcao = funcao
		self.id_hq = id_hq
		self.setNome()
		self.pontoAtual = pontoAtual
		self.pontoAtual.setObjeto(True)

	def setNome(self):
		letras = ['Corine', 'Nina', 'Laraine', 'Gaspard', 'Bartolemo', 'Rebe', 'Gasper', 'Pauli', 'Sheila-kathryn', 'Gus', 'Christabella', 'Thalia', 'Tyrone', 'Dennison', 'Udale', 'Annaliese', 'Rufus', 'Zebedee', 'Philbert', 'Collin', 'Colver', 'Marcile', 'Cherie', 'Janene', 'Ainslie', 'Bernardina', 'Ursula', 'Alene', 'Horatio', 'Edita', 'Sidnee', 'Gianna', 'Ashton', 'Cymbre', 'Adda', 'Charlena', 'Karly', 'York', 'Shanna', 'Tracie', 'Brook', 'Hilario', 'Darcy', 'Lisette', 'Jakie', 'Teodoro', 'Rochell', 'Jenn', 'Annadiana', 'Clint', 'Wilbur', 'Cariotta', 'Kinnie', 'Diarmid', 'Jocko', 'Mortie', 'Jarib', 'Westleigh', 'Mair', 'Trumaine', 'Emlyn', 'Abagael', 'Em', 'Dolores', 'Erina', 'Lou', 'Golda', 'Herold', 'Bryn', 'Christiane', 'Oralia', 'Bella', 'Kathi', 'Kerry', 'Lindsay', 'Claudetta', 'Manny', 'Cosette', 'Gordy', 'Jordan', 'Dean', 'Elaine', 'Andrey', 'Solly', 'Renie', 'Pepito', 'Godfree', 'Sabina', 'Liana', 'Stevana', 'Onfre', 'Hubert', 'Leslie', 'Chev', 'Caryn', 'Rollins', 'Adriane', 'Bealle', 'Catharine', 'Ulrich', 'Ikey']
		letra = random.randint(0, len(letras)-1)
		numero = random.randint(1,100)
		self.nome = str(letras[letra]) + str(letra)

class HQ:
	def __init__(self, numero_abelhas, pontoAtual):
		self.numero_abelhas = numero_abelhas
		self.setNome()
		self.pontoAtual = pontoAtual
		self.pontoAtual.setObjeto(True)
		self.abelhas = []
		self.criaAbelhas()

	def criaAbelhas(self):
		for iterador in range(0, self.numero_abelhas):
			abelhaTemp = Abelha('Tropa', self.nome, self.pontoAtual)
			self.abelhas.append(abelhaTemp)

	def setNome(self):
		letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
		letra = random.randint(0, len(letras)-1)
		numero = random.randint(1,100)
		self.nome =  str(letra) + str(letras[letra])


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

	cidade1 = Cidade(30)
	cidade1.criaFormigas()
	cidade1.criaHQs()
	cidade1.iniciaCidade()
	# cidade1.mostraCidade()