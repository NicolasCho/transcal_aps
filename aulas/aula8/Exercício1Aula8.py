# -*- coding: utf-8 -*-
"""
Created ...

@author: 
"""

import numpy as np
import matplotlib.pyplot as plt

"""
Considere uma barra longa de alumínio com difusividade 𝛼=0,835𝑐𝑚^2/𝑠 e
com um comprimento de 10𝑐𝑚. Use o método das diferenças finitas e faça
um gráfico para a temperatura em todos pontos da malha (Use Δ𝑥=2𝑐𝑚 e Δ𝑡=0,1𝑠)
para 𝑡 = 3,6,9 segundos. As condições de contorno são fixas em todos os tempo
𝑇(0)=100℃ e 𝑇(10)=50℃.

"""
#%% Entrada de dados

# Difusividade [cm²/s]
alpha = 0.835

# Discretização da malha em x [cm]
dx = 2/6

# Discretização no tempo [s]
dt = 0.1/4

# Comprimento da barra [cm]
L = 10

# Número de passos []
n = 100

#%% Cálculos iniciais

# Constante alpha*dt/dx**2
c = (alpha*dt)/dx**2

# Tempo total [s]
tt = dt*n

# Número de nós []
nn = int(L/dx)+1

#%% Matriz para armazenar todas as temperaturas [C] 

## TM = [nº passos no tempo, nº de nós na malha espacial]
TM = np.zeros((n,nn))

#%% Aplicando as condições de contorno e inicial
# Condição inicial nos nós internos
TM[0,1:nn-1] = 0.0

# Temperatura [C] em x=0
TM[:,0]=100 

# Temperatura [C] em x=L
TM[:,nn-1]=50

#%% Loop sobre os pontos da malha para determinar TM
for l in range(0,n-1):
    for i in range(1,nn-1):
        TM[l+1,i] = TM[l,i] + c * (TM[l,i+1] - 2*TM[l,i] + TM[l,i-1])

#%% Gráfico para a temperatura
# Instante plotado
inst = 100
# Posições dos nós
x = np.linspace(0.0,L,nn)
# Temperatura em todos pontos no instante considerado
T = np.array(TM[inst-1,:])
# Plot
plt.plot(x,T)
plt.ylabel('Temperatura [C]')
plt.xlabel('Posicao [cm]')
plt.show()


