'''
Codigo generado en base al prompt:
Ayúdame a crear una app en Python que muestre la hora en un reloj analógico, con manecillas para las hora y para los minutos. La hora  y los minutos deben ser ingresados en campos numéricos. El reloj debe actualizarse para mostrar la hora según los valores ingresados. El color del reloj debe ser rojo o de alguno de los colores seleccionados por el usuario (rojo, azul, verde, amarillo, celeste). El objetivo es enseñar a leer la hora a niños de 6 a 8 años.
2025-08-22
autor: Patricio Araneda
'''
import tkinter as tk
import math
import time

class RelojAnalogico:
    def __init__(self, root):
        self.root = root
        self.root.title("Reloj Analógico para Niños")
        self.root.geometry("650x750")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.hora = tk.StringVar(value="12")
        self.minuto = tk.StringVar(value="00")
        self.color_seleccionado = tk.StringVar(value="rojo")
        self.animacion_activa = False
        
        # Colores disponibles
        self.colores = {
            "rojo": "#FF5252",
            "azul": "#2196F3",
            "verde": "#4CAF50",
            "amarillo": "#FFD600",
            "celeste": "#00BCD4"
        }
        
        # Crear la interfaz
        self.crear_widgets()
        
        # Actualizar reloj inicialmente
        self.actualizar_reloj()
    
    def crear_widgets(self):
        # Marco principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        titulo = tk.Label(main_frame, text="Reloj Analógico para Niños", 
                         font=("Arial", 18, "bold"), bg='#f0f0f0', fg="#333333")
        titulo.pack(pady=10)
        
        # Marco para el reloj
        self.marco_reloj = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        self.marco_reloj.pack(pady=20)
        
        # Lienzo para el reloj
        self.lienzo = tk.Canvas(self.marco_reloj, width=400, height=400, bg='white', highlightthickness=0)
        self.lienzo.pack(padx=10, pady=10)
        
        # Marco para controles
        controles_frame = tk.Frame(main_frame, bg='#f0f0f0')
        controles_frame.pack(pady=20)
        
        # Controles de hora
        hora_frame = tk.Frame(controles_frame, bg='#f0f0f0')
        hora_frame.pack(pady=10)
        
        tk.Label(hora_frame, text="Hora (1-12):", font=("Arial", 16), bg='#f0f0f0').grid(row=0, column=0, padx=5)
        hora_spinbox = tk.Spinbox(hora_frame, from_=1, to=12, textvariable=self.hora, 
                                 width=5, font=("Arial", 16))
        hora_spinbox.grid(row=0, column=1, padx=5)
        
        tk.Label(hora_frame, text="Minutos (0-59):", font=("Arial", 16), bg='#f0f0f0').grid(row=0, column=2, padx=5)
        minuto_spinbox = tk.Spinbox(hora_frame, from_=0, to=59, textvariable=self.minuto, 
                                   width=5, font=("Arial", 16))
        minuto_spinbox.grid(row=0, column=3, padx=5)
        
        # Botón para actualizar
        tk.Button(hora_frame, text="Actualizar Reloj", font=("Arial", 16), 
                 command=self.iniciar_animacion, bg="#4CAF50", fg="green").grid(row=0, column=4, padx=10)
        
        # Controles de color
        color_frame = tk.Frame(controles_frame, bg='#f0f0f0')
        color_frame.pack(pady=10)
        
        tk.Label(color_frame, text="Color del reloj:", font=("Arial", 16), bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        
        for color in self.colores:
            tk.Radiobutton(color_frame, text=color.capitalize(), variable=self.color_seleccionado, 
                           font=("Arial", 16),
                          value=color, bg='#f0f0f0', command=self.actualizar_reloj).pack(side=tk.LEFT, padx=5)
        
        # Botón para hora actual
        tk.Button(controles_frame, text="Usar hora actual", font=("Arial", 16), 
                 command=self.establecer_hora_actual).pack(pady=10)
        
        # Instrucciones para niños
        instrucciones = tk.Label(main_frame, 
                                text="¡Aprende a leer la hora! Cambia la hora y los minutos y presiona 'Actualizar Reloj' para ver cómo se mueven las manecillas.",
                                font=("Arial", 14), bg='#f0f0f0', fg="#555555", wraplength=500)
        instrucciones.pack(pady=10)
    
    def dibujar_reloj(self, h=None, m=None):
        self.lienzo.delete("all")
        color = self.colores[self.color_seleccionado.get()]
        
        # Usar valores proporcionados o de los campos de entrada
        if h is None:
            try:
                h = int(self.hora.get())
            except ValueError:
                h = 12
        if m is None:
            try:
                m = int(self.minuto.get())
            except ValueError:
                m = 0
        
        # Dibujar círculo del reloj
        centro_x, centro_y, radio = 200, 200, 180
        self.lienzo.create_oval(centro_x - radio, centro_y - radio, 
                               centro_x + radio, centro_y + radio, 
                               width=3, outline=color)
        
        # Dibujar números
        for i in range(1, 13):
            angulo = math.radians(90 - i * 30)
            x = centro_x + (radio - 30) * math.cos(angulo)
            y = centro_y - (radio - 30) * math.sin(angulo)
            self.lienzo.create_text(x, y, text=str(i), font=("Arial", 16, "bold"), fill=color)
        
        # Dibujar marcas de minutos
        for i in range(60):
            angulo = math.radians(90 - i * 6)
            inicio_x = centro_x + (radio - 10) * math.cos(angulo)
            inicio_y = centro_y - (radio - 10) * math.sin(angulo)
            fin_x = centro_x + radio * math.cos(angulo)
            fin_y = centro_y - radio * math.sin(angulo)
            
            if i % 5 == 0:  # Marcas más largas para las horas
                self.lienzo.create_line(inicio_x, inicio_y, fin_x, fin_y, width=2, fill=color)
            else:  # Marcas más cortas para los minutos
                self.lienzo.create_line(inicio_x, inicio_y, fin_x, fin_y, width=1, fill=color)
        
        # Dibujar manecilla de horas
        angulo_hora = math.radians(90 - (h % 12) * 30 - m * 0.5)
        hora_x = centro_x + (radio * 0.5) * math.cos(angulo_hora)
        hora_y = centro_y - (radio * 0.5) * math.sin(angulo_hora)
        self.lienzo.create_line(centro_x, centro_y, hora_x, hora_y, width=6, fill=color, arrow=tk.LAST)
        
        # Dibujar manecilla de minutos
        angulo_minuto = math.radians(90 - m * 6)
        minuto_x = centro_x + (radio * 0.7) * math.cos(angulo_minuto)
        minuto_y = centro_y - (radio * 0.7) * math.sin(angulo_minuto)
        self.lienzo.create_line(centro_x, centro_y, minuto_x, minuto_y, width=4, fill=color, arrow=tk.LAST)
        
        # Dibujar centro del reloj
        self.lienzo.create_oval(centro_x - 10, centro_y - 10, centro_x + 10, centro_y + 10, 
                               fill=color, outline=color)
        
        # Mostrar hora digital
        hora_str = f"{h:02d}:{m:02d}"
        self.lienzo.create_text(centro_x, centro_y + radio + 30, text=hora_str, 
                               font=("Arial", 20, "bold"), fill=color)
        
        return h, m
    
    def actualizar_reloj(self):
        self.dibujar_reloj()
    
    def establecer_hora_actual(self):
        ahora = time.localtime()
        self.hora.set(str(ahora.tm_hour % 12 or 12))  # Convertir 0 a 12 para formato 12h
        self.minuto.set(str(ahora.tm_min))
        self.iniciar_animacion()
    
    def iniciar_animacion(self):
        if self.animacion_activa:
            return
            
        try:
            h_objetivo = int(self.hora.get())
            m_objetivo = int(self.minuto.get())
        except ValueError:
            return
        
        # Validar valores
        h_objetivo = max(1, min(12, h_objetivo))
        m_objetivo = max(0, min(59, m_objetivo))
        
        # Obtener hora actual del reloj (de los últimos valores dibujados)
        h_actual, m_actual = self.obtener_hora_actual()
        
        # Iniciar animación
        self.animacion_activa = True
        self.animar_manecillas(h_actual, m_actual, h_objetivo, m_objetivo, 0)
    
    def obtener_hora_actual(self):
        # Esta función debería obtener la hora actual del reloj
        # Por simplicidad, asumimos que siempre empieza desde la última posición
        try:
            return int(self.hora.get()), int(self.minuto.get())
        except ValueError:
            return 12, 0
    
    def animar_manecillas(self, h_actual, m_actual, h_objetivo, m_objetivo, paso):
        if not self.animacion_activa:
            return
        
        # Calcular pasos intermedios
        total_pasos = 20
        progreso = paso / total_pasos
        
        # Calcular valores intermedios
        if h_actual != h_objetivo:
            h_intermedio = h_actual + (h_objetivo - h_actual) * progreso
        else:
            h_intermedio = h_actual
            
        if m_actual != m_objetivo:
            m_intermedio = m_actual + (m_objetivo - m_actual) * progreso
        else:
            m_intermedio = m_actual
        
        # Dibujar reloj con valores intermedios
        self.dibujar_reloj(round(h_intermedio), round(m_intermedio))
        
        # Continuar animación o terminarla
        if paso < total_pasos:
            self.root.after(50, lambda: self.animar_manecillas(
                h_actual, m_actual, h_objetivo, m_objetivo, paso + 1))
        else:
            # Asegurarse de que terminamos en la posición exacta
            self.dibujar_reloj(h_objetivo, m_objetivo)
            self.animacion_activa = False

if __name__ == "__main__":
    root = tk.Tk()
    app = RelojAnalogico(root)
    root.mainloop()