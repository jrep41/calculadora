import customtkinter as ctk
import math
import tkinter.font as tkfont

# Configuración de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Calculadora(ctk.CTk):
    def __init__(self):
        """
        Constructor de la clase Calculadora.
        Inicializa la interfaz gráfica, configura la ventana y prepara los estados iniciales.
        """
        super().__init__()

        self.title("NexaCalc 1.4")
        self.geometry("400x620")
        self.resizable(False, False)
        self.configure(fg_color="#121821")
        self.familia_fuente_digital = self.obtener_familia_fuente_digital()

        # Modo científico y unidad de ángulo
        self.modo_cientifico = False
        self.usar_grados = True  # True para grados, False para radianes
        self.offset_basico = 0
        self.botones_cientificos = []
        self.botones_basicos = []
        self.mensaje_error_id = None
        self.mensaje_parpadeo_id = None
        self.mensaje_parpadeo_visible = False

        for col in range(8):
            self.grid_columnconfigure(col, weight=1)

        for row in range(3, 8):
            self.grid_rowconfigure(row, weight=1)

        self.crear_barra_modo()
        self.crear_display()
        self.crear_botones_basicos()
        self.crear_botones_cientificos()
        self.set_modo(False)

    def crear_barra_modo(self):
        self.btn_modo = ctk.CTkButton(
            self,
            text="Click toBASIC",
            height=38,
            corner_radius=10,
            font=("Segoe UI", 16, "bold"),
            fg_color="#1A222E",
            hover_color="#253142",
            text_color="#44D37A",
            border_width=2,
            border_color="#2DD873",
            command=lambda: self.set_modo(not self.modo_cientifico),
        )
        self.btn_modo.grid(
            row=0, column=0, columnspan=4, padx=18, pady=(18, 8), sticky="ew"
        )

    def crear_display(self):
        self.fuente_pantalla_normal = (self.familia_fuente_digital, 32, "normal")
        self.fuente_pantalla_error = (self.familia_fuente_digital, 16, "normal")
        self.color_texto_normal = "#44D37A"
        self.color_texto_error = "#44D37A"

        self.frame_display = ctk.CTkFrame(
            self,
            height=70,
            fg_color="#122A21",
            border_width=2,
            border_color="#2DD873",
            corner_radius=12,
        )
        self.frame_display.grid(
            row=1, column=0, columnspan=4, padx=18, pady=(4, 6), sticky="ew"
        )
        self.frame_display.grid_propagate(False)

        self.pantalla = ctk.CTkEntry(
            self.frame_display,
            font=self.fuente_pantalla_normal,
            height=34,
            corner_radius=0,
            justify="right",
            fg_color="transparent",
            border_width=0,
            text_color=self.color_texto_normal,
        )
        self.pantalla.place(relx=0.5, rely=0.5, relwidth=0.92, anchor="center")

        self.resultado_label = ctk.CTkLabel(
            self.frame_display,
            text="",
            font=(self.familia_fuente_digital, 14, "normal"),
            text_color="#B8CBC3",
            anchor="e",
        )
        self.resultado_label.place(relx=0.97, rely=0.9, anchor="e")

        self.mensaje_error_overlay = ctk.CTkLabel(
            self.frame_display,
            text="",
            font=self.fuente_pantalla_error,
            text_color=self.color_texto_error,
            anchor="center",
        )

        self.linea = ctk.CTkFrame(self, height=2, fg_color="#2D3A4D", corner_radius=0)
        self.linea.grid(
            row=2, column=0, columnspan=8, padx=18, pady=(2, 8), sticky="ew"
        )

    def crear_botones_basicos(self):
        layout_basico = [
            ("AC", 3, 0, 1, 1),
            ("=", 3, 1, 1, 1),
            ("+", 3, 2, 1, 1),
            ("×", 3, 3, 1, 1),
            ("7", 4, 0, 1, 1),
            ("8", 4, 1, 1, 1),
            ("9", 4, 2, 1, 1),
            ("÷", 4, 3, 1, 1),
            ("4", 5, 0, 1, 1),
            ("5", 5, 1, 1, 1),
            ("6", 5, 2, 1, 1),
            ("%", 5, 3, 1, 1),
            ("1", 6, 0, 1, 1),
            ("2", 6, 1, 1, 1),
            ("3", 6, 2, 1, 1),
            ("-", 6, 3, 1, 1),
            ("0", 7, 0, 1, 2),
            (".", 7, 2, 1, 1),
            ("=", 7, 3, 1, 1),
        ]

        for texto, fila, col, rowspan, colspan in layout_basico:
            estilo = self.obtener_estilo_boton_basico(texto)
            btn = ctk.CTkButton(
                self,
                text=texto,
                width=84,
                height=56,
                font=("Segoe UI", 30 if texto == "=" else 18, "bold"),
                fg_color=estilo["fg"],
                hover_color=estilo["hover"],
                border_width=2,
                border_color=estilo["border"],
                text_color=estilo["text"],
                corner_radius=10,
                command=lambda t=texto: self.on_click(t),
            )
            btn.grid(
                row=fila,
                column=col,
                rowspan=rowspan,
                columnspan=colspan,
                padx=5,
                pady=5,
                sticky="nsew",
            )
            self.botones_basicos.append(
                {
                    "widget": btn,
                    "fila": fila,
                    "col": col,
                    "rowspan": rowspan,
                    "colspan": colspan,
                }
            )

    def obtener_estilo_boton_basico(self, texto):
        if texto == "AC":
            return {
                "fg": "#2DCC6A",
                "hover": "#27B95E",
                "border": "#1A8C46",
                "text": "#EAF8F0",
            }
        if texto in {"+", "-", "×", "÷", "%"}:
            return {
                "fg": "#1E2936",
                "hover": "#2A384B",
                "border": "#3891DD",
                "text": "#4DAEFF",
            }
        if texto == "=":
            return {
                "fg": "#2DCC6A",
                "hover": "#27B95E",
                "border": "#1A8C46",
                "text": "#F5FFF8",
            }
        return {
            "fg": "#2E333D",
            "hover": "#3A404D",
            "border": "#1C2128",
            "text": "#EDF2F6",
        }

    def recolocar_botones_basicos(self):
        for info in self.botones_basicos:
            info["widget"].grid_configure(column=info["col"] + self.offset_basico)

    def crear_botones_cientificos(self):
        """
        Crea e inicializa todos los botones para funciones científicas (sin, cos, log, etc.).
        Los botones se crean ocultos por defecto.
        """
        botones_cient = [
            ("log", 3, 0),
            ("ln", 3, 1),
            ("√", 3, 2),
            ("x²", 3, 3),
            ("sin", 4, 0),
            ("cos", 4, 1),
            ("tan", 4, 2),
            ("exp", 4, 3),
            ("asin", 5, 0),
            ("acos", 5, 1),
            ("atan", 5, 2),
            ("π", 5, 3),
            ("(", 6, 0),
            (")", 6, 1),
            ("e", 6, 2),
        ]

        for texto, fila, col in botones_cient:
            fg_color = "#1E2936"
            hover_color = "#2A384B"
            border_color = "#2E86D7"

            btn = ctk.CTkButton(
                self,
                text=texto,
                width=80,
                height=56,
                font=("Segoe UI", 18, "bold"),
                fg_color=fg_color,
                hover_color=hover_color,
                text_color="#56B5FF",
                border_width=2,
                border_color=border_color,
                corner_radius=10,
                command=lambda t=texto: self.on_click_cientifico(t),
            )
            btn.grid(row=fila, column=col, padx=5, pady=5, sticky="nsew")
            btn.grid_remove()  # Ocultar inicialmente
            self.botones_cientificos.append(btn)

        self.angulo_btn = ctk.CTkButton(
            self,
            text="deg",
            width=80,
            height=56,
            font=("Segoe UI", 17, "bold"),
            fg_color="#1E2936",
            hover_color="#2A384B",
            text_color="#56B5FF",
            border_width=2,
            border_color="#2E86D7",
            corner_radius=10,
            command=self.toggle_angulo,
        )
        self.angulo_btn.grid(row=6, column=3, padx=5, pady=5, sticky="nsew")
        self.angulo_btn.grid_remove()

    def obtener_familia_fuente_digital(self):
        familias_disponibles = set(tkfont.families())
        familias_preferidas = [
            "DSEG14 Classic",
            "DSEG14 Modern",
            "DSEG7 Classic",
            "DS-Digital",
        ]

        for familia in familias_preferidas:
            if familia in familias_disponibles:
                return familia

        return "Courier New"

    def set_modo(self, cientifico):
        """
        Cambia entre el modo de calculadora básica y científica.
        Ajusta el tamaño de la ventana y muestra/oculta los botones adicionales.
        """
        self.modo_cientifico = cientifico

        if self.modo_cientifico:
            self.geometry("820x620")
            self.offset_basico = 4
            self.frame_display.grid_configure(columnspan=8)
            self.btn_modo.grid_configure(columnspan=8)
            for btn in self.botones_cientificos:
                btn.grid()
            self.angulo_btn.grid()
            self.btn_modo.configure(
                text="Click to BASIC",
                fg_color="#1B2A3F",
                border_color="#2E86D7",
                text_color="#56B5FF",
            )
        else:
            self.geometry("400x620")
            self.offset_basico = 0
            self.frame_display.grid_configure(columnspan=4)
            self.btn_modo.grid_configure(columnspan=4)
            for btn in self.botones_cientificos:
                btn.grid_remove()
            self.angulo_btn.grid_remove()
            self.btn_modo.configure(
                text="⚛  Click to SCIENTIFIC",
                fg_color="#1B2D25",
                border_color="#2DD873",
                text_color="#44D37A",
            )

        self.recolocar_botones_basicos()

    def toggle_angulo(self):
        """
        Cambia la unidad de medida angular para las funciones trigonométricas.
        Alterna entre Grados (DEG) y Radianes (RAD).
        """
        self.usar_grados = not self.usar_grados
        self.angulo_btn.configure(text="deg" if self.usar_grados else "rad")

    def on_click_cientifico(self, boton):
        """
        Maneja los eventos de clic de los botones científicos.
        Inserta la función matemática correspondiente en la posición del cursor o texto personalizado.

        Args:
            boton (str): El texto del botón presionado.
        """
        pos_cursor = self.pantalla.index("insert")

        if boton == "sin":
            self.pantalla.insert(pos_cursor, "sin(")
        elif boton == "cos":
            self.pantalla.insert(pos_cursor, "cos(")
        elif boton == "tan":
            self.pantalla.insert(pos_cursor, "tan(")
        elif boton == "asin":
            self.pantalla.insert(pos_cursor, "asin(")
        elif boton == "acos":
            self.pantalla.insert(pos_cursor, "acos(")
        elif boton == "atan":
            self.pantalla.insert(pos_cursor, "atan(")
        elif boton == "√":
            self.pantalla.insert(pos_cursor, "sqrt(")
        elif boton == "x²":
            self.pantalla.insert(pos_cursor, "**2")
        elif boton == "log":
            self.pantalla.insert(pos_cursor, "log10(")
        elif boton == "ln":
            self.pantalla.insert(pos_cursor, "log(")
        elif boton == "exp":
            self.pantalla.insert(pos_cursor, "exp(")
        elif boton == "π":
            self.pantalla.insert(pos_cursor, "pi")
        elif boton == "e":
            self.pantalla.insert(pos_cursor, "e")
        elif boton in ["%", "(", ")"]:
            self.pantalla.insert(pos_cursor, boton)

    def evaluar_expresion(self, expresion):
        """
        Evalúa de forma segura una expresión matemática dada en formato de cadena utilizando un entorno controlado.

        Args:
            expresion (str): La cadena que contiene la operación matemática.

        Returns:
            any: El resultado del cálculo evaluado.
        """
        # Crear un entorno seguro con funciones matemáticas
        safe_dict = {
            "sin": lambda x: math.sin(math.radians(x) if self.usar_grados else x),
            "cos": lambda x: math.cos(math.radians(x) if self.usar_grados else x),
            "tan": lambda x: math.tan(math.radians(x) if self.usar_grados else x),
            "asin": lambda x: (
                math.degrees(math.asin(x)) if self.usar_grados else math.asin(x)
            ),
            "acos": lambda x: (
                math.degrees(math.acos(x)) if self.usar_grados else math.acos(x)
            ),
            "atan": lambda x: (
                math.degrees(math.atan(x)) if self.usar_grados else math.atan(x)
            ),
            "sqrt": math.sqrt,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
            "__builtins__": {},
        }

        return eval(expresion, safe_dict)

    def mostrar_operacion_invalida(self):
        if self.mensaje_error_id is not None:
            self.after_cancel(self.mensaje_error_id)
            self.mensaje_error_id = None
        if self.mensaje_parpadeo_id is not None:
            self.after_cancel(self.mensaje_parpadeo_id)
            self.mensaje_parpadeo_id = None

        self.pantalla.configure(
            font=self.fuente_pantalla_normal,
            justify="right",
            text_color=self.color_texto_normal,
        )
        self.pantalla.delete(0, ctk.END)
        self.resultado_label.configure(text="")
        self.mensaje_error_overlay.configure(text="INVALID   OPERATION")
        self.mensaje_error_overlay.place(relx=0.5, rely=0.5, anchor="center")
        self.mensaje_parpadeo_visible = True
        self.mensaje_parpadeo_id = self.after(300, self.alternar_parpadeo_mensaje)
        self.mensaje_error_id = self.after(3000, self.limpiar_mensaje_error)

    def alternar_parpadeo_mensaje(self):
        if self.mensaje_parpadeo_visible:
            self.mensaje_error_overlay.place_forget()
        else:
            self.mensaje_error_overlay.place(relx=0.5, rely=0.5, anchor="center")

        self.mensaje_parpadeo_visible = not self.mensaje_parpadeo_visible
        self.mensaje_parpadeo_id = self.after(300, self.alternar_parpadeo_mensaje)

    def limpiar_mensaje_error(self):
        if self.mensaje_parpadeo_id is not None:
            self.after_cancel(self.mensaje_parpadeo_id)
            self.mensaje_parpadeo_id = None

        self.mensaje_error_overlay.place_forget()
        self.mensaje_parpadeo_visible = False
        self.pantalla.configure(
            font=self.fuente_pantalla_normal,
            justify="right",
            text_color=self.color_texto_normal,
        )
        self.mensaje_error_id = None

    def cancelar_mensaje_error(self):
        if self.mensaje_error_id is not None:
            self.after_cancel(self.mensaje_error_id)
            self.mensaje_error_id = None
        if self.mensaje_parpadeo_id is not None:
            self.after_cancel(self.mensaje_parpadeo_id)
            self.mensaje_parpadeo_id = None

        self.mensaje_error_overlay.place_forget()
        self.mensaje_parpadeo_visible = False

        self.pantalla.configure(
            font=self.fuente_pantalla_normal,
            justify="right",
            text_color=self.color_texto_normal,
        )

    def on_click(self, boton):
        """
        Maneja los eventos de clic de los botones básicos de la calculadora (números y operadores).
        También gestiona las acciones especiales de '=' para evaluar y 'C' para borrar.

        Args:
            boton (str): El texto o símbolo del botón presionado.
        """
        if boton == "=":
            try:
                self.cancelar_mensaje_error()
                resultado = self.evaluar_expresion(self.pantalla.get())
                self.resultado_label.configure(text=f"= {resultado}")
                self.pantalla.delete(0, ctk.END)
                self.pantalla.insert(ctk.END, str(resultado))
            except Exception:
                self.mostrar_operacion_invalida()
        elif boton == "AC":
            self.cancelar_mensaje_error()
            self.pantalla.delete(0, ctk.END)
            self.resultado_label.configure(text="")
        else:
            self.cancelar_mensaje_error()
            mapeo = {"×": "*", "÷": "/"}
            self.pantalla.insert(ctk.END, mapeo.get(boton, boton))


if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()
