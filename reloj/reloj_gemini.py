'''
Codigo generado en base al prompt:
Ayúdame a crear una app en Python que muestre la hora en un reloj analógico, con manecillas para las hora y para los minutos. La hora  y los minutos deben ser ingresados en campos numéricos. El reloj debe actualizarse para mostrar la hora según los valores ingresados. El color del reloj debe ser rojo o de alguno de los colores seleccionados por el usuario (rojo, azul, verde, amarillo, celeste). El objetivo es enseñar a leer la hora a niños de 6 a 8 años.
2025-08-22
autor: Patricio Araneda
'''
import tkinter as tk
import math
import time

class AnalogClockApp:
    def __init__(self, root):
        """
        Inicializa la aplicación del reloj analógico.
        """
        self.root = root
        self.root.title("Reloj Analógico Interactivo")
        self.root.geometry("600x650")
        self.root.configure(bg="#f0f4f8")

        # Variable para el color de las manecillas, inicializado en rojo
        self.clock_color = "red"
        # Variables para la posición actual y objetivo de las manecillas
        self.current_hours = 3
        self.current_minutes = 0
        self.target_hours = 3
        self.target_minutes = 0
        self.animation_step_count = 0
        self.max_animation_steps = 100  # Número de fotogramas para la animación

        # Título de la aplicación
        self.title_label = tk.Label(root, text="Aprende a leer la hora", font=("Inter", 18, "bold"), bg="#f0f4f8", fg="#333")
        self.title_label.pack(pady=(10, 5))

        # Canvas para dibujar el reloj
        self.canvas = tk.Canvas(root, width=300, height=300, bg="#fefefe", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.canvas.configure(bd=0, relief="solid", highlightbackground="#cbd5e1", highlightcolor="#cbd5e1")

        # Paleta de colores para las manecillas
        self.color_frame = tk.Frame(root, bg="#f0f4f8")
        self.color_frame.pack(pady=10)

        colors = {"Rojo": "red", "Azul": "blue", "Verde": "green", "Negro": "black"}
        for name, hex_code in colors.items():
            color_button = tk.Button(
            self.color_frame,
            text=name,
            bg=hex_code,
            fg=hex_code,  # El color del texto es igual al color seleccionado
            width=8,
            height=2,
            bd=0,
            relief="flat",
            command=lambda color=hex_code: self.change_color(color)
            )
            color_button.pack(side="left", padx=5)

        # Controles para la entrada de la hora
        self.controls_frame = tk.Frame(root, bg="#f0f4f8")
        self.controls_frame.pack(pady=10)

        # Entrada de horas
        self.hours_label = tk.Label(self.controls_frame, text="Horas", font=("Inter", 16, "bold"), bg="#f0f4f8", fg="#64748b")
        self.hours_label.grid(row=0, column=0, padx=10, pady=5)
        self.hours_input = tk.Entry(self.controls_frame, width=5, font=("Inter", 16), justify="center")
        self.hours_input.grid(row=1, column=0, padx=10, pady=5)
        self.hours_input.insert(0, "3")

        # Entrada de minutos
        self.minutes_label = tk.Label(self.controls_frame, text="Minutos", font=("Inter", 16, "bold"), bg="#f0f4f8", fg="#64748b")
        self.minutes_label.grid(row=0, column=1, padx=10, pady=5)
        self.minutes_input = tk.Entry(self.controls_frame, width=5, font=("Inter", 16), justify="center")
        self.minutes_input.grid(row=1, column=1, padx=10, pady=5)
        self.minutes_input.insert(0, "0")


        # Botón para actualizar el reloj (texto en negro)
        self.update_button = tk.Button(self.controls_frame, text="Actualizar", command=self.start_animation, font=("Inter", 16, "bold"), bg="#3b82f6", fg="black", bd=0, relief="flat")
        self.update_button.grid(row=1, column=2, padx=10, pady=5, ipadx=10, ipady=5)
        
        # Mensaje de retroalimentación
        self.message_label = tk.Label(root, text="", font=("Inter", 14), bg="#f0f4f8", fg="red")
        self.message_label.pack(pady=5)
        
        # Iniciar con un reloj de ejemplo en 3:00
        self.draw_clock(3, 0)

    def draw_clock(self, hours, minutes):
        """
        Dibuja el reloj analógico en el canvas.
        """
        self.canvas.delete("all")

        center_x, center_y = 150, 150
        radius = 140

        # Dibujar la esfera del reloj con el color seleccionado
        self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline=self.clock_color, width=8, fill="#fefefe")

        # Dibujar los números de la hora
        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)
            x = center_x + math.cos(angle) * (radius * 0.85)
            y = center_y + math.sin(angle) * (radius * 0.85)
            self.canvas.create_text(x, y, text=str(i), font=("Inter", 16))

        # Dibujar los marcadores de minutos
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            inner_radius = radius * 0.95
            outer_radius = radius
            line_width = 1

            # Marcadores de 5 minutos (más largos y gruesos)
            if i % 5 == 0:
                inner_radius = radius * 0.9
                line_width = 2
            
            x1 = center_x + math.cos(angle) * inner_radius
            y1 = center_y + math.sin(angle) * inner_radius
            x2 = center_x + math.cos(angle) * outer_radius
            y2 = center_y + math.sin(angle) * outer_radius
            self.canvas.create_line(x1, y1, x2, y2, fill=self.clock_color, width=line_width)

        # Calcular los ángulos de las manecillas
        hour_angle = math.radians((hours % 12) * 30 + (minutes / 60) * 30 - 90)
        minute_angle = math.radians(minutes * 6 - 90)

        # Dibujar la manecilla de la hora
        hour_length = radius * 0.5
        x_hour = center_x + math.cos(hour_angle) * hour_length
        y_hour = center_y + math.sin(hour_angle) * hour_length
        self.canvas.create_line(center_x, center_y, x_hour, y_hour, fill=self.clock_color, width=8, capstyle="round")

        # Dibujar la manecilla de los minutos
        minute_length = radius * 0.7
        x_minute = center_x + math.cos(minute_angle) * minute_length
        y_minute = center_y + math.sin(minute_angle) * minute_length
        self.canvas.create_line(center_x, center_y, x_minute, y_minute, fill=self.clock_color, width=5, capstyle="round")

        # Dibujar el centro del reloj
        self.canvas.create_oval(center_x - 5, center_y - 5, center_x + 5, center_y + 5, fill="black", outline="black")

    def animate_clock(self):
        """
        Función para la animación de las manecillas.
        """
        if self.animation_step_count < self.max_animation_steps:
            # Calcular las horas y minutos para este fotograma
            animated_hours = self.current_hours + (self.target_hours - self.current_hours) * (self.animation_step_count / self.max_animation_steps)
            animated_minutes = self.current_minutes + (self.target_minutes - self.current_minutes) * (self.animation_step_count / self.max_animation_steps)
            
            self.draw_clock(animated_hours, animated_minutes)
            self.animation_step_count += 1
            self.root.after(10, self.animate_clock) # Llamar a la función de nuevo después de 10ms
        else:
            self.current_hours = self.target_hours
            self.current_minutes = self.target_minutes
            self.draw_clock(self.current_hours, self.current_minutes)

    def start_animation(self):
        """
        Inicia el proceso de animación después de validar la entrada.
        """
        try:
            target_h = int(self.hours_input.get())
            target_m = int(self.minutes_input.get())

            # Validar que los valores estén en un rango razonable
            if not (0 <= target_h <= 12 and 0 <= target_m <= 59):
                self.message_label.config(text="Por favor, ingresa horas (0-12) y minutos (0-59).")
                return

            # Calcular el movimiento más corto para las horas (ejemplo: 12 a 1 en lugar de 12 a 13)
            # Esto es importante para un movimiento realista
            current_h_12 = self.current_hours % 12
            if current_h_12 == 0: current_h_12 = 12
            
            target_h_12 = target_h % 12
            if target_h_12 == 0: target_h_12 = 12

            # Ajuste para el movimiento más corto
            diff_h = target_h_12 - current_h_12
            if diff_h > 6:
                target_h_12 -= 12
            elif diff_h < -6:
                target_h_12 += 12

            self.target_hours = target_h_12
            self.target_minutes = target_m
            
            self.message_label.config(text="") # Limpiar mensaje de error

            self.animation_step_count = 0
            self.animate_clock()

        except ValueError:
            self.message_label.config(text="Por favor, ingresa solo números.")

    def change_color(self, color):
        """
        Cambia el color de las manecillas y los marcadores del reloj.
        """
        self.clock_color = color
        self.draw_clock(self.current_hours, self.current_minutes)


if __name__ == "__main__":
    root = tk.Tk()
    app = AnalogClockApp(root)
    root.mainloop()
