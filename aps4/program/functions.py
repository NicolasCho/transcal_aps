import numpy as np
import math

def calc_dist_cs(N, Inc):
    """
        Recebe matriz dos nós e de incidência. A função retorna uma nova matriz de incidência com as colunas de comprimento, cossenos e senos
        de cada membro.
    """
    l_list = []
    c_list = []
    s_list = []
    
    for membro in Inc:
        no1 = int(membro[0]) - 1 
        no2 = int(membro[1]) - 1
        l = (math.sqrt((N[0][no1] - N[0][no2])**2 + (N[1][no1] - N[1][no2])**2))
        c = (N[0][no2]-N[0][no1])/l
        s = (N[1][no2]-N[1][no1])/l
        l_list.append(l)
        c_list.append(c)
        s_list.append(s)
    l_array = np.c_[l_list]
    c_array = np.c_[c_list]
    s_array = np.c_[s_list]
    Inc = np.hstack((Inc, l_array))
    Inc = np.hstack((Inc, c_array))
    Inc = np.hstack((Inc, s_array))
    return Inc

def matrizes_rigidez(Inc, nm):
    """
        Recebe a matriz de incidência (com comprimento, cosseno e seno) e número de membros. A função retorna uma array 3D com as matrizes de rigidez de cada 
        elemento. A função também retorna uma matriz 4D de coordenadas correspondente a cada matriz de rigidez (a ser utilizada para determinar a matriz global).
    """
    matrizes = np.zeros(shape=(nm,4,4))   # Considerando a treliça com duas extremidades
    matrizes_coordenada = np.zeros(shape=(nm,4,4,2))   # Considerando as coordenadas alinhadas com os graus de liberdade
    
    i = 0
    for cs in Inc:
        rigidez = cs[2]*cs[3]/cs[4]  # E*A/L para todos os membros
        
    
        
        c = cs[5]
        s = cs[6]
        matriz_cs = [[c**2 ,     c*s,   -(c**2), -(c*s) ],
                     [c*s ,      s**2,  -(c*s),  -(s**2)],
                     [-(c**2),  -(c*s),  c**2,    c*s  ],
                     [-(c*s),   -(s**2), c*s,     s**2  ]]

        matriz_coord = np.zeros(shape=(4,4,2))

        grau_linha = 0
        grau_coluna = 0
        for m in range(4):
            if   m == 0:
                grau_linha = cs[0]*2-1
            elif m == 1:
                grau_linha = cs[0]*2 
            elif m == 2:
                grau_linha = cs[1]*2-1 
            elif m == 3:
                grau_linha = cs[1]*2 
                
            for n in range(4):
                if   n == 0:
                    grau_coluna = cs[0]*2-1
                elif n == 1:
                    grau_coluna = cs[0]*2
                elif n == 2:
                    grau_coluna = cs[1]*2-1
                elif n == 3:
                    grau_coluna = cs[1]*2

                matriz_coord[m][n] = (grau_linha-1, grau_coluna-1)
       
        
        matriz_cs = np.multiply(matriz_cs, rigidez)


        matrizes_coordenada[i,:,:,:] = matriz_coord[:,:,:]
        matrizes[i,:,:] = np.add(matrizes[i,:,:], matriz_cs)

        i+=1
       
    return matrizes, matrizes_coordenada

def rigidez_global(matrizes_rigidez, matrizes_coordenadas, nn):
    """
        Recebe as matrizes de rigidez e suas correspondentes matrizes de coordenadas. A função retorna a matriz global de rigidez.
    """
    matriz_global = np.zeros(shape=(nn*2,nn*2))   # Considerando 2 graus de liberdade~
    elemento = 0 
    pos_lin = 0
    pos_col = 0
    for matriz_coordenada in matrizes_coordenadas:
        for linha in matriz_coordenada:
            for coordenada in linha:
                matriz_global[int(coordenada[0])][int(coordenada[1])] += matrizes_rigidez[elemento][pos_lin][pos_col]
                pos_col += 1
            pos_col = 0
            pos_lin += 1
        pos_lin = 0
        elemento += 1
        
    return matriz_global

def contorno(mat_global, R, F):
    """
        Recebe a matriz global de rigidez, o vetor de restrições e o vetor de carregamento. A função retorna uma nova matriz de rigidez global e um novo
        vetor de carregamento, ambos com as condições de contorno aplicadas. A função também retorna as restrições em forma de lista. 
    """
    contorno_lista = []
    for linha in R:
        for indice in linha:
            contorno_lista.append(int(indice))

    matriz_contorno = np.delete(mat_global, contorno_lista, 0)
    matriz_contorno = np.delete(matriz_contorno, contorno_lista, 1)
    matriz_forca_contorno = np.delete(F, contorno_lista, 0)
    return matriz_contorno, matriz_forca_contorno, contorno_lista

def Gauss_Seidel(a, b):
    """
        Recebe uma matriz 'a' e uma matriz resposta 'b'. A função aplica o método de Gauss-Seidel para resolver o sistema e retorna o vetor solução.
    """
    x = np.zeros((len(b),1))
    erro = 10000
    n = 0
    while(erro > 1e-10):
        i = 0
        while(i < len(b)):
            sup = 0
            j = 0
            while(j < len(b)):
                if j != i:
                    sup += a[i][j]*x[j]
                j += 1
                
            y = (b[i]-sup)/a[i][i]
        
            if y != 0:
                erro = abs((y - x[i]) / y)
                x[i] = y
            i += 1
            
    return x

def resultado_deslocamentos(deslocamentos, restricoes, nn):
    """
        Recebe o vetor de deslocamento (incompleto), lista de restrições (criada pela função 'contorno()') e o número de nós. A função retorna o vetor de 
        deslocamento completo (sem as condições de contorno)
    """
    matriz_desolcamentos = np.zeros(shape=(nn*2, 1))
    i_deslocamento = 0
    linha_matriz = 0
    
    for elemento in matriz_desolcamentos[:,0]:
        if linha_matriz not in restricoes:
            matriz_desolcamentos[linha_matriz][0] = deslocamentos[i_deslocamento]
            i_deslocamento += 1
        linha_matriz += 1

    return matriz_desolcamentos

def resultado_apoio(matriz_global, matriz_desolcamentos, restricoes):
    """
        Recebe a matriz de rigidez global, o vetor de deslocamento (completo) e a lista de restrições. A função retorna o vetor correspondente 
        as reações de apoio.
    """
    matriz_forcas = np.matmul(matriz_global, matriz_desolcamentos)
    deletar = []
    for i in range(matriz_forcas.shape[0]):
        if i not in restricoes:
            deletar.append(i)
    
    matriz_forcas = np.delete(matriz_forcas, deletar, 0)
    return matriz_forcas
        
def resultado_deformacao(Inc, matriz_deslocamento, nm):
    """
        Recebe a matriz de incidência (com comprimento, cosseno e seno), o vetor de deslocamento(completo) e o número de membros. A função retorna o vetor 
        de deformação de cada membro.
    """
    matriz_deformacao = np.zeros(shape=(nm,1))
    i = 0
    for elemento in Inc:
        c = elemento[5]
        s = elemento[6]
        l = elemento[4]
        no1 = int(elemento[0])
        no2 = int(elemento[1])
        mat_cs = [-c, -s, c, s]
        mat_desloc =[[matriz_deslocamento[no1*2-2][0]],
                     [matriz_deslocamento[no1*2-1][0]],
                     [matriz_deslocamento[no2*2-2][0]],
                     [matriz_deslocamento[no2*2-1][0]]]
        #print(mat_desloc)
        resultado_mult = np.matmul(mat_cs, mat_desloc)
        deformacao = np.multiply(resultado_mult, 1/l)
        matriz_deformacao[i][0] = deformacao[0]
        i+=1
    return matriz_deformacao

def resultado_tensao(Inc, mat_deformacao):
    """
        Recebe a matriz de incidência (com comprimento, cosseno e seno) e o vetor de deformação. A função retorna o vetor de tensão interna em cada membro. 
    """
    mat_tensao = mat_deformacao.copy()
    i = 0
    for elemento in Inc: 
        mat_tensao[i][0] = mat_deformacao[i][0]*elemento[2]
        i+=1
    return mat_tensao

def resultado_forca(Inc, mat_tensao):
    """
        Recebe a matriz de incidência (com comprimento, cosseno e seno) e o vetor de tensão. A função retorna o vetor de forças interna em cada membro. 
    """
    mat_forca = mat_tensao.copy()
    i = 0
    for elemento in Inc: 
        mat_forca[i][0] = mat_tensao[i][0]*elemento[3]
        i+=1
    return mat_forca

def novas_coordenadas(N, matriz_deslocamentos, fator):
    """
        Recebe a matriz de coordenadas dos nós (N), o vetor de deslocamento e um fator de multiplicação para melhorar visualizalção no gráfico. A função retorna 
        uma nova matriz dos nós, com os respectivos deslocamentos aplicados.
    """
    novo_N = N.copy()
    i_desloc = 0
    x = 0
    y = 0
    for x in range(novo_N.shape[0]):
        for y in range(novo_N.shape[1]):
            novo_N[x][y] += matriz_deslocamentos[i_desloc][0]*10**(fator)
            i_desloc += 2
        i_desloc = 1
    return novo_N