import matplotlib.pyplot as plt
import numpy as np

data = np.genfromtxt('./results/eventos_output1_limpo.csv', delimiter=',', skip_header=10, skip_footer=10, names=['EVENTO', 'NOME', 'INTENSIDADE', 'PONTO', 'GRAU_ATUAL', 'GRAU_ORIGINAL', 'RODADAS', 'STATUS'])

plt.plot(data['PONTO'], data['INTENSIDADE'], label='linear')
plt.legend()
plt.show()