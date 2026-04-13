import customtkinter as ctk
import math

# Configuración de apariencia
ctk.set_appearance_mode("light")  # Modo claro para aspecto real
ctk.set_default_color_theme("green")


class Calculadora(ctk.CTk):
    def __init__(self):
        """Constructor de la clase Calculadora. Diseño realista tipo calculadora física."""
        super().__init__()

        self.title("NexaCalc Pro")
        self.geometry("340x560")
        self.resizable(False, False)

        # Color del cuerpo de la calculadora
        self.configure(fg_color="#C0C0C0")

        # Variables de estado
        self.modo_cientifico = False
        self.usar_grados = True
        self.botones_cientificos = []
        self.botones_basicos = []
        self.mensaje_error_id = None
        self.mensaje_parpadeo_id = None
        self.mensaje_parpadeo_visible = False
        self.ultimo_resultado = None

        # Configurar grid principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Crear interfaz
        self.crear_panel_solar()
        self.crear_display_lcd()
        self.crear_area_botones()
        self.crear_botones_basicos()
        self.crear_botones_cientificos()
        self.set_modo(False)

    def crear_panel_solar(self):
        """Crea el panel solar decorativo superior."""
        frame_top = ctk.CTkFrame(self, fg_color="#D8D8D8", height=40, corner_radius=0)
        frame_top.pack(fill="x", padx=5, pady=(5, 2))
        frame_top.pack_propagate(False)

        # Panel solar
        frame_solar = ctk.CTkFrame(frame_top, width=110, height=28, fg_color="#1a1a2e", corner_radius=3)
        frame_solar.pack(side="left", padx=(8, 0), pady=4)
        frame_solar.pack_propagate(False)

        for i in range(5):
            celda = ctk.CTkFrame(frame_solar, width=20, height=20, fg_color="#0a0a15", corner_radius=1)
            celda.pack(side="left", padx=1, pady=2)
            celda.pack_propagate(False)

        # Marca
        marca = ctk.CTkLabel(frame_top, text="NEXACALC", font=("Arial", 11, "bold"), text_color="#505050")
        marca.pack(side="right", padx=12)

    def crear_display_lcd(self):
        """Crea el display tipo LCD con efecto realista."""
        # Marco del display
        marco = ctk.CTkFrame(self, height=95, fg_color="#8A8A8A", corner_radius=8)
        marco.pack(fill="x", padx=5, pady=2)
        marco.pack_propagate(False)

        # LCD interior
        lcd_bg = ctk.CTkFrame(marco, fg_color="#5A7A5A", corner_radius=5)
        lcd_bg.pack(fill="both", expand=True, padx=4, pady=4)

        # Línea superior LCD
        ctk.CTkFrame(lcd_bg, height=3, fg_color="#4A6A4A").pack(fill="x", padx=3, pady=(2, 0))

        # Contenido LCD
        lcd_content = ctk.CTkFrame(lcd_bg, fg_color="transparent")
        lcd_content.pack(fill="both", expand=True, padx=5, pady=2)

        # Etiqueta de expresión
        self.resultado_label = ctk.CTkLabel(
            lcd_content, text="", font=("Consolas", 13, "normal"),
            text_color="#2A5A2A", anchor="e", height=18
        )
        self.resultado_label.pack(fill="x")

        # Pantalla principal
        self.pantalla = ctk.CTkEntry(
            lcd_content, font=("Consolas", 38, "normal"), height=45,
            corner_radius=0, justify="right", fg_color="transparent",
            border_width=0, text_color="#1A3A1A"
        )
        self.pantalla.pack(fill="x", pady=(0, 2))

        # Línea inferior LCD
        ctk.CTkFrame(lcd_bg, height=2, fg_color="#6A8A6A").pack(fill="x", padx=3, pady=(0, 2))

    def crear_area_botones(self):
        """Crea el área de botones con el marco."""
        self.frame_botones = ctk.CTkFrame(self, fg_color="#C0C0C0")
        self.frame_botones.pack(fill="both", expand=True, padx=8, pady=4)

        # Botón para cambiar a modo científico (visible en modo básico)
        self.btn_modo = ctk.CTkButton(
            self.frame_botones, text="▸ Modo Científico",
            font=("Arial", 13, "bold"),
            fg_color="#4A5880", hover_color="#3A4870",
            text_color="#FFFFFF", corner_radius=10,
            border_width=2, border_color="#3A4870",
            command=lambda: self.set_modo(not self.modo_cientifico)
        )
        self.btn_modo.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=1, pady=(5, 2))

        # Configurar grid para botones
        for col in range(8):
            self.frame_botones.grid_columnconfigure(col, weight=1, pad=2)
        for row in range(7):
            self.frame_botones.grid_rowconfigure(row, weight=1, pad=2)

    def crear_botones_basicos(self):
        """Crea los botones básicos estilo calculadora física."""
        layout_basico = [
            # (texto, fila, col, colspan, tipo)
            ("AC", 0, 0, 1, "funcion"), ("C", 0, 1, 1, "funcion"),
            ("%", 0, 2, 1, "operador"), ("÷", 0, 3, 1, "operador"),
            ("7", 1, 0, 1, "numero"), ("8", 1, 1, 1, "numero"),
            ("9", 1, 2, 1, "numero"), ("×", 1, 3, 1, "operador"),
            ("4", 2, 0, 1, "numero"), ("5", 2, 1, 1, "numero"),
            ("6", 2, 2, 1, "numero"), ("-", 2, 3, 1, "operador"),
            ("1", 3, 0, 1, "numero"), ("2", 3, 1, 1, "numero"),
            ("3", 3, 2, 1, "numero"), ("+", 3, 3, 1, "operador"),
            ("0", 4, 0, 2, "numero"), (".", 4, 2, 1, "numero"), ("=", 4, 3, 1, "igual"),
        ]

        for texto, fila, col, colspan, tipo in layout_basico:
            estilo = self.obtener_estilo_boton_realista(texto, tipo)
            btn = ctk.CTkButton(
                self.frame_botones, text=texto,
                font=("Arial", 20 if texto == "=" else 17, "bold"),
                fg_color=estilo["fg"], hover_color=estilo["hover"],
                text_color=estilo["text"], corner_radius=8,
                border_width=2, border_color=estilo["border"],
                command=lambda t=texto: self.on_click(t)
            )
            btn.grid(row=fila, column=col, columnspan=colspan, sticky="nsew", padx=1, pady=1)
            self.botones_basicos.append(btn)

    def obtener_estilo_boton_realista(self, texto, tipo):
        """Obtiene los colores realistas según el tipo de botón."""
        if tipo == "funcion":
            return {
                "fg": "#D84040", "hover": "#C03030",
                "text": "#FFFFFF", "border": "#A02020"
            }
        elif tipo == "operador":
            return {
                "fg": "#E89830", "hover": "#D08820",
                "text": "#FFFFFF", "border": "#B07818"
            }
        elif tipo == "igual":
            return {
                "fg": "#38A050", "hover": "#289040",
                "text": "#FFFFFF", "border": "#207030"
            }
        else:
            return {
                "fg": "#F2F2F2", "hover": "#E4E4E4",
                "text": "#1A1A1A", "border": "#C8C8C8"
            }

    def crear_botones_cientificos(self):
        """Crea los botones científicos."""
        botones_cient = [
            ("sin", 0, 4), ("cos", 0, 5), ("tan", 0, 6), ("ln", 0, 7),
            ("asin", 1, 4), ("acos", 1, 5), ("atan", 1, 6), ("log", 1, 7),
            ("√", 2, 4), ("x²", 2, 5), ("xʸ", 2, 6), ("π", 2, 7),
            ("(", 3, 4), (")", 3, 5), ("e", 3, 6), ("^", 3, 7),
            ("1/x", 4, 4), ("!", 4, 5), ("ANS", 4, 6), ("+/-", 4, 7),
        ]

        for texto, fila, col in botones_cient:
            btn = ctk.CTkButton(
                self.frame_botones, text=texto,
                font=("Arial", 13, "bold"),
                fg_color="#4A5880", hover_color="#3A4870",
                text_color="#D0D8F0", corner_radius=8,
                border_width=2, border_color="#3A4870",
                command=lambda t=texto: self.on_click_cientifico(t)
            )
            btn.grid(row=fila, column=col, sticky="nsew", padx=1, pady=1)
            btn.grid_remove()
            self.botones_cientificos.append(btn)

        # Botón DEG/RAD - integrado en la última fila científica
        self.angulo_btn = ctk.CTkButton(
            self.frame_botones, text="DEG",
            font=("Arial", 11, "bold"),
            fg_color="#606070", hover_color="#505060",
            text_color="#E0E0E0", corner_radius=6,
            border_width=2, border_color="#505060",
            command=self.toggle_angulo
        )
        # No se agrega al grid aquí, se maneja desde set_modo

    def set_modo(self, cientifico):
        """Cambia entre modo básico y científico."""
        self.modo_cientifico = cientifico
        if self.modo_cientifico:
            self.geometry("680x560")
            for btn in self.botones_cientificos:
                btn.grid()
            # Botón DEG en columna 4-5 de la fila 5
            self.angulo_btn.grid(row=5, column=4, columnspan=2, sticky="nsew", padx=1, pady=(5, 2))
            # Botón Modo Básico en columna 6-7 de la fila 5
            self.btn_modo.grid_forget()
            self.btn_modo.configure(text="◂ Modo Básico")
            self.btn_modo.grid(row=5, column=6, columnspan=2, sticky="nsew", padx=1, pady=(5, 2))
        else:
            self.geometry("340x560")
            for btn in self.botones_cientificos:
                btn.grid_remove()
            self.angulo_btn.grid_remove()
            self.btn_modo.grid_forget()
            self.btn_modo.configure(text="▸ Modo Científico")
            self.btn_modo.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=1, pady=(5, 2))

    def toggle_angulo(self):
        """Alterna entre grados y radianes."""
        self.usar_grados = not self.usar_grados
        self.angulo_btn.configure(text="DEG" if self.usar_grados else "RAD")

    def on_click_cientifico(self, boton):
        """Maneja los clics de botones científicos."""
        pos_cursor = self.pantalla.index("insert")
        mapeo = {
            "sin": "sin(", "cos": "cos(", "tan": "tan(",
            "asin": "asin(", "acos": "acos(", "atan": "atan(",
            "ln": "log(", "log": "log10(", "√": "sqrt(",
            "x²": "**2", "xʸ": "**(", "^": "**",
        }

        if boton == "ANS":
            if self.ultimo_resultado is not None:
                self.pantalla.insert(pos_cursor, str(self.ultimo_resultado))
        elif boton == "+/-":
            contenido = self.pantalla.get()
            if contenido and contenido != "Error":
                if contenido.startswith("-"):
                    self.pantalla.delete(0, ctk.END)
                    self.pantalla.insert(0, contenido[1:])
                else:
                    self.pantalla.insert(0, "-")
        elif boton == "1/x":
            self.pantalla.insert(pos_cursor, "1/(")
        elif boton == "!":
            self.pantalla.insert(pos_cursor, "factorial(")
        elif boton in mapeo:
            self.pantalla.insert(pos_cursor, mapeo[boton])
        elif boton in ["(", ")", "π", "e"]:
            texto = {"π": "pi", "e": "e"}.get(boton, boton)
            self.pantalla.insert(pos_cursor, texto)

    def evaluar_expresion(self, expresion):
        """Evalúa la expresión de forma segura."""
        def factorial(n):
            if n < 0:
                raise ValueError("Factorial no definido para negativos")
            if n > 170:
                raise ValueError("Número muy grande")
            result = 1
            for i in range(1, int(n) + 1):
                result *= i
            return result

        safe_dict = {
            "sin": lambda x: math.sin(math.radians(x) if self.usar_grados else x),
            "cos": lambda x: math.cos(math.radians(x) if self.usar_grados else x),
            "tan": lambda x: math.tan(math.radians(x) if self.usar_grados else x),
            "asin": lambda x: math.degrees(math.asin(max(-1, min(1, x)))) if self.usar_grados else math.asin(max(-1, min(1, x))),
            "acos": lambda x: math.degrees(math.acos(max(-1, min(1, x)))) if self.usar_grados else math.acos(max(-1, min(1, x))),
            "atan": lambda x: math.degrees(math.atan(x)) if self.usar_grados else math.atan(x),
            "sqrt": math.sqrt,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
            "factorial": factorial,
            "abs": abs,
            "pi": math.pi,
            "e": math.e,
            "__builtins__": {},
        }
        return eval(expresion, safe_dict)

    def mostrar_error(self):
        """Muestra el mensaje de error."""
        self.pantalla.delete(0, ctk.END)
        self.pantalla.insert(0, "Error")
        self.pantalla.configure(text_color="#803030")
        self.mensaje_parpadeo_visible = True
        self.mensaje_parpadeo_id = self.after(150, self._alternar_parpadeo)
        self.mensaje_error_id = self.after(2000, self.limpiar_error)

    def _alternar_parpadeo(self):
        color = "#503030" if self.mensaje_parpadeo_visible else "#803030"
        self.pantalla.configure(text_color=color)
        self.mensaje_parpadeo_visible = not self.mensaje_parpadeo_visible
        if self.mensaje_parpadeo_id:
            self.mensaje_parpadeo_id = self.after(150, self._alternar_parpadeo)

    def limpiar_error(self):
        if self.mensaje_parpadeo_id:
            self.after_cancel(self.mensaje_parpadeo_id)
            self.mensaje_parpadeo_id = None
        if self.mensaje_error_id:
            self.after_cancel(self.mensaje_error_id)
            self.mensaje_error_id = None
        self.pantalla.configure(text_color="#1A3A1A")
        if self.pantalla.get() == "Error":
            self.pantalla.delete(0, ctk.END)

    def on_click(self, boton):
        """Maneja los clics de botones básicos."""
        if boton == "=":
            try:
                if self.mensaje_error_id:
                    self.after_cancel(self.mensaje_error_id)
                if self.mensaje_parpadeo_id:
                    self.after_cancel(self.mensaje_parpadeo_id)
                self.pantalla.configure(text_color="#1A3A1A")

                expresion = self.pantalla.get()
                resultado = self.evaluar_expresion(expresion)
                self.ultimo_resultado = resultado
                self.resultado_label.configure(text=f"{expresion} =")
                self.pantalla.delete(0, ctk.END)
                self.pantalla.insert(0, str(resultado))
            except Exception:
                self.mostrar_error()
        elif boton == "AC":
            self.limpiar_error()
            self.pantalla.delete(0, ctk.END)
            self.resultado_label.configure(text="")
            self.ultimo_resultado = None
        elif boton == "C":
            self.limpiar_error()
            self.pantalla.delete(0, ctk.END)
        else:
            if self.mensaje_error_id:
                self.after_cancel(self.mensaje_error_id)
            if self.mensaje_parpadeo_id:
                self.after_cancel(self.mensaje_parpadeo_id)
            self.pantalla.configure(text_color="#1A3A1A")
            mapeo = {"×": "*", "÷": "/", "π": "pi"}
            texto = mapeo.get(boton, boton)
            self.pantalla.insert(ctk.END, texto)


if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()