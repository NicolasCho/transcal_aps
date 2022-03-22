# -*- coding: utf-8 -*-
"""
@author: 
"""

"""
Desenvolva um programa computacional para obter um gráfico
indicando a temperatura na placa.
 
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

#%% Entrada de dados
# Difusividade [m²/s]
alpha = ??

# Discretização da malha em x e y [m]
dx = .1
dy = .1

# Discretização no tempo [s]
dt = 1.0
dt = .01

# Dimensões da chapa [m]
Lx = ?
Ly = ?

# Número de passos no tempo []
nt = ?

#%% Cálculos iniciais
# Tempo total [s]
tt = dt*nt

# Número de nós []
nx = int(Lx/dx)+1
ny = int(Ly/dy)+1

#%% Matriz para armazenar todas as temperaturas [C] 
T = np.zeros(shape=(ny,nx,nt))

#%% Condição de contorno
T[ny-1,:,:] = ?
T[0,:,:] = ?
T[:,0,:] = ?
T[:,nx-1,:] = ?

# Condição inicial [t=0] foi inicializada como zero

#%% Tolerancia []
tol = ??

#%% Cálculos no tempo
for p in range(0,nt-1):
    for n in range(1,nx-1):
        for m in range(1,ny-1):
    
            T[m,n,p+1] = ?? 
               
    erro = np.amax(abs((T[1:nx-1,1:ny-1,p]-T[1:nx-1,1:ny-1,p-1])/T[1:nx-1,1:ny-1,p]))
    if tol>=erro:
        
        print('Convergiu!',p)
        break
      
#%% Gráfico para a temperatura
ax = plt.subplot(111)
im = ax.imshow(T[:,:,p])
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)
print(T[:,:,p])
