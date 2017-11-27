# -*- coding: utf-8 -*-
import math, random, copy
'''
*	Class Caminho:
*	Responsável por criar um caminho entre o ponto A e o ponto B
*	Define a distancia do caminho, quantidade de feromonio e a taxa de decaimento deste
'''
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

'''
*	Class Cidade:
*	Responsável por criar o grafo conexo, formigas, HQs e eventos, além de demais calculos
*	Possui as variáveis que definem qtd de abelhas no HQ, alfa e beta para o ACO, etc
'''
class Cidade:
	def __init__(self, iteracoes):
		#Parametros do ACO
		self.alfa=1.0
		self.beta=5.0
		self.formigas = []

		#Parametros das Abelha
		self.mediaAbelhas = random.randint(2,4)
		self.hqs = []

		#Parametro dos Eventos
		self.eventos = []

		#Parametros Gerais
		self.numero_pontos = random.randint(6, 10)
		self.pontos = []
		self.iteracoes = iteracoes
		self.caminhos = []

		print('QTD PONTOS: ', self.numero_pontos)
		# Dado o numero de pontos aleatórios
		for ponto in range(self.numero_pontos):
			# Crie pontos com coordenadas aleatórias
			a = Ponto(random.randint(1,10), random.randint(1,10))
			# Os adicione na lista de pontos da cidade
			self.pontos.append(a)
			# print('CRIADO PONTO', a.nome)
		# Após todos os pontos criados, criamos o grafo conexo
		self.criaGrafoConexo()

	def mostraCidade(self):
		print('MOSTRA CIDADE-----------------------------')
		for caminho in self.caminhos:
			print('Caminho A ' + caminho.pontoA.nome + '- B ' + caminho.pontoB.nome)

	def criaGrafoConexo(self):
		# Primeiro fazemos uma cópia do vetor de pontos
		self.pontos_backup = copy.copy(self.pontos)
		self.pontos_aux = []
		
		# Enquanto ainda existir um ponto sem conexão
		while(len(self.pontos_backup) > 0):
			# Retiramos um ponto aleatório do vetor
			ponto = self.pontos_backup.pop(random.randint(0, len(self.pontos_backup)-1))
			# Caso ja tenhamos ao menos um vertice na nossa lista auxiliar
			if(len(self.pontos_aux) > 0):
				# Escolhemos aleatóriamente um vertice na lista auxiliar para que o ponto aleatório se conecte
				b = self.pontos_aux[random.randint(0, len(self.pontos_aux)-1)]
				# Adicionamos o novo caminho dentro do vetor de caminhos da cidade
				self.caminhos.append(Caminho(ponto, b))
				# Adicionariamos o caminho oposto caso a cidade fosse um grafo direcionado
				# b.criaCaminho(b, ponto)
			# Adicionamos o vertice na lista auxiliar
			self.pontos_aux.append(ponto)

	def criaFormigas(self):
		# O número de formigas sempre será 1/3 do número de vertices
		self.qtdFormigas = int(round((float) (self.numero_pontos * 1)/3))
		# self.qtdFormigas = 1
		print('QTD DE FORMIGAS: ', self.qtdFormigas)
		for formiga in range(self.qtdFormigas):
			# Crie uma formiga do tipo patrulha e adicione em um ponto onde não exista nenhuma outra classe
			self.formigas.append(Formiga('Patrulha', self.getPontoAleatorio()))

	def criaEvento(self):
		evento = Evento(self.getPontoAleatorio())
		self.eventos.append(evento)
		return evento

	def criaHQs(self):
		# Número de HQ é sempre 1/5 do número de vertices do grafo
		self.qtdHQs = int(round((float) (self.numero_pontos * 1)/5))
		print('QTD DE HQs: ', self.qtdHQs)
		print('QTD DE Abelhas: ', self.mediaAbelhas)
		# Adiciona todos os HQ criados dentro da cidade
		for hq in range(self.qtdHQs):
			self.hqs.append(HQ(self.mediaAbelhas, self.getPontoAleatorio()))

	def getPontoAleatorio(self):
		break_please = 0
		while(True):
			pontoAleatorio = random.randint(0, self.numero_pontos-1)
			if self.pontos[pontoAleatorio].getObjeto() == False:
				return self.pontos[pontoAleatorio]	

	#Problemas para criar eventos em vertices vazios
	def iniciaCidade(self):
		# Inicia cidade - criando formigas, HQs, eventos, etc...
		# random.seed(42)
		iterador = 0
		self.criaFormigas()
		self.criaHQs()
		
		# MAIN 
		while(iterador < self.iteracoes):
			# Para cada loop de interação, ande com as formigas aleatóriamente
			for formiga in self.formigas:
				# formiga.caminhaAleatoriamente(self.caminhos)
				formiga.caminhaACO(self.caminhos, self.alfa, self.beta)

			if iterador % 3 == 0:
					evento = self.criaEvento()
					print(evento)

			
			iterador = iterador + 1

'''
*	Class Formiga:
*	Implementação customizada do algoritmo ACO - cada formiga esta localizada em um ponto, tem uma "força" e uma função
'''
class Formiga:
	def __init__(self, funcao, pontoAtual):
		self.funcao = funcao
		# self.forca = forca
		self.pontoAtual = pontoAtual
		# Define que o ponto atual da formiga agora esta ocupado
		self.pontoAtual.setObjeto(True)
		# Cria um nome para a formiga
		self.setNome()

	def setNome(self):
		letras = ['Corine', 'Nina', 'Laraine', 'Gaspard', 'Bartolemo', 'Rebe', 'Gasper', 'Pauli', 'Sheila-kathryn', 'Gus', 'Christabella', 'Thalia', 'Tyrone', 'Dennison', 'Udale', 'Annaliese', 'Rufus', 'Zebedee', 'Philbert', 'Collin', 'Colver', 'Marcile', 'Cherie', 'Janene', 'Ainslie', 'Bernardina', 'Ursula', 'Alene', 'Horatio', 'Edita', 'Sidnee', 'Gianna', 'Ashton', 'Cymbre', 'Adda', 'Charlena', 'Karly', 'York', 'Shanna', 'Tracie', 'Brook', 'Hilario', 'Darcy', 'Lisette', 'Jakie', 'Teodoro', 'Rochell', 'Jenn', 'Annadiana', 'Clint', 'Wilbur', 'Cariotta', 'Kinnie', 'Diarmid', 'Jocko', 'Mortie', 'Jarib', 'Westleigh', 'Mair', 'Trumaine', 'Emlyn', 'Abagael', 'Em', 'Dolores', 'Erina', 'Lou', 'Golda', 'Herold', 'Bryn', 'Christiane', 'Oralia', 'Bella', 'Kathi', 'Kerry', 'Lindsay', 'Claudetta', 'Manny', 'Cosette', 'Gordy', 'Jordan', 'Dean', 'Elaine', 'Andrey', 'Solly', 'Renie', 'Pepito', 'Godfree', 'Sabina', 'Liana', 'Stevana', 'Onfre', 'Hubert', 'Leslie', 'Chev', 'Caryn', 'Rollins', 'Adriane', 'Bealle', 'Catharine', 'Ulrich', 'Ikey']
		letra = random.randint(0, len(letras)-1)
		numero = random.randint(1,100)
		self.nome = 'ANT-' + str(letras[letra]) + str(letra)

	def caminhaAleatoriamente(self, caminhos):
		print('FORMIGA '+self.nome + 'LUGAR '+self.pontoAtual.nome)
		# print('caminhos antigos' + str(len(caminhos)))
		caminhos = [caminho for caminho in caminhos if caminho.pontoA.nome == self.pontoAtual.nome or caminho.pontoB.nome == self.pontoAtual.nome]
		# print('caminhos antigos depois' + str(len(caminhos)))
		# Escolhe aleatóriamente baseado nos caminhos disponíveis, qual seguir
		caminhoEscolhido = random.randint(0, len(caminhos)-1)
		# Sai do vertice atual
		self.pontoAtual.setObjeto(False)
		# Define o vertice atual como o novo vertice - de onde foi do ponto A para o ponto B
		if(self.pontoAtual.nome == caminhos[caminhoEscolhido].pontoA.nome):
			self.pontoAtual = caminhos[caminhoEscolhido].pontoB
		else:
			self.pontoAtual = caminhos[caminhoEscolhido].pontoA
		# Define que esta ocupando o ponto B agora
		self.pontoAtual.setObjeto(True)
		# Define novo feromonio (por enquanto aleatóriamente)
		print('CAMINHO ' + caminhos[caminhoEscolhido].pontoA.nome + ' - ' + caminhos[caminhoEscolhido].pontoB.nome)
		print('FEROMONIO ANTIGO: '+ str(caminhos[caminhoEscolhido].feromonio))
		caminhos[caminhoEscolhido].setFeromonio((random.randint(5,9)/10000.0) + (random.randint(1,9)/100000.0))
		print('FEROMONIO NOVO: '+ str(caminhos[caminhoEscolhido].feromonio))

	def caminhaACO(self, caminhos, alfa, beta):
		# print('FORMIGA '+self.nome + 'LUGAR '+self.pontoAtual.nome)
		# print('BEFORE-----------------------------------')
		# for caminho in caminhos:
		# 	print(caminho)
		caminhos = [caminho for caminho in caminhos if caminho.pontoA.nome == self.pontoAtual.nome or caminho.pontoB.nome == self.pontoAtual.nome]
		# print('AFTER-----------------------------------')
		for caminho in caminhos:
			# print(caminho)
			pass

		# Vetor que será armazenada as probabilidades dos caminhos
		probabilidades = []
		for caminho in caminhos:
			# Calcula a probabilidade baseado no feromonio do caminho e a sua distancia
			probabilidade = (math.pow(caminho.feromonio, alfa) * math.pow(1.0 / caminho.distancia, beta))
			probabilidades.append(probabilidade)
		# Somatório de todas as probabilidades
		somatoria_probabilidades = sum(float(prob) for prob in probabilidades)
		
		caminho_escolhido = 0
		index_escolhido = -1
		# Para todos as probabilidades calculadas
		for index, probabilidade in zip(range(len(probabilidades)), probabilidades):
			# print('Caminho', str(caminhos[index]) ,'Probabilidade: ', probabilidade/somatoria_probabilidades, 'Distancia', caminhos[index].distancia)
			# Selecionada caminho escolhido como maior caso sua probabilidade seja a maior de todas
			if((probabilidade/somatoria_probabilidades) > caminho_escolhido):
				# Recalcula o caminho escolhido
				caminho_escolhido = (probabilidade/somatoria_probabilidades)
				# Define o index
				# print('MELHRO INDEX É', index)
				index_escolhido = index

		# print('MELHOR PONTO - INDEX', index_escolhido)
		# print('Caminho', str(caminhos[index_escolhido]) ,'Probabilidade: ', probabilidades[index_escolhido]/somatoria_probabilidades, 'Distancia', caminhos[index_escolhido].distancia)
		
		if(index_escolhido == -1):
			print('caminhando aleatóriamente')
			return self.caminhaAleatoriamente(caminhos)

		# Sai do vertice atual
		self.pontoAtual.setObjeto(False)
		# Define o vertice atual como o novo vertice - de onde foi do ponto A para o ponto B
		if(self.pontoAtual.nome == str(caminhos[index_escolhido])):
			self.pontoAtual = caminhos[index].pontoB
		else:
			self.pontoAtual = caminhos[index].pontoA
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
		
'''
*	Class Abelha:
*	Implementação customizada do algoritmo Abelha - possui uma função (define seu comportamento) e sua "força", juntas formam uma colmeia
'''		
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
		self.nome = 'BEE-' + str(letras[letra]) + str(letra)

	def __str__(self):
		return self.nome

'''
*	Class HQ:
*	Implementação customizada da Colmeia de Abelhas - define número de abelhas e serve como local de reguardo destas
'''
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
		self.nome =  'COL-' + str(letra) + str(letras[letra])

	def __str__(self):
		return self.nome

'''
*	Class Evento:
*	Representa um evento/ocorrencia policial dentro de um grafo. Possui um range e uma intensidade que define sua dificuldade de ser destruido
'''
class Evento:
	def __init__(self, pontoAtual):
		self.setIntensidadeRange()
		self.setNome()
		self.pontoAtual = pontoAtual
		self.pontoAtual.setObjeto(True)

	def setNome(self):
		letras = ['Assalto', 'Briga', 'Corrida de Rua', 'Depredação', 'Extermínio', 'Fuga', 'G', 'H', 'Individuo Suspeito', 'J', 'K', 'Ladrão', 'M', 'N', 'Operação Policial', 'PM na Área', 'Quadrilha', 'R', 'S', 'Tiroteio', 'U', 'Vítima', 'W', 'X', 'Y', 'Z']
		letra = random.randint(0, len(letras)-1)
		self.nome =  str(letras[letra]) +str(letra)

	def setIntensidadeRange(self):
		self.intensidade = random.randint(1,3)
		# Intensidade é sempre o número de envolvidos x3 que precisa para solucionar o problema
		# self.range = random.randint(1,2)
		self.range = 1

	def __str__(self):
		resultado = "| Intensidade: " + str(self.intensidade) 
		resultado += " | Local: " + str(self.pontoAtual.nome)
		return self.nome + resultado

#-------------------- MAIN --------------------#
if __name__ == "__main__":
	cidade1 = Cidade(3)
	cidade1.mostraCidade()
	cidade1.iniciaCidade()