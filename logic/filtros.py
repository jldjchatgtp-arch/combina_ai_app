from logic.analizador import analizar

def cumple_filtros(comb, config):
    try:
        bajos, altos, pares, impares, suma, decenas, max_run = analizar(comb)

        b_sel, a_sel = map(int, config["bajos_altos"].split("-"))
        if len(bajos) != b_sel or len(altos) != a_sel:
            return False

        p_sel, i_sel = map(int, config["pares_impares"].split("-"))
        if len(pares) != p_sel or len(impares) != i_sel:
            return False

        suma_minima = int(config["suma_min"])
        suma_maxima = int(config["suma_max"])
        if suma_minima > suma_maxima:
            return False

        if not (suma_minima <= suma <= suma_maxima):
            return False

        valor = int(config["max_consec"])
        if valor not in (1, 2, 3):
            return False

        if max_run > valor:
            return False

        valor_decenas = int(config["decenas"])
        if valor_decenas < 1 or valor_decenas > 5:
            return False

        if len(set(decenas)) != valor_decenas:
            return False

        return True

    except (ValueError, KeyError):
        return False