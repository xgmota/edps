############# IMPORTAR #############
import numpy as np
import matplotlib.pyplot as plt

######### DADOS DO PROBLEMA ########
a = 3  # Comprimento eixo x 
b = 2  # Comprimento eixo y

# Condições de Contorno
def f1(x): return 0 # Borda inferior
def f2(x): return 0 # Borda superior
def g1(y): return 0 # Borda esquerda
def g2(y):          # Borda direita
    return np.where((0 <= y) & (y <= 1), y,
                           np.where((1 < y) & (y < 2), 2-y, 0))

############# DEFINIR ##############
Omega = 1.77 # Fator de Relaxação
h = 0.10     # Espaçamento da malha
tol = 1e-5   # Erro máximo
max = 500    # Quantidade máxima de iterações

############# MÉTODO ###############
M = int(a/h) # Dividi a em M partes
N = int(b/h) # Dividi b em N partes

# Cria a matriz das soluções U_i^j
U = np.zeros((M+1, N+1))

# Definindo condições de contorno
U[:, 0]  = f1(np.arange(0, M + 1) * h) # Borda inferior
U[:, -1] = f2(np.arange(0, M + 1) * h) # Borda superior
U[0, :]  = g1(np.arange(0, N + 1) * h) # Borda esquerda
U[-1, :] = g2(np.arange(0, N + 1) * h) # Borda direita

erro = tol + 1 # Inicia a variável que armazena o erro
iteracao = 0   # Inicia a contagem das iterações

while erro > tol and iteracao < max:
   erro = 0          # Reseta o erro a cada iteração
   Ua = U.copy()  # Matriz da iteração anterior
   for i in range(1,M):
      for j in range(1, N):
         U[i,j] = (1-Omega)*U[i,j] + Omega*(U[i+1,j]+U[i-1,j]+U[i,j+1]+U[i,j-1])/4
         erro = np.maximum(erro, np.abs(U[i,j] - Ua[i,j]))
   iteracao += 1
   # print(f'Iteração {iteracao}, Erro = {erro}')

########### GRAFICO 3D #############
x = np.arange(M+1)  # Coordenadas x
y = np.arange(N+1)  # Coordenadas t
X, Y = np.meshgrid(x, y)

# Criar o gráfico 3D
fig = plt.figure(figsize=(20, 8))
ax = fig.add_subplot(111, projection='3d')

# Definindo vmin e vmax
vmin = 0  # Valor mínimo que você deseja para a coloração
vmax = 1  # Valor máximo que você deseja para a coloração

# Adicionar a superfície com um novo colormap
surf = ax.plot_surface(X*h, Y*h, U.T, cmap='rainbow', vmin=vmin, vmax=vmax, edgecolor='none', antialiased=True)  # Suavizar a pintura
ax.invert_yaxis()  # Inverte o sentido do eixo y

# Ajustar o ângulo de visão
ax.view_init(elev=30, azim=230)

# Configurações do gráfico
ax.set_xlabel(r'$x$', labelpad=20)
ax.set_ylabel(r'$y$', labelpad=20)
ax.set_zlabel(r'$u$')

plt.show() # Exibe o gráfico