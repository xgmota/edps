############# IMPORTAR #############
import numpy as np
import matplotlib.pyplot as plt

######### DADOS DO PROBLEMA ########
a = 2  # Coeficiente
L = 30 # Comprimento da corda

# Condição de Contorno
U_0 = 0  # Posição inicial em x=0
U_M = 0  # Posição inicial em x=L

# Condição Inicial:
def f(x):
    return np.where((0 <= x) & (x <= 10), x / 10,
                    np.where((10 < x) & (x < 30), (30 - x) / 20, 0))

# Velocidade inicial
def g(x):
    return np.zeros_like(x)

############# DEFINIR ##############
T = 15  # Tempo máximo
M = 40  # Dividir L em M partes
N = 300 # Dividir T em N partes

############# MÉTODO ###############
# Determina o espaçamento da malha
dx = L/M
dt = T/N

# Verifica a estabilidade
C = a*dt/dx # Número de Courant
if abs(C) > 1:
    print("Critério de estabilidade violado")
    print(C)
    exit() # Interrompe

# Cria a matriz das soluções U_k^n
U = np.zeros((M+1, N+1))

# Valores iniciais para U
U[:,0] = f(np.arange(0, M + 1) * dx) # Condição de Inicial
U[0, 1:N+1] = U_0                    # Condição de Contorno
U[M, 1:N+1] = U_M                    # Condição de Contorno

# U_k^1
U[1:M, 1] = U[1:M, 0] + dt*g(np.arange(1, M)*dx) + C**2/2*(U[2:M + 1, 0] - 2 * U[1:M, 0] + U[0:M - 1, 0])

for n in range(1, N):
    U[2:M, n + 1] = 2*U[2:M, n] - U[2:M, n-1] + C**2 * (U[3:M + 1, n] - 2 * U[2:M, n] + U[1:M - 1, n])

########### GRAFICO 3D #############
x = np.arange(M+1)  # Coordenadas x
t = np.arange(N+1)  # Coordenadas t
X, Y = np.meshgrid(x, t)

# Criando a figura para plotagem 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Definindo limites de coloração
vmin = -1 # Limite inferior
vmax = 1  # Limite superior

surf = ax.plot_surface(X*dx, Y*dt, U.T, vmin=vmin, vmax=vmax, cmap='plasma', edgecolor='none', antialiased=True)
ax.set_ylim(0,T)
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