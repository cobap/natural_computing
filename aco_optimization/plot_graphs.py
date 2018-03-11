import matplotlib.pyplot as plt
import sys
import numpy as np

data = np.genfromtxt('./results/eventos_output' + sys.argv[1] + '_limpo.csv', delimiter=',', skip_header=10, skip_footer=10, names=['EVENTO', 'NOME', 'INTENSIDADE', 'PONTO', 'GRAU_ATUAL', 'GRAU_ORIGINAL', 'RODADAS', 'STATUS'])

# plt.plot(data['PONTO'], data['INTENSIDADE'], label='linear')
# plt.hist(data['PONTO'], normed=True, bins=30)
# alturas = list(range(647))
# plt.bar(data['PONTO'], height=alturas)
plt.legend()
plt.show()