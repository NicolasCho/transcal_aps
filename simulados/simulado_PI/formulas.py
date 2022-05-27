

def efetividade_max_mt(Tq, Tf):
    return (Tq - Tf)/Tq

def efetividade_real_mt(pot_util, pot_consumida):
    return pot_util/pot_consumida

def erro_dif_finita(T_anterior, T_atual):
    return abs(T_anterior-T_atual)/T_atual

