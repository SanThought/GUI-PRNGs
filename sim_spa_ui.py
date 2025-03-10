import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# ------------------------------
# Funciones y Clases de PRNGs
# ------------------------------

class GeneradorCongruencialLineal:
    """Generador Congruencial Lineal (LCG) adaptado"""
    def __init__(self, semilla, a, c, m):
        self.semilla = int(semilla)
        self.a = int(a)
        self.c = int(c)
        self.m = int(m)
        if self.m <= 0:
            raise ValueError("El módulo (m) debe ser mayor que 0")

    def random(self):
        """Genera el siguiente número pseudoaleatorio normalizado a [0, 1]"""
        self.semilla = (self.a * self.semilla + self.c) % self.m
        return self.semilla / self.m

class CuadradoMedio:
    """Generador de Cuadrado Medio adaptado"""
    def __init__(self, semilla):
        self.semilla = int(semilla)
        if self.semilla < 1000:
            raise ValueError("La semilla debe ser un número de al menos 4 dígitos.")

    def random(self):
        """Genera el siguiente número pseudoaleatorio normalizado a [0, 1]"""
        X_cuadrado = self.semilla ** 2
        X_str = str(X_cuadrado).zfill(8)
        medio = len(X_str) // 2
        self.semilla = int(X_str[medio - 2: medio + 2])
        return self.semilla / 10000

class GeneradorUniforme:
    """Generador de Distribución Uniforme"""
    def __init__(self, semilla, a, c, m):
        self.semilla = int(semilla)
        self.a = int(a)
        self.c = int(c)
        self.m = int(m)

    def random(self):
        """Genera el siguiente número pseudoaleatorio normalizado a [0, 1]"""
        self.semilla = (self.a * self.semilla + self.c) % self.m
        return self.semilla / self.m

class CuadradoMedioWeyl:
    """Generador de Cuadrado Medio con Secuencia Weyl"""
    def __init__(self, semilla, weyl, delta):
        self.semilla = int(semilla)
        self.weyl = int(weyl)
        self.delta = int(delta)

    def random(self):
        """Genera el siguiente número pseudoaleatorio normalizado a [0, 1]"""
        self.semilla = (self.semilla * self.semilla + self.weyl) & 0xffffffff
        self.weyl = (self.weyl + self.delta) & 0xffffffff
        return self.semilla / 2**32

# ------------------------------
# Funciones de Pruebas Estadísticas
# ------------------------------

def prueba_ks(datos):
    """Prueba de Kolmogorov-Smirnov para uniformidad"""
    estadistico, p_valor = stats.kstest(datos, 'uniform', args=(0, 1))
    return estadistico, p_valor

def prueba_media(datos):
    """Prueba de media para uniformidad"""
    n = len(datos)
    media_muestra = np.mean(datos)
    media_teorica = 0.5
    se = np.sqrt(1/12) / np.sqrt(n)
    z_estadistico = (media_muestra - media_teorica) / se
    p_valor = 2 * (1 - stats.norm.cdf(abs(z_estadistico)))
    return media_muestra, z_estadistico, p_valor

def prueba_varianza(datos):
    """Prueba de varianza para uniformidad"""
    n = len(datos)
    varianza_muestra = np.var(datos, ddof=1)
    varianza_teorica = 1/12
    chi2_estadistico = (n - 1) * varianza_muestra / varianza_teorica
    p_inferior = stats.chi2.cdf(chi2_estadistico, n - 1)
    p_superior = 1 - p_inferior
    p_valor = 2 * min(p_inferior, p_superior)
    return varianza_muestra, chi2_estadistico, min(p_valor, 1.0)

def prueba_chi_cuadrado(datos, bins):
    """Prueba de Chi-Cuadrado para uniformidad con bins configurables"""
    observados, bordes_bins = np.histogram(datos, bins=bins, range=(0, 1))
    esperados = [len(datos)/bins] * bins
    chi2_estadistico, p_valor = stats.chisquare(observados, f_exp=esperados)
    return chi2_estadistico, p_valor, observados, bordes_bins

def generar_muestra(prng, tamano_muestra):
    """Genera una muestra de números pseudoaleatorios usando el generador especificado"""
    return [prng.random() for _ in range(tamano_muestra)]

# ------------------------------
# Aplicación de Pruebas Estadísticas (GUI)
# ------------------------------

class AplicacionPruebasEstadisticas:
    """Aplicación gráfica para demostrar PRNGs y sus pruebas estadísticas"""
    def __init__(self, root):
        self.root = root
        self.root.title("Programa de Pruebas Estadísticas")
        self.root.geometry("900x800")
        self.root.configure(background="#FAFAFA")
        try:
            self.root.tk.call('tk', 'scaling', 1.0)
        except:
            pass

        self.establecer_estilos()
        
        self.mapa_prng = {
            "Generador Congruencial Lineal": GeneradorCongruencialLineal,
            "Cuadrado Medio": CuadradoMedio,
            "Generador Uniforme": GeneradorUniforme,
            "Cuadrado Medio Weyl": CuadradoMedioWeyl
        }
        
        self.mapa_pruebas = {
            "Prueba Kolmogorov-Smirnov": self.ejecutar_prueba_ks,
            "Prueba de Media": self.ejecutar_prueba_media,
            "Prueba de Varianza": self.ejecutar_prueba_varianza,
            "Prueba Chi-Cuadrado": self.ejecutar_prueba_chi_cuadrado
        }
        
        self.crear_widgets()
        
    def establecer_estilos(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        
        # Colores y fuentes Material
        fondo = "#FAFAFA"
        fondoFrame = "#E3F2FD"  # light blue for frames
        texto = "#212121"
        boton_bg = "#2196F3"
        boton_activo = "#1976D2"
        font_general = ("Segoe UI", 14)
        font_bold = ("Segoe UI", 14, "bold")
        
        # LabelFrame (contenedor)
        style.configure("Custom.TLabelframe",
                        background="#E3F2FD",  # color de fondo
                        borderwidth=2,
                        relief="groove")

        # Etiqueta del título del LabelFrame
        style.configure("Custom.TLabelframe.Label",
                        background="#E3F2FD",
                        foreground="#0D47A1",
                        font=("Segoe UI", 14, "bold"))
        
        style.configure("TFrame", background=fondo)
        style.configure("TLabel", background=fondo, foreground=texto, font=font_general)
        style.configure("TLabelFrame", background=fondoFrame, foreground="#0D47A1", font=font_bold, relief="groove", borderwidth=2)
        style.configure("TEntry", fieldbackground="white", font=font_general)
        style.configure("TCombobox", fieldbackground="white", font=font_general)
        
        style.configure("TButton", background=boton_bg, foreground="white", font=font_bold, padding=(10,6), relief="flat")
        style.map("TButton", background=[("active", boton_activo)])


        
        # Scrollbar styling
        style.configure("Vertical.TScrollbar", background="#BBDEFB", troughcolor="#E3F2FD", arrowcolor="#0D47A1")
        
    def crear_widgets(self):
        marco_principal = ttk.Frame(self.root)
        marco_principal.pack(fill="both", expand=True, padx=30, pady=30)
        
        lienzo = tk.Canvas(marco_principal, background="#FAFAFA", highlightthickness=0)
        barra_desplazamiento = ttk.Scrollbar(marco_principal, orient="vertical", command=lienzo.yview, style="Vertical.TScrollbar")
        self.marco_desplazable = ttk.Frame(lienzo, style="TFrame")
        
        def centrar(event):
            ancho = event.width
            self.marco_desplazable.update_idletasks()
            lienzo.itemconfigure(self.ventana, width=ancho)
            lienzo.coords(self.ventana, ancho/2, 0)
        
        self.marco_desplazable.bind("<Configure>", lambda e: lienzo.configure(scrollregion=lienzo.bbox("all")))
        self.ventana = lienzo.create_window(0, 0, window=self.marco_desplazable, anchor="n")
        lienzo.bind("<Configure>", centrar)
        
        lienzo.configure(yscrollcommand=barra_desplazamiento.set)
        lienzo.pack(side="left", fill="both", expand=True)
        barra_desplazamiento.pack(side="right", fill="y")
        
        # Selección de Prueba
        marco_prueba = ttk.LabelFrame(self.marco_desplazable, text="Selección de Prueba", style="Custom.TLabelframe")
        marco_prueba.pack(padx=10, pady=5, fill="x")
        
        self.var_prueba = tk.StringVar()
        desplegable_prueba = ttk.Combobox(marco_prueba, textvariable=self.var_prueba,
                                           values=list(self.mapa_pruebas.keys()), state="readonly")
        desplegable_prueba.pack(padx=10, pady=5, fill="x")
        desplegable_prueba.set("Seleccione Prueba Estadística")
        desplegable_prueba.bind("<<ComboboxSelected>>", self.actualizar_parametros_prueba)
        
        # Parámetros de Prueba
        self.marco_parametros_prueba = ttk.LabelFrame(self.marco_desplazable, text="Parámetros de Prueba", style="Custom.TLabelframe")
        self.marco_parametros_prueba.pack(padx=10, pady=5, fill="x")
        
        self.bins_var = tk.StringVar(value="10")
        self.actualizar_parametros_prueba(None)
        
        # Selección de PRNG
        marco_prng = ttk.LabelFrame(self.marco_desplazable, text="Selección de PRNG", style="Custom.TLabelframe")
        marco_prng.pack(padx=10, pady=5, fill="x")
        
        self.var_prng = tk.StringVar()
        desplegable_prng = ttk.Combobox(marco_prng, textvariable=self.var_prng,
                                         values=list(self.mapa_prng.keys()), state="readonly")
        desplegable_prng.pack(padx=10, pady=5, fill="x")
        desplegable_prng.set("Seleccione PRNG")
        desplegable_prng.bind("<<ComboboxSelected>>", self.actualizar_parametros)
        
        # Parámetros del PRNG
        self.marco_parametros = ttk.LabelFrame(self.marco_desplazable, text="Parámetros del PRNG", style="Custom.TLabelframe")
        self.marco_parametros.pack(padx=10, pady=5, fill="x")
        
        self.semilla_var = tk.StringVar(value="1234")
        self.a_var = tk.StringVar(value="1664525")
        self.c_var = tk.StringVar(value="1013904223")
        self.m_var = tk.StringVar(value="4294967296")
        self.weyl_var = tk.StringVar(value="362436069")
        self.delta_var = tk.StringVar(value="1633771879")
        self.actualizar_parametros(None)
        
        # Tamaño de Muestra
        marco_tamano = ttk.LabelFrame(self.marco_desplazable, text="Tamaño de Muestra", style="Custom.TLabelframe")
        marco_tamano.pack(padx=10, pady=5, fill="x")
        
        self.tamano_var = tk.StringVar(value="50")
        entrada_tamano = ttk.Entry(marco_tamano, textvariable=self.tamano_var)
        entrada_tamano.pack(padx=10, pady=5, fill="x")
        entrada_tamano.bind("<KeyRelease>", self.sugerir_bins)
        
        # Botón de Ejecución
        boton_ejecutar = ttk.Button(self.marco_desplazable, text="Ejecutar Prueba", command=self.ejecutar_prueba)
        boton_ejecutar.pack(padx=10, pady=10)
        
        # Resultados
        self.marco_resultados = ttk.LabelFrame(self.marco_desplazable, text="Resultados", style="Custom.TLabelframe")
        self.marco_resultados.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Datos Generados
        self.marco_datos = ttk.LabelFrame(self.marco_desplazable, text="Datos Generados", style="Custom.TLabelframe")
        self.marco_datos.pack(padx=10, pady=5, fill="both", expand=True)
        
        self.texto_datos = tk.Text(self.marco_datos, height=10, wrap=tk.WORD, font=("Segoe UI", 14))
        self.texto_datos.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Botones Inferiores
        marco_botones = ttk.Frame(self.marco_desplazable, style="TFrame")
        marco_botones.pack(padx=10, pady=5, fill="x")
        
        boton_exportar = ttk.Button(marco_botones, text="Exportar Datos", command=self.exportar_datos)
        boton_exportar.pack(side="left", padx=5)
        
        boton_salir = ttk.Button(marco_botones, text="Salir", command=self.salir_programa)
        boton_salir.pack(side="right", padx=5)
        
        # Permitir scroll con la rueda del ratón
        lienzo.bind_all("<MouseWheel>", lambda event: lienzo.yview_scroll(int(-1*(event.delta/120)), "units"))
        
    def sugerir_bins(self, event):
        try:
            tamano_muestra = int(self.tamano_var.get())
            bins_sugeridos = math.ceil(math.log2(tamano_muestra) + 1)
            bins_sugeridos = max(5, bins_sugeridos)
            self.bins_var.set(str(bins_sugeridos))
        except ValueError:
            self.bins_var.set("10")
    
    def actualizar_parametros_prueba(self, event):
        for widget in self.marco_parametros_prueba.winfo_children():
            widget.destroy()
        
        nombre_prueba = self.var_prueba.get()
        if nombre_prueba == "Prueba Chi-Cuadrado":
            ttk.Label(self.marco_parametros_prueba, text="Número de Intervalos (bins):").grid(row=0, column=0, padx=5, pady=5)
            ttk.Entry(self.marco_parametros_prueba, textvariable=self.bins_var).grid(row=0, column=1, padx=5, pady=5)
            ttk.Label(self.marco_parametros_prueba, text="(Sugerencia: Usa la regla de Sturges)").grid(row=1, column=0, columnspan=2, padx=5, pady=5)
            self.sugerir_bins(None)
    
    def actualizar_parametros(self, event):
        for widget in self.marco_parametros.winfo_children():
            widget.destroy()
        
        nombre_prng = self.var_prng.get()
        fila = 0
        
        ttk.Label(self.marco_parametros, text="Semilla:").grid(row=fila, column=0, padx=5, pady=5)
        ttk.Entry(self.marco_parametros, textvariable=self.semilla_var).grid(row=fila, column=1, padx=5, pady=5)
        fila += 1
        
        if nombre_prng in ["Generador Congruencial Lineal", "Generador Uniforme"]:
            ttk.Label(self.marco_parametros, text="a:").grid(row=fila, column=0, padx=5, pady=5)
            ttk.Entry(self.marco_parametros, textvariable=self.a_var).grid(row=fila, column=1, padx=5, pady=5)
            fila += 1
            ttk.Label(self.marco_parametros, text="c:").grid(row=fila, column=0, padx=5, pady=5)
            ttk.Entry(self.marco_parametros, textvariable=self.c_var).grid(row=fila, column=1, padx=5, pady=5)
            fila += 1
            ttk.Label(self.marco_parametros, text="m:").grid(row=fila, column=0, padx=5, pady=5)
            ttk.Entry(self.marco_parametros, textvariable=self.m_var).grid(row=fila, column=1, padx=5, pady=5)
        elif nombre_prng == "Cuadrado Medio Weyl":
            ttk.Label(self.marco_parametros, text="Weyl:").grid(row=fila, column=0, padx=5, pady=5)
            ttk.Entry(self.marco_parametros, textvariable=self.weyl_var).grid(row=fila, column=1, padx=5, pady=5)
            fila += 1
            ttk.Label(self.marco_parametros, text="Delta:").grid(row=fila, column=0, padx=5, pady=5)
            ttk.Entry(self.marco_parametros, textvariable=self.delta_var).grid(row=fila, column=1, padx=5, pady=5)
    
    def ejecutar_prueba(self):
        for widget in self.marco_resultados.winfo_children():
            widget.destroy()
        self.texto_datos.delete(1.0, tk.END)
        
        try:
            nombre_prng = self.var_prng.get()
            nombre_prueba = self.var_prueba.get()
            tamano_muestra = int(self.tamano_var.get())
            
            if nombre_prng == "Seleccione PRNG" or nombre_prueba == "Seleccione Prueba Estadística":
                raise ValueError("Por favor, seleccione un PRNG y una prueba.")
            
            clase_prng = self.mapa_prng[nombre_prng]
            if nombre_prng == "Generador Congruencial Lineal":
                prng = clase_prng(self.semilla_var.get(), self.a_var.get(), self.c_var.get(), self.m_var.get())
            elif nombre_prng == "Cuadrado Medio":
                prng = clase_prng(self.semilla_var.get())
            elif nombre_prng == "Generador Uniforme":
                prng = clase_prng(self.semilla_var.get(), self.a_var.get(), self.c_var.get(), self.m_var.get())
            elif nombre_prng == "Cuadrado Medio Weyl":
                prng = clase_prng(self.semilla_var.get(), self.weyl_var.get(), self.delta_var.get())
            
            muestra = generar_muestra(prng, tamano_muestra)
            self.texto_datos.insert(tk.END, "Datos Generados:\n")
            for num in muestra:
                self.texto_datos.insert(tk.END, f"{num:.6f}\n")
            self.texto_datos.config(state=tk.DISABLED)
            
            funcion_prueba = self.mapa_pruebas[nombre_prueba]
            if nombre_prueba == "Prueba Chi-Cuadrado":
                bins = int(self.bins_var.get())
                funcion_prueba(muestra, nombre_prng, bins)
            else:
                funcion_prueba(muestra, nombre_prng)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def ejecutar_prueba_ks(self, muestra, nombre_prng):
        estadistico, p_valor = prueba_ks(muestra)
        texto_resultado = tk.Text(self.marco_resultados, height=10, wrap=tk.WORD, font=("Segoe UI", 14))
        texto_resultado.pack(padx=10, pady=5, fill="both", expand=True)
        texto_resultado.insert(tk.END, f"Resultados de la Prueba Kolmogorov-Smirnov:\n")
        texto_resultado.insert(tk.END, f"PRNG: {nombre_prng}\n")
        texto_resultado.insert(tk.END, f"Estadístico KS: {estadistico:.4f}\n")
        texto_resultado.insert(tk.END, f"Valor P: {p_valor:.4f}\n")
        if p_valor > 0.05:
            texto_resultado.insert(tk.END, "Interpretación: Concordancia con una distribución uniforme (p > 0.05).\n")
        else:
            texto_resultado.insert(tk.END, "Interpretación: Discrepancia con una distribución uniforme (p ≤ 0.05).\n")
        texto_resultado.config(state=tk.DISABLED)
        self.crear_histograma(muestra)
    
    def ejecutar_prueba_media(self, muestra, nombre_prng):
        media_muestra, z_estadistico, p_valor = prueba_media(muestra)
        texto_resultado = tk.Text(self.marco_resultados, height=10, wrap=tk.WORD, font=("Segoe UI", 14))
        texto_resultado.pack(padx=10, pady=5, fill="both", expand=True)
        texto_resultado.insert(tk.END, f"Resultados de la Prueba de Media:\n")
        texto_resultado.insert(tk.END, f"PRNG: {nombre_prng}\n")
        texto_resultado.insert(tk.END, f"Media de la Muestra: {media_muestra:.4f}\n")
        texto_resultado.insert(tk.END, f"Estadístico Z: {z_estadistico:.4f}\n")
        texto_resultado.insert(tk.END, f"Valor P: {p_valor:.4f}\n")
        if p_valor > 0.05:
            texto_resultado.insert(tk.END, "Interpretación: Concordancia con la media esperada (p > 0.05).\n")
        else:
            texto_resultado.insert(tk.END, "Interpretación: Discrepancia con la media esperada (p ≤ 0.05).\n")
        texto_resultado.config(state=tk.DISABLED)
        self.crear_histograma(muestra)
    
    def ejecutar_prueba_varianza(self, muestra, nombre_prng):
        varianza_muestra, chi2_estadistico, p_valor = prueba_varianza(muestra)
        texto_resultado = tk.Text(self.marco_resultados, height=10, wrap=tk.WORD, font=("Segoe UI", 14))
        texto_resultado.pack(padx=10, pady=5, fill="both", expand=True)
        texto_resultado.insert(tk.END, f"Resultados de la Prueba de Varianza:\n")
        texto_resultado.insert(tk.END, f"PRNG: {nombre_prng}\n")
        texto_resultado.insert(tk.END, f"Varianza de la Muestra: {varianza_muestra:.4f}\n")
        texto_resultado.insert(tk.END, f"Estadístico Chi-Cuadrado: {chi2_estadistico:.4f}\n")
        texto_resultado.insert(tk.END, f"Valor P: {p_valor:.4f}\n")
        if p_valor > 0.05:
            texto_resultado.insert(tk.END, "Interpretación: Concordancia con la varianza teórica (p > 0.05).\n")
        else:
            texto_resultado.insert(tk.END, "Interpretación: Discrepancia con la varianza teórica (p ≤ 0.05).\n")
        texto_resultado.config(state=tk.DISABLED)
        self.crear_histograma(muestra)
    
    def ejecutar_prueba_chi_cuadrado(self, muestra, nombre_prng, bins):
        chi2_estadistico, p_valor, observados, bordes_bins = prueba_chi_cuadrado(muestra, bins)
        texto_resultado = tk.Text(self.marco_resultados, height=10, wrap=tk.WORD, font=("Segoe UI", 14))
        texto_resultado.pack(padx=10, pady=5, fill="both", expand=True)
        texto_resultado.insert(tk.END, f"Resultados de la Prueba Chi-Cuadrado:\n")
        texto_resultado.insert(tk.END, f"PRNG: {nombre_prng}\n")
        texto_resultado.insert(tk.END, f"Número de Intervalos: {bins}\n")
        texto_resultado.insert(tk.END, f"Estadístico Chi-Cuadrado: {chi2_estadistico:.4f}\n")
        texto_resultado.insert(tk.END, f"Valor P: {p_valor:.4f}\n")
        if p_valor > 0.05:
            texto_resultado.insert(tk.END, "Interpretación: Concordancia con una distribución uniforme (p > 0.05).\n")
        else:
            texto_resultado.insert(tk.END, "Interpretación: Discrepancia con una distribución uniforme (p ≤ 0.05).\n")
        texto_resultado.insert(tk.END, "\nFrecuencias Observadas:\n")
        for i in range(len(observados)):
            texto_resultado.insert(tk.END, f"Intervalo {i+1} ({bordes_bins[i]:.2f}-{bordes_bins[i+1]:.2f}): {observados[i]}\n")
        texto_resultado.config(state=tk.DISABLED)
        self.crear_histograma(muestra, bins)
    
    def crear_histograma(self, muestra, bins=10):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(muestra, bins=bins, range=(0, 1), edgecolor='black')
        ax.set_title('Distribución de la Muestra', fontname="Segoe UI", fontsize=16)
        ax.set_xlabel('Valor', fontname="Segoe UI", fontsize=14)
        ax.set_ylabel('Frecuencia', fontname="Segoe UI", fontsize=14)
        
        lienzo = FigureCanvasTkAgg(fig, master=self.marco_resultados)
        widget_lienzo = lienzo.get_tk_widget()
        widget_lienzo.pack(padx=10, pady=5)
        lienzo.draw()
    
    def exportar_datos(self):
        try:
            nombre_prng = self.var_prng.get()
            clase_prng = self.mapa_prng[nombre_prng]
            tamano_muestra = int(self.tamano_var.get())
            
            if nombre_prng == "Generador Congruencial Lineal":
                prng = clase_prng(self.semilla_var.get(), self.a_var.get(), self.c_var.get(), self.m_var.get())
            elif nombre_prng == "Cuadrado Medio":
                prng = clase_prng(self.semilla_var.get())
            elif nombre_prng == "Generador Uniforme":
                prng = clase_prng(self.semilla_var.get(), self.a_var.get(), self.c_var.get(), self.m_var.get())
            elif nombre_prng == "Cuadrado Medio Weyl":
                prng = clase_prng(self.semilla_var.get(), self.weyl_var.get(), self.delta_var.get())
            
            muestra = generar_muestra(prng, tamano_muestra)
            nombre_archivo = filedialog.asksaveasfilename(defaultextension=".txt",
                                                         filetypes=[("Archivos de texto", "*.txt"), ("Archivos CSV", "*.csv")])
            if nombre_archivo:
                if nombre_archivo.endswith('.csv'):
                    df = pd.DataFrame(muestra, columns=['Números Aleatorios'])
                    df.to_csv(nombre_archivo, index=False)
                else:
                    with open(nombre_archivo, 'w') as archivo:
                        for num in muestra:
                            archivo.write(f"{num:.6f}\n")
                messagebox.showinfo("Exportación Exitosa", f"Datos exportados a {nombre_archivo}")
        except Exception as e:
            messagebox.showerror("Error de Exportación", str(e))
    
    def salir_programa(self):
        self.root.quit()
        self.root.destroy()

def principal():
    root = tk.Tk()
    app = AplicacionPruebasEstadisticas(root)
    root.mainloop()

if __name__ == "__main__":
    principal()