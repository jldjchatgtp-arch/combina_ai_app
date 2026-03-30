import tkinter as tk

historial_set = set()

def agregar_historial(historial_text, combinaciones):
    historial_text.config(state="normal")
    for c in combinaciones:
        clave = tuple(c)
        if clave not in historial_set:
            historial_set.add(clave)
            historial_text.insert(tk.END, "• " + " - ".join(f"{n:02d}" for n in c) + "\n")
    historial_text.see(tk.END)
    historial_text.config(state="disabled")

def borrar_historial(historial_text):
    historial_text.config(state="normal")
    historial_text.delete("1.0", tk.END)
    historial_text.config(state="disabled")
    historial_set.clear()