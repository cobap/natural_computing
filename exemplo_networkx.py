import networkx as nx
import matplotlib.pyplot as plt
g = nx.Graph(alfa=0.5)
print(g.graph)
# g.add_node(1)
# g.add_node('teste')
# g.add_nodes_from([2,3])
# print(g)
# g.add_edge(1,2)
# g.add_edges_from([(1,'teste'), (2,3)])

# print(g.number_of_nodes())
# print(g.number_of_edges())

class Exemplo():
	x = 123

	def __init__(self, x):
		self.x = x

	def fala_oi(self):
		print('ooooi')

	def __str__(self):
		return str(self.x)

x = Exemplo(123456)
y = Exemplo(654321)
g.add_node(x)
g.add_node(y)
g.add_edge(x,y, {'teste':'oi'})

g.node[x]['attrib'] = 423
print(g.node[x])
# print(x)
# print(g.nodes())
print(g.edges())
# for no in g.nodes():
	# no.fala_oi()
# print(g[0])
# print(g.neighbors(1))
n1 =nx.random_lobster(100,0.9,0.9)
nx.draw(n1)
# nx.draw_random(n1)
# nx.draw_circular(n1)
plt.savefig("grafico.png")
plt.show()