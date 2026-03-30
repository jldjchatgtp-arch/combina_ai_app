def analizar(comb):
    bajos = [n for n in comb if n <= 24]
    altos = [n for n in comb if n > 24]
    pares = [n for n in comb if n % 2 == 0]
    impares = [n for n in comb if n % 2 != 0]
    suma = sum(comb)
    decenas = [n // 10 for n in comb]

    max_run = 1
    actual = 1

    for i in range(1, len(comb)):
        if comb[i] == comb[i - 1] + 1:
            actual += 1
            max_run = max(max_run, actual)
        else:
            actual = 1

    return bajos, altos, pares, impares, suma, decenas, max_run