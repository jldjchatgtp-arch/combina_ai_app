import random
from logic.filtros import cumple_filtros

def generar_combinacion():
    nums = random.sample(range(1, 50), 6)
    nums.sort()
    return nums

def generar_valida(config, max_intentos=50000):
    for _ in range(max_intentos):
        c = generar_combinacion()
        if cumple_filtros(c, config):
            return c
    return None