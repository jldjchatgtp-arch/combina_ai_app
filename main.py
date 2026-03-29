import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# -----------------------------
# COLORES
# -----------------------------
COLOR_FONDO = "#0B1120"
COLOR_PANEL = "#111827"
COLOR_PANEL_2 = "#1F2937"
COLOR_CAJA = "#F8FAFC"
COLOR_TEXTO = "#E5E7EB"
COLOR_TEXTO_SUAVE = "#94A3B8"
COLOR_AZUL = "#2563EB"
COLOR_AZUL_HOVER = "#1D4ED8"
COLOR_VERDE = "#22C55E"
COLOR_NARANJA = "#F59E0B"
COLOR_ROJO = "#EF4444"
COLOR_BORDE = "#334155"
COLOR_BLANCO = "#FFFFFF"
COLOR_AMARILLO_SUAVE = "#FEF3C7"
COLOR_VERDE_SUAVE = "#DCFCE7"

# -----------------------------
# GENERAR
# -----------------------------
def generar_combinacion():
    nums = random.sample(range(1, 50), 6)
    nums.sort()
    return nums

# -----------------------------
# ANALIZAR
# -----------------------------
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

# -----------------------------
# FILTROS
# -----------------------------
def cumple_filtros(comb):
    try:
        bajos, altos, pares, impares, suma, decenas, max_run = analizar(comb)

        b_sel, a_sel = map(int, combo_bajos_altos.get().split("-"))
        if len(bajos) != b_sel or len(altos) != a_sel:
            return False

        p_sel, i_sel = map(int, combo_pares_impares.get().split("-"))
        if len(pares) != p_sel or len(impares) != i_sel:
            return False

        suma_minima = int(suma_min.get())
        suma_maxima = int(suma_max.get())
        if suma_minima > suma_maxima:
            return False

        if not (suma_minima <= suma <= suma_maxima):
            return False

        valor = int(max_consec.get())
        if valor not in (1, 2, 3):
            return False
        if max_run > valor:
            return False

        valor_decenas = int(decenas_input.get())
        if valor_decenas < 1 or valor_decenas > 5:
            return False

        if len(set(decenas)) != valor_decenas:
            return False

        return True

    except ValueError:
        return False

# -----------------------------
# GENERAR VÁLIDA
# -----------------------------
def generar_valida():
    for _ in range(50000):
        c = generar_combinacion()
        if cumple_filtros(c):
            return c
    return None

# -----------------------------
# HISTORIAL
# -----------------------------
historial_set = set()

def agregar_historial(combinaciones):
    historial_text.config(state="normal")
    for c in combinaciones:
        clave = tuple(c)
        if clave not in historial_set:
            historial_set.add(clave)
            historial_text.insert(tk.END, "• " + " - ".join(f"{n:02d}" for n in c) + "\n")
    historial_text.see(tk.END)
    historial_text.config(state="disabled")

def borrar_historial():
    historial_text.config(state="normal")
    historial_text.delete("1.0", tk.END)
    historial_text.config(state="disabled")
    historial_set.clear()

# -----------------------------
# UTILIDADES VISUALES
# -----------------------------
def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def crear_ficha_numero(parent, numero):
    es_par = numero % 2 == 0
    es_bajo = numero <= 24

    color_numero = COLOR_AZUL if es_par else COLOR_ROJO
    color_linea = COLOR_VERDE if es_bajo else COLOR_NARANJA
    texto_tipo = "PAR" if es_par else "IMPAR"
    texto_rango = "BAJO" if es_bajo else "ALTO"

    contenedor = tk.Frame(
        parent,
        bg=COLOR_CAJA,
        width=110,
        height=140,
        highlightbackground="#CBD5E1",
        highlightthickness=1
    )
    contenedor.pack(side="left", padx=10, pady=10)
    contenedor.pack_propagate(False)

    banda_superior = tk.Frame(contenedor, bg=color_linea, height=6)
    banda_superior.pack(fill="x", side="top")

    cuerpo = tk.Frame(contenedor, bg=COLOR_CAJA)
    cuerpo.pack(fill="both", expand=True)

    tk.Label(
        cuerpo,
        text=f"{numero:02d}",
        bg=COLOR_CAJA,
        fg=color_numero,
        font=("Segoe UI", 28, "bold")
    ).pack(pady=(18, 6))

    tk.Label(
        cuerpo,
        text=texto_tipo,
        bg=COLOR_CAJA,
        fg="#475569",
        font=("Segoe UI", 9, "bold")
    ).pack()

    tk.Label(
        cuerpo,
        text=texto_rango,
        bg=COLOR_CAJA,
        fg="#64748B",
        font=("Segoe UI", 8)
    ).pack(pady=(2, 0))

# -----------------------------
# PANEL DE MÉTRICAS CENTRALES
# -----------------------------
def actualizar_panel_analisis(c, bajos, altos, pares, impares, suma, decenas, max_run):
    valor_combinacion.config(text=" - ".join(f"{n:02d}" for n in c))
    valor_suma.config(text=str(suma))
    valor_paridad.config(text=f"{len(pares)} / {len(impares)}")
    valor_altura.config(text=f"{len(bajos)} / {len(altos)}")
    valor_decenas.config(text=str(len(set(decenas))))
    valor_consecutivos.config(text=str(max_run))

# -----------------------------
# RESUMEN INFERIOR
# -----------------------------
def actualizar_resumen(c, bajos, altos, pares, impares, suma, decenas, max_run):
    texto_inferior.config(state="normal")
    texto_inferior.delete("1.0", tk.END)

    texto_inferior.insert(tk.END, "ANÁLISIS DETALLADO\n\n")
    texto_inferior.insert(tk.END, f"• Combinación: {' - '.join(f'{n:02d}' for n in c)}\n")
    texto_inferior.insert(tk.END, f"• Suma total: {suma}\n")
    texto_inferior.insert(tk.END, f"• Pares: {len(pares)} | Impares: {len(impares)}\n")
    texto_inferior.insert(tk.END, f"• Bajos: {len(bajos)} | Altos: {len(altos)}\n")
    texto_inferior.insert(tk.END, f"• Decenas distintas: {len(set(decenas))}\n")
    texto_inferior.insert(tk.END, f"• Máximo de consecutivos: {max_run}\n\n")
    texto_inferior.insert(tk.END, "LEYENDA VISUAL\n\n")
    texto_inferior.insert(tk.END, "• Azul = número par\n")
    texto_inferior.insert(tk.END, "• Rojo = número impar\n")
    texto_inferior.insert(tk.END, "• Banda verde = número bajo (1-24)\n")
    texto_inferior.insert(tk.END, "• Banda naranja = número alto (25-49)\n")

    texto_inferior.config(state="disabled")

# -----------------------------
# GENERAR 1
# -----------------------------
def generar_1():
    c = generar_valida()

    if not c:
        messagebox.showerror("Error", "Filtros demasiado estrictos o datos no válidos.")
        return

    bajos, altos, pares, impares, suma, decenas, max_run = analizar(c)

    limpiar_frame(frame_numeros_resultado)

    for n in c:
        crear_ficha_numero(frame_numeros_resultado, n)

    label_resultado_estado.config(
        text="Combinación generada según tus filtros activos"
    )

    label_chip_suma.config(text=f"SUMA · {suma}")
    label_chip_paridad.config(text=f"PARIDAD · {len(pares)}/{len(impares)}")
    label_chip_altura.config(text=f"ALTURA · {len(bajos)}/{len(altos)}")
    label_chip_decenas.config(text=f"DECENAS · {len(set(decenas))}")
    label_chip_consec.config(text=f"RUN · {max_run}")

    actualizar_panel_analisis(c, bajos, altos, pares, impares, suma, decenas, max_run)
    actualizar_resumen(c, bajos, altos, pares, impares, suma, decenas, max_run)
    agregar_historial([c])

# -----------------------------
# VENTANA PRINCIPAL
# -----------------------------
ventana = tk.Tk()
ventana.title("LotoStrategy")
ventana.geometry("1680x980")
ventana.minsize(1400, 860)
ventana.configure(bg=COLOR_FONDO)

# -----------------------------
# ESTILOS
# -----------------------------
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCombobox",
    fieldbackground=COLOR_CAJA,
    background=COLOR_CAJA,
    foreground="#111827",
    padding=8
)

style.configure(
    "Accent.TButton",
    font=("Segoe UI", 12, "bold"),
    padding=14,
    background=COLOR_AZUL,
    foreground="white",
    borderwidth=0
)

style.map(
    "Accent.TButton",
    background=[("active", COLOR_AZUL_HOVER)],
    foreground=[("active", "white")]
)

# -----------------------------
# CONTENEDOR GENERAL
# -----------------------------
contenedor = tk.Frame(ventana, bg=COLOR_FONDO)
contenedor.pack(fill="both", expand=True, padx=18, pady=18)

# -----------------------------
# CABECERA
# -----------------------------
cabecera = tk.Frame(contenedor, bg=COLOR_FONDO)
cabecera.pack(fill="x", pady=(0, 18))

titulo_app = tk.Label(
    cabecera,
    text="LotoStrategy",
    bg=COLOR_FONDO,
    fg=COLOR_BLANCO,
    font=("Segoe UI", 34, "bold"),
    anchor="center",
    justify="center"
)
titulo_app.pack(fill="x")

subtitulo_app = tk.Label(
    cabecera,
    text="Generador visual de combinaciones 6/49 con filtros inteligentes y diseño profesional",
    bg=COLOR_FONDO,
    fg=COLOR_TEXTO_SUAVE,
    font=("Segoe UI", 11),
    anchor="center",
    justify="center"
)
subtitulo_app.pack(fill="x", pady=(4, 0))

linea = tk.Frame(cabecera, bg=COLOR_BORDE, height=1)
linea.pack(fill="x", pady=(14, 0))

# -----------------------------
# CUERPO PRINCIPAL
# -----------------------------
cuerpo = tk.Frame(contenedor, bg=COLOR_FONDO)
cuerpo.pack(fill="both", expand=True)

# -----------------------------
# PANEL IZQUIERDO
# -----------------------------
panel_izquierdo = tk.Frame(
    cuerpo,
    bg=COLOR_PANEL,
    width=320,
    highlightbackground=COLOR_BORDE,
    highlightthickness=1
)
panel_izquierdo.pack(side="left", fill="y", padx=(0, 16))
panel_izquierdo.pack_propagate(False)

tk.Label(
    panel_izquierdo,
    text="PANEL DE FILTROS",
    bg=COLOR_PANEL,
    fg=COLOR_BLANCO,
    font=("Segoe UI", 18, "bold")
).pack(anchor="w", padx=20, pady=(20, 8))

tk.Label(
    panel_izquierdo,
    text="Configura las reglas antes de generar una nueva combinación.",
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO_SUAVE,
    font=("Segoe UI", 10),
    wraplength=270,
    justify="left"
).pack(anchor="w", padx=20, pady=(0, 18))

def crear_label(parent, texto):
    return tk.Label(
        parent,
        text=texto,
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO,
        font=("Segoe UI", 10, "bold")
    )

opciones = ["3-3", "2-4", "4-2", "1-5", "5-1", "6-0", "0-6"]

crear_label(panel_izquierdo, "Bajos / Altos").pack(anchor="w", padx=20, pady=(0, 6))
combo_bajos_altos = ttk.Combobox(panel_izquierdo, values=opciones, state="readonly", font=("Segoe UI", 11))
combo_bajos_altos.set("3-3")
combo_bajos_altos.pack(fill="x", padx=20, pady=(0, 14))

crear_label(panel_izquierdo, "Pares / Impares").pack(anchor="w", padx=20, pady=(0, 6))
combo_pares_impares = ttk.Combobox(panel_izquierdo, values=opciones, state="readonly", font=("Segoe UI", 11))
combo_pares_impares.set("3-3")
combo_pares_impares.pack(fill="x", padx=20, pady=(0, 14))

crear_label(panel_izquierdo, "Suma mínima").pack(anchor="w", padx=20, pady=(0, 6))
suma_min = tk.Entry(panel_izquierdo, font=("Segoe UI", 11), bg=COLOR_CAJA, fg="#111827", relief="flat", insertbackground="#111827")
suma_min.insert(0, "120")
suma_min.pack(fill="x", padx=20, ipady=8, pady=(0, 14))

crear_label(panel_izquierdo, "Suma máxima").pack(anchor="w", padx=20, pady=(0, 6))
suma_max = tk.Entry(panel_izquierdo, font=("Segoe UI", 11), bg=COLOR_CAJA, fg="#111827", relief="flat", insertbackground="#111827")
suma_max.insert(0, "180")
suma_max.pack(fill="x", padx=20, ipady=8, pady=(0, 14))

crear_label(panel_izquierdo, "Consecutivos máximos (1, 2 o 3)").pack(anchor="w", padx=20, pady=(0, 6))
max_consec = tk.Entry(panel_izquierdo, font=("Segoe UI", 11), bg=COLOR_CAJA, fg="#111827", relief="flat", insertbackground="#111827")
max_consec.insert(0, "2")
max_consec.pack(fill="x", padx=20, ipady=8, pady=(0, 14))

crear_label(panel_izquierdo, "Decenas distintas (1 a 5)").pack(anchor="w", padx=20, pady=(0, 6))
decenas_input = tk.Entry(panel_izquierdo, font=("Segoe UI", 11), bg=COLOR_CAJA, fg="#111827", relief="flat", insertbackground="#111827")
decenas_input.insert(0, "3")
decenas_input.pack(fill="x", padx=20, ipady=8, pady=(0, 22))

ttk.Button(
    panel_izquierdo,
    text="GENERAR COMBINACIÓN",
    command=generar_1,
    style="Accent.TButton"
).pack(fill="x", padx=20, pady=(0, 20))

# -----------------------------
# PANEL CENTRAL
# -----------------------------
panel_central = tk.Frame(cuerpo, bg=COLOR_FONDO)
panel_central.pack(side="left", fill="both", expand=True, padx=(0, 16))

# TARJETA 1 - COMBINACIÓN PREMIUM
tarjeta_resultado = tk.Frame(
    panel_central,
    bg=COLOR_PANEL,
    height=320,
    highlightbackground=COLOR_BORDE,
    highlightthickness=1
)
tarjeta_resultado.pack(fill="x", pady=(0, 16))
tarjeta_resultado.pack_propagate(False)

tk.Label(
    tarjeta_resultado,
    text="PANTALLA PRINCIPAL",
    bg=COLOR_PANEL,
    fg=COLOR_BLANCO,
    font=("Segoe UI", 18, "bold")
).pack(anchor="w", padx=20, pady=(18, 6))

tk.Label(
    tarjeta_resultado,
    text="La combinación generada aparecerá aquí con un formato visual más premium.",
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO_SUAVE,
    font=("Segoe UI", 10)
).pack(anchor="w", padx=20, pady=(0, 10))

contenedor_resultado_premium = tk.Frame(
    tarjeta_resultado,
    bg="#0F172A",
    highlightbackground="#1E293B",
    highlightthickness=1
)
contenedor_resultado_premium.pack(fill="both", expand=True, padx=20, pady=(0, 18))

franja_superior_resultado = tk.Frame(
    contenedor_resultado_premium,
    bg=COLOR_AZUL,
    height=4
)
franja_superior_resultado.pack(fill="x", side="top")

header_resultado = tk.Frame(contenedor_resultado_premium, bg="#0F172A")
header_resultado.pack(fill="x", padx=24, pady=(18, 8))

label_titulo_resultado = tk.Label(
    header_resultado,
    text="COMBINACIÓN DESTACADA",
    bg="#0F172A",
    fg=COLOR_BLANCO,
    font=("Segoe UI", 20, "bold")
)
label_titulo_resultado.pack(side="left")

label_badge_resultado = tk.Label(
    header_resultado,
    text="IA",
    bg=COLOR_AZUL,
    fg=COLOR_BLANCO,
    font=("Segoe UI", 10, "bold"),
    padx=12,
    pady=4
)
label_badge_resultado.pack(side="right")

label_resultado_estado = tk.Label(
    contenedor_resultado_premium,
    text="Pulsa el botón azul para generar una combinación premium",
    bg="#0F172A",
    fg=COLOR_TEXTO_SUAVE,
    font=("Segoe UI", 10)
)
label_resultado_estado.pack(anchor="w", padx=24, pady=(0, 8))

frame_numeros_resultado = tk.Frame(
    contenedor_resultado_premium,
    bg="#0F172A"
)
frame_numeros_resultado.pack(padx=24, pady=(0, 10), anchor="center")

frame_chips_resultado = tk.Frame(
    contenedor_resultado_premium,
    bg="#0F172A"
)
frame_chips_resultado.pack(fill="x", padx=24, pady=(0, 18))

def crear_chip_resultado(parent, texto):
    label = tk.Label(
        parent,
        text=texto,
        bg="#111827",
        fg=COLOR_TEXTO,
        font=("Segoe UI", 9, "bold"),
        padx=12,
        pady=8,
        highlightbackground="#334155",
        highlightthickness=1
    )
    label.pack(side="left", padx=(0, 8))
    return label

label_chip_suma = crear_chip_resultado(frame_chips_resultado, "SUMA · --")
label_chip_paridad = crear_chip_resultado(frame_chips_resultado, "PARIDAD · --/--")
label_chip_altura = crear_chip_resultado(frame_chips_resultado, "ALTURA · --/--")
label_chip_decenas = crear_chip_resultado(frame_chips_resultado, "DECENAS · --")
label_chip_consec = crear_chip_resultado(frame_chips_resultado, "RUN · --")

# TARJETA 2 - ANÁLISIS Y LEYENDA
tarjeta_info = tk.Frame(
    panel_central,
    bg=COLOR_PANEL,
    highlightbackground=COLOR_BORDE,
    highlightthickness=1
)
tarjeta_info.pack(fill="both", expand=True, pady=(0, 16))

tk.Label(
    tarjeta_info,
    text="ANÁLISIS Y LEYENDA",
    bg=COLOR_PANEL,
    fg=COLOR_BLANCO,
    font=("Segoe UI", 16, "bold")
).pack(anchor="w", padx=20, pady=(18, 8))

tk.Label(
    tarjeta_info,
    text="Análisis completo, leyenda visual y zona preparada para futuras herramientas.",
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO_SUAVE,
    font=("Segoe UI", 10)
).pack(anchor="w", padx=20, pady=(0, 12))

contenedor_info = tk.Frame(tarjeta_info, bg=COLOR_PANEL)
contenedor_info.pack(fill="both", expand=True, padx=20, pady=(0, 18))

columna_izquierda = tk.Frame(
    contenedor_info,
    bg=COLOR_PANEL_2,
    highlightbackground=COLOR_BORDE,
    highlightthickness=1
)
columna_izquierda.pack(side="left", fill="both", expand=True, padx=(0, 10))

columna_derecha = tk.Frame(
    contenedor_info,
    bg=COLOR_PANEL_2,
    width=300,
    highlightbackground=COLOR_BORDE,
    highlightthickness=1
)
columna_derecha.pack(side="left", fill="y")
columna_derecha.pack_propagate(False)

tk.Label(
    columna_izquierda,
    text="ANÁLISIS DE LA COMBINACIÓN",
    bg=COLOR_PANEL_2,
    fg=COLOR_BLANCO,
    font=("Segoe UI", 13, "bold")
).pack(anchor="w", padx=16, pady=(14, 10))

panel_metricas = tk.Frame(columna_izquierda, bg=COLOR_PANEL_2)
panel_metricas.pack(fill="x", padx=16, pady=(0, 12))

def crear_tarjeta_metrica(parent, titulo, valor_inicial):
    tarjeta = tk.Frame(parent, bg=COLOR_PANEL, highlightbackground=COLOR_BORDE, highlightthickness=1)
    tk.Label(
        tarjeta,
        text=titulo,
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO_SUAVE,
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="w", padx=10, pady=(8, 2))
    valor = tk.Label(
        tarjeta,
        text=valor_inicial,
        bg=COLOR_PANEL,
        fg=COLOR_BLANCO,
        font=("Segoe UI", 14, "bold")
    )
    valor.pack(anchor="w", padx=10, pady=(0, 8))
    return tarjeta, valor

tarjeta_suma, valor_suma = crear_tarjeta_metrica(panel_metricas, "SUMA", "--")
tarjeta_suma.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))

tarjeta_paridad, valor_paridad = crear_tarjeta_metrica(panel_metricas, "PARES / IMPARES", "-- / --")
tarjeta_paridad.grid(row=0, column=1, sticky="nsew", padx=(0, 8), pady=(0, 8))

tarjeta_altura, valor_altura = crear_tarjeta_metrica(panel_metricas, "BAJOS / ALTOS", "-- / --")
tarjeta_altura.grid(row=0, column=2, sticky="nsew", pady=(0, 8))

tarjeta_decenas, valor_decenas = crear_tarjeta_metrica(panel_metricas, "DECENAS DISTINTAS", "--")
tarjeta_decenas.grid(row=1, column=0, sticky="nsew", padx=(0, 8))

tarjeta_consec, valor_consecutivos = crear_tarjeta_metrica(panel_metricas, "CONSECUTIVOS", "--")
tarjeta_consec.grid(row=1, column=1, sticky="nsew", padx=(0, 8))

for i in range(3):
    panel_metricas.grid_columnconfigure(i, weight=1)

panel_detalle = tk.Frame(columna_izquierda, bg=COLOR_PANEL_2)
panel_detalle.pack(fill="both", expand=True, padx=16, pady=(0, 14))

tk.Label(
    panel_detalle,
    text="DETALLE",
    bg=COLOR_PANEL_2,
    fg=COLOR_BLANCO,
    font=("Segoe UI", 11, "bold")
).pack(anchor="w", pady=(0, 8))

valor_combinacion = tk.Label(
    panel_detalle,
    text="--",
    bg=COLOR_PANEL_2,
    fg=COLOR_TEXTO,
    font=("Segoe UI", 12),
    justify="left",
    anchor="w"
)
valor_combinacion.pack(fill="x", pady=(0, 8))

texto_inferior = tk.Text(
    panel_detalle,
    font=("Segoe UI", 10),
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO,
    wrap="word",
    relief="flat",
    height=8
)
texto_inferior.pack(fill="both", expand=True)
texto_inferior.insert(tk.END, "Aquí aparecerá el análisis de la combinación cuando generes una nueva.\n\n")
texto_inferior.insert(tk.END, "Usa el panel de filtros para controlar mejor el resultado.")
texto_inferior.config(state="disabled")

tk.Label(
    columna_derecha,
    text="LEYENDA VISUAL",
    bg=COLOR_PANEL_2,
    fg=COLOR_BLANCO,
    font=("Segoe UI", 13, "bold")
).pack(anchor="w", padx=16, pady=(14, 12))

leyenda_items = [
    ("Azul = número par", COLOR_AZUL),
    ("Rojo = número impar", COLOR_ROJO),
    ("Banda verde = número bajo (1-24)", COLOR_VERDE),
    ("Banda naranja = número alto (25-49)", COLOR_NARANJA),
]

for texto, color in leyenda_items:
    fila = tk.Frame(columna_derecha, bg=COLOR_PANEL_2)
    fila.pack(fill="x", padx=16, pady=6)
    punto = tk.Canvas(fila, width=12, height=12, bg=COLOR_PANEL_2, highlightthickness=0)
    punto.create_oval(2, 2, 10, 10, fill=color, outline=color)
    punto.pack(side="left", padx=(0, 8))
    tk.Label(
        fila,
        text=texto,
        bg=COLOR_PANEL_2,
        fg=COLOR_TEXTO,
        font=("Segoe UI", 10),
        justify="left",
        anchor="w",
        wraplength=220
    ).pack(side="left", fill="x", expand=True)

separador = tk.Frame(columna_derecha, bg=COLOR_BORDE, height=1)
separador.pack(fill="x", padx=16, pady=(14, 12))

tk.Label(
    columna_derecha,
    text="ESPACIO RESERVADO",
    bg=COLOR_PANEL_2,
    fg=COLOR_BLANCO,
    font=("Segoe UI", 12, "bold")
).pack(anchor="w", padx=16, pady=(0, 8))

tk.Label(
    columna_derecha,
    text="Zona pensada para futuras herramientas, acciones rápidas o nuevos botones.",
    bg=COLOR_PANEL_2,
    fg=COLOR_TEXTO_SUAVE,
    font=("Segoe UI", 10),
    justify="left",
    wraplength=220
).pack(anchor="w", padx=16)

# TARJETA 3 - ACCIONES FUTURAS
tarjeta_acciones = tk.Frame(
    panel_central,
    bg=COLOR_PANEL,
    height=110,
    highlightbackground=COLOR_BORDE,
    highlightthickness=1
)
tarjeta_acciones.pack(fill="x")
tarjeta_acciones.pack_propagate(False)

tk.Label(
    tarjeta_acciones,
    text="ACCIONES FUTURAS",
    bg=COLOR_PANEL,
    fg=COLOR_BLANCO,
    font=("Segoe UI", 15, "bold")
).pack(anchor="w", padx=20, pady=(16, 6))

tk.Label(
    tarjeta_acciones,
    text="Espacio preparado para añadir nuevos botones sin modificar los filtros ni el historial.",
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO_SUAVE,
    font=("Segoe UI", 10)
).pack(anchor="w", padx=20, pady=(0, 12))

fila_acciones_placeholder = tk.Frame(tarjeta_acciones, bg=COLOR_PANEL)
fila_acciones_placeholder.pack(fill="x", padx=20, pady=(0, 12))

for texto in ["Botón futuro 1", "Botón futuro 2", "Botón futuro 3", "Botón futuro 4"]:
    tk.Label(
        fila_acciones_placeholder,
        text=texto,
        bg=COLOR_PANEL_2,
        fg=COLOR_TEXTO_SUAVE,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padx=16,
        pady=10,
        highlightbackground=COLOR_BORDE,
        highlightthickness=1
    ).pack(side="left", padx=(0, 10))

# -----------------------------
# PANEL DERECHO
# -----------------------------
panel_derecho = tk.Frame(
    cuerpo,
    bg=COLOR_PANEL,
    width=320,
    highlightbackground=COLOR_BORDE,
    highlightthickness=1
)
panel_derecho.pack(side="left", fill="y")
panel_derecho.pack_propagate(False)

tk.Label(
    panel_derecho,
    text="HISTORIAL",
    bg=COLOR_PANEL,
    fg=COLOR_BLANCO,
    font=("Segoe UI", 18, "bold")
).pack(anchor="w", padx=20, pady=(20, 8))

tk.Label(
    panel_derecho,
    text="Aquí se guardan las combinaciones que ya se generaron.",
    bg=COLOR_PANEL,
    fg=COLOR_TEXTO_SUAVE,
    font=("Segoe UI", 10),
    wraplength=270,
    justify="left"
).pack(anchor="w", padx=20, pady=(0, 12))

historial_text = tk.Text(
    panel_derecho,
    font=("Consolas", 13),
    bg=COLOR_CAJA,
    fg="#0F172A",
    wrap="word",
    relief="flat"
)
historial_text.pack(fill="both", expand=True, padx=20, pady=(0, 12))
historial_text.config(state="disabled")

ttk.Button(
    panel_derecho,
    text="BORRAR HISTORIAL",
    command=borrar_historial,
    style="Accent.TButton"
).pack(fill="x", padx=20, pady=(0, 20))

ventana.mainloop()