############# IMPORTAR #############
import numpy as np
import matplotlib.pyplot as plt

######### DADOS DO PROBLEMA ########
a = 1  # Difusividade térmica
L = 30 # Comprimento da barra

# Condição de Contorno
T_1 = 20  # Temperatura em x=0
T_2 = 50  # Temperatura em x=L

# Condição Inicial:
def f(x):
    return 60-2*x

############# DEFINIR ##############
T = 40  # Tempo máximo
M = 80  # Dividir L em M partes
N = 600 # Dividir T em N partes

############# MÉTODO ###############
# Determina o espaçamento da malha
dx = L/M
dt = T/N

# Verifica a estabilidade
sigma = a**2*dt/((dx)**2)
if sigma > 0.5:
    print("Critério de estabilidade violado")
    exit() # Interrompe

# Cria a matriz das soluções U_k^n
U = np.zeros((M+1, N+1))

# Valores iniciais para U
U[:,0] = f(np.arange(0, M + 1) * dx) # Condição de Inicial
U[0, 1:N+1] = T_1                    # Condição de Contorno
U[M, 1:N+1] = T_2                    # Condição de Contorno

for n in range(0, N):
    U[1:M, n + 1] = U[1:M, n] + sigma * (U[2:M + 1, n] - 2 * U[1:M, n] + U[0:M - 1, n])

########### GRAFICO 3D #############
x = np.arange(M+1)  # Coordenadas x
t = np.arange(N+1)  # Coordenadas t
X, Y = np.meshgrid(x, t)

# Criando a figura para plotagem 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Definindo limites de coloração
vmin = 20  # Limite inferior
vmax = 50  # Limite superior

surf = ax.plot_surface(X*dx, Y*dt, U.T, vmin=vmin, vmax=vmax, cmap='coolwarm', edgecolor='none', antialiased=True)
ax.invert_yaxis()  # Inverte o sentido do eixo t

# Ajustar o ângulo de visão
ax.view_init(elev=40, azim=230)

# Configurações do gráfico
ax.set_xlabel(r'$x$', labelpad=20)
ax.set_ylabel(r'$t$', labelpad=20)
ax.set_zlabel(r'$u$')

# Barra de cores para indicar temperatura
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
cbar.set_label('Temperatura (u)')
cbar.ax.yaxis.set_label_position('left')

plt.show() # Exibe o gráfico
