import tkinter as tk

def crear_ficha_numero(parent, numero, color_caja, color_azul, color_rojo, color_verde, color_naranja):
    es_par = numero % 2 == 0
    es_bajo = numero <= 24

    color_numero = color_azul if es_par else color_rojo
    color_linea = color_verde if es_bajo else color_naranja
    texto_tipo = "PAR" if es_par else "IMPAR"
    texto_rango = "BAJO" if es_bajo else "ALTO"

    contenedor = tk.Frame(
        parent,
        bg=color_caja,
        width=110,
        height=140,
        highlightbackground="#CBD5E1",
        highlightthickness=1
    )
    contenedor.pack(side="left", padx=10, pady=10)
    contenedor.pack_propagate(False)

    banda_superior = tk.Frame(contenedor, bg=color_linea, height=6)
    banda_superior.pack(fill="x", side="top")

    cuerpo = tk.Frame(contenedor, bg=color_caja)
    cuerpo.pack(fill="both", expand=True)

    tk.Label(
        cuerpo,
        text=f"{numero:02d}",
        bg=color_caja,
        fg=color_numero,
        font=("Segoe UI", 28, "bold")
    ).pack(pady=(18, 6))

    tk.Label(
        cuerpo,
        text=texto_tipo,
        bg=color_caja,
        fg="#475569",
        font=("Segoe UI", 9, "bold")
    ).pack()

    tk.Label(
        cuerpo,
        text=texto_rango,
        bg=color_caja,
        fg="#64748B",
        font=("Segoe UI", 8)
    ).pack(pady=(2, 0))


def crear_chip_resultado(parent, texto, color_texto):
    label = tk.Label(
        parent,
        text=texto,
        bg="#111827",
        fg=color_texto,
        font=("Segoe UI", 9, "bold"),
        padx=12,
        pady=8,
        highlightbackground="#334155",
        highlightthickness=1
    )
    label.pack(side="left", padx=(0, 8))
    return label


def crear_tarjeta_metrica(parent, titulo, valor_inicial, color_panel, color_borde, color_texto_suave, color_blanco):
    tarjeta = tk.Frame(parent, bg=color_panel, highlightbackground=color_borde, highlightthickness=1)

    tk.Label(
        tarjeta,
        text=titulo,
        bg=color_panel,
        fg=color_texto_suave,
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="w", padx=10, pady=(8, 2))

    valor = tk.Label(
        tarjeta,
        text=valor_inicial,
        bg=color_panel,
        fg=color_blanco,
        font=("Segoe UI", 14, "bold")
    )
    valor.pack(anchor="w", padx=10, pady=(0, 8))

    return tarjeta, valor


def crear_label(parent, texto, color_panel, color_texto):
    return tk.Label(
        parent,
        text=texto,
        bg=color_panel,
        fg=color_texto,
        font=("Segoe UI", 10, "bold")
    )