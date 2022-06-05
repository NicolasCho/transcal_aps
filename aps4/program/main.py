from functions import *
from funcoesTermosol import plota, importa, geraSaida
import matplotlib.pyplot as plt
import sys

def main():
    args = sys.argv
    entrada = "entradas/" + args[1] + ".xls"
    saida = "saidas/" + args[2]
    fator = int(args[3])

    # Entrada
    [nn,N,nm,Inc,nc,F,nr,R] = importa(entrada)

    # Organizando matrizes
    Inc_comp = calc_dist_cs(N,Inc)
    a, b= matrizes_rigidez(Inc_comp,nm)
    mat_global = rigidez_global(a, b, nn)
    global_contorno, forca_contorno, restricoes = contorno(mat_global, R, F)

    # Encontrando resultados
    deslocamentos = Gauss_Seidel(global_contorno, forca_contorno)
    matriz_desolcamentos = resultado_deslocamentos(deslocamentos, restricoes, nn)
    apoios = resultado_apoio(mat_global, matriz_desolcamentos, restricoes)
    matriz_deformacao = resultado_deformacao(Inc_comp, matriz_desolcamentos, nm)
    tensoes = resultado_tensao(Inc_comp, matriz_deformacao)
    forcas = resultado_forca(Inc_comp, tensoes)

    # Saída
    geraSaida(saida, apoios, matriz_desolcamentos,matriz_deformacao, forcas, tensoes)

    #Gráficos
    new_N = novas_coordenadas(N, matriz_desolcamentos, fator)
    plota(N, Inc_comp, "entradas/" + args[1])
    plota(new_N, Inc_comp, "saidas/" + args[2])

    return None


if __name__ == "__main__":
   main()