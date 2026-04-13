import customtkinter as ctk
import math

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================
# Appearance: modo claro para un aspecto real de calculadora física
ctk.set_appearance_mode("light")
# Color theme: verde para los elementos interactivos (botones hover, etc)
ctk.set_default_color_theme("green")


# ============================================================================
# CLASE PRINCIPAL: Calculadora
# ============================================================================
# Implementa una calculadora de escritorio con dos modos de operación:
# - Modo básico: operaciones aritméticas estándar (+, -, ×, ÷)
# - Modo científico: funciones trigonométricas, logarítmicas y avanzadas
#
# Características principales:
# * Display LCD con efecto visual realista
# * Panel solar decorativo
# * Evaluador de expresiones seguro (eval con dict limitado)
# * Soporte para grados y radianes en funciones trigonométricas
# * Almacenamiento del último resultado (ANS) para reutilización
# ============================================================================
class Calculadora(ctk.CTk):
    def __init__(self):
        """Constructor de la clase Calculadora. Configura la ventana y crea la interfaz."""
        super().__init__()

        self.title("NexaCalc Pro")
        self.geometry("340x560")
        self.resizable(False, False)

        # Color del cuerpo de la calculadora (gris metálico)
        self.configure(fg_color="#C0C0C0")

        # ---------------------------------------------------------------------
        # VARIABLES DE ESTADO
        # ---------------------------------------------------------------------
        self.modo_cientifico = False          # True = modo científico activo
        self.usar_grados = True               # True = grados, False = radianes
        self.botones_cientificos = []        # Lista de botones científicos (ocultos/mostrados según modo)
        self.botones_basicos = []            # Lista de botones básicos (siempre visibles)
        self.mensaje_error_id = None         # ID del timer de error (para poder cancelarlo)
        self.mensaje_parpadeo_id = None      # ID del timer de parpadeo (para poder cancelarlo)
        self.mensaje_parpadeo_visible = False # Estado de visibilidad del parpadeo
        self.ultimo_resultado = None         # Último resultado calculado (para botón ANS)

        # Configurar grid principal para responsividad interna
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Crear componentes de la interfaz en orden
        self.crear_panel_solar()
        self.crear_display_lcd()
        self.crear_area_botones()
        self.crear_botones_basicos()
        self.crear_botones_cientificos()
        # Iniciar en modo básico (False = modo básico)
        self.set_modo(False)

    # ========================================================================
    # COMPONENTE: Panel Solar Decorativo
    # ========================================================================
    def crear_panel_solar(self):
        """Crea el panel solar decorativo superior de la calculadora.

        Incluye celdas solares estilizadas y la marca NEXACALC.
        Es puramente decorativo, no tiene funcionalidad.
        """
        # Frame contenedor superior
        frame_top = ctk.CTkFrame(self, fg_color="#D8D8D8", height=40, corner_radius=0)
        frame_top.pack(fill="x", padx=5, pady=(5, 2))
        frame_top.pack_propagate(False)

        # Panel solar: fondo oscuro con celdas estilo fotovoltaico
        frame_solar = ctk.CTkFrame(frame_top, width=110, height=28, fg_color="#1a1a2e", corner_radius=3)
        frame_solar.pack(side="left", padx=(8, 0), pady=4)
        frame_solar.pack_propagate(False)

        # Celdas solares individuales (5 franjas horizontales)
        for i in range(5):
            celda = ctk.CTkFrame(frame_solar, width=20, height=20, fg_color="#0a0a15", corner_radius=1)
            celda.pack(side="left", padx=1, pady=2)
            celda.pack_propagate(False)

        # Etiqueta con el nombre de la calculadora
        marca = ctk.CTkLabel(frame_top, text="NEXACALC", font=("Arial", 11, "bold"), text_color="#505050")
        marca.pack(side="right", padx=12)

    # ========================================================================
    # COMPONENTE: Display LCD
    # ========================================================================
    def crear_display_lcd(self):
        """Crea el display tipo LCD con efecto visual realista.

        Incluye:
        - Marco exterior metálico
        - Fondo LCD verde estilo calculadora clásica
        - Línea de expresión (muestra operación realizada)
        - Pantalla principal para entrada/resultado
        """
        # Marco metálico exterior
        marco = ctk.CTkFrame(self, height=95, fg_color="#8A8A8A", corner_radius=8)
        marco.pack(fill="x", padx=5, pady=2)
        marco.pack_propagate(False)

        # Fondo LCD verde (color clásico de pantallas de cristal líquido)
        lcd_bg = ctk.CTkFrame(marco, fg_color="#5A7A5A", corner_radius=5)
        lcd_bg.pack(fill="both", expand=True, padx=4, pady=4)

        # Línea superior del LCD (efecto de brillo)
        ctk.CTkFrame(lcd_bg, height=3, fg_color="#4A6A4A").pack(fill="x", padx=3, pady=(2, 0))

        # Contenedor del contenido del LCD
        lcd_content = ctk.CTkFrame(lcd_bg, fg_color="transparent")
        lcd_content.pack(fill="both", expand=True, padx=5, pady=2)

        # Etiqueta de expresión: muestra "2 + 3 =" después de pulsar "="
        self.resultado_label = ctk.CTkLabel(
            lcd_content, text="", font=("Consolas", 13, "normal"),
            text_color="#2A5A2A", anchor="e", height=18
        )
        self.resultado_label.pack(fill="x")

        # Pantalla principal: entrada de números y resultado
        self.pantalla = ctk.CTkEntry(
            lcd_content, font=("Consolas", 38, "normal"), height=45,
            corner_radius=0, justify="right", fg_color="transparent",
            border_width=0, text_color="#1A3A1A"
        )
        self.pantalla.pack(fill="x", pady=(0, 2))

        # Línea inferior del LCD (efecto de sombra)
        ctk.CTkFrame(lcd_bg, height=2, fg_color="#6A8A6A").pack(fill="x", padx=3, pady=(0, 2))

    # ========================================================================
    # COMPONENTE: Área de Botones
    # ========================================================================
    def crear_area_botones(self):
        """Crea el contenedor de botones y el botón de cambio de modo.

        Configura el grid para 8 columnas (modo científico) y 7 filas.
        El botón de modo permite alternar entre modo básico y científico.
        """
        # Frame contenedor del área de botones
        self.frame_botones = ctk.CTkFrame(self, fg_color="#C0C0C0")
        self.frame_botones.pack(fill="both", expand=True, padx=8, pady=4)

        # Botón para cambiar entre modos (visible en ambos modos)
        self.btn_modo = ctk.CTkButton(
            self.frame_botones, text="▸ Modo Científico",
            font=("Arial", 13, "bold"),
            fg_color="#4A5880", hover_color="#3A4870",
            text_color="#FFFFFF", corner_radius=10,
            border_width=2, border_color="#3A4870",
            command=lambda: self.set_modo(not self.modo_cientifico)
        )
        self.btn_modo.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=1, pady=(5, 2))

        # Configurar columnas del grid (8 para modo científico)
        for col in range(8):
            self.frame_botones.grid_columnconfigure(col, weight=1, pad=2)
        # Configurar filas del grid (7 para acomodar todos los botones)
        for row in range(7):
            self.frame_botones.grid_rowconfigure(row, weight=1, pad=2)

    # ========================================================================
    # BOTONES BÁSICOS
    # ========================================================================
    def crear_botones_basicos(self):
        """Crea los botones del modo básico de la calculadora.

        Layout de 6x4 (6 filas, 4 columnas principales):
        - Fila 0: AC, C, %, ÷
        - Fila 1: 7, 8, 9, ×
        - Fila 2: 4, 5, 6, -
        - Fila 3: 1, 2, 3, +
        - Fila 4: 0 (2 cols), ., =

        Cada botón tiene un 'tipo' que define sus colores:
        - 'funcion': rojo (AC, C)
        - 'operador': naranja (%, ÷, ×, -, +)
        - 'igual': verde (=)
        - 'numero': gris claro (dígitos, punto)
        """
        # Layout: (texto, fila, columna, colspan, tipo)
        layout_basico = [
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

        # Crear cada botón con su estilo correspondiente
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
        """Retorna los colores de estilo según el tipo de botón.

        Args:
            texto: Texto del botón (para casos especiales)
            tipo: Categoría del botón ('funcion', 'operador', 'igual', 'numero')

        Returns:
            dict: Diccionario con 'fg', 'hover', 'text', 'border'
        """
        if tipo == "funcion":
            # Rojo: botones de acción especial (borrar)
            return {
                "fg": "#D84040", "hover": "#C03030",
                "text": "#FFFFFF", "border": "#A02020"
            }
        elif tipo == "operador":
            # Naranja: botones de operadores aritméticos
            return {
                "fg": "#E89830", "hover": "#D08820",
                "text": "#FFFFFF", "border": "#B07818"
            }
        elif tipo == "igual":
            # Verde: botón de igual (resultado)
            return {
                "fg": "#38A050", "hover": "#289040",
                "text": "#FFFFFF", "border": "#207030"
            }
        else:
            # Gris claro: números y punto decimal
            return {
                "fg": "#F2F2F2", "hover": "#E4E4E4",
                "text": "#1A1A1A", "border": "#C8C8C8"
            }

    # ========================================================================
    # BOTONES CIENTÍFICOS
    # ========================================================================
    def crear_botones_cientificos(self):
        """Crea los botones del modo científico.

        Se ubicarán en columnas 4-7 (a la derecha de los básicos).
        Estilo azul oscuro consistente con el botón de cambio de modo.

        Layout (columnas 4-7):
        - Fila 0: sin, cos, tan, ln
        - Fila 1: asin, acos, atan, log
        - Fila 2: √, x², xʸ, π
        - Fila 3: (, ), e, ^
        - Fila 4: 1/x, !, ANS, +/-
        """
        # Layout: (texto, fila, columna)
        botones_cient = [
            ("sin", 0, 4), ("cos", 0, 5), ("tan", 0, 6), ("ln", 0, 7),
            ("asin", 1, 4), ("acos", 1, 5), ("atan", 1, 6), ("log", 1, 7),
            ("√", 2, 4), ("x²", 2, 5), ("xʸ", 2, 6), ("π", 2, 7),
            ("(", 3, 4), (")", 3, 5), ("e", 3, 6), ("^", 3, 7),
            ("1/x", 4, 4), ("!", 4, 5), ("ANS", 4, 6), ("+/-", 4, 7),
        ]

        # Crear botones científicos con estilo azul
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
            # Ocultar inicialmente (se mostrarán con set_modo)
            btn.grid_remove()
            self.botones_cientificos.append(btn)

        # Botón DEG/RAD para alternar entre grados y radianes
        self.angulo_btn = ctk.CTkButton(
            self.frame_botones, text="DEG",
            font=("Arial", 11, "bold"),
            fg_color="#606070", hover_color="#505060",
            text_color="#E0E0E0", corner_radius=6,
            border_width=2, border_color="#505060",
            command=self.toggle_angulo
        )
        # No se agrega al grid aquí, se maneja dinámicamente en set_modo

    # ========================================================================
    # CONTROL DE MODOS
    # ========================================================================
    def set_modo(self, cientifico):
        """Cambia entre modo básico y modo científico.

        Args:
            cientifico (bool): True = mostrar botones científicos y expandir ventana,
                               False = ocultar y mantener tamaño básico

        Efectos:
        - Cambia el tamaño de la ventana (340px básico, 680px científico)
        - Muestra/oculta los botones científicos
        - Reubica los botones de control (DEG/RAD, cambio de modo)
        """
        self.modo_cientifico = cientifico
        if self.modo_cientifico:
            # --- MODO CIENTÍFICO ---
            # Expandir ventana para acomodar columnas adicionales
            self.geometry("680x560")

            # Mostrar todos los botones científicos
            for btn in self.botones_cientificos:
                btn.grid()

            # Colocar botón DEG/RAD en columna 4-5 de la fila 5
            self.angulo_btn.grid(row=5, column=4, columnspan=2, sticky="nsew", padx=1, pady=(5, 2))

            # Reubicar botón de cambio de modo a la derecha
            self.btn_modo.grid_forget()
            self.btn_modo.configure(text="◂ Modo Básico")
            self.btn_modo.grid(row=5, column=6, columnspan=2, sticky="nsew", padx=1, pady=(5, 2))
        else:
            # --- MODO BÁSICO ---
            # Volver al tamaño original
            self.geometry("340x560")

            # Ocultar botones científicos
            for btn in self.botones_cientificos:
                btn.grid_remove()
            self.angulo_btn.grid_remove()

            # Reubicar botón de cambio de modo a la izquierda
            self.btn_modo.grid_forget()
            self.btn_modo.configure(text="▸ Modo Científico")
            self.btn_modo.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=1, pady=(5, 2))

    def toggle_angulo(self):
        """Alterna entre grados y radianes para funciones trigonométricas.

        DEG: Las funciones trigonométricas usan grados (360° = círculo completo)
        RAD: Las funciones trigonométricas usan radianes (2π = círculo completo)

        Afecta: sin, cos, tan, asin, acos, atan
        """
        self.usar_grados = not self.usar_grados
        self.angulo_btn.configure(text="DEG" if self.usar_grados else "RAD")

    # ========================================================================
    # MANEJO DE BOTONES CIENTÍFICOS
    # ========================================================================
    def on_click_cientifico(self, boton):
        """Maneja los clics de botones del modo científico.

        Args:
            boton (str): Texto del botón presionado

        Comportamiento:
        - La mayoría inserta texto en la posición del cursor
        - ANS inserta el último resultado calculado
        - +/- cambia el signo del número actual
        - 1/x inserta "1/(" para crear una fracción

        Mapeo de texto a expresión:
        - sin, cos, tan → func( → funciones trigonométricas
        - asin, acos, atan → afunc( → funciones trigonométricas inversas
        - ln → log( → logaritmo natural
        - log → log10( → logaritmo base 10
        - √ → sqrt( → raíz cuadrada
        - x² → **2 → exponente 2
        - xʸ → **( → preparar exponente genérico
        - ^ → ** → operador de potenciación
        """
        pos_cursor = self.pantalla.index("insert")

        # Mapeo de botones a texto insertado
        mapeo = {
            "sin": "sin(", "cos": "cos(", "tan": "tan(",
            "asin": "asin(", "acos": "acos(", "atan": "atan(",
            "ln": "log(", "log": "log10(", "√": "sqrt(",
            "x²": "**2", "xʸ": "**(", "^": "**",
        }

        if boton == "ANS":
            # Insertar último resultado en la posición del cursor
            if self.ultimo_resultado is not None:
                self.pantalla.insert(pos_cursor, str(self.ultimo_resultado))
        elif boton == "+/-":
            # Cambiar signo: prepend "-" o remover si ya existe
            contenido = self.pantalla.get()
            if contenido and contenido != "Error":
                if contenido.startswith("-"):
                    self.pantalla.delete(0, ctk.END)
                    self.pantalla.insert(0, contenido[1:])
                else:
                    self.pantalla.insert(0, "-")
        elif boton == "1/x":
            # Insertar "1/(" para escribir fracciones
            self.pantalla.insert(pos_cursor, "1/(")
        elif boton == "!":
            # Insertar función factorial
            self.pantalla.insert(pos_cursor, "factorial(")
        elif boton in mapeo:
            # Insertar texto mapeado (funciones con paréntesis, etc)
            self.pantalla.insert(pos_cursor, mapeo[boton])
        elif boton in ["(", ")", "π", "e"]:
            # Insertar paréntesis o constantes matemáticas
            # π → pi, e → e (constante de Euler)
            texto = {"π": "pi", "e": "e"}.get(boton, boton)
            self.pantalla.insert(pos_cursor, texto)

    # ========================================================================
    # EVALUACIÓN DE EXPRESIONES
    # ========================================================================
    def evaluar_expresion(self, expresion):
        """Evalúa la expresión aritmética de forma segura.

        Utiliza eval() con un diccionario seguro que:
        1. Restringe las funciones disponibles (solo matemáticas)
        2. Elimina __builtins__ para prevenir ejecución de código arbitrario
        3. Convierte automáticamente grados a radianes si self.usar_grados=True

        Args:
            expresion (str): Expresión a evaluar (ej: "2+3", "sin(45)")

        Returns:
            float: Resultado de la evaluación

        Raises:
            ValueError: Si la expresión es inválida o el factorial es negativo
        """
        # Función factorial con validación de límites
        def factorial(n):
            """Calcula el factorial de n.

            Args:
                n: Número no negativo (se convierte a int)

            Returns:
                int: n! = 1×2×3×...×n

            Raises:
                ValueError: Si n es negativo o mayor a 170
            """
            if n < 0:
                raise ValueError("Factorial no definido para negativos")
            if n > 170:
                raise ValueError("Número muy grande")
            result = 1
            for i in range(1, int(n) + 1):
                result *= i
            return result

        # Diccionario seguro: solo contiene funciones y constantes matemáticas
        # ¡NO incluye __builtins__ para prevenir acceso al sistema!
        safe_dict = {
            # Funciones trigonométricas (conversión automática grados/radianes)
            "sin": lambda x: math.sin(math.radians(x) if self.usar_grados else x),
            "cos": lambda x: math.cos(math.radians(x) if self.usar_grados else x),
            "tan": lambda x: math.tan(math.radians(x) if self.usar_grados else x),
            # Funciones trigonométricas inversas (retornan grados si usar_grados=True)
            "asin": lambda x: math.degrees(math.asin(max(-1, min(1, x)))) if self.usar_grados else math.asin(max(-1, min(1, x))),
            "acos": lambda x: math.degrees(math.acos(max(-1, min(1, x)))) if self.usar_grados else math.acos(max(-1, min(1, x))),
            "atan": lambda x: math.degrees(math.atan(x)) if self.usar_grados else math.atan(x),
            # Funciones matemáticas comunes
            "sqrt": math.sqrt,   # Raíz cuadrada
            "log": math.log,     # Logaritmo natural
            "log10": math.log10, # Logaritmo base 10
            "exp": math.exp,    # Exponencial e^x
            "factorial": factorial,  # Factorial n!
            "abs": abs,          # Valor absoluto
            # Constantes matemáticas
            "pi": math.pi,      # π ≈ 3.14159
            "e": math.e,        # e ≈ 2.71828
            # SEGURIDAD: Eliminar __builtins__ para impedir ejecución de código
            "__builtins__": {},
        }
        return eval(expresion, safe_dict)

    # ========================================================================
    # MANEJO DE ERRORES
    # ========================================================================
    def mostrar_error(self):
        """Muestra el mensaje de error con efecto de parpadeo.

        El error se muestra en rojo y parpadea durante 2 segundos
        antes de limpiarse automáticamente.
        """
        self.pantalla.delete(0, ctk.END)
        self.pantalla.insert(0, "Error")
        self.pantalla.configure(text_color="#803030")

        # Iniciar efecto de parpadeo
        self.mensaje_parpadeo_visible = True
        self.mensaje_parpadeo_id = self.after(150, self._alternar_parpadeo)

        # Limpiar error después de 2 segundos
        self.mensaje_error_id = self.after(2000, self.limpiar_error)

    def _alternar_parpadeo(self):
        """Auxiliar para el efecto de parpadeo del mensaje de error.

        Alterna entre dos tonos de rojo para crear efecto visual de advertencia.
        Se llama recursivamente cada 150ms hasta que se cancele.
        """
        color = "#503030" if self.mensaje_parpadeo_visible else "#803030"
        self.pantalla.configure(text_color=color)
        self.mensaje_parpadeo_visible = not self.mensaje_parpadeo_visible
        if self.mensaje_parpadeo_id:
            self.mensaje_parpadeo_id = self.after(150, self._alternar_parpadeo)

    def limpiar_error(self):
        """Limpia el mensaje de error y restaura el color normal.

        Cancela cualquier timer pendiente y restaura el color de texto
        original si la pantalla aún muestra "Error".
        """
        # Cancelar timers de parpadeo
        if self.mensaje_parpadeo_id:
            self.after_cancel(self.mensaje_parpadeo_id)
            self.mensaje_parpadeo_id = None
        if self.mensaje_error_id:
            self.after_cancel(self.mensaje_error_id)
            self.mensaje_error_id = None

        # Restaurar color original
        self.pantalla.configure(text_color="#1A3A1A")

        # Limpiar pantalla si todavía muestra "Error"
        if self.pantalla.get() == "Error":
            self.pantalla.delete(0, ctk.END)

    # ========================================================================
    # MANEJO DE BOTONES BÁSICOS
    # ========================================================================
    def on_click(self, boton):
        """Maneja los clics de botones del modo básico.

        Args:
            boton (str): Texto del botón presionado

        Comportamiento por botón:
        - '=': Evalúa la expresión y muestra el resultado
        - 'AC': Borra todo (pantalla, expresión, historial)
        - 'C': Borra solo la pantalla actual
        - Otros: Inserta el carácter en la pantalla

        Mapeo de operadores:
        - × → * (multiplicación)
        - ÷ → / (división)
        - π → pi (constante)
        """
        if boton == "=":
            # --- EVALUAR EXPRESIÓN ---
            try:
                # Cancelar timers de errores anteriores
                if self.mensaje_error_id:
                    self.after_cancel(self.mensaje_error_id)
                if self.mensaje_parpadeo_id:
                    self.after_cancel(self.mensaje_parpadeo_id)
                self.pantalla.configure(text_color="#1A3A1A")

                # Obtener expresión, evaluar y mostrar resultado
                expresion = self.pantalla.get()
                resultado = self.evaluar_expresion(expresion)

                # Guardar resultado para el botón ANS
                self.ultimo_resultado = resultado

                # Mostrar expresión completa en la etiqueta superior
                self.resultado_label.configure(text=f"{expresion} =")

                # Mostrar resultado en pantalla
                self.pantalla.delete(0, ctk.END)
                self.pantalla.insert(0, str(resultado))
            except Exception:
                # Si hay error, mostrar mensaje de error
                self.mostrar_error()
        elif boton == "AC":
            # --- BORRAR TODO (All Clear) ---
            self.limpiar_error()
            self.pantalla.delete(0, ctk.END)
            self.resultado_label.configure(text="")
            self.ultimo_resultado = None
        elif boton == "C":
            # --- BORRAR ACTUAL (Clear) ---
            self.limpiar_error()
            self.pantalla.delete(0, ctk.END)
        else:
            # --- INSERTAR CARÁCTER ---
            # Cancelar timers de errores si los hay
            if self.mensaje_error_id:
                self.after_cancel(self.mensaje_error_id)
            if self.mensaje_parpadeo_id:
                self.after_cancel(self.mensaje_parpadeo_id)
            self.pantalla.configure(text_color="#1A3A1A")

            # Mapeo de operadores a símbolos Python
            mapeo = {"×": "*", "÷": "/", "π": "pi"}
            texto = mapeo.get(boton, boton)
            self.pantalla.insert(ctk.END, texto)


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================
if __name__ == "__main__":
    # Crear instancia de la calculadora y ejecutar el loop principal
    app = Calculadora()
    app.mainloop()
