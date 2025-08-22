'''
Codigo generado en base al prompt:
Ayúdame a crear una app en Python que muestre la hora en un reloj analógico, con manecillas para las hora y para los minutos. La hora  y los minutos deben ser ingresados en campos numéricos. El reloj debe actualizarse para mostrar la hora según los valores ingresados. El color del reloj debe ser rojo o de alguno de los colores seleccionados por el usuario (rojo, azul, verde, amarillo, celeste). El objetivo es enseñar a leer la hora a niños de 6 a 8 años.
2025-08-22
autor: Patricio Araneda
'''
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import pygame

class RelojAnalogico:
    def __init__(self, root):
        self.root = root
        self.root.title("Reloj Analógico - Aprende la Hora")
        
        # Inicializar pygame para sonidos
        pygame.mixer.init()
        self.sonido_correcto = "reloj/correcto.wav"
        self.sonido_incorrecto = "reloj/incorrecto.wav"

        # Variables
        self.hora = tk.IntVar(value=3)
        self.minuto = tk.IntVar(value=15)
        self.color_reloj = tk.StringVar(value='Rojo')
        self.ver_24h = tk.BooleanVar(value=False)
        self.pregunta = None

        # Colores disponibles
        self.colores = {
            'Rojo': 'red',
            'Azul': 'blue',
            'Verde': 'green',
            'Amarillo': 'yellow',
            'Celeste': 'cyan'
        }

        # Construcción de interfaz
        self.crear_widgets()
        self.dibujar_reloj()

    def crear_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Hora (0-23):").grid(row=0, column=0)
        tk.Spinbox(frame, from_=0, to=23, textvariable=self.hora, width=5).grid(row=0, column=1)

        tk.Label(frame, text="Minuto (0-59):").grid(row=1, column=0)
        tk.Spinbox(frame, from_=0, to=59, textvariable=self.minuto, width=5).grid(row=1, column=1)

        tk.Label(frame, text="Color del Reloj:").grid(row=2, column=0)
        color_cb = ttk.Combobox(frame, values=list(self.colores.keys()), textvariable=self.color_reloj, 
                                state='readonly', width=10)
        color_cb.grid(row=2, column=1)

        tk.Checkbutton(frame, text="Ver en formato 24h", variable=self.ver_24h).grid(row=3, column=0, columnspan=2)

        tk.Button(self.root, text="Mostrar Hora", command=self.dibujar_reloj).pack(pady=5)
        tk.Button(self.root, text="¿Qué hora es?", command=self.generar_pregunta).pack(pady=5)

        self.fig, self.ax = plt.subplots(figsize=(4, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    def dibujar_reloj(self):
        h = self.hora.get() % 12
        m = self.minuto.get()
        color = self.colores.get(self.color_reloj.get(), 'red')

        self.ax.clear()
        self.ax.set_facecolor("white")
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        circ = plt.Circle((0, 0), 1, fill=False, color=color, linewidth=4)
        self.ax.add_artist(circ)

        for i in range(12):
            ang = np.deg2rad(i * 30)
            x_out = np.sin(ang)
            y_out = np.cos(ang)
            x_in = 0.9 * x_out
            y_in = 0.9 * y_out
            self.ax.plot([x_in, x_out], [y_in, y_out], color='black', linewidth=2)
            self.ax.text(0.75 * x_out, 0.75 * y_out, str(i if i != 0 else 12), ha='center', va='center', fontsize=12)

        ang_h = np.deg2rad((h + m / 60) * 30)
        self.ax.plot([0, 0.5 * np.sin(ang_h)], [0, 0.5 * np.cos(ang_h)], color='black', linewidth=4)

        ang_m = np.deg2rad(m * 6)
        self.ax.plot([0, 0.8 * np.sin(ang_m)], [0, 0.8 * np.cos(ang_m)], color='black', linewidth=2)

        self.ax.plot(0, 0, 'o', color='black')
        self.canvas.draw()

        if self.ver_24h.get():
            hora_texto = f"{self.hora.get():02d}:{self.minuto.get():02d}"
        else:
            h12 = self.hora.get() % 12 or 12
            ampm = "AM" if self.hora.get() < 12 else "PM"
            hora_texto = f"{h12:02d}:{self.minuto.get():02d} {ampm}"

        self.root.title(f"Hora mostrada: {hora_texto}")

    def generar_pregunta(self):
        h = random.randint(0, 23)
        m = random.choice([0, 15, 30, 45])
        self.pregunta = (h, m)
        self.hora.set(0)
        self.minuto.set(0)
        self.dibujar_hora_pregunta()
        self.root.after(500, lambda: self.verificar_pregunta(h, m))

    def dibujar_hora_pregunta(self):
        h, m = self.pregunta
        self.hora.set(h)
        self.minuto.set(m)
        self.dibujar_reloj()

    def verificar_pregunta(self, h, m):
        respuesta = tk.simpledialog.askstring("Pregunta", "¿Qué hora es? (formato HH:MM)")
        if respuesta:
            try:
                hr, mn = map(int, respuesta.strip().split(":"))
                if hr == h and mn == m:
                    self.reproducir_sonido(True)
                    messagebox.showinfo("¡Correcto!", "¡Muy bien!")
                else:
                    self.reproducir_sonido(False)
                    messagebox.showerror("Incorrecto", f"La respuesta correcta era {h:02d}:{m:02d}")
            except:
                messagebox.showerror("Error", "Formato incorrecto. Usa HH:MM")
        else:
            messagebox.showinfo("Sin respuesta", "Intenta responder la próxima vez.")

    def reproducir_sonido(self, correcto=True):
        archivo = self.sonido_correcto if correcto else self.sonido_incorrecto
        try:
            pygame.mixer.music.load(archivo)
            pygame.mixer.music.play()
        except Exception as e:
            print("No se pudo reproducir el sonido:", e)

if __name__ == "__main__":
    import tkinter.simpledialog
    root = tk.Tk()
    app = RelojAnalogico(root)
    root.mainloop()
