# codigo generado por Qwen3 eb base al prompt:
'''
Ayúdame a crear una app en Python que muestre la hora en un reloj analógico, con manecillas para las hora y para los minutos. La hora  y los minutos deben ser ingresados en campos numéricos. El reloj debe actualizarse para mostrar la hora según los valores ingresados. El color del reloj debe ser rojo o de alguno de los colores seleccionados por el usuario (rojo, azul, verde, amarillo, celeste). El objetivo es enseñar a leer la hora a niños de 6 a 8 años.

Mejoras propuestas por QWEN:
incluye sonidos para la actualización de la hora y los minutos, y que la transición de las manecillas a la nueva hora sea suave (mostrando el desplazamiento).(utiliza pygame). Agregar una etiqueta que diga la hora en texto (ej: "Son las 3 y 15")
Agrega las siguientes características:
- Añadir un botón "Hora actual" que muestre la hora del sistema.
- Incluir una opción de "Modo juego" con preguntas tipo: "Mueve las manecillas a las 4 y 30".
- Agregar fondo con dibujos infantiles (sol, nube, etc.).

2025-08-22
autor: Patricio Araneda
'''

import tkinter as tk
from tkinter import ttk

import math
import pygame
import threading
import random
from datetime import datetime
import numpy as np

# Inicializar Pygame para sonidos
pygame.mixer.init()

# Generar sonidos simples (sin necesidad de archivos externos)

def crear_sonido(frecuencia=440, duracion=0.1):
    sample_rate = 22050
    n_samples = int(duracion * sample_rate)
    t = np.linspace(0, duracion, n_samples, False)
    wave = 0.5 * np.sign(np.sin(2 * np.pi * frecuencia * t))  # Onda cuadrada
    audio = np.array(wave * 32767, dtype=np.int16)
    stereo_audio = np.column_stack((audio, audio))  # Estéreo
    sound = pygame.sndarray.make_sound(stereo_audio)
    return sound

sonido_actualizacion = crear_sonido(523, 0.1)  # Do (C5)
sonido_final = crear_sonido(659, 0.2)          # Mi (E5)
sonido_correcto = crear_sonido(784, 0.3)       # Sol (G5) - correcto
sonido_error = crear_sonido(392, 0.3)          # Sol bajo - error

# Variables globales
animando = False
hora_actual = [3, 15]  # [hora, minutos]
hora_objetivo = [3, 15]
modo_juego = False
pregunta_actual = None

# Función para dibujar fondo infantil
def dibujar_fondo():
    ancho = canvas.winfo_width()
    alto = canvas.winfo_height()

    # Cielo
    canvas.create_rectangle(0, 0, ancho, alto * 0.7, fill="#87CEEB", outline="")
    # Pasto
    canvas.create_rectangle(0, alto * 0.7, ancho, alto, fill="#32CD32", outline="")

    # Sol
    canvas.create_oval(20, 20, 80, 80, fill="#FFD700", outline="#FFA500", width=3)
    for i in range(8):
        angle = math.radians(i * 45)
        x1 = 50 + 50 * math.cos(angle)
        y1 = 50 + 50 * math.sin(angle)
        x2 = 50 + 80 * math.cos(angle)
        y2 = 50 + 80 * math.sin(angle)
        canvas.create_line(x1, y1, x2, y2, fill="#FFA500", width=3)

    # Nubes
    canvas.create_oval(200, 30, 260, 70, fill="white", outline="white")
    canvas.create_oval(230, 50, 290, 90, fill="white", outline="white")
    canvas.create_oval(260, 30, 320, 70, fill="white", outline="white")

    canvas.create_oval(450, 50, 500, 90, fill="white", outline="white")
    canvas.create_oval(480, 40, 540, 80, fill="white", outline="white")
    canvas.create_oval(510, 50, 570, 90, fill="white", outline="white")

# Función para dibujar el reloj analógico
def dibujar_reloj(hora, minutos):
    canvas.delete("all")
    dibujar_fondo()  # Fondo infantil

    try:
        color = color_var.get()
    except:
        color = "rojo"

    colores = {
        "rojo": "#d92626",
        "azul": "#265fd9",
        "verde": "#26a626",
        "amarillo": "#e6d21a",
        "celeste": "#1aaee6"
    }
    color_hex = colores.get(color.lower(), "#d92626")

    ancho = canvas.winfo_width()
    alto = canvas.winfo_height()
    centro_x = ancho // 2
    centro_y = alto // 2
    radio = min(centro_x, centro_y) - 60  # Ajustado por el fondo

    # Círculo del reloj
    canvas.create_oval(centro_x - radio, centro_y - radio,
                       centro_x + radio, centro_y + radio,
                       outline=color_hex, width=5)

    # Números del 1 al 12
    for i in range(1, 13):
        angulo = math.radians(90 - i * 30)
        x = centro_x + (radio * 0.8) * math.cos(angulo)
        y = centro_y - (radio * 0.8) * math.sin(angulo)
        canvas.create_text(x, y, text=str(i), font=("Arial", 18, "bold"), fill="#000")

    # Ángulos de las manecillas
    angulo_minutos = math.radians(90 - minutos * 6)
    angulo_horas = math.radians(90 - (hora * 30 + minutos * 0.5))

    # Longitudes
    longitud_minutos = radio * 0.85
    longitud_horas = radio * 0.6

    # Manecilla minutos
    x_min = centro_x + longitud_minutos * math.cos(angulo_minutos)
    y_min = centro_y - longitud_minutos * math.sin(angulo_minutos)
    canvas.create_line(centro_x, centro_y, x_min, y_min, width=5, fill=color_hex, arrow=tk.LAST)

    # Manecilla horas
    x_hora = centro_x + longitud_horas * math.cos(angulo_horas)
    y_hora = centro_y - longitud_horas * math.sin(angulo_horas)
    canvas.create_line(centro_x, centro_y, x_hora, y_hora, width=7, fill=color_hex, arrow=tk.LAST)

# Función para actualizar texto de la hora
def actualizar_texto(hora, minutos):
    horas_texto = ["una", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce"]
    num_hora = hora if hora != 0 else 12
    hora_palabra = horas_texto[num_hora - 1]
    texto_hora.set(f"Son las {hora_palabra} y {minutos:02d}")

# Animar suavemente las manecillas
def animar_reloj():
    global animando, hora_actual, hora_objetivo

    if not animando:
        return

    pasos = 20
    h_actual, m_actual = hora_actual
    h_obj, m_obj = hora_objetivo

    dh = (h_obj - h_actual) / pasos
    dm = (m_obj - m_actual) / pasos

    for i in range(1, pasos + 1):
        h_intermedio = h_actual + dh * i
        m_intermedio = m_actual + dm * i

        if i % 5 == 0:
            pygame.mixer.Sound.play(sonido_actualizacion)

        root.after(int(40 * i), lambda h=int(h_intermedio), m=int(m_intermedio): [
            dibujar_reloj(h, m),
            actualizar_texto(h, m)
        ])

    # Al finalizar
    def final():
        global hora_actual
        dibujar_reloj(h_obj, m_obj)
        actualizar_texto(h_obj, m_obj)
        hora_actual = [h_obj, m_obj]
        animando = False
        verificar_juego(h_obj, m_obj)

    root.after(40 * pasos + 100, final)
    root.after(40 * pasos + 200, lambda: pygame.mixer.Sound.play(sonido_final))

# Verificar si la hora ingresada coincide con la pregunta (modo juego)
def verificar_juego(h, m):
    if modo_juego and pregunta_actual:
        h_preg, m_preg = pregunta_actual
        if h == h_preg and m == m_preg:
            texto_mensaje.set("¡Muy bien! 🎉")
            pygame.mixer.Sound.play(sonido_correcto)
            root.after(2000, nueva_pregunta_juego)
        else:
            texto_mensaje.set("Intenta otra vez...")

# Botón: Actualizar con animación
def actualizar_reloj_btn():
    global animando, hora_objetivo

    if animando:
        return

    try:
        h = int(entry_hora.get()) % 12
        m = int(entry_minutos.get()) % 60
    except ValueError:
        texto_mensaje.set("Por favor, ingresa números válidos.")
        return

    hora_objetivo = [h, m]
    animando = True
    threading.Thread(target=animar_reloj, daemon=True).start()

# Mostrar hora actual del sistema
def mostrar_hora_actual():
    now = datetime.now()
    h = now.hour % 12
    m = now.minute
    entry_hora.delete(0, tk.END)
    entry_hora.insert(0, str(h if h != 0 else 12))
    entry_minutos.delete(0, tk.END)
    entry_minutos.insert(0, str(m))
    actualizar_reloj_btn()

# Modo juego: generar pregunta aleatoria
def iniciar_modo_juego():
    global modo_juego, pregunta_actual
    modo_juego = True
    nueva_pregunta_juego()

def nueva_pregunta_juego():
    h = random.randint(1, 12)
    m = random.randrange(0, 60, 5)  # Minutos múltiplos de 5
    pregunta_actual = [h, m]
    horas_texto = ["una", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce"]
    hora_palabra = horas_texto[h - 1]
    texto_pregunta.set(f"🎯 Mueve las manecillas a las {hora_palabra} y {m:02d}")
    texto_mensaje.set("")

# Salir del modo juego
def salir_modo_juego():
    global modo_juego, pregunta_actual
    modo_juego = False
    pregunta_actual = None
    texto_pregunta.set("")
    texto_mensaje.set("")

# --- Interfaz gráfica ---
root = tk.Tk()
root.title("Reloj Analógico Educativo para Niños")
root.geometry("700x700")
root.configure(bg="#f0f8ff")

# Título principal
tk.Label(root, text="⏰ Aprende a Leer la Hora", font=("Arial", 22, "bold"), bg="#f0f8ff", fg="#2c3e50").pack(pady=15)

# Marco de entrada
frame_entradas = tk.Frame(root, bg="#f0f8ff")
frame_entradas.pack(pady=10)

tk.Label(frame_entradas, text="Hora (1-12):", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=5)
entry_hora = tk.Entry(frame_entradas, width=5, font=("Arial", 12), justify="center")
entry_hora.insert(0, "3")
entry_hora.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_entradas, text="Minutos (0-59):", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=2, padx=10, pady=5)
entry_minutos = tk.Entry(frame_entradas, width=5, font=("Arial", 12), justify="center")
entry_minutos.insert(0, "15")
entry_minutos.grid(row=0, column=3, padx=5, pady=5)

# Botones principales
frame_botones = tk.Frame(root, bg="#f0f8ff")
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Actualizar Reloj", command=actualizar_reloj_btn,
          font=("Arial", 11), bg="#4CAF50", fg="white", relief="flat", padx=10).grid(row=0, column=0, padx=10)

tk.Button(frame_botones, text="⏰ Hora Actual", command=mostrar_hora_actual,
          font=("Arial", 11), bg="#2196F3", fg="white", relief="flat", padx=10).grid(row=0, column=1, padx=10)

tk.Button(frame_botones, text="🎮 Modo Juego", command=iniciar_modo_juego,
          font=("Arial", 11), bg="#FF9800", fg="white", relief="flat", padx=10).grid(row=0, column=2, padx=10)

tk.Button(frame_botones, text="⏹️ Salir Juego", command=salir_modo_juego,
          font=("Arial", 11), bg="#9E9E9E", fg="white", relief="flat", padx=10).grid(row=0, column=3, padx=10)

# Selector de color
tk.Label(root, text="Color del reloj:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
color_var = tk.StringVar(value="rojo")
colores_opciones = ["rojo", "azul", "verde", "amarillo", "celeste"]
color_menu = ttk.Combobox(root, textvariable=color_var, values=colores_opciones, state="readonly", font=("Arial", 11))
color_menu.pack(pady=5)
color_menu.bind("<<ComboboxSelected>>", lambda e: dibujar_reloj(*hora_actual))

# Texto de la hora en palabras
texto_hora = tk.StringVar()
texto_hora.set("Son las tres y quince")
tk.Label(root, textvariable=texto_hora, font=("Arial", 16, "italic"), bg="#f0f8ff", fg="#555").pack(pady=10)

# Pregunta del modo juego
texto_pregunta = tk.StringVar()
tk.Label(root, textvariable=texto_pregunta, font=("Arial", 14, "bold"), fg="#e65100", bg="#f0f8ff").pack(pady=5)

# Mensaje de retroalimentación
texto_mensaje = tk.StringVar()
tk.Label(root, textvariable=texto_mensaje, font=("Arial", 14, "bold"), fg="#00695C", bg="#f0f8ff").pack(pady=5)

# Canvas para el reloj (con fondo)
canvas = tk.Canvas(root, width=400, height=400, bg="white", highlightthickness=0)
canvas.pack(pady=20)

# Inicializar
dibujar_fondo()
dibujar_reloj(3, 15)
actualizar_texto(3, 15)

# Iniciar
root.mainloop()