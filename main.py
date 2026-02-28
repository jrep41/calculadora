import customtkinter as ctk
from tkinter import messagebox
import math

# Configuración de apariencia
ctk.set_appearance_mode("light")  # Modos: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue" (standard), "green", "dark-blue"


class Calculadora(ctk.CTk):
    def __init__(self):
        """
        Constructor de la clase Calculadora.
        Inicializa la interfaz gráfica, configura la ventana y prepara los estados iniciales.
        """
        super().__init__()

        self.title("Calculadora Pro")
        self.geometry("370x480")  # Aumentado de 440 a 480 para dar más espacio
        self.resizable(False, False)
        self.configure(
            fg_color="#D3D3D3"
        )  # Configura el fondo a gris claro (LightGray)

        # Modo científico y unidad de ángulo
        self.modo_cientifico = False
        self.usar_grados = True  # True para grados, False para radianes
        self.botones_cientificos = []

        # Toggle de modo científico
        self.toggle_btn = ctk.CTkButton(
            self,
            text="Modo Científico",
            width=160,
            height=35,
            font=("Arial", 14, "bold"),
            fg_color="#1f6aa5",
            hover_color="#144970",
            command=self.toggle_modo,
        )
        self.toggle_btn.grid(
            row=0, column=0, columnspan=2, padx=(20, 5), pady=(20, 5), sticky="ew"
        )

        # Toggle de unidad de ángulo (inicialmente oculto)
        self.angulo_btn = ctk.CTkButton(
            self,
            text="DEG",
            width=160,
            height=35,
            font=("Arial", 14, "bold"),
            fg_color="#5a4a8a",
            hover_color="#3d3260",
            command=self.toggle_angulo,
        )
        self.angulo_btn.grid(
            row=0, column=2, columnspan=2, padx=(5, 20), pady=(20, 5), sticky="ew"
        )
        self.angulo_btn.grid_remove()  # Ocultar inicialmente

        # Aumentada la altura (height) de 50
        self.pantalla = ctk.CTkEntry(
            self, font=("Arial", 32), height=50, corner_radius=10, justify="right"
        )
        self.pantalla.grid(
            row=1, column=0, columnspan=4, padx=20, pady=(5, 20), sticky="nsew"
        )

        botones = [
            "7",
            "8",
            "9",
            "/",
            "4",
            "5",
            "6",
            "*",
            "1",
            "2",
            "3",
            "-",
            "C",
            "0",
            "=",
            "+",
        ]

        r, c = 2, 0
        for boton in botones:
            # Colores base y de borde para efecto de profundidad
            if boton == "=":
                fg_color = "#2fa572"
                hover_color = "#217350"
                border_color = "#1a5a3f"  # Borde más oscuro (sombra inferior)
            elif boton == "C":
                fg_color = "#d35b58"
                hover_color = "#a54543"
                border_color = "#7a3231"
            elif boton in ["/", "*", "-", "+"]:
                fg_color = "#1f6aa5"
                hover_color = "#144970"
                border_color = "#0e3451"
            else:
                fg_color = "#3b3b3b"
                hover_color = "#4b4b4b"
                border_color = "#222222"

            ctk.CTkButton(
                self,
                text=boton,
                width=80,
                height=60,
                font=("Arial", 22, "bold"),
                fg_color=fg_color,
                hover_color=hover_color,
                border_width=3,  # Borde más grueso
                border_color=border_color,  # Actúa como sombra
                corner_radius=8,  # Un poco más cuadrado para solidez
                command=lambda b=boton: self.on_click(b),
            ).grid(
                row=r, column=c, padx=5, pady=(5, 12)
            )  # Más margen inferior
            c += 1
            if c > 3:
                c = 0
                r += 1

        # Botones científicos (inicialmente ocultos)
        self.crear_botones_cientificos()

    def crear_botones_cientificos(self):
        """
        Crea e inicializa todos los botones para funciones científicas (sin, cos, log, etc.).
        Los botones se crean ocultos por defecto.
        """
        botones_cient = [
            ("sin", 2, 4),
            ("cos", 3, 4),
            ("tan", 4, 4),
            ("√", 5, 4),
            ("asin", 2, 5),
            ("acos", 3, 5),
            ("atan", 4, 5),
            ("x²", 5, 5),
            ("log", 2, 6),
            ("ln", 3, 6),
            ("exp", 4, 6),
            ("%", 5, 6),
            ("π", 2, 7),
            ("e", 3, 7),
            ("(", 4, 7),
            (")", 5, 7),
        ]

        for texto, fila, col in botones_cient:
            fg_color = "#5a4a8a"
            hover_color = "#3d3260"
            border_color = "#2a1f45"

            btn = ctk.CTkButton(
                self,
                text=texto,
                width=80,
                height=60,
                font=("Arial", 18, "bold"),
                fg_color=fg_color,
                hover_color=hover_color,
                border_width=3,
                border_color=border_color,
                corner_radius=8,
                command=lambda t=texto: self.on_click_cientifico(t),
            )
            btn.grid(row=fila, column=col, padx=5, pady=(5, 12))
            btn.grid_remove()  # Ocultar inicialmente
            self.botones_cientificos.append(btn)

    def toggle_modo(self):
        """
        Cambia entre el modo de calculadora básica y científica.
        Ajusta el tamaño de la ventana y muestra/oculta los botones adicionales.
        """
        self.modo_cientifico = not self.modo_cientifico

        if self.modo_cientifico:
            self.geometry("730x480")  # Ajustado a 480 de alto según el cambio anterior
            self.toggle_btn.configure(text="Modo Básico")
            self.angulo_btn.grid()
            # Expandir la pantalla para que cubra las 8 columnas (0 a 7)
            self.pantalla.grid(columnspan=8)
            for btn in self.botones_cientificos:
                btn.grid()
        else:
            self.geometry("370x480")  # Ajustado a 480 de alto según el cambio anterior
            self.toggle_btn.configure(text="Modo Científico")
            self.angulo_btn.grid_remove()  # Ocultar toggle de ángulo
            # Reducir la pantalla a las 4 columnas originales
            self.pantalla.grid(columnspan=4)
            for btn in self.botones_cientificos:
                btn.grid_remove()

    def toggle_angulo(self):
        """
        Cambia la unidad de medida angular para las funciones trigonométricas.
        Alterna entre Grados (DEG) y Radianes (RAD).
        """
        self.usar_grados = not self.usar_grados
        self.angulo_btn.configure(text="DEG" if self.usar_grados else "RAD")

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

    def on_click(self, boton):
        """
        Maneja los eventos de clic de los botones básicos de la calculadora (números y operadores).
        También gestiona las acciones especiales de '=' para evaluar y 'C' para borrar.
        
        Args:
            boton (str): El texto o símbolo del botón presionado.
        """
        if boton == "=":
            try:
                resultado = self.evaluar_expresion(self.pantalla.get())
                self.pantalla.delete(0, ctk.END)
                self.pantalla.insert(ctk.END, str(resultado))
            except Exception:
                messagebox.showerror("Error", "Expresión inválida")
                self.pantalla.delete(0, ctk.END)
        elif boton == "C":
            self.pantalla.delete(0, ctk.END)
        else:
            self.pantalla.insert(ctk.END, boton)


if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()
