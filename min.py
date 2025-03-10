d='Interpretación: Discrepancia con una distribución uniforme (p ≤ 0.05).\n'
c='Interpretación: Concordancia con una distribución uniforme (p > 0.05).\n'
b='Seleccione PRNG'
a='Seleccione Prueba Estadística'
Z='Vertical.TScrollbar'
Y=range
V=None
U='TFrame'
T='Prueba Chi-Cuadrado'
S='Cuadrado Medio'
R='#FAFAFA'
Q=1.
O='Cuadrado Medio Weyl'
N='Generador Uniforme'
M='Generador Congruencial Lineal'
L=str
I=len
E=ValueError
J='Custom.TLabelframe'
H=True
G='both'
F='Segoe UI'
D=int
import tkinter as A
from tkinter import ttk as C,messagebox as P,filedialog as e
import numpy as B,pandas as f
from scipy import stats as K
import matplotlib.pyplot as g
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as h
import math as W
class i:
	def __init__(A,semilla,a,c,m):
		A.semilla=D(semilla);A.a=D(a);A.c=D(c);A.m=D(m)
		if A.m<=0:raise E('El módulo (m) debe ser mayor que 0')
	def random(A):A.semilla=(A.a*A.semilla+A.c)%A.m;return A.semilla/A.m
class j:
	def __init__(A,semilla):
		A.semilla=D(semilla)
		if A.semilla<1000:raise E('La semilla debe ser un número de al menos 4 dígitos.')
	def random(A):E=A.semilla**2;B=L(E).zfill(8);C=I(B)//2;A.semilla=D(B[C-2:C+2]);return A.semilla/10000
class k:
	def __init__(A,semilla,a,c,m):A.semilla=D(semilla);A.a=D(a);A.c=D(c);A.m=D(m)
	def random(A):A.semilla=(A.a*A.semilla+A.c)%A.m;return A.semilla/A.m
class l:
	def __init__(A,semilla,weyl,delta):A.semilla=D(semilla);A.weyl=D(weyl);A.delta=D(delta)
	def random(A):A.semilla=A.semilla*A.semilla+A.weyl&4294967295;A.weyl=A.weyl+A.delta&4294967295;return A.semilla/2**32
def m(datos):A,B=K.kstest(datos,'uniform',args=(0,1));return A,B
def n(datos):A=datos;E=I(A);C=B.mean(A);F=.5;G=B.sqrt(1/12)/B.sqrt(E);D=(C-F)/G;H=2*(1-K.norm.cdf(abs(D)));return C,D,H
def o(datos):A=datos;C=I(A);D=B.var(A,ddof=1);G=1/12;E=(C-1)*D/G;F=K.chi2.cdf(E,C-1);H=1-F;J=2*min(F,H);return D,E,min(J,Q)
def p(datos,bins):C=datos;A=bins;D,E=B.histogram(C,bins=A,range=(0,1));F=[I(C)/A]*A;G,H=K.chisquare(D,f_exp=F);return G,H,D,E
def X(prng,tamano_muestra):return[prng.random()for A in Y(tamano_muestra)]
class q:
	def __init__(A,root):
		A.root=root;A.root.title('Programa de Pruebas Estadísticas');A.root.geometry('900x800');A.root.configure(background=R)
		try:A.root.tk.call('tk','scaling',Q)
		except:pass
		A.establecer_estilos();A.mapa_prng={M:i,S:j,N:k,O:l};A.mapa_pruebas={'Prueba Kolmogorov-Smirnov':A.ejecutar_prueba_ks,'Prueba de Media':A.ejecutar_prueba_media,'Prueba de Varianza':A.ejecutar_prueba_varianza,T:A.ejecutar_prueba_chi_cuadrado};A.crear_widgets()
	def establecer_estilos(N):M='TButton';L='groove';K='bold';G='white';E='#0D47A1';B='#E3F2FD';A=C.Style(N.root);A.theme_use('clam');H=R;O=B;P='#212121';Q='#2196F3';S='#1976D2';D=F,14;I=F,14,K;A.configure(J,background=B,borderwidth=2,relief=L);A.configure('Custom.TLabelframe.Label',background=B,foreground=E,font=(F,14,K));A.configure(U,background=H);A.configure('TLabel',background=H,foreground=P,font=D);A.configure('TLabelFrame',background=O,foreground=E,font=I,relief=L,borderwidth=2);A.configure('TEntry',fieldbackground=G,font=D);A.configure('TCombobox',fieldbackground=G,font=D);A.configure(M,background=Q,foreground=G,font=I,padding=(10,6),relief='flat');A.map(M,background=[('active',S)]);A.configure(Z,background='#BBDEFB',troughcolor=B,arrowcolor=E)
	def crear_widgets(B):
		d='<<ComboboxSelected>>';c='readonly';Y='right';X='left';W='<Configure>';I='x';K=C.Frame(B.root);K.pack(fill=G,expand=H,padx=30,pady=30);E=A.Canvas(K,background=R,highlightthickness=0);O=C.Scrollbar(K,orient='vertical',command=E.yview,style=Z);B.marco_desplazable=C.Frame(E,style=U)
		def e(event):A=event.width;B.marco_desplazable.update_idletasks();E.itemconfigure(B.ventana,width=A);E.coords(B.ventana,A/2,0)
		B.marco_desplazable.bind(W,lambda e:E.configure(scrollregion=E.bbox('all')));B.ventana=E.create_window(0,0,window=B.marco_desplazable,anchor='n');E.bind(W,e);E.configure(yscrollcommand=O.set);E.pack(side=X,fill=G,expand=H);O.pack(side=Y,fill='y');P=C.LabelFrame(B.marco_desplazable,text='Selección de Prueba',style=J);P.pack(padx=10,pady=5,fill=I);B.var_prueba=A.StringVar();L=C.Combobox(P,textvariable=B.var_prueba,values=list(B.mapa_pruebas.keys()),state=c);L.pack(padx=10,pady=5,fill=I);L.set(a);L.bind(d,B.actualizar_parametros_prueba);B.marco_parametros_prueba=C.LabelFrame(B.marco_desplazable,text='Parámetros de Prueba',style=J);B.marco_parametros_prueba.pack(padx=10,pady=5,fill=I);B.bins_var=A.StringVar(value='10');B.actualizar_parametros_prueba(V);Q=C.LabelFrame(B.marco_desplazable,text='Selección de PRNG',style=J);Q.pack(padx=10,pady=5,fill=I);B.var_prng=A.StringVar();M=C.Combobox(Q,textvariable=B.var_prng,values=list(B.mapa_prng.keys()),state=c);M.pack(padx=10,pady=5,fill=I);M.set(b);M.bind(d,B.actualizar_parametros);B.marco_parametros=C.LabelFrame(B.marco_desplazable,text='Parámetros del PRNG',style=J);B.marco_parametros.pack(padx=10,pady=5,fill=I);B.semilla_var=A.StringVar(value='1234');B.a_var=A.StringVar(value='1664525');B.c_var=A.StringVar(value='1013904223');B.m_var=A.StringVar(value='4294967296');B.weyl_var=A.StringVar(value='362436069');B.delta_var=A.StringVar(value='1633771879');B.actualizar_parametros(V);S=C.LabelFrame(B.marco_desplazable,text='Tamaño de Muestra',style=J);S.pack(padx=10,pady=5,fill=I);B.tamano_var=A.StringVar(value='50');T=C.Entry(S,textvariable=B.tamano_var);T.pack(padx=10,pady=5,fill=I);T.bind('<KeyRelease>',B.sugerir_bins);f=C.Button(B.marco_desplazable,text='Ejecutar Prueba',command=B.ejecutar_prueba);f.pack(padx=10,pady=10);B.marco_resultados=C.LabelFrame(B.marco_desplazable,text='Resultados',style=J);B.marco_resultados.pack(padx=10,pady=5,fill=G,expand=H);B.marco_datos=C.LabelFrame(B.marco_desplazable,text='Datos Generados',style=J);B.marco_datos.pack(padx=10,pady=5,fill=G,expand=H);B.texto_datos=A.Text(B.marco_datos,height=10,wrap=A.WORD,font=(F,14));B.texto_datos.pack(padx=10,pady=5,fill=G,expand=H);N=C.Frame(B.marco_desplazable,style=U);N.pack(padx=10,pady=5,fill=I);g=C.Button(N,text='Exportar Datos',command=B.exportar_datos);g.pack(side=X,padx=5);h=C.Button(N,text='Salir',command=B.salir_programa);h.pack(side=Y,padx=5);E.bind_all('<MouseWheel>',lambda event:E.yview_scroll(D(-1*(event.delta/120)),'units'))
	def sugerir_bins(A,event):
		try:C=D(A.tamano_var.get());B=W.ceil(W.log2(C)+1);B=max(5,B);A.bins_var.set(L(B))
		except E:A.bins_var.set('10')
	def actualizar_parametros_prueba(A,event):
		for B in A.marco_parametros_prueba.winfo_children():B.destroy()
		D=A.var_prueba.get()
		if D==T:C.Label(A.marco_parametros_prueba,text='Número de Intervalos (bins):').grid(row=0,column=0,padx=5,pady=5);C.Entry(A.marco_parametros_prueba,textvariable=A.bins_var).grid(row=0,column=1,padx=5,pady=5);C.Label(A.marco_parametros_prueba,text='(Sugerencia: Usa la regla de Sturges)').grid(row=1,column=0,columnspan=2,padx=5,pady=5);A.sugerir_bins(V)
	def actualizar_parametros(A,event):
		for E in A.marco_parametros.winfo_children():E.destroy()
		D=A.var_prng.get();B=0;C.Label(A.marco_parametros,text='Semilla:').grid(row=B,column=0,padx=5,pady=5);C.Entry(A.marco_parametros,textvariable=A.semilla_var).grid(row=B,column=1,padx=5,pady=5);B+=1
		if D in[M,N]:C.Label(A.marco_parametros,text='a:').grid(row=B,column=0,padx=5,pady=5);C.Entry(A.marco_parametros,textvariable=A.a_var).grid(row=B,column=1,padx=5,pady=5);B+=1;C.Label(A.marco_parametros,text='c:').grid(row=B,column=0,padx=5,pady=5);C.Entry(A.marco_parametros,textvariable=A.c_var).grid(row=B,column=1,padx=5,pady=5);B+=1;C.Label(A.marco_parametros,text='m:').grid(row=B,column=0,padx=5,pady=5);C.Entry(A.marco_parametros,textvariable=A.m_var).grid(row=B,column=1,padx=5,pady=5)
		elif D==O:C.Label(A.marco_parametros,text='Weyl:').grid(row=B,column=0,padx=5,pady=5);C.Entry(A.marco_parametros,textvariable=A.weyl_var).grid(row=B,column=1,padx=5,pady=5);B+=1;C.Label(A.marco_parametros,text='Delta:').grid(row=B,column=0,padx=5,pady=5);C.Entry(A.marco_parametros,textvariable=A.delta_var).grid(row=B,column=1,padx=5,pady=5)
	def ejecutar_prueba(B):
		for K in B.marco_resultados.winfo_children():K.destroy()
		B.texto_datos.delete(Q,A.END)
		try:
			C=B.var_prng.get();H=B.var_prueba.get();R=D(B.tamano_var.get())
			if C==b or H==a:raise E('Por favor, seleccione un PRNG y una prueba.')
			F=B.mapa_prng[C]
			if C==M:G=F(B.semilla_var.get(),B.a_var.get(),B.c_var.get(),B.m_var.get())
			elif C==S:G=F(B.semilla_var.get())
			elif C==N:G=F(B.semilla_var.get(),B.a_var.get(),B.c_var.get(),B.m_var.get())
			elif C==O:G=F(B.semilla_var.get(),B.weyl_var.get(),B.delta_var.get())
			I=X(G,R);B.texto_datos.insert(A.END,'Datos Generados:\n')
			for U in I:B.texto_datos.insert(A.END,f"{U:.6f}\n")
			B.texto_datos.config(state=A.DISABLED);J=B.mapa_pruebas[H]
			if H==T:V=D(B.bins_var.get());J(I,C,V)
			else:J(I,C)
		except E as W:P.showerror('Error',L(W))
	def ejecutar_prueba_ks(C,muestra,nombre_prng):
		D=muestra;I,E=m(D);B=A.Text(C.marco_resultados,height=10,wrap=A.WORD,font=(F,14));B.pack(padx=10,pady=5,fill=G,expand=H);B.insert(A.END,f"Resultados de la Prueba Kolmogorov-Smirnov:\n");B.insert(A.END,f"PRNG: {nombre_prng}\n");B.insert(A.END,f"Estadístico KS: {I:.4f}\n");B.insert(A.END,f"Valor P: {E:.4f}\n")
		if E>.05:B.insert(A.END,c)
		else:B.insert(A.END,d)
		B.config(state=A.DISABLED);C.crear_histograma(D)
	def ejecutar_prueba_media(C,muestra,nombre_prng):
		D=muestra;I,J,E=n(D);B=A.Text(C.marco_resultados,height=10,wrap=A.WORD,font=(F,14));B.pack(padx=10,pady=5,fill=G,expand=H);B.insert(A.END,f"Resultados de la Prueba de Media:\n");B.insert(A.END,f"PRNG: {nombre_prng}\n");B.insert(A.END,f"Media de la Muestra: {I:.4f}\n");B.insert(A.END,f"Estadístico Z: {J:.4f}\n");B.insert(A.END,f"Valor P: {E:.4f}\n")
		if E>.05:B.insert(A.END,'Interpretación: Concordancia con la media esperada (p > 0.05).\n')
		else:B.insert(A.END,'Interpretación: Discrepancia con la media esperada (p ≤ 0.05).\n')
		B.config(state=A.DISABLED);C.crear_histograma(D)
	def ejecutar_prueba_varianza(C,muestra,nombre_prng):
		D=muestra;I,J,E=o(D);B=A.Text(C.marco_resultados,height=10,wrap=A.WORD,font=(F,14));B.pack(padx=10,pady=5,fill=G,expand=H);B.insert(A.END,f"Resultados de la Prueba de Varianza:\n");B.insert(A.END,f"PRNG: {nombre_prng}\n");B.insert(A.END,f"Varianza de la Muestra: {I:.4f}\n");B.insert(A.END,f"Estadístico Chi-Cuadrado: {J:.4f}\n");B.insert(A.END,f"Valor P: {E:.4f}\n")
		if E>.05:B.insert(A.END,'Interpretación: Concordancia con la varianza teórica (p > 0.05).\n')
		else:B.insert(A.END,'Interpretación: Discrepancia con la varianza teórica (p ≤ 0.05).\n')
		B.config(state=A.DISABLED);C.crear_histograma(D)
	def ejecutar_prueba_chi_cuadrado(E,muestra,nombre_prng,bins):
		J=muestra;D=bins;N,K,L,M=p(J,D);B=A.Text(E.marco_resultados,height=10,wrap=A.WORD,font=(F,14));B.pack(padx=10,pady=5,fill=G,expand=H);B.insert(A.END,f"Resultados de la Prueba Chi-Cuadrado:\n");B.insert(A.END,f"PRNG: {nombre_prng}\n");B.insert(A.END,f"Número de Intervalos: {D}\n");B.insert(A.END,f"Estadístico Chi-Cuadrado: {N:.4f}\n");B.insert(A.END,f"Valor P: {K:.4f}\n")
		if K>.05:B.insert(A.END,c)
		else:B.insert(A.END,d)
		B.insert(A.END,'\nFrecuencias Observadas:\n')
		for C in Y(I(L)):B.insert(A.END,f"Intervalo {C+1} ({M[C]:.2f}-{M[C+1]:.2f}): {L[C]}\n")
		B.config(state=A.DISABLED);E.crear_histograma(J,D)
	def crear_histograma(C,muestra,bins=10):D,A=g.subplots(figsize=(6,4));A.hist(muestra,bins=bins,range=(0,1),edgecolor='black');A.set_title('Distribución de la Muestra',fontname=F,fontsize=16);A.set_xlabel('Valor',fontname=F,fontsize=14);A.set_ylabel('Frecuencia',fontname=F,fontsize=14);B=h(D,master=C.marco_resultados);E=B.get_tk_widget();E.pack(padx=10,pady=5);B.draw()
	def exportar_datos(A):
		try:
			B=A.var_prng.get();E=A.mapa_prng[B];H=D(A.tamano_var.get())
			if B==M:F=E(A.semilla_var.get(),A.a_var.get(),A.c_var.get(),A.m_var.get())
			elif B==S:F=E(A.semilla_var.get())
			elif B==N:F=E(A.semilla_var.get(),A.a_var.get(),A.c_var.get(),A.m_var.get())
			elif B==O:F=E(A.semilla_var.get(),A.weyl_var.get(),A.delta_var.get())
			G=X(F,H);C=e.asksaveasfilename(defaultextension='.txt',filetypes=[('Archivos de texto','*.txt'),('Archivos CSV','*.csv')])
			if C:
				if C.endswith('.csv'):I=f.DataFrame(G,columns=['Números Aleatorios']);I.to_csv(C,index=False)
				else:
					with open(C,'w')as J:
						for K in G:J.write(f"{K:.6f}\n")
				P.showinfo('Exportación Exitosa',f"Datos exportados a {C}")
		except Exception as Q:P.showerror('Error de Exportación',L(Q))
	def salir_programa(A):A.root.quit();A.root.destroy()
def r():B=A.Tk();C=q(B);B.mainloop()
if __name__=='__main__':r()